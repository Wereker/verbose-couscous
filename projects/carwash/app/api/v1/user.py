from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check

from app.schemas import UserResponse, UserCreate, UserUpdate, User
from app.utils.filters import UserFilter
from app.repositories import UserRepository
from app.db.db_helper import db_helper
from app.core.config import settings
from app.auth.dependencies import require_admin_role

disable_installed_extensions_check()

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["User"],
)

user_repository = UserRepository()


@router.get("/", response_model=Page[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    users_filter: UserFilter = FilterDepends(UserFilter),
    user: User = Depends(require_admin_role)):

    users = await user_repository.get_all(db, users_filter)

    return paginate([UserResponse.from_orm(user) for user in users])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    user_in: UserCreate,
    user: User = Depends(require_admin_role)):

    user_created = await user_repository.create(db, user_in)

    return UserResponse.from_orm(user_created)


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    user_id: int,
    user: User = Depends(require_admin_role)):

    db_user = await user_repository.get(db, user_id)
    
    return UserResponse.from_orm(db_user)

@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    user_id: int, 
    user_in: UserUpdate,
    user: User = Depends(require_admin_role)):

    user_updated = await user_repository.update(db, user_id, user_in)

    return UserResponse.from_orm(user_updated)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    user_id: int,
    user: User = Depends(require_admin_role)):
    
    await user_repository.delete(db, user_id)