# 🚀 Kanban Flow API

> **API RESTful completa para gerenciamento ágil de projetos usando metodologia Kanban**

Uma solução robusta e escalável desenvolvida com **FastAPI** e **PostgreSQL** que oferece autenticação JWT, gerenciamento de tarefas com drag-and-drop, e arquitetura profissional pronta para produção.

---

## 🎯 Características Principais

### ✨ Funcionalidades Core

- 🔐 **Autenticação Completa**: Sistema JWT com refresh tokens e bcrypt
- 📊 **Gestão de Projetos**: CRUD completo com múltiplos boards
- 📋 **Sistema Kanban**: Colunas customizáveis com WIP limits
- ✅ **Gerenciamento de Tarefas**: Criação, edição, movimentação e priorização
- 🏷️ **Sistema de Tags**: Categorização flexível de tarefas
- 💬 **Comentários**: Discussões em tarefas
- 📈 **Activity Log**: Histórico completo de ações
- 🔍 **Filtros Avançados**: Busca por prioridade, status, responsável

### 🛠️ Stack Tecnológico

#### Backend

- **Framework**: FastAPI 0.115.0
- **Linguagem**: Python 3.11+
- **Banco de Dados**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0.35 (async)
- **Migrations**: Alembic 1.13.3
- **Autenticação**: JWT (python-jose)
- **Hashing**: bcrypt
- **Validação**: Pydantic 2.9.2

#### Infraestrutura

- **ASGI Server**: Uvicorn
- **Containerização**: Docker + Docker Compose
- **Cache** (opcional): Redis 7
- **Admin Panel**: Adminer

---

## 🏗️ Arquitetura

### Estrutura do Projeto

```
backend/
├── app/
│   ├── core/               # Configurações centrais
│   │   ├── config.py       # Variáveis de ambiente
│   │   ├── database.py     # Setup do SQLAlchemy
│   │   └── security.py     # JWT e bcrypt
│   ├── models/             # Models SQLAlchemy
│   │   ├── user.py         # Usuários
│   │   ├── project.py      # Projetos
│   │   ├── board.py        # Boards Kanban
│   │   ├── column.py       # Colunas
│   │   ├── task.py         # Tarefas
│   │   ├── tag.py          # Tags
│   │   ├── comment.py      # Comentários
│   │   └── activity_log.py # Logs de atividade
│   ├── schemas/            # Schemas Pydantic
│   │   ├── user.py
│   │   ├── project.py
│   │   └── task.py
│   ├── routes/             # Endpoints REST
│   │   ├── auth.py         # Autenticação
│   │   ├── projects.py     # Projetos
│   │   ├── boards.py       # Boards
│   │   ├── columns.py      # Colunas
│   │   └── tasks.py        # Tarefas
│   ├── middleware/         # Middlewares
│   │   └── auth.py         # Validação JWT
│   └── main.py             # App principal
├── migrations/             # Alembic migrations
├── tests/                  # Testes unitários
├── .env.example            # Template de variáveis
├── requirements.txt        # Dependências
└── docker-compose.yml      # Setup Docker
```

### Modelo de Dados (ER Diagram)

```
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│   Users     │──1:N──│   Projects   │──1:N──│   Boards    │
└─────────────┘       └──────────────┘       └─────────────┘
      │                                              │
      │                                              │
      │                                           1:N│
      │                                              ↓
      │                                       ┌─────────────┐
      │                                       │   Columns   │
      │                                       └─────────────┘
      │                                              │
      │                                           1:N│
      │                                              ↓
      └────────────────────1:N────────────→  ┌─────────────┐
                                             │    Tasks    │
                                             └─────────────┘
                                                   │ │
                                              ┌────┘ └────┐
                                              ↓           ↓
                                       ┌──────────┐  ┌──────────┐
                                       │   Tags   │  │ Comments │
                                       └──────────┘  └──────────┘
```

---

## 🚀 Começando

### Pré-requisitos

- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (opcional)

### Instalação Rápida

#### 1️⃣ Clone o repositório

```bash
git clone https://github.com/seu-usuario/kanban-api.git
cd kanban-api/backend
```

#### 2️⃣ Crie o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

#### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

#### 4️⃣ Configure as variáveis de ambiente

```bash
cp .env.example .env
# Edite o .env com suas configurações
```

#### 5️⃣ Suba o banco de dados (Docker)

```bash
docker-compose up -d postgres redis adminer
```

#### 6️⃣ Execute as migrations

```bash
alembic upgrade head
```

#### 7️⃣ Inicie o servidor

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

🎉 **API rodando em:** `http://localhost:8000`

📚 **Documentação interativa:** `http://localhost:8000/api/docs`

---

## 📡 Endpoints da API

### 🔐 Autenticação

