from typing import Optional
from pydantic import BaseModel

from app.schemas import Brand

class CarBase(BaseModel):
    model: str
    brand: Brand


class CarCreate(BaseModel):
    model: str
    brand_id: int


class CarUpdate(BaseModel):
    model: Optional[str] = None
    brand_id: Optional[int] = None


class Car(CarBase):
    id: int

    class Config:
        from_attributes = True


class CarResponse(BaseModel):
    id: int
    model: str
    brand: str

    @classmethod
    def from_orm(cls, car):
        return cls(
            id=car.id,
            model=car.model, 
            brand=car.brand.name
        )


class CarVO(BaseModel):
    model: str
    brand: str

    @classmethod
    def from_orm(cls, car):
        return cls(
            model=car.model, 
            brand=car.brand.name
        )

    class Config:
        from_attributes = True