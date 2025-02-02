from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    password: str
    email: EmailStr
    is_send_notify: Optional[bool] = False


class UserCreate(UserBase):
    role_id: int


class UserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_send_notify: Optional[bool] = None


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


# Схема для отправки ответа о пользователях
class UserResponse(BaseModel):
    id: int
    full_name: str
    username: str
    email: EmailStr
    role: str

    @classmethod
    def from_orm(cls, user):
        return cls(
            id=user.id, 
            full_name=user.full_name,
            email=user.email,
            username=user.username,
            role=user.role_user.role.name
        )


# Отдельная схема для работников атомойки
class UserVO(BaseModel):
    id: int
    full_name: str

    @classmethod
    def from_orm(cls, user):
        return cls(
            id=user.id, 
            full_name=user.full_name
        )


# Отдельная схема для владельца автомобиля
class CustomerVO(UserVO):
    email: str

    @classmethod
    def from_orm(cls, user):
        return cls(
            id=user.id, 
            full_name=user.full_name,
            email=user.email
        )

    class Config:
        from_attributes = True


class UserSignUp(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None



class UserLogin(BaseModel):
    username: str
    password: str
