from dataclasses import dataclass
from domain.exceptions.base_exception import BaseException

@dataclass(eq=False)
class UserAlreadyExist(BaseException):
    text: str

    @property
    def message(self):
        return f'Пользователь уже существует "{self.text[:255]}..."'
