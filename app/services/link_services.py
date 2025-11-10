import hashlib
import secrets
from domain.entities.link import Link
from domain.repo.link_repository import LinkRepository

class LinkService:
    def __init__(self, link_repo: LinkRepository):
        self.link_repo = link_repo
        
    def create_short_link(self, original_url: str, user_id: str) -> Link:
        short_code = self.generate_short_code()
        link = Link.create(original_url, short_code, user_id)
        return self.link_repo.save()
    
    def get_original_url(self, short_code: str) -> str:
        link = self.link_repo.get_by_short_code(short_code)
        if not link:
            raise LinkNotFoundError()
        
        link.increment_click_count()
        self.link_repo.save(link)
        return link.original_url
    
    def _generate_short_code(self) -> str:
        return secrets.token_urlsafe(6)[:6]