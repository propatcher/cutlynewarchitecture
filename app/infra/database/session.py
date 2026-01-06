from sqlalchemy.ext.asyncio import async_sessionmaker,create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.settings.config import config

class Base(DeclarativeBase):
    pass

engine = create_async_engine(url=config.DATABASE_URL, echo=True if config.MODE == "DEV" else False, pool_pre_ping=True, pool_size=20, max_overflow=10)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)