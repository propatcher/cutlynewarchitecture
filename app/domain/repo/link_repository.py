from abc import ABC, abstractmethod
from typing import Optional
from app.domain.value_objects.short_code import ShortCode
from domain.entities.link import Link

class LinkRepository(ABC):

    @abstractmethod
    def get_by_short_code(self,code:ShortCode) -> Optional[Link]:
        ...
    
    @abstractmethod
    def get_by_url(self, url: str, user_id: str = None) -> Optional[Link]:
        ...
        
    @abstractmethod
    def save(self, link: Link) -> Link:
        ...
    
    @abstractmethod
    def get_user_links(self, user_id: str) -> list[Link]:
        ...