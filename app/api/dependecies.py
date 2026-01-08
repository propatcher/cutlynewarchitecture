from typing import Annotated, AsyncGenerator, Optional
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from app.domain.entities.user import User
from app.domain.exceptions.user_exceptions import IncorrectId, IncorrectIdType, TokenAbsentException, TokenJwtException
from app.domain.repo.user_repository import UserRepository
from app.infra.auth.password_hasher import PasswordHasher
from app.infra.repo.user_repository import UserPostgresRepository
from app.services.user_services import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from app.infra.database.session import async_session
from app.settings.config import config
import jwt

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login",description="Bearer Token New System",auto_error=False)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], user_repo: UserRepository = Depends(get_user_repository)) -> Optional[User]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        login = payload.get("sub")
        if login is None:
            raise credentials_exception
        user = await user_repo.get_by_login(login=login)
        if user is None:
            raise credentials_exception
        return user 
    except jwt.InvalidTokenError:
        raise credentials_exception
