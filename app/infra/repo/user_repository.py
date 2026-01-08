from typing import Optional
from sqlalchemy import select,or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.repo.user_repository import UserRepository
from app.domain.entities.user import User
from app.infra.database.models import UserModel
from uuid import UUID

class UserPostgresRepository(UserRepository):
    def __init__(self, db_session: AsyncSession):
        self.db = db_session    

    async def get_by_id(self,id:UUID) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.id == id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def get_by_login(self,login:str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.login == login)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def get_by_email(self,email:str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
        
    async def get_by_username(self,username:str) -> Optional[User]:
        stmt = select(UserModel).where(or_(UserModel.email == username, UserModel.login == username))
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def save(self, user: User) -> User:
        stmt = select(UserModel).where(UserModel.id == user.id)
        result = await self.db.execute(stmt)
        existing = result.scalar_one_or_none()
        
        if existing:
            existing.login = user.login
            existing.email = user.email
            existing.hashed_password = user.hashed_password
            existing.created_at = user.created_at
        else:
            model = UserModel(
                id=user.id,
                login=user.login,
                email=user.email,
                hashed_password=user.hashed_password,
                created_at=user.created_at
            )
            self.db.add(model)
        
        return user

    def _to_entity(self, model:UserModel) -> User:
        return User(
            id = model.id,
            login = model.login,
            email = model.email,
            hashed_password = model.hashed_password,
            created_at = model.created_at
        )