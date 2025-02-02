from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from app.schemas import User, CustomerCars
from app.schemas import UserVO, CustomerCarVO
from app.schemas import ServiceVO


class OrderBase(BaseModel):
    status: int
    start_date: datetime
    end_date: datetime
    administrator: User
    customer_car: CustomerCars
    employee: User


# class OrderCreate(BaseModel):
#     # start_date: datetime
#     administrator_id: int
#     customer_car_id: int
#     employee_id: int

class OrderCreate(BaseModel):
    services_ids: List[int]
    car_id: int


class AssignEmployee(BaseModel):
    employee_id: int


class OrderUpdate(BaseModel):
    status: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    administrator_id: Optional[int] = None
    customer_car_id: Optional[int] = None
    employee_id: Optional[int] = None


class Order(OrderBase):
    id: int

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    status: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    totalTime: int  # минуты
    totalPrice: int  # рублей
    administrator: Optional[UserVO] = None
    employee: Optional[UserVO] = None
    customerCar: Optional[CustomerCarVO] = None
    services: List[ServiceVO] = None

    @classmethod
    def from_orm(cls, order, total_time, total_price):

        return cls(
            id=order.id,
            status=order.status,
            start_date=order.start_date,
            end_date=order.end_date,
            totalTime=total_time,
            totalPrice=total_price,
            administrator=UserVO.from_orm(order.administrator) if order.administrator else None,
            employee=UserVO.from_orm(order.employee) if order.employee else None,
            customerCar=CustomerCarVO.from_orm(order.customer_car) if order.customer_car else None,
            services=[ServiceVO.from_orm(os.service) for os in order.order_services]
        )


class OrderVO(BaseModel):
    id: int
    status: int
    administrator: UserVO
    employee: UserVO
    customerCar: CustomerCarVO

    @classmethod
    def from_orm(cls, order):
        return cls(
            id=order.id,
            status=order.status,
            administrator=UserVO.from_orm(order.administrator),
            employee=UserVO.from_orm(order.employee),
            customerCar=CustomerCarVO.from_orm(order.customer_car)
        )