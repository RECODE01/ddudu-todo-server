from sqlalchemy import Column, Integer, ForeignKey
from app.db.base_class import Base



class Link(Base):
    __tablename__ = 'link'
    challenge_id = Column(Integer, ForeignKey("challenge.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
