from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Challenge_request(Base):
    __tablename__ = "challenge_request"
    id = Column(Integer, primary_key=True, index=True)
    is_accept = Column(Boolean, default=False)
    challenge_id = Column(Integer, ForeignKey("challenge.id"))
    challenge = relationship("Challenge", back_populates="requests")
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="requests")
