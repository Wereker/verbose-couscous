from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, paginate

from app.schemas import OrderServiceResponse, OrderServiceCreate, OrderServiceUpdate, User
from app.utils.filters import OrderServiceFilter
from app.repositories import OrderServiceRepository
from app.db.db_helper import db_helper
from app.core.config import settings
from app.auth.dependencies import require_admin_role


router = APIRouter(
    prefix=settings.api.v1.order_services,
    tags=["Order Service"],
)

order_service_repository = OrderServiceRepository()


@router.get("/", response_model=Page[OrderServiceResponse], status_code=status.HTTP_200_OK)
async def get_order_services(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    order_services_filter: OrderServiceFilter = FilterDepends(OrderServiceFilter),
    user: User = Depends(require_admin_role)):

    order_services = await order_service_repository.get_all(db, order_services_filter)
    
    return paginate([ OrderServiceResponse.from_orm(order_service) for order_service in order_services ])


@router.post("/", response_model=OrderServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_order_service(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    order_service_in: OrderServiceCreate,
    user: User = Depends(require_admin_role)):

    order_service_created = await order_service_repository.create(db, order_service_in)

    return OrderServiceResponse.from_orm(order_service_created)


@router.get("/{order_service_id}", response_model=OrderServiceResponse, status_code=status.HTTP_200_OK)
async def get_order_service(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    order_service_id: int,
    user: User = Depends(require_admin_role)):

    order_service = await order_service_repository.get(db, order_service_id)
    
    return OrderServiceResponse.from_orm(order_service)


@router.patch("/{order_service_id}", response_model=OrderServiceResponse, status_code=status.HTTP_200_OK)
async def update_order_service(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    order_service_id: int, 
    order_service_in: OrderServiceUpdate,
    user: User = Depends(require_admin_role)):

    order_service_updated = await order_service_repository.update(db, order_service_id, order_service_in)

    return OrderServiceResponse.from_orm(order_service_updated)


@router.delete("/{order_service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_service(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    order_service_id: int,
    user: User = Depends(require_admin_role)):
    
    await order_service_repository.delete(db, order_service_id)