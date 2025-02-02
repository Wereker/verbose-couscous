from typing import Optional
from pydantic import BaseModel


class ServiceBase(BaseModel):
    name: str
    price: int
    time: int


class ServiceCreate(ServiceBase):
    ...


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    time: Optional[int] = None


class Service(ServiceBase):
    id: int

    class Config:
        from_attributes = True


class TimeVO(BaseModel):
    second: int
    minute: int

    @classmethod
    def from_seconds(cls, second_in: int):
        return cls(
            second=second_in,
            minute=second_in / 60
        )


class PriceVO(BaseModel):
    minValue: int
    maxValue: int
    format: str

    @classmethod
    def from_values(cls, min_value: int, max_value: int):
        return cls(
            minValue=min_value,
            maxValue=max_value,
            format=f"{min_value} руб."
        )
    

class ServiceResponse(BaseModel):
    id: int
    name: str
    price: PriceVO
    time: TimeVO


    @classmethod
    def from_orm(cls, service):
        return cls(
            id=service.id,
            name=service.name,
            price=PriceVO.from_values(service.price / 1000, service.price / 100),
            time=TimeVO.from_seconds(service.time)
        )


class ServiceVO(BaseModel):
    id: int
    name: str
    time: int
    price: PriceVO


    @classmethod
    def from_orm(cls, service):
        return cls(
            id=service.id,
            name=service.name,
            time=service.time / 60,
            price=PriceVO.from_values(service.price / 1000, service.price / 100),
        )