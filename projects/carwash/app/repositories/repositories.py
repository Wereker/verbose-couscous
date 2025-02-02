from datetime import datetime, timezone, timedelta
from typing import List, Type, Optional, Tuple
from abc import ABC, abstractmethod

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, and_, or_
from sqlalchemy.orm import joinedload
from fastapi_filter.contrib.sqlalchemy import Filter

from app.auth.utils import get_password_hash, verify_password, create_access_token, create_refresh_token

from app.schemas import (
    BrandCreate, BrandUpdate,
    CarCreate, CarUpdate,
    ServiceCreate, ServiceUpdate,
    RoleCreate, RoleUpdate,
    UserCreate, UserUpdate, UserLogin, UserSignUp,
    RoleUserCreate, RoleUserUpdate,
    CustomerCarsCreate, CustomerCarsUpdate, CustomerCarsProfileCreate,
    OrderCreate, OrderUpdate,
    OrderServiceCreate, OrderServiceUpdate,
)

from app.models import (
    Brand,
    Service,
    Car,
    Role,
    User,
    RoleUser,
    CustomerCars,
    Order,
    OrderService,
)

from app.redis.redis_cache import RedisCache
from app.utils.exception import ObjectNotFoundException, InvalidCredentialsException

class CRUDBase(ABC):
    def __init__(self, model: object, model_name: str):
        self.model = model
        self.model_name = model_name
    
    @abstractmethod
    async def get(self, db: AsyncSession, id: int):
        """Метод для получения объекта"""
        pass

    @abstractmethod
    async def get_all(self, db: AsyncSession, model_filter: Filter):
        """Метод получения всех объектов"""
        pass

    @abstractmethod
    async def create(self, db: AsyncSession, obj_in):
        """Метод создания нового объекта"""
        pass

    @abstractmethod
    async def update(self, db: AsyncSession, id: int, obj_in):
        """Метод обновления существующего объекта"""
        pass

    @abstractmethod
    async def delete(self, db: AsyncSession, id: int):
        """Метод удаления существующего объекта"""
        pass
    

class BrandRepository(CRUDBase):
    def __init__(self):
        super().__init__(Brand, "Brand")
    

    async def get(self, db: AsyncSession, id: int) -> Brand:
        """Получение бренда автомобилей по ID из бд"""
        query = select(self.model).where(self.model.id == id)

        result = await db.execute(query)
        brand = result.scalars().first()

        if not brand:
            raise ObjectNotFoundException(self.model_name)
        
        return brand
    

    async def get_all(self, db: AsyncSession, model_filter: Filter) -> List[Brand]:
        """Получение всех брендов автомобилей из бд"""
        query = model_filter.filter(select(self.model))
        query = model_filter.sort(query)

        result = await db.execute(query)
        brands = result.scalars().all()

        if not brands:
            raise ObjectNotFoundException(self.model_name)
        
        return brands


    async def create(self, db: AsyncSession, obj_in: BrandCreate) -> Brand:
        """Создание нового бренда и добавление его в бд"""
        brand = self.model(**obj_in.model_dump())
        db.add(brand)

        await db.commit()
        await db.refresh(brand)

        return brand

    
    async def update(self, db: AsyncSession, id: int, obj_in: BrandUpdate) -> Brand:
        """Обновление (частичное) бренда автомобиля с конкретным ID"""
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**obj_in.model_dump(exclude_unset=True))
            .returning(self.model)
        )

        result = await db.execute(query)
        await db.commit()
        brand = result.scalars().first()

        if not brand:
            raise ObjectNotFoundException(self.model_name)
        
        return brand
    

    async def delete(self, db: AsyncSession, id: int) -> bool:
        """Удаление бренда автомобиля по ID"""
        query = delete(self.model).where(self.model.id == id)
        result = await db.execute(query)
        await db.commit()

        if result.rowcount == 0:
            raise ObjectNotFoundException(self.model_name)

        return result.rowcount > 0
        

