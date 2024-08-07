from datetime import datetime
import email
from typing import Optional
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class PostResponse(PostBase):
    created_at: datetime
    id: int
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True
        
class PostVote(BaseModel):
    Post: PostResponse
    votes: int
    
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    

class Vote(BaseModel):
    post_id: int
    like_status: bool