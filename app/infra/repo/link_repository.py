from typing import Optional

from sqlalchemy import UUID, select
from app.domain.exceptions.link_exceptions import ShortCodeAlreadyExistsError
from app.domain.value_objects.short_code import ShortCode
from app.domain.repo.link_repository import LinkRepository
from app.domain.entities.link import Link
from sqlalchemy.ext.asyncio import AsyncSession
from app.infra.database.models import LinkModel

class LinkPostgresRepository(LinkRepository):
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def get_by_short_code(self, code: ShortCode) -> Optional[Link]:
        stmt = select(LinkModel).where(LinkModel.short_code == code.value)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None    
        
    async def get_by_url_and_user(self, url: str, user_id: UUID = None) -> Optional[Link]:
        stmt = select(LinkModel).where(LinkModel.original_url == url)
        if user_id:
            stmt = stmt.where(LinkModel.user_id == user_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def save(self, link: Link) -> Link:
        existing = await self.get_by_short_code(link.short_code)
        
        if existing and existing.id == link.id:
            raise ShortCodeAlreadyExistsError(f"Short code {link.short_code} already exists")
        
        stmt = select(LinkModel).where(LinkModel.id == link.id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            model.original_url = link.original_url
            model.short_code = str(link.short_code)
            model.user_id = link.user_id
            model.click_count = link.click_count
            model.created_at = link.created_at
        else:
            model = LinkModel(
                id=link.id,
                original_url=link.original_url,
                short_code=str(link.short_code),
                user_id=link.user_id,
                created_at=link.created_at,
                click_count=link.click_count
            )
            self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
    
    async def increment_click_count(self, link_id:UUID) -> None:
        stmt = select(LinkModel).where(LinkModel.id == link_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            model.click_count += 1
            await self.db.commit()
    
    async def get_user_links(self, user_id: UUID) -> list[Link]:
        stmt = select(LinkModel).where(LinkModel.user_id == user_id)
        result = await self.db.execute(stmt)
        models  = result.scalars().all()
        return [self._to_entity(model) for model in models]
        
        
    def _to_entity(self, model: LinkModel) -> Link:
        
        short_code = ShortCode(model.short_code)
        
        return Link(
            id = model.id,
            original_url = model.original_url,
            short_code = short_code,
            user_id = model.user_id,
            created_at = model.created_at,
            click_count = model.click_count
        )