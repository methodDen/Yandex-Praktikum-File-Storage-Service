from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class File(
    TimestampMixin,
    Base,
):
    __tablename__ = "file"
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False,)
    user = relationship("User", back_populates="files")
    name = Column(String(255), nullable=False)
    path = Column(String(255), nullable=False, unique=True)
    size = Column(Integer, nullable=False)
    is_downloadable = Column(Boolean, default=True)

    def __repr__(self):
        return (
            "<File(file_name='%s')>"
            % (
                self.name,
            )
        )
