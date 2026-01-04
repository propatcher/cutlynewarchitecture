from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.user import User

class UserRepository(ABC):

    @abstractmethod
    def get_by_id(self,id:str) -> Optional[User]:
        ...
    
    @abstractmethod
    def get_by_login(self, login: str) -> Optional[User]:
        ...
        
    @abstractmethod
    def get_by_email(self,email:str) -> Optional[User]:
        ...
        
    @abstractmethod
    def save(self, user: User) -> User:
        ...