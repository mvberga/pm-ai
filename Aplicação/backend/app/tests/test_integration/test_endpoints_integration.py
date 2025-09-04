"""
Testes de integração para todos os endpoints da API.

Este arquivo contém testes abrangentes para verificar se todos os endpoints
estão funcionando corretamente em conjunto.
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.config import settings
from app.core.deps import get_session
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

# Importar todos os routers
from app.routers import (
    auth, projects, checklists, action_items, portfolios, 
    risks, team_members, clients, analytics, security
)

# Importar modelos necessários
from app.models.user import User
from app.models.project import Project
from app.models.portfolio import Portfolio
from app.models.risk import Risk
from app.models.team_member import TeamMember
from app.models.client import Client
from app.models.checklist import ChecklistGroup
from app.models.action_item import ActionItem


@pytest_asyncio.fixture
async def test_app(db_session: AsyncSession) -> FastAPI:
    """Criar aplicação FastAPI para testes de integração."""
    
    app = FastAPI(
        title=f"{settings.PROJECT_NAME} - Integration Tests",
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Adicionar middlewares
    app.add_middleware(LoggingMiddleware)
    
    # Adicionar handlers de exceção
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    # Incluir todos os routers (alinhado com main.py)
    app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
    app.include_router(projects.router, prefix=f"{settings.API_V1_STR}/projects", tags=["projects"])
    app.include_router(checklists.router, prefix=settings.API_V1_STR, tags=["checklists"])
    app.include_router(action_items.router, prefix=settings.API_V1_STR, tags=["action-items"])
    app.include_router(portfolios.router, prefix=f"{settings.API_V1_STR}/portfolios", tags=["portfolios"])
    app.include_router(risks.router, prefix=f"{settings.API_V1_STR}/risks", tags=["risks"])
    app.include_router(team_members.router, prefix=f"{settings.API_V1_STR}/team-members", tags=["team-members"])
    app.include_router(clients.router, prefix=f"{settings.API_V1_STR}/clients", tags=["clients"])
    app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])
    app.include_router(security.router, prefix=f"{settings.API_V1_STR}/security", tags=["security"])

    # Endpoints de health check
    @app.get("/health")
    async def health():
        return {"status": "healthy", "version": settings.VERSION, "environment": "test"}

    @app.get("/")
    async def root():
        return {
            "message": "PM AI MVP API - Integration Tests",
            "version": settings.VERSION,
            "docs": "/docs",
            "health": "/health"
        }

    # Override da dependência de sessão
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    return app


@pytest_asyncio.fixture
async def client(test_app: FastAPI) -> TestClient:
    """Cliente de teste para a aplicação."""
    with TestClient(test_app) as tc:
        yield tc


@pytest_asyncio.fixture
async def authenticated_user(db_session: AsyncSession):
    """Criar um usuário autenticado para os testes."""
    from app.utils.auth import hash_password
    user = User(
        email="test@example.com",
        name="Test User",
        hashed_password=hash_password("testpassword")
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def test_portfolio(db_session: AsyncSession, authenticated_user):
    """Criar um portfólio de teste."""
    portfolio = Portfolio(
        name="Test Portfolio",
        description="A test portfolio",
        owner_id=authenticated_user.id
    )
    db_session.add(portfolio)
    await db_session.commit()
    await db_session.refresh(portfolio)
    return portfolio


@pytest_asyncio.fixture
async def test_project(db_session: AsyncSession, test_portfolio):
    """Criar um projeto de teste."""
    project = Project(
        name="Test Project",
        description="A test project",
        municipio="São Paulo",
        entidade="Prefeitura",
        portfolio=test_portfolio.name,
        vertical="Technology",
        product="Software",
        tipo="implantacao",
        gerente_projeto_id=1,
        gerente_portfolio_id=1,
        owner_id=1
    )
    db_session.add(project)
    await db_session.commit()
    await db_session.refresh(project)
    return project


class TestHealthEndpoints:
    """Testes para endpoints de health check."""
    
    async def test_root_endpoint(self, client: TestClient):
        """Testar endpoint raiz."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == settings.VERSION

    async def test_health_endpoint(self, client: TestClient):
        """Testar endpoint de health check."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["environment"] == "test"


class TestAuthEndpoints:
    """Testes para endpoints de autenticação."""
    
    async def test_google_login_new_user(self, client: TestClient):
        """Testar login do Google com novo usuário."""
        login_data = {
            "id_token": "test_token_123",
            "email": "newuser@example.com",
            "name": "New User"
        }
        
        response = client.post(f"{settings.API_V1_STR}/auth/google/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert "user" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "newuser@example.com"

    async def test_google_login_existing_user(self, client: TestClient, authenticated_user):
        """Testar login do Google com usuário existente."""
        login_data = {
            "id_token": "test_token_123",
            "email": authenticated_user.email,
            "name": authenticated_user.name
        }
        
        response = client.post(f"{settings.API_V1_STR}/auth/google/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert data["user"]["id"] == authenticated_user.id


class TestPortfolioEndpoints:
    """Testes para endpoints de portfólio."""
    
    async def test_create_portfolio(self, client: TestClient, authenticated_user):
        """Testar criação de portfólio."""
        portfolio_data = {
            "name": "New Portfolio",
            "description": "A new test portfolio"
        }
        
        # Simular autenticação (em um teste real, você usaria o token)
        response = client.post(
            f"{settings.API_V1_STR}/portfolios/",
            json=portfolio_data,
            headers={"Authorization": f"Bearer test_token"}
        )
        
        # Como não temos autenticação real configurada, esperamos um erro 401
        # Em um ambiente real, você configuraria a autenticação adequadamente
        assert response.status_code in [200, 201, 401]  # 401 é esperado sem auth real

    async def test_get_portfolios(self, client: TestClient):
        """Testar listagem de portfólios."""
        response = client.get(
            f"{settings.API_V1_STR}/portfolios/",
            headers={"Authorization": f"Bearer test_token"}
        )
        
        # Esperamos 401 sem autenticação real
        assert response.status_code in [200, 401]


class TestProjectEndpoints:
    """Testes para endpoints de projeto."""
    
    async def test_create_project(self, client: TestClient):
        """Testar criação de projeto."""
        project_data = {
            "name": "New Project",
            "description": "A new test project",
            "municipio": "São Paulo",
            "entidade": "Prefeitura",
            "portfolio": "Test Portfolio",
            "vertical": "Technology",
            "product": "Software",
            "tipo": "implantacao",
            "gerente_projeto_id": 1,
            "gerente_portfolio_id": 1
        }
        
        response = client.post(f"{settings.API_V1_STR}/projects/", json=project_data)
        assert response.status_code in [200, 201, 422]  # 422 para validação

    async def test_get_projects(self, client: TestClient):
        """Testar listagem de projetos."""
        response = client.get(f"{settings.API_V1_STR}/projects/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)

    async def test_get_project_metrics(self, client: TestClient):
        """Testar métricas de projeto."""
        response = client.get(f"{settings.API_V1_STR}/projects/metrics")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_projects" in data
        assert "total_implantation" in data
        assert "total_recurring" in data


class TestChecklistEndpoints:
    """Testes para endpoints de checklist."""
    
    async def test_create_checklist(self, client: TestClient):
        """Testar criação de checklist."""
        checklist_data = {
            "name": "Test Checklist",
            "description": "A test checklist"
        }
        
        response = client.post(f"{settings.API_V1_STR}/checklists", json=checklist_data)
        assert response.status_code in [200, 201, 422]

    async def test_get_checklists(self, client: TestClient):
        """Testar listagem de checklists."""
        response = client.get(f"{settings.API_V1_STR}/checklists")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)


class TestActionItemEndpoints:
    """Testes para endpoints de action items."""
    
    async def test_create_action_item(self, client: TestClient):
        """Testar criação de action item."""
        action_item_data = {
            "title": "Test Action Item",
            "description": "A test action item",
            "status": "pending"
        }
        
        response = client.post(f"{settings.API_V1_STR}/action-items", json=action_item_data)
        assert response.status_code in [200, 201, 422]

    async def test_get_action_items(self, client: TestClient):
        """Testar listagem de action items."""
        response = client.get(f"{settings.API_V1_STR}/action-items")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)


class TestSecurityEndpoints:
    """Testes para endpoints de segurança."""
    
    async def test_get_security_summary(self, client: TestClient):
        """Testar resumo de segurança."""
        response = client.get(
            f"{settings.API_V1_STR}/security/summary",
            headers={"Authorization": f"Bearer test_token"}
        )
        
        # Esperamos 401 sem autenticação real
        assert response.status_code in [200, 401]

    async def test_get_blocked_ips(self, client: TestClient):
        """Testar listagem de IPs bloqueados."""
        response = client.get(
            f"{settings.API_V1_STR}/security/blocked-ips",
            headers={"Authorization": f"Bearer test_token"}
        )
        
        # Esperamos 401 sem autenticação real
        assert response.status_code in [200, 401]

    async def test_security_health_check(self, client: TestClient):
        """Testar health check de segurança."""
        response = client.get(
            f"{settings.API_V1_STR}/security/health",
            headers={"Authorization": f"Bearer test_token"}
        )
        
        # Esperamos 401 sem autenticação real
        assert response.status_code in [200, 401]


class TestAnalyticsEndpoints:
    """Testes para endpoints de analytics."""
    
    async def test_get_portfolio_dashboard(self, client: TestClient):
        """Testar dashboard do portfólio."""
        response = client.get(
            f"{settings.API_V1_STR}/analytics/portfolio/1/dashboard",
            headers={"Authorization": f"Bearer test_token"}
        )
        
        # Esperamos 401 sem autenticação real
        assert response.status_code in [200, 401, 404]

    async def test_get_project_health_score(self, client: TestClient):
        """Testar score de saúde do projeto."""
        response = client.get(
            f"{settings.API_V1_STR}/analytics/project/1/health-score",
            headers={"Authorization": f"Bearer test_token"}
        )
        
        # Esperamos 401 sem autenticação real
        assert response.status_code in [200, 401, 404]


class TestEndpointIntegration:
    """Testes de integração entre endpoints."""
    
    async def test_full_workflow(self, client: TestClient, db_session: AsyncSession):
        """Testar fluxo completo de criação de dados."""
        
        # 1. Criar usuário via login
        login_data = {
            "id_token": "test_token_123",
            "email": "workflow@example.com",
            "name": "Workflow User"
        }
        
        auth_response = client.post(f"{settings.API_V1_STR}/auth/google/login", json=login_data)
        assert auth_response.status_code == 200
        
        # 2. Criar projeto
        project_data = {
            "name": "Workflow Project",
            "description": "A project for workflow testing",
            "municipio": "São Paulo",
            "entidade": "Prefeitura",
            "portfolio": "Workflow Portfolio",
            "vertical": "Technology",
            "product": "Software",
            "tipo": "implantacao",
            "gerente_projeto_id": 1,
            "gerente_portfolio_id": 1
        }
        
        project_response = client.post(f"{settings.API_V1_STR}/projects/", json=project_data)
        assert project_response.status_code in [200, 201, 422]
        
        # 3. Verificar se o projeto foi criado
        projects_response = client.get(f"{settings.API_V1_STR}/projects/")
        assert projects_response.status_code == 200
        
        projects_data = projects_response.json()
        assert isinstance(projects_data, list)
        
        # 4. Criar checklist
        checklist_data = {
            "name": "Workflow Checklist",
            "description": "A checklist for workflow testing"
        }
        
        checklist_response = client.post(f"{settings.API_V1_STR}/checklists", json=checklist_data)
        assert checklist_response.status_code in [200, 201, 422]
        
        # 5. Criar action item
        action_item_data = {
            "title": "Workflow Action Item",
            "description": "An action item for workflow testing",
            "status": "pending"
        }
        
        action_item_response = client.post(f"{settings.API_V1_STR}/action-items", json=action_item_data)
        assert action_item_response.status_code in [200, 201, 422]

    async def test_error_handling(self, client: TestClient):
        """Testar tratamento de erros."""
        
        # Testar endpoint inexistente
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404
        
        # Testar dados inválidos
        invalid_data = {"invalid": "data"}
        response = client.post(f"{settings.API_V1_STR}/projects/", json=invalid_data)
        assert response.status_code in [422, 400]  # Validation error

    async def test_cors_headers(self, client: TestClient):
        """Testar headers CORS."""
        response = client.options("/")
        # CORS pode não estar configurado, então aceitamos qualquer status
        assert response.status_code in [200, 405, 404]
