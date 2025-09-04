from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.db.session import init_models, close_engine
from app.middlewares.logging import LoggingMiddleware
from app.middlewares.error_handler import (
    validation_exception_handler,
    http_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.routers import auth, projects, checklists, action_items, portfolios, team_members, clients, risks, analytics, security

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    await init_models()
    yield
    # Shutdown
    await close_engine()

# Create FastAPI app with lifespan
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    ## PM AI MVP - Sistema de Gestão de Projetos com IA
    
    API completa para gestão de projetos com funcionalidades avançadas de IA.
    
    ### Funcionalidades Principais:
    
    * **Autenticação**: Sistema de autenticação OAuth com Google
    * **Projetos**: Gestão completa de projetos e portfólios
    * **Equipes**: Gestão de membros da equipe e funções
    * **Clientes**: Gestão de clientes e níveis de comunicação
    * **Riscos**: Análise e gestão de riscos com IA
    * **Checklists**: Sistema de checklists para projetos
    * **Action Items**: Gestão de itens de ação e tarefas
    
    ### Arquitetura:
    
    * **Services Layer**: Lógica de negócio separada dos controllers
    * **Repository Pattern**: Camada de abstração para acesso a dados
    * **Cache Redis**: Sistema de cache para performance
    * **Processamento Assíncrono**: Tarefas em background com Celery
    * **IA Integration**: Integração com Gemini API para análise de riscos
    
    ### Tecnologias:
    
    * **FastAPI**: Framework web moderno e rápido
    * **SQLAlchemy**: ORM robusto com suporte assíncrono
    * **PostgreSQL**: Banco de dados relacional
    * **Redis**: Sistema de cache
    * **Celery**: Processamento assíncrono
    * **Pydantic**: Validação de dados
    """,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Equipe de Desenvolvimento PM AI MVP",
        "email": "dev@pm-ai-mvp.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Add middlewares
app.add_middleware(LoggingMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(projects.router, prefix=f"{settings.API_V1_STR}/projects", tags=["projects"])
app.include_router(checklists.router, prefix=settings.API_V1_STR, tags=["checklists"])
app.include_router(action_items.router, prefix=settings.API_V1_STR, tags=["action-items"])
app.include_router(portfolios.router, prefix=f"{settings.API_V1_STR}/portfolios", tags=["portfolios"])
app.include_router(team_members.router, prefix=f"{settings.API_V1_STR}/team-members", tags=["team-members"])
app.include_router(clients.router, prefix=f"{settings.API_V1_STR}/clients", tags=["clients"])
app.include_router(risks.router, prefix=f"{settings.API_V1_STR}/risks", tags=["risks"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])
app.include_router(security.router, prefix=f"{settings.API_V1_STR}/security", tags=["security"])

@app.get("/health")
async def health():
    """Health check endpoint"""
    return JSONResponse(
        content={
            "status": "healthy",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT
        },
        status_code=200
    )

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "PM AI MVP API",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health"
    }
