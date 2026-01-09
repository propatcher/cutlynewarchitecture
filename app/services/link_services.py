import secrets

from sqlalchemy import UUID
from app.domain.entities.link import Link
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.exceptions.link_exceptions import LinkNotFoundError
from app.domain.value_objects.short_code import ShortCode
from app.infra.repo.link_repository import LinkPostgresRepository

class LinkService:
    def __init__(self, link_repository: LinkPostgresRepository):
        self.link_repository = link_repository
        
    def create_short_link(self, original_url: str, user_id: UUID) -> Link:
        short_code = self.generate_short_code()
        link = Link.create(original_url, short_code, user_id)
        return self.link_repository.save(link)
    
    def get_original_url(self, short_code: ShortCode) -> str:
        link = self.link_repository.get_by_short_code(short_code)
        if not link:
            raise LinkNotFoundError(short_code)
        
        link.increment_click_count()
        self.link_repository.save(link)
        return link.original_url
    
    def _generate_short_code(self) -> str:
        return secrets.token_urlsafe(6)[:6]