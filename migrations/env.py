from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# Adicionar o diretório app ao Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.getcwd())

# Importar a Base e settings
from app.core.config import settings
from app.models.base import Base

# Objeto de configuração do Alembic
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # ✅ CORREÇÃO: Garante que configuration seja um dict, mesmo que a seção seja None
    section = config.get_section(config.config_ini_section)
    configuration = dict(section) if section is not None else {}

    # Sobrescreve a URL com a variável de ambiente do settings
    configuration["sqlalchemy.url"] = settings.DATABASE_URL

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
