from datetime import datetime, timedelta, timezone
from jose import jwt
from app.settings.config import config

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(
        to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM
    )
    return encoded_jwt