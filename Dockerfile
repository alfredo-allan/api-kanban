# ✅ Use o 3.11 que é estável e compatível com suas libs
FROM python:3.11-slim

# Instala dependências do sistema para o Postgres
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia e instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# ✅ Cria o script de inicialização diretamente no Dockerfile para facilitar
RUN echo '#!/bin/bash\n\
    echo "🚀 Iniciando processo de deploy..."\n\
    echo "📂 Rodando migrações do banco de dados (Alembic)..."\n\
    alembic upgrade head\n\
    echo "✅ Migrações concluídas!"\n\
    echo "📡 Iniciando servidor FastAPI..."\n\
    exec uvicorn app.main:app --host 0.0.0.0 --port 10000' > /app/start.sh

# Dá permissão de execução para o script
RUN chmod +x /app/start.sh

# O segredo agora é chamar o script em vez do uvicorn direto
CMD ["/app/start.sh"]
