from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item
    from .schedule import Schedule


class ChallengeScheduleDetail(Base):
    __tablename__ = "challenge_schedule_detail"
    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("challenge.id"))
    challenge = relationship("Challenge", back_populates="schedules")
    schedules = relationship("Schedule", back_populates="challenge_info")
    title = Column(String, nullable=False)
    contents = Column(String, nullable=False)
    image = Column(String, nullable=False)
    start_date = Column(DateTime, default=func.now(), nullable=False)
    end_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
