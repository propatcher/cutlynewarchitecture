from typing import AsyncGenerator
from fastapi import Depends
from app.domain.repo.user_repository import UserRepository
from app.infra.auth.password_hasher import PasswordHasher
from app.infra.repo.user_repository import UserPostgresRepository
from app.services.user_services import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from app.infra.database.session import async_session

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency для получения сессии БД.
    Использовать в эндпоинтах как: db: AsyncSession = Depends(get_db)
    """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

def get_user_repository(db = Depends(get_db)) -> UserRepository:
    return UserPostgresRepository(db)

def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()

def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
    db: AsyncSession = Depends(get_db)
) -> UserService:
    return UserService(user_repository=user_repo, password_hasher=password_hasher,db_session=db)