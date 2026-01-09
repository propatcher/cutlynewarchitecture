from dataclasses import dataclass
from app.domain.exceptions.base_exception import BaseException

@dataclass(eq=False)
class LinkNotFoundError(BaseException):
    text: str

    @property
    def message(self):
        return f'Ссылка не найдена "{self.text[:255]}..."'

class ShortCodeAlreadyExistsError(BaseException):
    text: str

    @property
    def message(self):
        return f'Ссылка уже существует "{self.text[:255]}..."'
