from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserRegisterRequest(BaseModel):
    login: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    login: str
    email: str
    created_at: datetime
    
    class Config:
        orm_mode = True
