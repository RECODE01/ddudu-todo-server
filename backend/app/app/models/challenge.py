from typing import TYPE_CHECKING

from sqlalchemy import ARRAY, Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

if TYPE_CHECKING:
    from .schedule import Schedule  # noqa: F401


class Challenge(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    contents = Column(String, nullable=False)
    image = Column(String, nullable=False)
    master_id = Column(Integer, ForeignKey("user.id"))
    tags = Column(ARRAY(String), nullable=True)
    start_date = Column(DateTime, default=func.now(), nullable=False)
    end_date = Column(DateTime, default=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    master = relationship("User", back_populates="my_callange")

    users = relationship('User', secondary = 'link')
