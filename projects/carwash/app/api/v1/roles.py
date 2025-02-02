from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, paginate

from app.schemas import RoleResponse, RoleCreate, RoleUpdate, User
from app.utils.filters import RoleFilter
from app.repositories import RoleRepository
from app.db.db_helper import db_helper
from app.core.config import settings
from app.auth.dependencies import require_admin_role

role_repository = RoleRepository()

router = APIRouter(
    prefix=settings.api.v1.roles,
    tags=["Role"],
)

@router.get("/", response_model=Page[RoleResponse], status_code=status.HTTP_200_OK)
async def get_roles(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    roles_filter: RoleFilter = FilterDepends(RoleFilter),
    user: User = Depends(require_admin_role)):

    roles = await role_repository.get_all(db, roles_filter)
    
    return paginate([RoleResponse.from_orm(role) for role in roles])


@router.get("/{role_id}", response_model=RoleResponse, status_code=status.HTTP_200_OK)
async def get_role(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    role_id: int,
    user: User = Depends(require_admin_role)):

    role = await role_repository.get(db, role_id)
    
    return RoleResponse.from_orm(role)


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    role_in: RoleCreate,
    user: User = Depends(require_admin_role)):

    role_created = await role_repository.create(db, role_in)

    return RoleResponse.from_orm(role_created)


@router.patch("/{role_id}", response_model=RoleResponse, status_code=status.HTTP_200_OK)
async def update_role(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    role_id: int, 
    role_in: RoleUpdate,
    user: User = Depends(require_admin_role)):
    
    role_updated = await role_repository.update(db, role_id, role_in)

    return RoleResponse.from_orm(role_updated)

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    role_id: int,
    user: User = Depends(require_admin_role)):
    
    await role_repository.delete(db, role_id)