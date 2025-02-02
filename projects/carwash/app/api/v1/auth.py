from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.schemas import UserResponse, UserSignUp, Token, UserProfile, UserUpdate
from app.repositories import UserRepository, RoleRepository
from app.db.db_helper import db_helper
from app.core.config import settings
from app.auth.utils import verify_password
from app.auth.dependencies import  get_current_user

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)

user_repository = UserRepository()
role_repository = RoleRepository()

@router.post("/signup", summary="Create new user", response_model=UserResponse)
async def signup_user(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)], 
    user_in: UserSignUp,
    role_id: int):

    # user = await user_repository.get(db, email=user_in.email)
    # if user is not None:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="User with this email already exist"
    #     )
    
    role = await role_repository.get(db, role_id)
    
    user_created = await user_repository.signup(db, user_in, role_id)

    return UserResponse.from_orm(user_created)


@router.post("/login", summary="Create access and refresh tokens for user", response_model=Token)
async def login_user(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    form_data: OAuth2PasswordRequestForm = Depends()
):
    # Аутентификация пользователя по username (email) и паролю
    user = await user_repository.get(db, username=form_data.username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )

    # Создание токенов
    access_token, refresh_token = await user_repository.login(db, form_data.username, form_data.password)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )

