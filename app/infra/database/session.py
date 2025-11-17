from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import engine,declarative_base

engine = create_async_engine(url=DATABASE_URL, **DATABASE_PARAMS)

async_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()