class ServiceRepository(CRUDBase):
    def __init__(self):
        super().__init__(Service, "Service")
        self.format_price = {"копейка": 100, "рубль": 1} # Возможно, это того не стоит 
        self.format_time = {"секунда": 60, "минута": 1, "час": 1 / 60} # Но мне было лень искать библиотеку

    
    async def get(self, db: AsyncSession, id: int) -> Service:
        """Получение сервиса автомойки по ID из бд"""
        query = select(self.model).where(self.model.id == id)
        result = await db.execute(query)
        service = result.scalars().first()

        if not service:
            raise ObjectNotFoundException(self.model_name)
        
        return service


    async def get_all(self, db: AsyncSession, model_filter: Filter) -> List[Service]:
        """Получение всех сервисов автомойки из бд"""
        query = model_filter.filter(select(self.model))
        query = model_filter.sort(query)

        result = await db.execute(query)
        services = result.scalars().all()

        if not services:
            raise ObjectNotFoundException(self.model_name)
        
        return services


    async def create(self, db: AsyncSession, obj_in: ServiceCreate) -> Service:
        """Создание нового сервиса автомойки и добавление его в бд"""
        service = self.model(**obj_in.model_dump())
        service.price *= self.format_price["копейка"] # Переводим рубли в копейки
        service.time *= self.format_time["секунда"] # Переводим минуты в секунды
        db.add(service)

        await db.commit()
        await db.refresh(service)

        return service

    
    async def update(self, db: AsyncSession, id: int, obj_in: ServiceUpdate) -> Service:
        """Обновление (частичное) сервиса автомойки с конкретным ID"""
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**obj_in.model_dump(exclude_unset=True))
            .returning(self.model)
        )

        result = await db.execute(query)
        await db.commit()
        service = result.scalars().first()

        if not service:
            raise ObjectNotFoundException(self.model_name)
        
        return service
    

    async def delete(self, db: AsyncSession, id: int) -> bool:
        """Удаление сервиса автомойки по ID"""
        query = delete(self.model).where(self.model.id == id)
        result = await db.execute(query)
        await db.commit()

        if result.rowcount == 0:
            raise ObjectNotFoundException(self.model_name)
    
        return result.rowcount > 0


class CarRepository(CRUDBase):
    def __init__(self):
        super().__init__(Car, "Car")

    async def get(self, db: AsyncSession, id: int) -> Car:
        """Получение машины по ID из бд"""
        query = select(self.model).where(self.model.id == id)
        result = await db.execute(query)
        car = result.scalars().first()

        if not car:
            raise ObjectNotFoundException(self.model_name)
        
        return car


    async def get_all(self, db: AsyncSession, model_filter: Filter) -> List[Car]:
        """Получение всех машин из бд"""
        query = model_filter.filter(select(self.model))
        query = model_filter.sort(query)

        result = await db.execute(query)
        cars = result.scalars().all()

        if not cars:
            raise ObjectNotFoundException(self.model_name)
        
        return cars


    async def create(self, db: AsyncSession, obj_in: CarCreate) -> Car:
        """Создание нового машины и добавление его в бд"""
        car = self.model(**obj_in.model_dump())
        db.add(car)

        await db.commit()
        await db.refresh(car)

        return car

    
    async def update(self, db: AsyncSession, id: int, obj_in: CarUpdate) -> Car:
        """Обновление (частичное) машины с конкретным ID"""
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**obj_in.model_dump(exclude_unset=True))
            .returning(self.model)
        )

        result = await db.execute(query)
        car = result.scalars().first()

        await db.commit()

        if not car:
            raise ObjectNotFoundException(self.model_name)
        
        await db.refresh(car)

        return car
    

    async def delete(self, db: AsyncSession, id: int) -> bool:
        """Удаление машины по ID"""
        query = delete(self.model).where(self.model.id == id)
        result = await db.execute(query)
        await db.commit()

        if result.rowcount == 0:
            raise ObjectNotFoundException(self.model_name)
        
        return result.rowcount > 0
    

