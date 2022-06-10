import datetime
from typing import Optional

from pydantic import BaseModel

# Shared properties


class ChallengeScheduleDetail(BaseModel):
    title: str
    contents: str
    image: str
    start_date: datetime.date
    end_date: Optional[datetime.date] = None
    pass

# Properties to receive on item creation


class ChallengeScheduleDetailCreate(ChallengeScheduleDetail):
    pass


class ChallengeScheduleDetailUpdate(ChallengeScheduleDetail):
    pass
# Properties shared by models stored in DB


class ChallengeScheduleDetailInDBBase(ChallengeScheduleDetail):
    id: int
    #challenge
    class Config:
        orm_mode = True


class ChallengeScheduleDetailDetailInDBBase(ChallengeScheduleDetail):
    id: int
    class Config:
        orm_mode = True


# Properties to return to client
class ChallengeScheduleDetail(ChallengeScheduleDetailInDBBase):
    pass


class ChallengeScheduleDetailDetail(ChallengeScheduleDetailDetailInDBBase):
    pass

# Properties properties stored in DB


class ChallengeScheduleDetailInDB(ChallengeScheduleDetailInDBBase):
    pass
