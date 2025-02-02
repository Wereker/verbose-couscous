from fastapi import APIRouter, Depends, status, HTTPException, Security
from typing import Annotated
from fastapi_pagination import Page, paginate
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import BrandResponse, BrandCreate, BrandUpdate, User
from app.utils.filters import BrandFilter
from app.auth.dependencies import require_admin_role
from app.repositories import BrandRepository
from app.db.db_helper import db_helper
from app.core.config import settings
from app.auth.dependencies import reuseable_oauth

router = APIRouter(
    prefix=settings.api.v1.brands,
    tags=["Brand"],
)

brand_repository = BrandRepository()


@router.get("/", response_model=Page[BrandResponse], status_code=200)
async def get_brands(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    brand_filter: BrandFilter = FilterDepends(BrandFilter),
    user: User = Depends(require_admin_role)):

    brands = await brand_repository.get_all(db, brand_filter)

    return paginate([BrandResponse(id=brand.id, name=brand.name) for brand in brands])


@router.post("/", response_model=BrandResponse, status_code=status.HTTP_201_CREATED,)
async def create_brand(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    brand_in: BrandCreate,
    user: User = Depends(require_admin_role)):

    brand_created = await brand_repository.create(db, brand_in)

    return BrandResponse(id=brand_created.id, name=brand_created.name)


@router.get("/{brand_id}", response_model=BrandResponse, status_code=status.HTTP_200_OK)
async def get_brand(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    brand_id: int,
    user: User = Depends(require_admin_role)):

    brand = await brand_repository.get(db, brand_id)
    
    return BrandResponse(id=brand.id, name=brand.name)


@router.patch("/{brand_id}", response_model=BrandResponse, status_code=status.HTTP_200_OK)
async def update_brand(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    brand_id: int, 
    brand_in: BrandUpdate,
    user: User = Depends(require_admin_role)):

    brand_updated = await brand_repository.update(db, brand_id, brand_in)

    return BrandResponse(id=brand_updated.id, name=brand_updated.name)


@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_brand(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    brand_id: int,
    user: User = Depends(require_admin_role)):
    
    await brand_repository.delete(db, brand_id)