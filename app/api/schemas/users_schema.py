from pydantic import BaseModel, EmailStr

class SUserRegistration(BaseModel):
    login: str
    email: EmailStr
    password: str