from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, paginate

from app.schemas import CustomerCarsResponse, CustomerCarsCreate, CustomerCarsUpdate, User
from app.utils.filters import CustomerCarFilter
from app.repositories import CustomerCarsRepository
from app.db.db_helper import db_helper
from app.core.config import settings
from app.auth.dependencies import require_admin_role


router = APIRouter(
    prefix=settings.api.v1.customer_cars,
    tags=["Customer Car"],
)

customer_car_repository = CustomerCarsRepository()


@router.get("/", response_model=Page[CustomerCarsResponse], status_code=status.HTTP_200_OK)
async def get_customer_cars(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    customer_cars_filter: CustomerCarFilter = FilterDepends(CustomerCarFilter),
    user: User = Depends(require_admin_role)):

    customer_cars = await customer_car_repository.get_all(db, customer_cars_filter)

    return paginate([CustomerCarsResponse.from_orm(customer_car) for customer_car in customer_cars])


@router.post("/", response_model=CustomerCarsResponse, status_code=status.HTTP_201_CREATED)
async def create_customer_car(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    customer_car_in: CustomerCarsCreate,
    user: User = Depends(require_admin_role)):

    customer_car_created = await customer_car_repository.create(db, customer_car_in)

    return CustomerCarsResponse.from_orm(customer_car_created)


@router.get("/{customer_car_id}", response_model=CustomerCarsResponse, status_code=status.HTTP_200_OK)
async def get_customer_car(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    customer_car_id: int,
    user: User = Depends(require_admin_role)):

    customer_car = await customer_car_repository.get(db, customer_car_id)
    
    return CustomerCarsResponse.from_orm(customer_car)


@router.patch("/{customer_car_id}", response_model=CustomerCarsResponse, status_code=status.HTTP_200_OK)
async def update_customer_car(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    customer_car_id: int, 
    customer_car_in: CustomerCarsUpdate,
    user: User = Depends(require_admin_role)):

    customer_car_updated = await customer_car_repository.update(db, customer_car_id, customer_car_in)

    return CustomerCarsResponse.from_orm(customer_car_updated)


@router.delete("/{customer_car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_car(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    customer_car_id: int,
    user: User = Depends(require_admin_role)):
    
    await customer_car_repository.delete(db, customer_car_id)