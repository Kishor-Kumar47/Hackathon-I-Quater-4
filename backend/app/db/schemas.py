from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    programming_level: Optional[str] = None
    hardware_background: Optional[str] = None
    ai_knowledge: Optional[str] = None
    ros_experience: Optional[bool] = None

class UserInDBBase(UserBase):
    id: Optional[int] = None
    programming_level: Optional[str] = None
    hardware_background: Optional[str] = None
    ai_knowledge: Optional[str] = None
    ros_experience: Optional[bool] = None

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
