from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import Generator, AsyncGenerator
from app.core.config import settings

# Base para os models
Base = declarative_base()

# Engine síncrono (para Alembic migrations)
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Session síncrona
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Engine assíncrono (para uso na API)
async_engine = create_async_engine(
    settings.DATABASE_URL_ASYNC,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Session assíncrona
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# Dependency para obter session do banco (síncrono)
def get_db() -> Generator[Session, None, None]:
    """
    Dependency que fornece uma sessão do banco de dados
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency para obter session async do banco
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency que fornece uma sessão assíncrona do banco de dados
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# Função para criar todas as tabelas (útil para desenvolvimento)
def create_tables():
    """
    Cria todas as tabelas no banco de dados
    Usar apenas em desenvolvimento - em produção use Alembic migrations
    """
    Base.metadata.create_all(bind=engine)


# Função para deletar todas as tabelas (útil para testes)
def drop_tables():
    """
    Remove todas as tabelas do banco de dados
    CUIDADO: Use apenas em desenvolvimento/testes
    """
    Base.metadata.drop_all(bind=engine)
