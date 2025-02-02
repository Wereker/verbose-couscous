from fastapi_filter.contrib.sqlalchemy import Filter
from fastapi_filter import FilterDepends, with_prefix
from typing import Optional, List
from pydantic import ConfigDict
from pydantic import BaseModel


from app.models import (
    Brand,
    Car,
    Role,
    Service,
    User,
    RoleUser,
    CustomerCars,
    Order,
    OrderService,
)


class BaseFilter(Filter):
    model_config = ConfigDict(protected_namespaces=())


class BrandFilter(BaseFilter):
    name__ilike: Optional[str] = None 
    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = Brand


class CarFilter(BaseFilter):
    model__ilike: Optional[str] = None
    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = Car


class UserFilter(BaseFilter):
    first_name__ilike: Optional[str] = None
    last_name__ilike: Optional[str] = None
    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = User


class ServiceFilter(BaseFilter):
    name__ilike: Optional[str] = None
    price__gt: Optional[int] = None
    price__lt: Optional[int] = None
    time__gt: Optional[int] = None
    time__lt: Optional[int] = None
    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = Service


class RoleFilter(BaseFilter):
    name__ilike: Optional[str] = None
    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = Role


class RoleUserFilter(BaseFilter):
    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = RoleUser


class CustomerCarFilter(BaseFilter):
    year__gt: Optional[int] = None
    year__lt: Optional[int] = None
    number__ilike: Optional[str] = None
    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = CustomerCars


class OrderFilter(BaseFilter):
    status__in: Optional[List[int]] = None
    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = Order


class OrderServiceFilter(BaseFilter):
    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = OrderService


class CustomOrderFilter(BaseModel):
    brand_name_ilike: Optional[str] = None
    car_number_ilike: Optional[str] = None
    car_year_gt: Optional[int] = None
    car_year_lt: Optional[int] = None