class RoleRepository(CRUDBase):
    def __init__(self):
        super().__init__(Role, "Role")
    

    async def get(self, db: AsyncSession, id: int) -> Role:
        """Получение роли пользователей по ID из бд"""
        query = select(self.model).where(self.model.id == id)
        result = await db.execute(query)
        role = result.scalars().first()

        if not role:
            raise ObjectNotFoundException(self.model_name)
        
        return role


    async def get_all(self, db: AsyncSession, model_filter: Filter) -> List[Role]:
        """Получение всех ролей пользователй из бд"""
        query = model_filter.filter(select(self.model))
        query = model_filter.sort(query)

        result = await db.execute(query)
        roles = result.scalars().all()

        if not roles:
            raise ObjectNotFoundException(self.model_name)
        
        return roles
    

    async def create(self, db: AsyncSession, obj_in: RoleCreate) -> Role:
        """Создание новой роли для пользователя"""
        role = self.model(**obj_in.model_dump())
        db.add(role)

        await db.commit()
        await db.refresh(role)

        return role


    async def update(self, db: AsyncSession, id: int, obj_in: RoleUpdate) -> Role:
        """Обновление (частичное) роли пользователя"""
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**obj_in.model_dump(exclude_unset=True))
            .returning(self.model)
        )

        result = await db.execute(query)
        await db.commit()
        role = result.scalars().first()

        if not role:
            raise ObjectNotFoundException(self.model_name)
    
        return role

    async def delete(self, db: AsyncSession, id: int) -> bool:
        """Удаление роли пользователя из бд"""
        query = delete(self.model).where(self.model.id == id)
        result = await db.execute(query)
        await db.commit()

        if result.rowcount == 0:
            raise ObjectNotFoundException(self.model_name)
        
        return result.rowcount > 0


class UserRepository(CRUDBase):
    def __init__(self):
        super().__init__(User, "User")

    async def get(
        self, db: AsyncSession, id: Optional[int] = None, username: Optional[str] = None, email: Optional[str] = None
    ) -> User:
        """Получение пользователя из бд"""        
        filters = []

        if id:
            filters.append(User.id == id)
        if username:
            filters.append(User.username == username)
        if email:
            filters.append(User.email == email)

        query = (
            select(User)
            .where(and_(*filters))
            .options(
                joinedload(User.role_user),
                joinedload(User.customer_cars)
            )
        )

        result = await db.execute(query)
        user = result.scalars().first()

        if not user:
            raise ObjectNotFoundException(self.model_name)
        
        return user
    

    async def get_all(self, db: AsyncSession, model_filter: Filter) -> List[User]:
        """Получение всех ользователй из бд"""
        query = model_filter.filter(select(self.model))
        query = model_filter.sort(query)

        result = await db.execute(query)
        users = result.scalars().all()

        if not users:
            raise ObjectNotFoundException(self.model_name)
        
        return users
    

    async def create(self, db: AsyncSession, obj_in: UserCreate) -> User:
        """Создание нового пользователя (только для адимина)"""
        hashed_password = get_password_hash(obj_in.password)

        user = User(
            email=obj_in.email,
            hashed_password=hashed_password,
            username=obj_in.username,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            patronymic=obj_in.patronymic,
        )

        db.add(user)

        await db.commit()
        await db.refresh(user)

        role_user = RoleUser(user_id=user.id, role_id=obj_in.role_id)
        db.add(role_user)
        await db.commit()
        await db.refresh(user)

        return user


    async def update(self, db: AsyncSession, id: int, obj_in: UserUpdate) -> User:
        """Обновление (частичное) пользователя"""
        update_data = obj_in.model_dump(exclude_unset=True)
        print(update_data)
        
        if not update_data:
            raise ValueError("No fields provided for update")

        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**update_data)
            .returning(self.model)
        )

        result = await db.execute(query)
        await db.commit()
        user = result.scalars().first()

        if not user:
            raise ObjectNotFoundException(self.model_name)
        
        return user


    async def delete(self, db: AsyncSession, id: int) -> bool:
        """Удаление пользователя из бд"""
        query = delete(self.model).where(self.model.id == id)
        result = await db.execute(query)
        await db.commit()

        if result.rowcount == 0:
            raise ObjectNotFoundException(self.model_name)

        return result.rowcount > 0
        

    async def signup(self, db: AsyncSession, user_in: UserSignUp, role_id: int) -> User:
        """Метод для реализации регистрации пользователя в бд"""
        hashed_password = get_password_hash(user_in.password)

        db_user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            username=user_in.username,
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            patronymic=user_in.patronymic,
        )

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        role_user = RoleUser(user_id=db_user.id, role_id=role_id)

        db.add(role_user)
        await db.commit()
        await db.refresh(db_user)

        query = (
            select(self.model)
            .options(joinedload(self.model.role_user).joinedload(RoleUser.role))
            .where(self.model.id == db_user.id)
        )
        result = await db.execute(query)
        user = result.scalars().first()

        if not user:
            raise ObjectNotFoundException(self.model_name)
        
        return user

    
    async def login(self, db: AsyncSession, username: str, password: str) -> str | None:
        """Методд для проверки входа пользователя в систему"""
        query = select(self.model).where(self.model.username == username)
        result = await db.execute(query)
        user = result.scalars().first()

        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException()

        access_token = create_access_token(user.username)
        refresh_token = create_refresh_token(user.username)

        return access_token, refresh_token
    

