from dataclasses import dataclass

from domain.exceptions.base_exception import ApplicationException


@dataclass(eq=False)
class LinkNotFoundError(ApplicationException):
    text: str

    @property
    def message(self):
        return f'Ссылка не найдена "{self.text[:255]}..."'
