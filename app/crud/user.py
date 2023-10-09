from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import User
from app.schemas.user import (
    UserCreateSchema,
    UserUpdateSchema,
)
from app.services.password import get_password_hash


class CRUDUser(CRUDBase[User, UserCreateSchema, UserUpdateSchema]):
    async def create(self, db: AsyncSession, *, obj_in: UserCreateSchema) -> User:
        """
        Create a new row in the database
        """
        obj_in_data = jsonable_encoder(obj_in)
        password = obj_in_data.pop('password')
        hashed_password = get_password_hash(password)
        obj_in_data['password'] = hashed_password
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        return db_obj

    async def get_by_username(self, db: AsyncSession, *, username: str) -> User:
        """
        Get user by username
        """
        query = select(
            self.model
        ).where(
            self.model.username == username
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()


user = CRUDUser(User)