```http
POST   /api/auth/register     # Registrar novo usuário
POST   /api/auth/login        # Login e obter tokens
GET    /api/auth/me           # Dados do usuário autenticado
POST   /api/auth/refresh      # Renovar access token
```

### 📁 Projetos

```http
GET    /api/projects          # Listar projetos do usuário
POST   /api/projects          # Criar novo projeto
GET    /api/projects/{id}     # Buscar projeto específico
PUT    /api/projects/{id}     # Atualizar projeto
DELETE /api/projects/{id}     # Deletar projeto
```

### 📊 Boards

```http
GET    /api/boards/project/{project_id}  # Listar boards do projeto
POST   /api/boards                       # Criar novo board
GET    /api/boards/{id}                  # Buscar board
PUT    /api/boards/{id}                  # Atualizar board
DELETE /api/boards/{id}                  # Deletar board
```

### 📋 Colunas

```http
GET    /api/columns/board/{board_id}     # Listar colunas do board
POST   /api/columns                      # Criar coluna
PUT    /api/columns/{id}                 # Atualizar coluna
DELETE /api/columns/{id}                 # Deletar coluna
```

### ✅ Tarefas

```http
GET    /api/tasks                        # Listar tarefas (com filtros)
POST   /api/tasks                        # Criar tarefa
GET    /api/tasks/{id}                   # Buscar tarefa
PUT    /api/tasks/{id}                   # Atualizar tarefa
PATCH  /api/tasks/{id}/move              # Mover tarefa (drag-and-drop)
DELETE /api/tasks/{id}                   # Deletar tarefa
```

**Filtros disponíveis:**

- `?column_id=uuid` - Filtrar por coluna
- `?priority=high` - Filtrar por prioridade (low, medium, high)
- `?assignee_id=uuid` - Filtrar por responsável
- `?skip=0&limit=100` - Paginação

---

## 🔒 Segurança

### Implementações de Segurança

- ✅ **Autenticação JWT**: Tokens com expiração configurável
- ✅ **Bcrypt Hashing**: Senhas criptografadas com salt
- ✅ **CORS Configurável**: Controle de origens permitidas
- ✅ **Validação de Entrada**: Pydantic em todas as requisições
- ✅ **SQL Injection Protection**: ORM SQLAlchemy
- ✅ **Rate Limiting**: Proteção contra abuso (opcional)

### Exemplo de Uso com Token

```bash
# 1. Registrar usuário
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "senha123",
    "full_name": "John Doe"
  }'

# 2. Fazer login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "senha123"
  }'

# Resposta:
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "token_type": "bearer"
# }

# 3. Usar o token nas requisições
curl -X GET http://localhost:8000/api/projects \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN"
```

---

## 🧪 Testes

```bash
# Rodar todos os testes
pytest

# Com cobertura
pytest --cov=app --cov-report=html

# Testes específicos
pytest tests/test_auth.py
```

---

## 🐳 Docker

### Deploy Completo com Docker Compose

```bash
# Subir todos os serviços
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down
```

**Serviços incluídos:**

- PostgreSQL (porta 5432)
- Redis (porta 6379)
- Adminer (porta 8080)
- API (porta 8000)

---

## 🌍 Deploy em Produção

### Variáveis de Ambiente Essenciais

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db
DATABASE_URL_ASYNC=postgresql+asyncpg://user:pass@host:5432/db

# Security
SECRET_KEY=seu-secret-key-min-32-chars-production
DEBUG=False
ALLOWED_ORIGINS=https://seu-frontend.com

# Server
HOST=0.0.0.0
PORT=8000
```

### Comandos de Produção

```bash
# Com Gunicorn + Uvicorn workers
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000

# Ou apenas Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 📈 Performance

### Otimizações Implementadas

- ✅ **Queries Assíncronas**: AsyncPG para PostgreSQL
- ✅ **Connection Pooling**: Pool otimizado de conexões
- ✅ **Lazy Loading**: Relacionamentos carregados sob demanda
- ✅ **Índices no Banco**: Username, email, foreign keys
- ✅ **Paginação**: Limite padrão de 100 items
- ✅ **Cache-Ready**: Preparado para Redis

### Métricas Esperadas

- **Tempo de Resposta**: < 100ms (queries simples)
- **Throughput**: 1000+ req/s (com 4 workers)
- **Concurrent Users**: 500+ simultâneos

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👨‍💻 Autor

**Alfredo Allan**

- GitHub: [@seu-usuario](https://github.com/alfredo-allan)
- LinkedIn: [Seu Nome](https://linkedin.com/in/alfredo-allan)
- Email: kali.sonic.developer@gmail.com

---

## 🙏 Agradecimentos

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM poderoso
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Validação de dados
- Comunidade Python pela excelência em tooling

---

## 📚 Documentação Adicional

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela!**

Made with ❤️ and ☕ by [Seu Nome]

</div>
