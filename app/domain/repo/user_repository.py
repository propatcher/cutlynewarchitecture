from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import UUID
from app.domain.entities.user import User

class UserRepository(ABC):

    @abstractmethod
    async def get_by_id(self,id:UUID) -> Optional[User]:
        ...
    
    @abstractmethod
    async def get_by_login(self, login: str) -> Optional[User]:
        ...
        
    @abstractmethod
    async def get_by_email(self,email:str) -> Optional[User]:
        ...
        
    @abstractmethod
    async def save(self, user: User) -> User:
        ...