class RoleUserRepository(CRUDBase):
    def __init__(self):
        super().__init__(RoleUser, "Role user")

    async def get_role_for_user(self, db: AsyncSession, userId: int) -> Role:
        query = (
            select(self.model)
            .where(self.model.user_id == userId)
            .options(joinedload(self.model.role))
        )
        result = await db.execute(query)
        role_user = result.scalars().first()

        return role_user.role

    async def get(self, db: AsyncSession, id: int) -> RoleUser:
        """Получение пользователя и его роли"""
        query = (
            select(self.model)
            .where(self.model.id == id)
        )

        result = await db.execute(query)
        role_user = result.scalars().first()

        if not role_user:
            raise ObjectNotFoundException(self.model_name)

        return role_user
    

    async def get_all(self, db: AsyncSession, model_filter: Filter) -> List[RoleUser]:
        """Получение всех пользователей и их соответсвующие роли"""
        query = (
            select(self.model)
        )
        query = model_filter.filter(query)
        query = model_filter.sort(query)
        result = await db.execute(query)
        
        return result.scalars().all()
    

    async def create(self, db: AsyncSession, obj_in: RoleUserCreate) -> RoleUser:
        """Добавление ролди для пользователя"""
        role_user = self.model(**obj_in.model_dump())
        db.add(role_user)

        await db.commit()
        await db.refresh(role_user)

        return role_user


    async def update(self, db: AsyncSession, id: int, obj_in: RoleUserUpdate) -> RoleUser:
        """Обновление (частичное) роли для пользователя"""
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**obj_in.model_dump(exclude_unset=True))
            .returning(self.model)
        )

        result = await db.execute(query)
        await db.commit()
        
        role_user = result.scalars().first()

        if not role_user:
            raise ObjectNotFoundException(self.model_name)

        await db.refresh(role_user)

        return role_user


    async def delete(self, db: AsyncSession, id: int) -> bool:
        """Удаление роли для пользователя из бд"""
        query = delete(self.model).where(self.model.id == id)
        result = await db.execute(query)
        await db.commit()

        if result.rowcount == 0:
            raise ObjectNotFoundException(self.model_name)

        return result.rowcount > 0
    

