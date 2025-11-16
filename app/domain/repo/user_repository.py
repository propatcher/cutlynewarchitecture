from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.user import User

class UserRepository(ABC):

    @abstractmethod
    def get_by_id(self,code:str) -> Optional[User]:
        ...
    
    @abstractmethod
    def get_by_login(self, user: User) -> User:
        ...
    