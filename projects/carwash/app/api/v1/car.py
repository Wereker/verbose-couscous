from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi_pagination import Page, paginate
from fastapi_filter import FilterDepends

from app.schemas import CarResponse, CarCreate, CarUpdate, User
from app.utils.filters import CarFilter
from app.auth.dependencies import require_admin_role
from app.repositories import CarRepository
from app.db.db_helper import db_helper
from app.core.config import settings


router = APIRouter(
    prefix=settings.api.v1.cars,
    tags=["Car"],
)

car_repository = CarRepository()


@router.get("/", response_model=Page[CarResponse], status_code=status.HTTP_200_OK)
async def get_cars(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    car_filter: CarFilter = FilterDepends(CarFilter),
    user: User = Depends(require_admin_role)):

    cars = await car_repository.get_all(db, car_filter)

    return paginate([CarResponse.from_orm(car) for car in cars])


@router.post("/", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
async def create_car(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    car_in: CarCreate,
    user: User = Depends(require_admin_role)):

    car_created = await car_repository.create(db=db, obj_in=car_in)

    return CarResponse.from_orm(car_created)


@router.get("/{car_id}", response_model=CarResponse, status_code=status.HTTP_200_OK)
async def get_car(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    car_id: int,
    user: User = Depends(require_admin_role)):

    car = await car_repository.get(db=db, id=car_id)
    
    return CarResponse.from_orm(car)


@router.patch("/{car_id}", response_model=CarResponse, status_code=status.HTTP_200_OK)
async def update_car(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    car_id: int, 
    car_in: CarUpdate,
    user: User = Depends(require_admin_role)):

    car_updated = await car_repository.update(db=db, id=car_id, obj_in=car_in)

    return CarResponse.from_orm(car_updated)


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    car_id: int,
    user: User = Depends(require_admin_role)):

    await car_repository.delete(db=db, id=car_id)