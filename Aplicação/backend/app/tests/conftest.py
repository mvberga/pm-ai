import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient  # Mudança aqui: AsyncClient ao invés de TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
import sys
import os

# Adicionar o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# FORÇAR IMPORT dos modelos ANTES de importar o Base
# Isso é CRÍTICO para que o metadata seja populado
import app.models.user
import app.models.project
import app.models.checklist
import app.models.action_item

# IMPORTAR O BASE CORRETO (app.db.session, não db.session)
from app.db.session import get_session, Base

# Test database URL (in-memory SQLite for testing)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False
)

# Create test session factory
TestingSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# REMOVER a definição customizada do event_loop - deixar o pytest-asyncio gerenciar
# @pytest.fixture(scope="session")
# def event_loop():
#     """Create an instance of the default event loop for the test session"""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()

@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncSession:
    """Create a test database session with tables created for EACH test"""
    
    # DEBUG: Verificar se o metadata está populado
    print(f"Metadata contem {len(Base.metadata.tables)} tabelas antes de criar")
    print(f"Tabelas no metadata: {list(Base.metadata.tables.keys())}")
    
    # SOLUÇÃO: Criar tabelas ANTES de cada teste para garantir isolamento
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Tabelas criadas com sucesso no fixture")
    
    # Criar sessão limpa para cada teste
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        await session.close()
        # Limpar dados após cada teste
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            print("Limpando banco de dados...")

