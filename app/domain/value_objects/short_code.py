from dataclasses import dataclass
import secrets


@dataclass(frozen=True)
class ShortCode:
    value: str
    
    @classmethod
    def generate(cls, length: int = 6) -> "ShortCode":
        return cls(secrets.token_urlsafe(length)[:length ])
    
    classmethod
    def create(cls, value: str) -> "ShortCode":
        return cls(value)
    
    def __str__(self) -> str:
        return self.value