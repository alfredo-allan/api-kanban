# ✅ Use o 3.11 que é estável e compatível com suas libs
FROM python:3.11-slim

# Mantém o resto igual
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# O segredo é manter o "app.main:app" que você já sabe que funciona
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
