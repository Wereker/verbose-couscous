import jwt
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import TokenPayload, User
from app.repositories import UserRepository, RoleUserRepository
from app.db.db_helper import db_helper
from app.core.config import settings


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", scheme_name="JWT")
user_repository = UserRepository()
role_user_repository = RoleUserRepository()

async def get_current_user(
    db: AsyncSession = Depends(db_helper.session_getter),
    token: str = Depends(reuseable_oauth)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Декодирование токена с использованием pyjwt
        payload = jwt.decode(token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])
        token_data = TokenPayload(**payload)

        # Проверка истечения срока действия токена
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWKError:
        raise credentials_exception

    # Получаем пользователя по ID из базы данных
    user = await user_repository.get(db, username=token_data.sub)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user

async def get_role_of_user(user: User, db: AsyncSession):
    role = await role_user_repository.get_role_for_user(db, user.id)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has no role assigned"
        )
    return role

async def require_admin_role(user: User = Depends(get_current_user), db: AsyncSession = Depends(db_helper.session_getter)):
    role = await get_role_of_user(user, db)
    if role.name != "Администратор":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required"
        )
    return user

async def require_client_role(user: User = Depends(get_current_user), db: AsyncSession = Depends(db_helper.session_getter)):
    role = await get_role_of_user(user, db)
    
    if role.name != "Клиент":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this resource"
        )
    return user

async def require_worker_or_client_role(user: User = Depends(get_current_user), db: AsyncSession = Depends(db_helper.session_getter)):
    role = await get_role_of_user(user, db)
    
    if role.name not in ['Работник', 'Клиент']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this resource"
        )
    return user