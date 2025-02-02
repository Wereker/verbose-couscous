from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, paginate

from app.schemas import ServiceResponse, ServiceCreate, ServiceUpdate, User
from app.utils.filters import ServiceFilter
from app.repositories import ServiceRepository
from app.db.db_helper import db_helper
from app.core.config import settings
from app.auth.dependencies import require_admin_role


router = APIRouter(
    prefix=settings.api.v1.services,
    tags=["Service"],
)

service_repository = ServiceRepository()


@router.get("/", response_model=Page[ServiceResponse], status_code=status.HTTP_200_OK)
async def get_services(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    services_filter: ServiceFilter = FilterDepends(ServiceFilter),
    user: User = Depends(require_admin_role)):

    services = await service_repository.get_all(db, services_filter)

    return paginate([ServiceResponse.from_orm(service) for service in services])


@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED, description="Цена и время указывается в **рублях** и в **минутах**")
async def create_service(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    service_in: ServiceCreate,
    user: User = Depends(require_admin_role)):

    service_created = await service_repository.create(db, service_in)

    return ServiceResponse.from_orm(service_created)


@router.get("/{service_id}", response_model=ServiceResponse, status_code=status.HTTP_200_OK)
async def get_service(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    service_id: int,
    user: User = Depends(require_admin_role)):

    service = await service_repository.get(db, service_id)
    
    return ServiceResponse.from_orm(service)


@router.patch("/{service_id}", response_model=ServiceResponse, status_code=status.HTTP_200_OK)
async def update_service(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    service_id: int, 
    service_in: ServiceUpdate,
    user: User = Depends(require_admin_role)):

    service_updated = await service_repository.update(db, service_id, service_in)

    return ServiceResponse.from_orm(service_updated)


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    service_id: int,
    user: User = Depends(require_admin_role)):
    
    await service_repository.delete(db, service_id)