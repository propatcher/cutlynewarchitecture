from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import UUID
from app.domain.value_objects.short_code import ShortCode
from app.domain.entities.link import Link

class LinkRepository(ABC):

    @abstractmethod
    async def get_by_short_code(self,code:ShortCode) -> Optional[Link]:
        ...
    
    @abstractmethod
    async def get_by_url(self, url: str, user_id: UUID = None) -> Optional[Link]:
        ...
        
    @abstractmethod
    async def save(self, link: Link) -> Link:
        ...
    
    @abstractmethod
    async def get_user_links(self, user_id: UUID) -> list[Link]:
        ...