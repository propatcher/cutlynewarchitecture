from dataclasses import dataclass
import secrets


@dataclass
class ShortCode:
    @property
    def code(self) -> str:
        return self._code
    
    @classmethod
    def generate(cls) -> "ShortCode":
        return cls(secrets.token_urlsafe(6)[:6])