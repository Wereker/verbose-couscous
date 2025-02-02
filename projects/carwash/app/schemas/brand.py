from typing import Optional
from pydantic import BaseModel
from fastapi_pagination import Page


class BrandBase(BaseModel):
    name: str


class BrandCreate(BrandBase):
    ...


class BrandUpdate(BaseModel):
    name: Optional[str] = None


class Brand(BrandBase):
    id: int

    class Config:
        from_attributes = True


class BrandResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True