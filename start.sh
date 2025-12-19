#!/bin/bash

# Roda as migrações para garantir que o banco está atualizado
echo "Running migrations..."
alembic upgrade head

# Inicia a aplicação FastAPI
echo "Starting application..."
uvicorn app.main:app --host 0.0.0.0 --port 10000
