from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """
    Configurações da aplicação carregadas de variáveis de ambiente
    """

    # Database
    DATABASE_URL: str = "postgresql://kanban_user:kanban_pass@localhost:5432/kanban_db"
    DATABASE_URL_ASYNC: str = (
        "postgresql+asyncpg://kanban_user:kanban_pass@localhost:5432/kanban_db"
    )

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production-min-32-characters"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Application
    APP_NAME: str = "Kanban API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Redis (opcional)
    REDIS_URL: str = "redis://localhost:6379/0"

    # Email (opcional - para notificações futuras)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )

    @property
    def cors_origins(self) -> List[str]:
        """Retorna lista de origens permitidas para CORS"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


# Instância global das configurações
settings = Settings()
