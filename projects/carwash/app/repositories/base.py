from typing import Generic, Type, TypeVar, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi_filter.contrib.sqlalchemy import Filter

# Типы для общей типизации
ModelType = TypeVar("ModelType")  # Тип SQLAlchemy модели
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)  # Тип Pydantic схемы создания
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)  # Тип Pydantic схемы обновления


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUDBase инициализируется моделью SQLAlchemy.
        :param model: SQLAlchemy модель (например, User, Car).
        """
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        """
        Получить объект по ID.
        """
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalars().first()

    async def get_all(self, db: AsyncSession, model_filter: Filter) -> List[ModelType]:
        """
        Получить все объекты с поддержкой пагинации.
        """
        query = model_filter.filter(select(self.model))
        query = model_filter.sort(query)
        result = await db.execute(query)
        return result.scalars().all()
    
        # result = await db.execute(select(self.model).limit(limit).offset(offset))
        # return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        """
        Создать новый объект.
        """
        obj = self.model(**obj_in.model_dump())
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def update(self, db: AsyncSession, id: int, obj_in: UpdateSchemaType) -> Optional[ModelType]:
        """
        Обновить объект по ID.
        """
        result = await db.execute(
            sqlalchemy_update(self.model)
            .where(self.model.id == id)
            .values(**obj_in.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        await db.commit()

        return result.scalars().first()

    async def delete(self, db: AsyncSession, id: int) -> bool:
        """
        Удалить объект по ID.
        """
        result = await db.execute(sqlalchemy_delete(self.model).where(self.model.id == id))
        await db.commit()
        return result.rowcount > 0
