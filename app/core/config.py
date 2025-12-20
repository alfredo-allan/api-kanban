from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os


class Settings(BaseSettings):
    """
    Configurações da aplicação carregadas de variáveis de ambiente ou arquivo .env
    """

    # ✅ Database: Prioriza o que está no ambiente (Render) ou no .env (Secret File)
    DATABASE_URL: str = (
        os.environ.get("DATABASE_URL")
        or "postgresql://kanban_user:kanban_pass@localhost:5432/kanban_db"
    )

    @property
    def DATABASE_URL_ASYNC(self) -> str:
        """Gera a URL assíncrona corrigindo o prefixo para SQLAlchemy 2.0"""
        url = self.DATABASE_URL

        # 1. Correção para o SQLAlchemy 2.0 (exige 'postgresql' em vez de 'postgres')
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)

        # 2. Segurança: Se a URL ainda contiver o texto de exemplo, resetamos para localhost
        if "SUA_URL_AQUI" in url:
            url = "postgresql://kanban_user:kanban_pass@localhost:5432/kanban_db"

        # 3. Transforma em Async (usado pelo FastAPI/SQLAlchemy Async)
        if "postgresql+asyncpg://" not in url:
            return url.replace("postgresql://", "postgresql+asyncpg://")
        return url

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Application
    APP_NAME: str = "Leap Tech Kanban"
    APP_VERSION: str = "1.0.0"

    # DEBUG: No Render, a variável DEBUG=False no Secret File desativa o modo de inspeção
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    # ✅ CORS: Liberado para Vercel e Localhost
    ALLOWED_ORIGINS: str = (
        "http://localhost:5173," "http://localhost:3000," "https://visual-guard-kanban.vercel.app"
    )

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 10000

    # Configuração do Pydantic para ler o arquivo .env
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )

    @property
    def cors_origins(self) -> List[str]:
        """Retorna lista de origens permitidas para CORS"""
        if not self.ALLOWED_ORIGINS:
            return []
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


# ✅ Ajuste manual final para garantir que a variável global DATABASE_URL esteja correta
_db_url_raw = os.getenv("DATABASE_URL", "")
if _db_url_raw.startswith("postgres://"):
    os.environ["DATABASE_URL"] = _db_url_raw.replace("postgres://", "postgresql://", 1)


# Instância global das configurações
settings = Settings()
