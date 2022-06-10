import datetime
from typing import Optional

from pydantic import BaseModel

# Shared properties
class ChallengeUserDetail(BaseModel):
    pass

# Properties to receive on item creation
class ChallengeUserDetailCreate(ChallengeUserDetail):
    is_master: Optional[bool] = False
    challenge_id: str

class ChallengeUserDetailUpdate(ChallengeUserDetail):
    is_master: Optional[bool] = False
    challenge_id: str

# Properties shared by models stored in DB
class ChallengeUserDetailInDBBase(ChallengeUserDetail):
    id: int
    class Config:
        orm_mode = True

class ChallengeUserDetailDetailInDBBase(ChallengeUserDetail):
    id: int
    # user_details
    # schedules
    class Config:
        orm_mode = True


# Properties to return to client
class ChallengeUserDetail(ChallengeUserDetailInDBBase):
    pass

class ChallengeUserDetailDetail(ChallengeUserDetailDetailInDBBase):
    pass

# Properties properties stored in DB
class ChallengeUserDetailInDB(ChallengeUserDetailInDBBase):
    pass
