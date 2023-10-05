from datetime import datetime

from pydantic import BaseModel


class FileBaseSchema(BaseModel):
    name: str
    path: str
    size: int
    is_downloadable: bool
    user_id: int


class FileCreateSchema(FileBaseSchema):
    pass


class FileUpdateSchema(FileBaseSchema):
    pass


class FileResponseSchema(FileBaseSchema):
    id: int
    created_at: datetime


class FileListResponseSchema(BaseModel):
    account_id: int
    files: list[FileResponseSchema]