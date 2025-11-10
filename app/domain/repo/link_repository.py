from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.link import Link

class LinkRepository(ABC):
    
    @abstractmethod
    def get_by_short_code(self,code:str) -> Optional[Link]:
        ...
    
    @abstractmethod
    def save(self, link: Link) -> Link:
        ...
    
    @abstractmethod
    def get_user_links(self, user_id: str) -> list[Link]:
        ...