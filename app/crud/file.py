from app.crud.base import CRUDBase
from app.models import File
from app.schemas.file import (
    FileCreateSchema,
    FileUpdateSchema,
)


class CRUDFile(CRUDBase[File, FileCreateSchema, FileUpdateSchema]):
    pass


file = CRUDFile(File)