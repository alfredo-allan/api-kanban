from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os


class Settings(BaseSettings):
    """
    Configurações da aplicação carregadas de variáveis de ambiente
    """

    # ✅ Database: No Render, a DATABASE_URL será injetada automaticamente.
    # Se não houver, ele usa o fallback do localhost para seu desenvolvimento.
    DATABASE_URL: str = "postgresql://kanban_user:kanban_pass@localhost:5432/kanban_db"

    # Geramos a URL assíncrona automaticamente para evitar erro de configuração manual
    @property
    def DATABASE_URL_ASYNC(self) -> str:
        return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Application
    APP_NAME: str = "Kanban API"
    APP_VERSION: str = "1.0.0"

    # ✅ Importante: No Render, mude DEBUG para False nas variáveis de ambiente!
    DEBUG: bool = True

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # Server: O Render injeta a porta na variável PORT
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )

    @property
    def cors_origins(self) -> List[str]:
        """Retorna lista de origens permitidas para CORS"""
        if not self.ALLOWED_ORIGINS:
            return []
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


# Instância global das configurações
settings = Settings()
