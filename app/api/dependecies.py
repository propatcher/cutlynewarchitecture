from typing import AsyncGenerator
from fastapi import Depends, Request
from app.domain.entities.user import User
from app.domain.exceptions.user_exceptions import IncorrectId, IncorrectIdType, TokenAbsentException, TokenJwtException
from app.domain.repo.user_repository import UserRepository
from app.infra.auth.password_hasher import PasswordHasher
from app.infra.repo.user_repository import UserPostgresRepository
from app.services.user_services import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from app.infra.database.session import async_session
from app.settings.config import config
from jose import JWTError, jwt
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Использовать как: db: AsyncSession = Depends(get_db)
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

def get_token(request: Request):
    token = request.cookies.get("cutly_auth_token")
    if not token:
        raise TokenAbsentException
    return token

async def get_current_user(user_repo: UserRepository = Depends(get_user_repository), token: str = Depends(get_token)) -> User:
    try:
        payload = jwt.decode(
            token, config.SECRET_KEY, algorithms=[config.ALGORITHM]
        )
    except JWTError:
        raise TokenJwtException

    user_id = payload.get("sub")
    if not user_id:
        raise IncorrectIdType
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise IncorrectId
    user = await UserRepository.find_by_id(int(user_id))
    if not user:
        raise IncorrectId
    return user