import datetime
from typing import Optional

from pydantic import BaseModel

# Shared properties
class ChallengeRequest(BaseModel):
    pass

# Properties to receive on item creation
class ChallengeRequestCreate(ChallengeRequest):
    challenge_id: str
    pass

class ChallengeRequestUpdate(ChallengeRequest):
    challenge_id: str
    pass

class ChallengeRequestAccept(ChallengeRequest):
    id: int
    pass

# Properties shared by models stored in DB
class ChallengeRequestInDBBase(ChallengeRequest):
    id: int
    class Config:
        orm_mode = True

class ChallengeRequestDetailInDBBase(ChallengeRequest):
    id: int
    # user_details
    # schedules
    class Config:
        orm_mode = True


# Properties to return to client
class ChallengeRequest(ChallengeRequestInDBBase):
    pass

class ChallengeRequestDetail(ChallengeRequestDetailInDBBase):
    pass

# Properties properties stored in DB
class ChallengeRequestInDB(ChallengeRequestInDBBase):
    pass
