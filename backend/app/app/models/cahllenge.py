from typing import TYPE_CHECKING

from sqlalchemy import ARRAY, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  
    from .schedule import Schedule


class Challenge(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contents = Column(String)
    image = Column(String, nullable=True)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    tags = Column(ARRAY(str), nullable=True)
    user_details = relationship("ChallengeUserDetail", back_populates="challenge")
    schedules = relationship("ChallengeScheduleDetail", back_populates="challenge")
    requests = relationship("ChallengeRequest", back_populates="challenge")
