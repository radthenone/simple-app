import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BACKEND_DIR: str = Field(default=os.path.dirname(os.path.abspath(__file__)))
    JWT_SECRET: str = Field(default=os.environ.get("SECRET", "secret"))
    JWT_ALGORITHM: str = Field(default=os.environ.get("ALGORITHM", "HS256"))

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "local.env"),
        env_file_encoding="utf-8",
        extra="allow",
    )


settings = Settings()
