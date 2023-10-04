from sqlalchemy import Column, String

from src.db.base_class import Base
from src.models.mixins import TimestampMixin


class User(
    TimestampMixin,
    Base,
):
    __tablename__ = "user"
    username = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)