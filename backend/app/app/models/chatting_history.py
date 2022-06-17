from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class ChattingHistory(Base):
    __tablename__ = "chatting_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="chatting_histories")
    challenge_id = Column(Integer, ForeignKey("challenge.id"))
    challenge = relationship("Challenge", back_populates="chatting_histories")
    contents = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
