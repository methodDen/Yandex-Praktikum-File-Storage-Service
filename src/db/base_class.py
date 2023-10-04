import uuid

from sqlalchemy import (
    Column,
    Integer,
)
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr
from sqlalchemy_utils import UUIDType


@as_declarative()
class Base:
    __name__: str

    id = Column(UUIDType, primary_key=True, index=True, default=uuid.uuid4)

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()