@pytest_asyncio.fixture
async def client(db_session: AsyncSession):
    """Client de teste que suporta tanto uso síncrono quanto awaitable."""
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from app.core.config import settings
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

    test_app = FastAPI(
        title=f"{settings.PROJECT_NAME} - Test",
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc"
    )

    test_app.add_middleware(LoggingMiddleware)

    test_app.add_exception_handler(RequestValidationError, validation_exception_handler)
    test_app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    test_app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    test_app.add_exception_handler(Exception, general_exception_handler)

    test_app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
    test_app.include_router(projects.router, prefix=f"{settings.API_V1_STR}/projects", tags=["projects"])
    test_app.include_router(checklists.router, prefix=settings.API_V1_STR, tags=["checklists"])
    test_app.include_router(action_items.router, prefix=settings.API_V1_STR, tags=["action-items"])
    test_app.include_router(portfolios.router, prefix=f"{settings.API_V1_STR}/portfolios", tags=["portfolios"])
    test_app.include_router(team_members.router, prefix=f"{settings.API_V1_STR}/team-members", tags=["team-members"])
    test_app.include_router(clients.router, prefix=f"{settings.API_V1_STR}/clients", tags=["clients"])
    test_app.include_router(risks.router, prefix=f"{settings.API_V1_STR}/risks", tags=["risks"])
    test_app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])
    test_app.include_router(security.router, prefix=f"{settings.API_V1_STR}/security", tags=["security"])

    @test_app.get("/health")
    async def health():
        return {"status": "healthy", "version": settings.VERSION, "environment": "test"}

    @test_app.get("/")
    async def root():
        return {
            "message": "PM AI MVP API - Test",
            "version": settings.VERSION,
            "docs": "/docs",
            "health": "/health"
        }

    async def override_get_session():
        yield db_session

    test_app.dependency_overrides[get_session] = override_get_session

    # Wrapper para suportar ambos os estilos
    class DualResponse:
        def __init__(self, resp):
            self._resp = resp
        def __getattr__(self, name):
            return getattr(self._resp, name)
        def __await__(self):
            if False:
                yield None
            return self

    class DualClient:
        def __init__(self, tc: TestClient):
            self._tc = tc
        def get(self, *args, **kwargs):
            return DualResponse(self._tc.get(*args, **kwargs))
        def post(self, *args, **kwargs):
            return DualResponse(self._tc.post(*args, **kwargs))
        def put(self, *args, **kwargs):
            return DualResponse(self._tc.put(*args, **kwargs))
        def delete(self, *args, **kwargs):
            return DualResponse(self._tc.delete(*args, **kwargs))

    with TestClient(test_app) as tc:
        yield DualClient(tc)

    test_app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def client_with_auth(db_session: AsyncSession):
    """Client de teste com autenticação mock"""
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from app.core.config import settings
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

    test_app = FastAPI(
        title=f"{settings.PROJECT_NAME} - Test with Auth",
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc"
    )

    test_app.add_middleware(LoggingMiddleware)

    test_app.add_exception_handler(RequestValidationError, validation_exception_handler)
    test_app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    test_app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    test_app.add_exception_handler(Exception, general_exception_handler)

    test_app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
    test_app.include_router(projects.router, prefix=f"{settings.API_V1_STR}/projects", tags=["projects"])
    test_app.include_router(checklists.router, prefix=settings.API_V1_STR, tags=["checklists"])
    test_app.include_router(action_items.router, prefix=settings.API_V1_STR, tags=["action-items"])
    test_app.include_router(portfolios.router, prefix=f"{settings.API_V1_STR}/portfolios", tags=["portfolios"])
    test_app.include_router(team_members.router, prefix=f"{settings.API_V1_STR}/team-members", tags=["team-members"])
    test_app.include_router(clients.router, prefix=f"{settings.API_V1_STR}/clients", tags=["clients"])
    test_app.include_router(risks.router, prefix=f"{settings.API_V1_STR}/risks", tags=["risks"])
    test_app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])
    test_app.include_router(security.router, prefix=f"{settings.API_V1_STR}/security", tags=["security"])

    @test_app.get("/health")
    async def health():
        return {"status": "healthy", "version": settings.VERSION, "environment": "test"}

    @test_app.get("/")
    async def root():
        return {
            "message": "PM AI MVP API - Test with Auth",
            "version": settings.VERSION,
            "docs": "/docs",
            "health": "/health"
        }

    async def override_get_session():
        yield db_session

    # Mock da autenticação para testes que precisam de usuário logado
    async def override_get_current_user():
        from app.models.user import User
        # Criar um usuário mock para os testes
        mock_user = User(
            id=1,
            email="test@example.com",
            name="Test User",
            hashed_password="mock_password"
        )
        return mock_user

    test_app.dependency_overrides[get_session] = override_get_session
    
    # Importar e sobrescrever a dependência de autenticação
    from app.core.deps import get_current_user
    test_app.dependency_overrides[get_current_user] = override_get_current_user

    # Wrapper para suportar ambos os estilos
    class DualResponse:
        def __init__(self, resp):
            self._resp = resp
        def __getattr__(self, name):
            return getattr(self._resp, name)
        def __await__(self):
            if False:
                yield None
            return self

    class DualClient:
        def __init__(self, tc: TestClient):
            self._tc = tc
        def get(self, *args, **kwargs):
            return DualResponse(self._tc.get(*args, **kwargs))
        def post(self, *args, **kwargs):
            return DualResponse(self._tc.post(*args, **kwargs))
        def put(self, *args, **kwargs):
            return DualResponse(self._tc.put(*args, **kwargs))
        def delete(self, *args, **kwargs):
            return DualResponse(self._tc.delete(*args, **kwargs))

    with TestClient(test_app) as tc:
        yield DualClient(tc)

    test_app.dependency_overrides.clear()

@pytest.fixture
def test_user_data():
    """Test user data for authentication tests"""
    return {
        "email": "test@example.com",
        "name": "Test User",
        "id_token": "test_token_123"
    }

@pytest.fixture
def create_test_user():
    """Helper function to create test users with proper hashed_password"""
    from app.models.user import User
    from app.utils.auth import hash_password
    
    def _create_user(email: str, name: str, user_id: int = None, **kwargs):
        """Create a test user with hashed password"""
        user_data = {
            "email": email,
            "name": name,
            "hashed_password": hash_password("testpassword"),
            "is_active": True,
            "is_superuser": False,
            **kwargs
        }
        
        if user_id:
            user_data["id"] = user_id
            
        return User(**user_data)
    
    return _create_user

@pytest.fixture
def test_project_data():
    """Test project data for project tests"""
    return {
        "name": "Test Project",
        "description": "A test project for testing purposes",
        "portfolio_name": "Test Portfolio",
        "vertical": "Technology",
        "product": "Software"
    }
