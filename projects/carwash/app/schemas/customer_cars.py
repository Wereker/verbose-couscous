from typing import Optional
from pydantic import BaseModel

from app.schemas import Car, User
from app.schemas import CustomerVO, CarVO

class CustomerCarsBase(BaseModel):
    year: int
    number: str
    car: Car
    customer: User


class CustomerCarsCreate(BaseModel):
    year: int
    number: str
    car_id: int
    customer_id: int


# Отдельная схема для регистрации автомобиля на пользователя
class CustomerCarsProfileCreate(BaseModel):
    year: int
    number: str
    car_id: int


class CustomerCarsUpdate(BaseModel):
    year: Optional[int] = None
    number: Optional[str] = None
    car_id: Optional[int] = None
    customer_id: Optional[int] = None


class CustomerCars(CustomerCarsBase):
    id: int

    class Config:
        from_attributes = True

        
class CustomerCarsResponse(BaseModel):
    id: int
    year: int
    number: str
    customer: CustomerVO
    car: CarVO

    @classmethod
    def from_orm(cls, customer_car):
        return cls(
            id=customer_car.id,
            year=customer_car.year,
            number=customer_car.number,
            customer=CustomerVO.from_orm(customer_car.customer),
            car=CarVO.from_orm(customer_car.car),
        )

    class Config:
        from_attributes = True


class CustomerCarVO(BaseModel):
    id: int
    year: int
    number: str
    customer: CustomerVO
    car: CarVO

    @classmethod
    def from_orm(cls, customer_car):
        return cls(
            id=customer_car.id,
            year=customer_car.year,
            number=customer_car.number,
            customer=CustomerVO.from_orm(customer_car.customer),
            car=CarVO.from_orm(customer_car.car),
        )