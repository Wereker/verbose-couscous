from typing import Optional, List
from pydantic import BaseModel, EmailStr

from app.schemas import RoleVO, CarVO


# Схема для отображения данных об автомобиле в профиле пользователя
class VehicleProfileVO(BaseModel):
    id: int
    year: int
    number: str
    details: CarVO

    @classmethod
    def from_orm(cls, vehicle):
        return cls(
            id=vehicle.id,
            year=vehicle.year,
            number=vehicle.number,
            details=CarVO.from_orm(vehicle.car),
        )


class UserProfile(BaseModel):
    id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_send_notify: Optional[bool] = False
    role: Optional[RoleVO] = None
    vehicles: List[VehicleProfileVO] = []

    @classmethod
    def from_orm(cls, user):
        return cls(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            patronymic=user.patronymic,
            email=user.email,
            is_active=user.is_active,
            role=RoleVO.from_orm(user.role_user.role),
            vehicles=[VehicleProfileVO.from_orm(car) for car in user.customer_cars],
        )

