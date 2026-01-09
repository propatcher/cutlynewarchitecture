from datetime import timedelta
from typing import Optional
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.user import User
from app.infra.auth.token_setter import create_access_token
from app.infra.repo.user_repository import UserPostgresRepository
from app.infra.auth.password_hasher import PasswordHasher
from app.domain.exceptions.user_exceptions import UserAlreadyExists, UserNotExist

class UserService:
    def __init__(self, user_repository: UserPostgresRepository,password_hasher: PasswordHasher,db_session: AsyncSession):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.db_session = db_session    
        
    async def register_user(self, login:str, email:EmailStr, password: str) -> Optional[User]:
        existing_email = await self.user_repository.get_by_email(email = email)
        if existing_email:
            raise UserAlreadyExists("Пользователь уже существует")
        existing_login = await self.user_repository.get_by_login(login=login)
        if existing_login:
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
    async def authenticate_user(self, username:str, password:str) -> User:
        existing_user = await self.user_repository.get_by_username(username=username)
        if not existing_user:
            raise UserNotExist("Аутентификация не пройдена")
        is_password_valid = self.password_hasher.verify(password,existing_user.hashed_password)
        if not is_password_valid:
            raise UserNotExist("Аутентификация не пройдена")
        return existing_user
            
    async def get_token_and_authenticate_user(self,username:str, password:str) -> tuple[User, str]:
        user = await self.authenticate_user(username=username,password=password)
        access_token_expires = timedelta(minutes=60)
        access_token = create_access_token(
            data={"sub": user.login,
            "type": "access", 
            "user_id": str(user.id)}, 
            expires_delta=access_token_expires
        )
        return user,access_token