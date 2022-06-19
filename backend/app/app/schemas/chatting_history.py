# import datetime
# from typing import List, Optional
import datetime
from app.schemas.user import User

from pydantic import BaseModel

# Shared properties
class ChattingHistoryBase(BaseModel):
    contents : str
#입력할 때, 수정할 때 들어가는 애들, 다른 스키마들의 교집합

class ChattingHistoryCreate(ChattingHistoryBase):
    pass

class ChattingHistoryUpdate(ChattingHistoryBase):
    pass

class ChattingHistoryInDBBase(ChattingHistoryBase):
    id : int
    user : User
    created_at : datetime.datetime
    class Config:
        orm_mode = True
# 뿌려줄 때, 줄 수 있는 게 콘텐츠랑 아이디, 사용자들에게 보여줄 것들. createdAt, userInfo, challengeInfo

class ChattingHistory(ChattingHistoryInDBBase):
    pass