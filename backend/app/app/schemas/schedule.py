import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Date, DateTime


# Shared properties
class ScheduleBase(BaseModel):
    id: int
    title: str
    contents: str
    image: Optional[str] = None
    start_date = DateTime
    # end_date: Optional[DateTime] = None


# Properties to receive on item creation
class ScheduleCreate(ScheduleBase):
    challange_id: Optional[str] = None


# Properties to receive on item update
class ScheduleUpdate(ScheduleBase):
    pass


# Properties shared by models stored in DB
class ScheduleInDBBase(ScheduleBase):
    id: int
    title: str
    user_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Schedule(ScheduleInDBBase):
    pass


# Properties properties stored in DB
class ScheduleInDB(ScheduleInDBBase):
    pass
