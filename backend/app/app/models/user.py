from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nick_name = Column(String, unique=True, index=True)
    picture: Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    deleted = Column(Boolean(), default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    items = relationship("Item", back_populates="owner")
    schedules = relationship("Schedule", back_populates="user")
    my_challenges = relationship("Schedule", back_populates="master")

    challenges = relationship('Challenge', secondary = 'link')
