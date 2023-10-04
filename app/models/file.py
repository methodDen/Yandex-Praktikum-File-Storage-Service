from sqlalchemy import Column, String, Integer, ForeignKey
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

    def __repr__(self):
        return (
            "<User(username='%s')>"
            % (
                self.username,
            )
        )
