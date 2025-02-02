from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Optional
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, paginate
from redis.asyncio import Redis

from app.schemas import OrderResponse, OrderCreate, AssignEmployee, OrderUpdate, User
from app.utils.filters import OrderFilter, CustomOrderFilter
from app.repositories import OrderRepository
from app.db.db_helper import db_helper
from app.core.config import settings
from app.auth.dependencies import get_current_user, require_client_role, require_admin_role
from app.redis.redis_cache import RedisCache
from app.redis.dependencies import get_redis_client

from app.celery.celery_app import send_email_task


router = APIRouter(
    prefix=settings.api.v1.orders,
    tags=["Order"],
)

order_repository = OrderRepository()

@router.get("/", response_model=Page[OrderResponse], status_code=status.HTTP_200_OK)
async def get_orders(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    redis_client: Annotated[Redis, Depends(get_redis_client)],
    user: Annotated[User, Depends(get_current_user)],
    orders_filter: OrderFilter = FilterDepends(OrderFilter),
    custom_order_filter: CustomOrderFilter = Depends()):

    orders = await order_repository.get_all(db, orders_filter, custom_order_filter, user)

    redis_cache = RedisCache(redis_client)

    # Добавление мета-данных к каждому заказу
    orders_with_metadata = []
    for order in orders:
        total_price, total_time = await order_repository.get_cached_price_and_time_for_order(redis_cache, order)
        order_data = OrderResponse.from_orm(order, total_time, total_price)
        orders_with_metadata.append(order_data)

    return paginate([order for order in orders_with_metadata])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    redis_client: Annotated[Redis, Depends(get_redis_client)],
    user: Annotated[User, Depends(require_client_role)],
    order_in: OrderCreate):

    # Создание заказа (добавление услуг и владельца автомобиля)
    order_created = await order_repository.create(db, order_in, user)

    # Расчет мета-данных
    total_price = sum(service.service.price for service in order_created.order_services) / 100
    total_time = sum(service.service.time for service in order_created.order_services) / 60

    metadata = {
        "total_price": total_price,
        "total_time": total_time,
    }

    # Сохранение мета-данных в Redis
    redis_cache = RedisCache(redis_client)
    await redis_cache.set_order_metadata(order_created.id, metadata)

    return OrderResponse.from_orm(order_created, total_time, total_price)


@router.patch("/{order_id}/assign", response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def assign_employee(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    redis_client: Annotated[Redis, Depends(get_redis_client)],
    current_user: Annotated[User, Depends(require_admin_role)],
    order_id: int,
    assign_in: AssignEmployee):
    # Объединяем все проверки в одном запросе
    order, employee, role_employee = await order_repository.get_order_and_employee_with_role(
        db, order_id, assign_in.employee_id
    )

    # Обновляем данные заказа
    updated_order = await order_repository.assign_employee_and_admin(
        db, order, employee.id, current_user.id
    )

    redis_cache = RedisCache(redis_client)
    total_price, total_time = await order_repository.get_cached_price_and_time_for_order(redis_cache, updated_order)

    await order_repository.set_end_date_for_order(db, updated_order, total_time)

    send_email_task.delay(
            email_to=updated_order.customer_car.customer.email,
            subject=f"Здравствуйте, {order.customer_car.customer.first_name}! 👋",
            message_content=f"Ваш автомобиль принят на мойку, и мы уже начали выполнение заказа. 🚗💦\n\nСпасибо, что выбрали нашу автомойку!"
        )
    
    return OrderResponse.from_orm(updated_order, total_time, total_price)


@router.patch("/{order_id}/services", response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def update_services(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    redis_client: Annotated[Redis, Depends(get_redis_client)],
    user: Annotated[User, Depends(require_admin_role)],
    order_id: int,
    assign_in: OrderCreate,
    ):
    # Получение заказа и проверка прав клиента
    order = await order_repository.get_order_with_services(db, order_id, user.id)

    # Проверка на дублирующиеся услуги
    existing_service_ids = {service.service_id for service in order.order_services}
    new_service_ids = set(assign_in.services_ids)

    if existing_service_ids & new_service_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duplicate services are not allowed in the order"
        )

    # Добавление новых услуг
    order_updated = await order_repository.add_services_to_order(db, order, new_service_ids)

    # Расчет мета-данных
    total_price = sum(service.service.price for service in order_updated.order_services) / 100
    total_time = sum(service.service.time for service in order_updated.order_services) / 60

    metadata = {
        "total_price": total_price,
        "total_time": total_time,
    }

    redis_cache = RedisCache(redis_client)
    await redis_cache.set_order_metadata(order_updated.id, metadata)

    await order_repository.set_end_date_for_order(db, order_updated, total_time)

    return OrderResponse.from_orm(order_updated, total_time, total_price)


@router.patch("/{order_id}/complete", response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def update_order_to_complete(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    redis_client: Annotated[RedisCache, Depends(get_redis_client)],
    user: Annotated[User, Depends(require_admin_role)],
    order_id: int):
    
    order = await order_repository.change_order_status(db, order_id)

    redis_cache = RedisCache(redis_client)
    total_price, total_time = await order_repository.get_cached_price_and_time_for_order(redis_cache, order)

    if order.status == 1:
        send_email_task.delay(
            email_to=order.customer_car.customer.email,
            subject=f"Здравствуйте, {order.customer_car.customer.first_name}! 👋",
            message_content=f"Ваш автомобиль полностью готов! ✅ Мы завершили выполнение всех услуг и ждем вас для передачи ключей. 🚗✨\n\nПожалуйста, подойдите к стойке администратора или свяжитесь с нами, если потребуется дополнительная помощь.\n\nСпасибо за доверие и до встречи! 😊"
        )

    return OrderResponse.from_orm(order, total_time, total_price)


@router.get("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def get_order(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    redis_client: Annotated[Redis, Depends(get_redis_client)],
    user: Annotated[User, Depends(get_current_user)],
    order_id: int):

    order = await order_repository.get(db, order_id)

    redis_cache = RedisCache(redis_client)
    total_price, total_time = await order_repository.get_cached_price_and_time_for_order(redis_cache, order)
    
    return OrderResponse.from_orm(order, total_time, total_price)


@router.patch("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def update_order(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    redis_client: Annotated[Redis, Depends(get_redis_client)],
    user: Annotated[User, Depends(require_admin_role)],
    order_id: int, 
    order_in: OrderUpdate):

    order_updated = await order_repository.update(db, order_id, order_in)

    redis_cache = RedisCache(redis_client)
    total_price, total_time = await order_repository.get_cached_price_and_time_for_order(redis_cache, order_updated)

    return OrderResponse.from_orm(order_updated, total_time, total_price)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    redis_client: Annotated[Redis, Depends(get_redis_client)],
    user: Annotated[User, Depends(require_admin_role)],
    order_id: int):
    
    redis_cache = RedisCache(redis_client)
    await redis_cache.delete_order_metadata(order_id)

    await order_repository.delete(db, order_id)