import secrets

from sqlalchemy import UUID
from app.domain.entities.link import Link
from app.domain.repo.link_repository import LinkRepository
from app.domain.exceptions.link_exceptions import LinkNotFoundError
from app.domain.value_objects.short_code import ShortCode

class LinkService:
    def __init__(self, link_repo: LinkRepository):
        self.link_repo = link_repo
        
    def create_short_link(self, original_url: str, user_id: UUID) -> Link:
        short_code = self.generate_short_code()
        link = Link.create(original_url, short_code, user_id)
        return self.link_repo.save(link)
    
    def get_original_url(self, short_code: ShortCode) -> str:
        link = self.link_repo.get_by_short_code(short_code)
        if not link:
            raise LinkNotFoundError(short_code)
        
        link.increment_click_count()
        self.link_repo.save(link)
        return link.original_url
    
    def _generate_short_code(self) -> str:
        return secrets.token_urlsafe(6)[:6]