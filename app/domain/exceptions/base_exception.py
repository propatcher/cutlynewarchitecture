from dataclasses import dataclass


@dataclass(eq=False)
class BaseException(Exception):
    @property
    def message(self):
        return 'Произошла ошибка приложения,'