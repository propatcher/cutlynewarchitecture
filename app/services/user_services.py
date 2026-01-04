from typing import Optional
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.user import User
from app.infra.repo.user_repository import UserPostgresRepository
from infra.auth.password_hasher import PasswordHasher
from domain.exceptions.user_exceptions import UserAlreadyExist

class UserService:
    def __init__(
        self, 
        user_repository: UserPostgresRepository,
        password_hasher: PasswordHasher,        
        db: AsyncSession
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        
    def register_user(self, login:str, email:EmailStr, password: str) -> Optional[User]:
        existing_user = self.user_repository.get_by_email(email = email)
        if existing_user:
            raise UserAlreadyExist
        
        hashed_password = self.password_hasher.hash(password)
        user = User.create(login, email, hashed_password)
        saved_user = await self.user_repository.save(user)
        await self.db.commit()
        
        return saved_user