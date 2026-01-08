from pwdlib import PasswordHash

class PasswordHasher:
    def __init__(self):
        self.password_hash = PasswordHash.recommended()
    
    def hash(self, password: str) -> str:
        return self.password_hash.hash(password)
    
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self.password_hash.verify(plain_password, hashed_password)