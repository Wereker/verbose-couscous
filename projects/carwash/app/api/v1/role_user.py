from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, paginate

from app.schemas import RoleUserResponse, RoleUserCreate, RoleUserUpdate, User
from app.utils.filters import RoleUserFilter
from app.repositories import RoleUserRepository
from app.db.db_helper import db_helper
from app.core.config import settings
from app.auth.dependencies import require_admin_role


router = APIRouter(
    prefix=settings.api.v1.role_users,
    tags=["Role User"],
)

role_user_repository = RoleUserRepository()


@router.get("/", response_model=Page[RoleUserResponse], status_code=status.HTTP_200_OK)
async def get_role_users(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    role_users_filter: RoleUserFilter = FilterDepends(RoleUserFilter),
    user: User = Depends(require_admin_role)):

    role_users = await role_user_repository.get_all(db, role_users_filter)

    return paginate([RoleUserResponse.from_orm(role_user) for role_user in role_users])


@router.post("/", response_model=RoleUserResponse, status_code=status.HTTP_201_CREATED)
async def create_role_user(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    role_user_in: RoleUserCreate,
    user: User = Depends(require_admin_role)):

    role_user_created = await role_user_repository.create(db, role_user_in)

    return RoleUserResponse.from_orm(role_user_created)


@router.get("/{role_user_id}", response_model=RoleUserResponse, status_code=status.HTTP_200_OK)
async def get_role_user(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    role_user_id: int,
    user: User = Depends(require_admin_role)):

    role_user = await role_user_repository.get(db, role_user_id)
    
    return RoleUserResponse.from_orm(role_user)


@router.patch("/{role_user_id}", response_model=RoleUserResponse, status_code=status.HTTP_200_OK)
async def update_role_user(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    role_user_id: int, role_user_in: RoleUserUpdate,
    user: User = Depends(require_admin_role)):

    role_user_updated = await role_user_repository.update(db, role_user_id, role_user_in)

    return RoleUserResponse.from_orm(role_user_updated)


@router.delete("/{role_user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role_user(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    role_user_id: int,
    user: User = Depends(require_admin_role)):

    await role_user_repository.delete(db, role_user_id)