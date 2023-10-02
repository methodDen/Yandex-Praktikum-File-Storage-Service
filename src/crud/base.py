from typing import (
    Any,
    Generic,
    Optional,
    Type,
    TypeVar,
    List,
)

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from src.db.base_class import Base
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get_multi_query(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 0,
    ) -> List[ModelType]:
        """
        Get multiple ORM-level SQL construction object
        """
        query = select(self.model).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """
        Return the first result or None if the result doesn't contain any row
        """
        query = select(self.model).where(self.model.id == id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new row in the database
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_multi(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> List[ModelType]:
        """
        Create multiple rows in the database
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_objs = [self.model(**obj_in_data) for obj_in_data in obj_in_data]
        db.add_all(db_objs)
        await db.commit()
        for db_obj in db_objs:
            await db.refresh(db_obj)
        return db_objs
