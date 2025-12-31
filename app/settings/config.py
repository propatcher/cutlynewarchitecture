from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file="./.env")
    
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: str
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    REDIS_HOST: str
    REDIS_PORT: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

config = Config()