class CustomerCarsRepository(CRUDBase):
    def __init__(self):
        super().__init__(CustomerCars, "Customer car")

    async def get(self, db: AsyncSession, id: int) -> CustomerCars:
        """Получение бренда автомобилей по ID из бд"""
        query = select(self.model).where(self.model.id == id)

        result = await db.execute(query)
        customer_car = result.scalars().first()

        if not customer_car:
            raise ObjectNotFoundException(self.model_name)
        
        return customer_car
    

    async def get_all(self, db: AsyncSession, model_filter: Filter) -> List[CustomerCars]:
        """Получение всех владельцов автомобилей из бд"""
        query = model_filter.filter(select(self.model))
        query = model_filter.sort(query)

        result = await db.execute(query)
        customer_cars = result.scalars().all()

        if not customer_cars:
            raise ObjectNotFoundException(self.model_name)
        
        return customer_cars


    async def create(self, db: AsyncSession, obj_in: CustomerCarsCreate) -> CustomerCars:
        """Добавление владельца автомобиля в бд"""
        customer_car = self.model(**obj_in.model_dump())
        db.add(customer_car)

        await db.commit()
        await db.refresh(customer_car)

        return customer_car

    
    async def update(self, db: AsyncSession, id: int, obj_in: CustomerCarsUpdate) -> CustomerCars:
        """Обновление (частичное) владельца автомобиля с конкретным ID"""
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**obj_in.model_dump(exclude_unset=True))
            .returning(self.model)
        )

        result = await db.execute(query)
        await db.commit()
        
        customer_car = result.scalars().first()

        if not customer_car:
            raise ObjectNotFoundException(self.model_name)
        
        await db.refresh(customer_car)
        
        return customer_car
    

    async def delete(self, db: AsyncSession, id: int) -> bool:
        """Удаление владельца автомобиля по ID"""
        query = delete(self.model).where(self.model.id == id)
        result = await db.execute(query)
        await db.commit()

        if result.rowcount == 0:
            raise ObjectNotFoundException(self.model_name)

        return result.rowcount > 0
    
    async def regiser_car_to_user(self, db: AsyncSession, user_id: int, car_in: CustomerCarsProfileCreate):
        """Добавления владельца автомобиля по id пользователя"""
        customer_car = self.model(**car_in.model_dump())
        customer_car.customer_id = user_id
        db.add(customer_car)
        
        await db.commit()
        await db.refresh(customer_car)

        return customer_car


