from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  
    from .schedule import Schedule


class ChallengeUserDetail(Base):
    __tablename__ = "challenge_user_detail"
    id = Column(Integer, primary_key=True, index=True)
    is_master = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="challenges")
    challenge_id = Column(Integer, ForeignKey("challenge.id"))
    challenge = relationship("Challenge", back_populates="user_details")