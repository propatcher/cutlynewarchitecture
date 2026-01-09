from dataclasses import dataclass
from app.domain.exceptions.base_exception import BaseException


@dataclass(eq=False)
class UserAlreadyExists(BaseException):
    text: str

    @property
    def message(self):
        return f'Пользователь уже существует "{self.text[:255]}..."'

@dataclass(eq=False)
class UserNotExist(BaseException):
    text: str
    
    @property
    def message(self):
        return f'Пользователя не существует "{self.text[:255]}"'

@dataclass(eq=False)
class UserWrongData(BaseException):
    text: str
    
    @property
    def message(self):
        return f'Неправильный логин или пароль "{self.text[:255]}"'

@dataclass(eq=False)
class TokenJwtException(BaseException):
    text: str
    
    @property
    def message(self):
        return f'Ошибка кодировки jwt "{self.text[:255]}"'
    
@dataclass(eq=False)
class TokenAbsentException(BaseException):
    text: str
    
    @property
    def message(self):
        return f'Токен просрочек "{self.text[:255]}"'
    
@dataclass(eq=False)
class IncorrectIdType(BaseException):
    text: str
    
    @property
    def message(self):
        return f'Неправильный тип ID "{self.text[:255]}"'
    
@dataclass(eq=False)
class IncorrectId(BaseException):
    text: str
    
    @property
    def message(self):
        return f'Неправильный ID "{self.text[:255]}"'
    