class OrderRepository(CRUDBase):
    def __init__(self):
        super().__init__(Order, "Order")

    
    async def get(self, db: AsyncSession, id: int):
        """Получение заказа пользователя по ID"""
        query = select(self.model).where(self.model.id == id)
        result = await db.execute(query)
        order = result.scalars().first()

        if not order:
            raise ObjectNotFoundException(self.model_name)
        
        return order


    async def get_all(self, db: AsyncSession, model_filter: Filter, custom_filter, current_user: User):
        """Получение заказов из бд. Для работников и клиентов выводятся только те, которых они присутствуют"""
        query = select(self.model).options(
            joinedload(self.model.order_services).joinedload(OrderService.service),
            joinedload(self.model.administrator),
            joinedload(self.model.employee),
            joinedload(self.model.customer_car)
        )

        if current_user.role_user.role.name != "Администратор":
            query = query.filter(
                or_(
                    self.model.administrator_id == current_user.id,
                    self.model.employee_id == current_user.id,
                    self.model.customer_car.has(CustomerCars.customer_id == current_user.id)
                )
            )

        query = model_filter.filter(query)
        query = model_filter.sort(query)

        if custom_filter:
            if custom_filter.brand_name_ilike:
                query = query.filter(
                    self.model.customer_car.has(
                        CustomerCars.car.has(
                            Car.brand.has(
                                Brand.name.ilike(f"%{custom_filter.brand_name_ilike}%")
                            )
                        )
                    )
                )
            if custom_filter.car_number_ilike:
                query = query.filter(
                    self.model.customer_car.has(
                        CustomerCars.number.ilike(f"%{custom_filter.car_number_ilike}%")
                    )
                )
            if custom_filter.car_year_gt:
                query = query.filter(
                    self.model.customer_car.has(CustomerCars.year > custom_filter.car_year_gt)
                )
            if custom_filter.car_year_lt:
                query = query.filter(
                    self.model.customer_car.has(CustomerCars.year < custom_filter.car_year_lt)
                )
        
        results = await db.execute(query)
        orders = results.unique().scalars().all()

        if not orders:
            raise ObjectNotFoundException(self.model_name)
        
        return orders


    async def create(self, db: AsyncSession, services_in: OrderCreate, current_user: User):
        """Создание нового заказа (только для пользователя)"""
        # Находим id владельца автомобиля
        query = (
            select(CustomerCars)
            .where(
                and_(
                    CustomerCars.customer_id == current_user.id,
                    CustomerCars.id == services_in.car_id,
                )
            )
        )
        result = await db.execute(query)
        customer_car = result.scalars().first()

        if not customer_car:
            raise ObjectNotFoundException(self.model_name)
        
        service_query = select(Service).where(Service.id.in_(services_in.services_ids))
        service_result = await db.execute(service_query)
        found_services = {service.id for service in service_result.scalars().all()}

        missing_services = set(services_in.services_ids) - found_services
        if missing_services:
            raise ObjectNotFoundException(f"Services with IDs {missing_services} not found.")

        new_order = Order(
            customer_car_id=customer_car.id,
        )

        db.add(new_order)
        await db.commit()

        for service_id in services_in.services_ids:
            db_order_service = OrderService(order_id=new_order.id, service_id=service_id)
            db.add(db_order_service)
        
        await db.commit()
        await db.refresh(new_order)
        return new_order
    

    async def update(self, db: AsyncSession, id: int, obj_in: OrderUpdate):
        """Обновление (частичное) данных о заказе """
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**obj_in.model_dump(exclude_unset=True))
            .returning(self.model)
        )

        result = await db.execute(query)
        await db.commit()
        await db.refresh(result)
        order = result.scalars().first()

        if not order:
            raise ObjectNotFoundException(self.model_name)

        return order
    
    
    async def get_order_and_employee_with_role(
        self, db: AsyncSession, order_id: int, employee_id: int
    ):
        """Получение заказа, пользователя и роли в одном запросе"""
        query = (
            select(Order, User, RoleUser)
            .select_from(Order)
            .outerjoin(User, User.id == employee_id)
            .outerjoin(RoleUser, RoleUser.user_id == User.id)
            .options(
                joinedload(Order.order_services).joinedload(OrderService.service),
                joinedload(Order.administrator),
                joinedload(Order.employee),
                joinedload(Order.customer_car),
            )
            .where(Order.id == order_id)
        )

        result = await db.execute(query)
        order, employee, role_employee = result.unique().first() or (None, None, None)

        # Если заказ не найден
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        # Если пользователь не найден
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        # Если пользователь не является "Работником"
        if not role_employee or role_employee.role.name != "Работник":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not employee",
            )

        return order, employee, role_employee
    

    async def assign_employee_and_admin(
        self, db: AsyncSession, order: Order, employee_id: int, admin_id: int
    ):
        """Обновление заказа с назначением работника и администратора"""
        order.employee_id = employee_id
        order.administrator_id = admin_id

        await db.commit()
        await db.refresh(order)

        return order
    

    async def get_order_with_services(self, db: AsyncSession, order_id: int, client_id: int):
        """Получение заказа клиента с услугами"""
        query = (
            select(Order)
            .join(Order.customer_car)
            .options(
                joinedload(Order.order_services).joinedload(OrderService.service),
                joinedload(Order.customer_car),
            )
            .where(Order.id == order_id, CustomerCars.customer_id == client_id)
        )
        result = await db.execute(query)
        order = result.unique().scalar_one_or_none()

        if not order: 
            raise ObjectNotFoundException(self.model_name)
        
        return order
    

    async def change_order_status(self, db: AsyncSession, order_id: int):
        """Изменить статус заказа на противоположный"""

        query = (
            select(self.model)
            .where(self.model.id == order_id)
        )

        result = await db.execute(query)
        order = result.scalars().first()

        order.status = 1 - order.status if order.status < 2 else order.status - 1

        await db.commit()
        await db.refresh(order)

        return order
    

    async def get_orders_to_complete(self, db: AsyncSession):
        """Получение заказов, которые уже должны были завершиться"""
        query = (
            select(self.model)
            .where(self.model.end_date <= datetime.now(timezone.utc))
            .options(
                joinedload(Order.order_services).joinedload(OrderService.service),
                joinedload(Order.administrator),
                joinedload(Order.employee),
                joinedload(Order.customer_car),
            )
        )
        result = await db.execute(query)
        orders = result.scalars().unique().all()

        return orders
    

    async def add_services_to_order(self, db: AsyncSession, order: Order, service_ids: set[int]):
        """Добавление услуг в заказ"""
        new_services = [
            OrderService(order_id=order.id, service_id=service_id)
            for service_id in service_ids
        ]
        db.add_all(new_services)
        await db.commit()
        await db.refresh(order)
        return order


    async def get_cached_price_and_time_for_order(self, redis_cache: RedisCache, order: Order):
        """Получение мета-данных по стоимости услуг и продолжительности по времени заказа"""
        metadata = await redis_cache.get_order_metadata(order.id)

        if metadata:
            total_price = metadata.get("total_price")
            total_time = metadata.get("total_time")
        else:
            total_price = sum(service.service.price for service in order.order_services) / 100
            total_time = sum(service.service.time for service in order.order_services) / 60
            
            metadata = {
                "total_price": total_price,
                "total_time": total_time,
            }
            await redis_cache.set_order_metadata(order.id, metadata)

        return total_price, total_time
    

    async def set_end_date_for_order(self, db: AsyncSession, order: Order, total_time_seconds: int):
        """Метод, который устанавливает начальное и конечное время заказа"""
        if not order.start_date:
            order.start_date = datetime.now(timezone.utc)
        
        order.end_date = order.start_date + timedelta(seconds=total_time_seconds)

        await db.commit()
        await db.refresh(order)
        return order

    async def delete(self, db: AsyncSession, id: int) -> bool:
        """Удаление заказа по ID"""
        query = delete(self.model).where(self.model.id == id)
        result = await db.execute(query)
        await db.commit()

        if result.rowcount == 0:
            raise ObjectNotFoundException(self.model_name)

        return result.rowcount > 0


