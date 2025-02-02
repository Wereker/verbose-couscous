from typing import Optional
from pydantic import BaseModel


class RoleUserBase(BaseModel):
    user_id: int
    role_id: int


class RoleUserCreate(BaseModel):
    user_id: int
    role_id: int


class RoleUserUpdate(BaseModel):
    user_id: Optional[int] = None
    role_id: Optional[int] = None


class RoleUser(RoleUserBase):
    id: int

    class Config:
        from_attributes = True


class RoleUserResponse(BaseModel):
    id: int
    user_id: int
    role_id: int

    @classmethod
    def from_orm(cls, role_user):
        return cls(
            id=role_user.id,
            user_id=role_user.user_id,
            role_id=role_user.role_id,
        )