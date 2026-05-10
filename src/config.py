from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    CHAT_ID: str

    CORS_ORIGINS: List[str]
    APP_HOST: str
    APP_PORT: int
    APP_DEBUG: bool

    TELEGRAM_PROXY_URL: Optional[str] = None


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

settings = Settings()