class OrderServiceRepository(CRUDBase):
    def __init__(self):
        super().__init__(OrderService, "Order service")
    

    async def get(self, db: AsyncSession, id: int) -> OrderService:
        """Получение бренда автомобилей по ID из бд"""
        query = select(self.model).where(self.model.id == id)

        result = await db.execute(query)
        order_serivce = result.scalars().first()

        if not order_serivce:
            raise ObjectNotFoundException(self.model_name)
        
        return order_serivce
    

    async def get_all(self, db: AsyncSession, model_filter: Filter) -> List[OrderService]:
        """Получение всех брендов автомобилей из бд"""
        query = (
            select(self.model)
        )
        query = model_filter.filter(query)
        query = model_filter.sort(query)

        result = await db.execute(query)
        order_services = result.scalars().unique().all()

        if not order_services:
            raise ObjectNotFoundException(self.model_name)
        
        return order_services


    async def create(self, db: AsyncSession, obj_in: OrderServiceCreate) -> OrderService:
        """Создание нового бренда и добавление его в бд"""
        order_service = self.model(**obj_in.model_dump())
        db.add(order_service)

        await db.commit()
        await db.refresh(order_service)

        return order_service

    
    async def update(self, db: AsyncSession, id: int, obj_in: OrderServiceUpdate) -> OrderService:
        """Обновление (частичное) бренда автомобиля с конкретным ID"""
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**obj_in.model_dump(exclude_unset=True))
            .returning(self.model)
        )

        result = await db.execute(query)
        await db.commit()

        order_service = result.scalars().first()

        if not order_service:
            raise ObjectNotFoundException(self.model_name)
        
        await db.refresh(order_service)

        return order_service
    

    async def delete(self, db: AsyncSession, id: int) -> bool:
        """Удаление бренда автомобиля по ID"""
        query = delete(self.model).where(self.model.id == id)
        result = await db.execute(query)
        await db.commit()

        if result.rowcount == 0:
            raise ObjectNotFoundException(self.model_name)

        return result.rowcount > 0