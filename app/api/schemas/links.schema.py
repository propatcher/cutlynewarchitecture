from typing import Union
from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserRegisterRequest(BaseModel):
    login: str
    email: EmailStr
    password: str