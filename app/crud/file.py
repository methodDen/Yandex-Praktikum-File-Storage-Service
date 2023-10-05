from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import File as FileType
from app.crud.base import CRUDBase
from app.models import File
from app.schemas.file import (
    FileCreateSchema,
    FileUpdateSchema,
)
from app.services.file import write_to_file


class CRUDFile(CRUDBase[File, FileCreateSchema, FileUpdateSchema]):

    async def delete_by_name(self, db: AsyncSession, file_name: str):
        query = delete(self.model).where(self.model.name == file_name)
        await db.execute(query)
        await db.commit()

    async def create_or_override_file(
        self,
        db: AsyncSession,
        file_to_save: FileType,
        path_to_save: str,
        file_owner_id: int,
    ):
        await write_to_file(file_to_save, path_to_save)

        file_object = await self.get_file_by_name(db, file_to_save.filename)
        if file_object:
            await self.delete_by_name(db, file_to_save.filename)

        file_object = await self.create(
            db,
            obj_in=FileCreateSchema(
                name=file_to_save.filename,
                path=path_to_save,
                size=file_to_save.size,
                is_downloadable=True,
                user_id=file_owner_id,
            )
        )
        return file_object

    async def get_file_by_name(self, db: AsyncSession, file_name: str):
        query = select(self.model).where(self.model.name == file_name)
        file_object = await db.execute(query)
        return file_object.scalar_one_or_none()

    async def get_file_list_by_user_id(self, db: AsyncSession, user_id: int):
        query = select(self.model).where(self.model.user_id == user_id)
        file_list = await db.execute(query)
        return file_list.scalars().all()

    async def get_file_by_id(self, db: AsyncSession, file_id: int, user_id: int,):
        query = select(self.model).where(self.model.id == file_id, self.model.user_id == user_id)
        file_object = await db.execute(query)
        return file_object.scalar_one_or_none()

    async def get_file_by_path(self, db: AsyncSession, file_path: str, user_id: int,):
        query = select(self.model).where(self.model.path == file_path, self.model.user_id == user_id)
        file_object = await db.execute(query)
        return file_object.scalar_one_or_none()




file = CRUDFile(File)