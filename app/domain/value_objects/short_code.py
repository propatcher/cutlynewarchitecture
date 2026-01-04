from dataclasses import dataclass
import secrets


@dataclass(frozen=True)
class ShortCode:
    value: str
    
    @classmethod
    def generate(cls) -> "ShortCode":
        return cls(secrets.token_urlsafe(6)[:6])
    
    def __str__(self) -> str:
        return self.value