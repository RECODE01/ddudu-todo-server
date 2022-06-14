import datetime
from typing import Optional
from app.schemas.user import User

from pydantic import BaseModel
from sqlalchemy import Date, DateTime

from app.models.challenge_schedule_detail import ChallengeScheduleDetail


# Shared properties
class ScheduleBase(BaseModel):
    title: str
    contents: str
    image: Optional[str] = None
    completed: Optional[bool] = False
    start_date: datetime.datetime
    end_date: Optional[datetime.datetime] = None


# Properties to receive on item creation
class ScheduleCreate(ScheduleBase):
    pass
class ChallengeScheduleCreate(BaseModel):
    title: str
    contents: str
    image: Optional[str] = None
    start_date: datetime.datetime
    end_date: Optional[datetime.datetime] = None

# Properties to receive on item update
class ScheduleUpdate(ScheduleBase):
    pass


# Properties shared by models stored in DB
class ScheduleInDBBase(ScheduleBase):
    id: int
    user : User
    # challenge_info: None
    class Config:
        orm_mode = True


# Properties to return to client
class Schedule(ScheduleInDBBase):
    pass


# Properties properties stored in DB
class ScheduleInDB(ScheduleInDBBase):
    pass
