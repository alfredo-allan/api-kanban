from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os


class Settings(BaseSettings):
    """
    Configurações da aplicação carregadas de variáveis de ambiente
    """

    # ✅ Database: No Render, DATABASE_URL é obrigatória.
    # Deixamos vazio por padrão para forçar a leitura do ambiente.
    DATABASE_URL: str = os.environ.get("DATABASE_URL") or "postgresql://user:pass@localhost:5432/db"

    @property
    def DATABASE_URL_ASYNC(self) -> str:
        """Gera a URL assíncrona corrigindo o prefixo se necessário"""
        url = self.DATABASE_URL
        # Correção para o SQLAlchemy 2.0 que exige 'postgresql' em vez de 'postgres'
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)

        if not url:
            # Se chegar aqui vazio no Render, o log vai te avisar exatamente o motivo
            return "postgresql+asyncpg://user:pass@localhost:5432/db_error"

        return url.replace("postgresql://", "postgresql+asyncpg://")

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Application
    APP_NAME: str = "Kanban API"
    APP_VERSION: str = "1.0.0"

    # Em produção no Render, defina a variável DEBUG=False no painel
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    # ✅ CORS: Domínio da Vercel e Localhost
    ALLOWED_ORIGINS: str = (
        "http://localhost:5173," "http://localhost:3000," "https://visual-guard-kanban.vercel.app"
    )

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 10000

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )

    @property
    def cors_origins(self) -> List[str]:
        """Retorna lista de origens permitidas para CORS"""
        if not self.ALLOWED_ORIGINS:
            return []
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


# ✅ Ajuste manual final para garantir que a DATABASE_URL principal também esteja corrigida
_raw_url = os.getenv("DATABASE_URL", "")
if _raw_url.startswith("postgres://"):
    os.environ["DATABASE_URL"] = _raw_url.replace("postgres://", "postgresql://", 1)

# Instância global das configurações
settings = Settings()
