from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

if TYPE_CHECKING:
    from .schedule import Schedule  # noqa: F401


class Schedule(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    contents = Column(String, nullable=False)
    image = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="schedules")
    challange_id = Column(Integer, ForeignKey("challange.id"), nullable=True)
    challange = relationship("User", back_populates="user_schedules")
    completed = Column(Boolean, default=False)
    start_date = Column(DateTime, default=func.now(), nullable=False)
    end_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
