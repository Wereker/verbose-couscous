from typing import Optional
from pydantic import BaseModel

from app.schemas import Service, Order

class OrderServiceBase(BaseModel):
    service_id: int
    order_id: int


class OrderServiceCreate(BaseModel):
    service_id: int
    order_id: int


class OrderServiceUpdate(BaseModel):
    service_id: Optional[int] = None
    order_id: Optional[int] = None


class OrderService(OrderServiceBase):
    id: int

    class Config:
        from_attributes = True



class OrderServiceResponse(BaseModel):
    id: int
    service_id: int
    order_id: int

    @classmethod
    def from_orm(cls, order_service):
        return cls(
            id=order_service.id,
            service_id=order_service.service_id,
            order_id=order_service.order_id,
        )