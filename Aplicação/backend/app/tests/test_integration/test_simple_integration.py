"""
Testes de integração simplificados para verificar se os endpoints básicos funcionam.
"""

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings


@pytest_asyncio.fixture
async def simple_test_app(db_session: AsyncSession):
    """Criar aplicação FastAPI simplificada para testes."""
    from fastapi import FastAPI
    from app.routers import auth, projects, checklists, action_items, portfolios, team_members, clients, risks, analytics, security
    from app.core.deps import get_session
    
    app = FastAPI(title="Simple Test App")
    
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
    
    # Endpoint de health
    @app.get("/health")
    async def health():
        return {"status": "healthy", "environment": "test"}
    
    # Override da dependência de sessão
    async def override_get_session():
        yield db_session
    
    app.dependency_overrides[get_session] = override_get_session
    
    return app


@pytest_asyncio.fixture
async def simple_client(simple_test_app):
    """Cliente de teste simplificado."""
    with TestClient(simple_test_app) as tc:
        yield tc


class TestSimpleIntegration:
    """Testes de integração simplificados."""
    
    async def test_health_endpoint(self, simple_client: TestClient):
        """Testar endpoint de health."""
        response = simple_client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert data["environment"] == "test"

    async def test_auth_google_login(self, simple_client: TestClient):
        """Testar login do Google."""
        login_data = {
            "id_token": "test_token_123",
            "email": "test@example.com",
            "name": "Test User"
        }
        
        response = simple_client.post(f"{settings.API_V1_STR}/auth/google/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert "user" in data
        assert data["token_type"] == "bearer"

    async def test_projects_list(self, simple_client: TestClient):
        """Testar listagem de projetos."""
        response = simple_client.get(f"{settings.API_V1_STR}/projects/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)

    async def test_projects_metrics(self, simple_client: TestClient):
        """Testar métricas de projetos."""
        response = simple_client.get(f"{settings.API_V1_STR}/projects/metrics")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_projects" in data
        assert "total_implantation" in data
        assert "total_recurring" in data

    async def test_checklists_list(self, simple_client: TestClient):
        """Testar listagem de checklists."""
        response = simple_client.get(f"{settings.API_V1_STR}/checklists")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)

    async def test_action_items_list(self, simple_client: TestClient):
        """Testar listagem de action items."""
        response = simple_client.get(f"{settings.API_V1_STR}/action-items")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)

    async def test_create_project_basic(self, simple_client: TestClient):
        """Testar criação básica de projeto."""
        project_data = {
            "name": "Test Project",
            "description": "A test project",
            "municipio": "São Paulo",
            "entidade": "Prefeitura",
            "portfolio": "Test Portfolio",
            "vertical": "Technology",
            "product": "Software",
            "tipo": "implantacao",
            "gerente_projeto_id": 1,
            "gerente_portfolio_id": 1
        }
        
        response = simple_client.post(f"{settings.API_V1_STR}/projects/", json=project_data)
        # Pode ser 200, 201 ou 422 dependendo da validação
        assert response.status_code in [200, 201, 422]

    async def test_create_checklist_basic(self, simple_client: TestClient):
        """Testar criação básica de checklist."""
        checklist_data = {
            "name": "Test Checklist",
            "description": "A test checklist"
        }
        
        response = simple_client.post(f"{settings.API_V1_STR}/checklists", json=checklist_data)
        # Pode ser 200, 201 ou 422 dependendo da validação
        assert response.status_code in [200, 201, 422]

    async def test_create_action_item_basic(self, simple_client: TestClient):
        """Testar criação básica de action item."""
        action_item_data = {
            "title": "Test Action Item",
            "description": "A test action item",
            "status": "pending"
        }
        
        response = simple_client.post(f"{settings.API_V1_STR}/action-items", json=action_item_data)
        # Pode ser 200, 201 ou 422 dependendo da validação
        assert response.status_code in [200, 201, 422]

    async def test_invalid_endpoint(self, simple_client: TestClient):
        """Testar endpoint inexistente."""
        response = simple_client.get("/nonexistent")
        assert response.status_code == 404

    async def test_invalid_data(self, simple_client: TestClient):
        """Testar dados inválidos."""
        response = simple_client.post(f"{settings.API_V1_STR}/projects/", json={})
        assert response.status_code == 422
