from abc import ABC, abstractmethod
from typing import Optional
from domain.repo.user_repository import UserRepository
from domain.entities.user import User
from infra.database.models import UserModel

class UserPostgresRepository(UserRepository):
    def __init__(self, db_session):
        self.db = db_session

    def get_by_id(self,id:str) -> Optional[User]:
        model = db.query(UserModel).filter(UserModel.id == id).first()
        return self._to_entity(model) if model
    @abstractmethod
    def get_by_login(self, user: User) -> User:
        ...
    def _to_entity(self, model:UserModel) -> User:
        return User(
            id = model.id,
            username = model.username,
            email = model.email,
            feeds = model.feeds
        )
    