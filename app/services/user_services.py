from typing import Optional
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.user import User
from app.infra.repo.user_repository import UserPostgresRepository
from app.infra.auth.password_hasher import PasswordHasher
from app.domain.exceptions.user_exceptions import UserAlreadyExists

class UserService:
    def __init__(
        self, 
        user_repository: UserPostgresRepository,
        password_hasher: PasswordHasher,
        db_session: AsyncSession        
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.db_session = db_session    
        
    async def register_user(self, login:str, email:EmailStr, password: str) -> Optional[User]:
        existing_user = await self.user_repository.get_by_email(email = email)
        if existing_user:
            raise UserAlreadyExists("Пользователь уже существует")
        
        hashed_password = self.password_hasher.hash(password)
        user = User.create(login, email, hashed_password) 
        try:      
            saved_user = await self.user_repository.save(user)
            await self.db_session.commit()
            return saved_user
        except Exception as e:
            await self.db_session.rollback()
            raise e