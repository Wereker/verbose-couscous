from typing import Optional
from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    ...


class RoleUpdate(BaseModel):
    name: Optional[str] = None


class Role(RoleBase):
    id: int

    class Config:
        from_attributes = True


class RoleResponse(BaseModel):
    id: int
    name: str

    @classmethod
    def from_orm(cls, role):
        return cls(
            id=role.id,
            name=role.name
        )



class RoleVO(BaseModel):
    name: str

    @classmethod
    def from_orm(cls, role):
        return cls(
            id=role.id,
            name=role.name
        )