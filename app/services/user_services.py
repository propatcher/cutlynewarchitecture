from typing import Optional
from pydantic import EmailStr
from app.domain.entities.user import User
from infra.auth.password_hasher import PasswordHasher


class UserService:
    def __init__(self, password_hasher: PasswordHasher):
        self.password_hasher = password_hasher
        
    def register_user(self, login:str, email:EmailStr, password: str) -> Optional[User]:
        hashed_password = self.password_hasher.hash(password)
        return User.create(login, email, hashed_password)