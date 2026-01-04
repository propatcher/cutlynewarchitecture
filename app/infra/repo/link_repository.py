from typing import Optional
from domain.repo.link_repository import LinkRepository
from domain.entities.link import Link
from infra.database.models import LinkModel

class PostgresLinkRepository(LinkRepository):
    def __init__(self, db_session):
        self.db = db_session
    
    def get_by_short_code(self, code: str) -> Optional[Link]:
        model = self.db.query(LinkModel).filter(LinkModel.short_code == code).first()
        return self._to_entity(model) if model else None
    
    def get_by_url(self, url: str, user_id: str = None) -> Optional[Link]:
        query = self.db.query(LinkModel).filter(LinkModel.original_url == url).first()
        if user_id:
            query = query.filter(LinkModel.user_id == user_id)
        model = query.first()
        return self._to_entity(model) if model else None
    
    def save(self, link: Link) -> Link:
        model = LinkModel(
            id = link.id,
            original_url = link.original_url,
            short_code = link.short_code,
            user_id = link.user_id,
            click_count = link.click_count
        )
        self.db.add(model)
        self.db.commit()
        return link
    
    def get_user_links(self, user_id: str) -> list[Link]:
        models = self.db.query(LinkModel).filter(LinkModel.user_id == user_id).all()
        return [self._to_entity(model) for model in models]
        
    def _to_entity(self, model: LinkModel) -> Link:
        return Link(
            id = model.id,
            original_url = model.original_url,
            short_code = model.short_code,
            user_id = model.user_id,
            created_at = model.created_at,
            click_count = model.click_count
        )