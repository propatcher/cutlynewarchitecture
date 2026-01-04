from typing import Optional

from sqlalchemy import select
from app.domain.value_objects.short_code import ShortCode
from domain.repo.link_repository import LinkRepository
from domain.entities.link import Link
from sqlalchemy.ext.asyncio import AsyncSession
from infra.database.models import LinkModel

class PostgresLinkRepository(LinkRepository):
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def get_by_short_code(self, code: ShortCode) -> Optional[Link]:
        stmt = select(LinkModel).where(LinkModel.short_code == code.value)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None    
        
    async def get_by_url(self, url: str, user_id: str = None) -> Optional[Link]:
        stmt = select(LinkModel).where(LinkModel.original_url == url)
        if user_id:
            stmt = stmt.where(LinkModel.user_id == user_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def save(self, link: Link) -> Link:
        stmt = select(LinkModel).where(LinkModel.id == link.id)
        result = await self.db.execute(stmt)
        existing = result.scalar_one_or_none()
        
        if existing:
            existing.original_url = link.original_url,
            existing.short_code = link.short_code.value,
            existing.user_id = link.user_id,
            existing.click_count = link.click_count
        
        else:
            model = LinkModel(
                id=link.id,
                original_url=link.original_url,
                short_code=link.short_code.value,
                user_id=link.user_id,
                created_at=link.created_at,
                click_count=link.click_count
            )
            self.db.add(model)
    
    async def get_user_links(self, user_id: str) -> list[Link]:
        stmt = select(LinkModel).where(LinkModel.user_id == user_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
        
        
    def _to_entity(self, model: LinkModel) -> Link:
        return Link(
            id = model.id,
            original_url = model.original_url,
            short_code = model.short_code,
            user_id = model.user_id,
            created_at = model.created_at,
            click_count = model.click_count
        )