from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):

    # Database
    DATABASE_URL: str = "postgresql://kanban_user:kanban_pass@localhost:5432/kanban_db"

    @property
    def DATABASE_URL_ASYNC(self) -> str:
        url = self.DATABASE_URL

        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)

        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

        return url

    # Security
    SECRET_KEY: str = "change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Application
    APP_NAME: str = "Leap Tech Kanban"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # CORS
    ALLOWED_ORIGINS: str = (
        "http://localhost:5173," "http://localhost:3000," "https://visual-guard-kanban.vercel.app"
    )

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 10000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


settings = Settings()
