#!/bin/bash
set -e  # Para o script se qualquer comando falhar

echo "🚀 Iniciando processo de deploy..."

# Verifica se o arquivo de configuração do Alembic existe
if [ -f "alembic.ini" ]; then
    echo "📂 Rodando migrações do banco de dados..."
    alembic upgrade head
else
    echo "⚠️ Erro: alembic.ini não encontrado na raiz do projeto!"
    # Você pode optar por sair ou continuar. Vamos continuar para a API subir:
fi

echo "✅ Pronto para iniciar!"
echo "📡 Iniciando servidor FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 10000
