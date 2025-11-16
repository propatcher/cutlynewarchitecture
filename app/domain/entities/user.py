from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

@dataclass
class User:
    id : UUID
    login : str
    email : str
    hashed_password : str
    created_at : datetime
    
    @classmethod
    def create(cls, login : str, email : str, hashed_password : str) -> "User":
        return cls(
            id = uuid4(),
            login = login,
            email = email,
            hashed_password = hashed_password,
            created_at = datetime.now()
        )
    