from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes import auth, tasks, projects, boards, columns

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API para gerenciamento de projetos usando metodologia Kanban",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Configurar CORS (ANTES de outras middlewares!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Middleware para remover trailing slash redirect
@app.middleware("http")
async def remove_trailing_slash_redirect(request, call_next):
    """Remove trailing slash redirects que causam 307"""
    response = await call_next(request)
    # Se for redirect 307 e for por causa de trailing slash, retornar 200
    if response.status_code == 307:
        return await call_next(request)
    return response


# Event handlers
@app.on_event("startup")
async def startup_event():
    """
    Executado quando a aplicação inicia
    """
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📊 Database: {settings.DATABASE_URL.split('@')[-1]}")
    print(f"🌍 Environment: {'Development' if settings.DEBUG else 'Production'}")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Executado quando a aplicação é encerrada
    """
    print("👋 Shutting down application...")


# Rota raiz
@app.get("/", tags=["Health"])
async def root():
    """
    Endpoint raiz da API
    """
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/api/docs",
    }


# Health check
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Verifica se a API está funcionando
    """
    return {"status": "healthy", "service": settings.APP_NAME}


# Registrar rotas
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(boards.router, prefix="/api/boards", tags=["Boards"])
app.include_router(columns.router, prefix="/api/columns", tags=["Columns"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
