from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.schemas import UserProfile, UserUpdate, CustomerCarsProfileCreate, CustomerCarsResponse
from app.repositories import UserRepository, CustomerCarsRepository
from app.db.db_helper import db_helper
from app.core.config import settings
from app.auth.dependencies import  get_current_user


router = APIRouter(
    prefix=settings.api.v1.profile,
    tags=["Profile"],
)

user_repository = UserRepository()
customer_car_repository = CustomerCarsRepository()


@router.get('/me', summary='Get profile current user', response_model=UserProfile, status_code=status.HTTP_200_OK)
async def get_me(user: UserProfile = Depends(get_current_user)):
    
    return UserProfile.from_orm(user)


@router.patch("/me", summary="Update profile current user", response_model=UserProfile, status_code=status.HTTP_200_OK)
async def update_me(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[UserProfile, Depends(get_current_user)],
    user_in: UserUpdate):
    
    updated_user = await user_repository.update(db, user.id, user_in)

    return UserProfile.from_orm(user)


@router.post('/me/vehicles', summary="Registration of the vehicle to the user", response_model=UserProfile, status_code=status.HTTP_200_OK)
async def register_vehicles(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[UserProfile, Depends(get_current_user)],
    car_in: CustomerCarsProfileCreate):
    
    customer_car = await customer_car_repository.regiser_car_to_user(db, user.id, car_in)
    await db.refresh(user)
    
    return UserProfile.from_orm(user)