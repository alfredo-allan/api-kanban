FROM python:3.9-slim

# Dependências para psycopg2 e drivers de rede
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Comando para FastAPI usando Gunicorn + UvicornWorker
# O Render espera que sua API responda na porta definida pela variável $PORT
CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:${PORT:-10000}
