from typing import Union
from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserRegisterRequest(BaseModel):
    login: str
    email: EmailStr
    password: str

class UserLoginRequest(BaseModel):
    username: Union[str, EmailStr]
    password: str

class UserResponse(BaseModel):
    id: UUID
    login: str
    email: str
    created_at: datetime
    
    class Config:
        orm_mode = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    
class UserRegisterResponse(BaseModel):
    user: UserResponse 
    token: TokenResponse