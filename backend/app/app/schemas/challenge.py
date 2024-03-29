import datetime
from typing import List, Optional
from app.schemas.user import User

from pydantic import BaseModel

# Shared properties
class Challenge(BaseModel):
    name: str
    contents: str
    image: Optional[str] = None
    start_date: datetime.datetime
    end_date: Optional[datetime.datetime] = None
    tags: Optional[List[str]] = None

# Properties to receive on item creation
class ChallengeCreate(Challenge):
    pass

# Properties to receive on item update
class ChallengeUpdate(Challenge):
    pass


# Properties shared by models stored in DB
class ChallengeInDBBase(Challenge):
    id: int
    class Config:
        orm_mode = True

class ChallengeDetailInDBBase(Challenge):
    id: int
    master : User
    class Config:
        orm_mode = True


# Properties to return to client
class Challenge(ChallengeInDBBase):
    user_cnt : Optional[int] = 1
    pass

class ChallengeDetail(ChallengeDetailInDBBase):
    pass

# Properties properties stored in DB
class ChallengeInDB(ChallengeInDBBase):
    pass