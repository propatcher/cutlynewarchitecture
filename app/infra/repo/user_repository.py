from abc import ABC, abstractmethod
from typing import Optional
from domain.repo.user_repository import UserRepository
from domain.entities.user import User
from infra.database.models import UserModel

class UserPostgresRepository(UserRepository):
    def __init__(self, db_session):
        self.db = db_session

    def get_by_id(self,id:str) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.id == id).first()
        return self._to_entity(model) if model else None

    def get_by_login(self,login:str) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.login == login).first()
        return self._to_entity(model) if model else None
    
    def get_by_email(self,email:str) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(model) if model else None

    def _to_entity(self, model:UserModel) -> User:
        return User(
            id = UUID(model.id),
            login = model.login,
            email = model.email,
            hashed_password = model.hashed_password
            created_at = model.created_at
        )