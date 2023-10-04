from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class User(
    TimestampMixin,
    Base,
):
    __tablename__ = "user"
    username = Column(String(128), nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    files = relationship("File", back_populates="user")

    def __repr__(self):
        return (
            "<User(username='%s')>"
            % (
                self.username,
            )
        )
