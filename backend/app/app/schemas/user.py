from typing import List, Optional
from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    nick_name: str
    picture: Optional[str] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None
    nick_name: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None
    complete_rate: Optional[float] = None
    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass

# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str