"""
Testes de integração avançados para endpoints de portfólio.
"""

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.portfolio import Portfolio
from app.models.project import Project, ProjectStatus
from app.models.user import User


class TestPortfolioAdvanced:
    """Testes de integração avançados para portfólio."""
    
    async def test_create_portfolio_complete_flow(self, client: TestClient, db_session: AsyncSession):
        """Testar fluxo completo de criação de portfólio."""

        # Primeiro, criar um usuário de teste
        from app.models.user import User
        from app.utils.auth import hash_password
        
        test_user = User(
            email="test@example.com",
            name="Test User",
            hashed_password=hash_password("testpassword")
        )
        db_session.add(test_user)
        await db_session.commit()
        await db_session.refresh(test_user)

        # Fazer login via Google OAuth para obter token
        google_login_data = {
            "id_token": "mock_token",
            "email": "test@example.com",
            "name": "Test User"
        }
        login_response = client.post(f"{settings.API_V1_STR}/auth/google/login", json=google_login_data)
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Headers com token de autenticação
        headers = {"Authorization": f"Bearer {token}"}

        # Dados do portfólio
        portfolio_data = {
            "name": "Portfólio de Teste Avançado",
            "description": "Portfólio para testes de integração avançados",
            "owner_id": test_user.id
        }
        
        # Criar portfólio
        response = client.post(f"{settings.API_V1_STR}/portfolios/", json=portfolio_data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        assert response.status_code == 201
        
        portfolio = response.json()
        assert portfolio["name"] == portfolio_data["name"]
        assert portfolio["description"] == portfolio_data["description"]
        assert portfolio["owner_id"] == portfolio_data["owner_id"]
        assert "id" in portfolio
        assert "created_at" in portfolio
        assert "updated_at" in portfolio

        
        portfolio_id = portfolio["id"]
        
        # Verificar se o portfólio foi criado no banco
        from sqlalchemy import select
        result = await db_session.execute(select(Portfolio).where(Portfolio.id == portfolio_id))
        db_portfolio = result.scalar_one_or_none()
        assert db_portfolio is not None
        assert db_portfolio.name == portfolio_data["name"]
    
    async def test_portfolio_with_projects_relationship(self, client: TestClient, db_session: AsyncSession):
        """Testar relacionamento entre portfólio e projetos."""
        
        # Criar portfólio
        portfolio_data = {
            "name": "Portfólio com Projetos",
            "description": "Portfólio para testar relacionamentos",
            "status": "active"
        }
        
        response = client.post(f"{settings.API_V1_STR}/portfolios", json=portfolio_data)
        assert response.status_code == 201
        portfolio = response.json()
        portfolio_id = portfolio["id"]
        
        # Criar projeto associado ao portfólio
        project_data = {
            "name": "Projeto do Portfólio",
            "description": "Projeto associado ao portfólio",
            "municipio": "São Paulo",
            "entidade": "Prefeitura",
            "portfolio_id": portfolio_id,
            "portfolio_name": portfolio_data["name"],
            "status": "planning"
        }
        
        response = client.post(f"{settings.API_V1_STR}/projects", json=project_data)
        assert response.status_code == 201
        project = response.json()
        assert project["portfolio_id"] == portfolio_id
        
        # Verificar relacionamento no banco
        from sqlalchemy import select
        result = await db_session.execute(
            select(Project).where(Project.portfolio_id == portfolio_id)
        )
        db_project = result.scalar_one_or_none()
        assert db_project is not None
        assert db_project.portfolio_id == portfolio_id
    
    async def test_portfolio_list_with_filters(self, client: TestClient, db_session: AsyncSession):
        """Testar listagem de portfólios com filtros."""
        
        # Criar múltiplos portfólios
        portfolios_data = [
            {
                "name": "Portfólio Ativo 1",
                "description": "Primeiro portfólio ativo",
                "status": "active"
            },
            {
                "name": "Portfólio Ativo 2", 
                "description": "Segundo portfólio ativo",
                "status": "active"
            },
            {
                "name": "Portfólio Inativo",
                "description": "Portfólio inativo",
                "status": "inactive"
            }
        ]
        
        created_portfolios = []
        for data in portfolios_data:
            response = client.post(f"{settings.API_V1_STR}/portfolios", json=data)
            assert response.status_code == 201
            created_portfolios.append(response.json())
        
        # Testar filtro por status ativo
        response = client.get(f"{settings.API_V1_STR}/portfolios?status=active")
        assert response.status_code == 200
        active_portfolios = response.json()
        assert len(active_portfolios) == 2
        
        # Testar filtro por status inativo
        response = client.get(f"{settings.API_V1_STR}/portfolios?status=inactive")
        assert response.status_code == 200
        inactive_portfolios = response.json()
        assert len(inactive_portfolios) == 1
    
    async def test_portfolio_update_flow(self, client: TestClient, db_session: AsyncSession):
        """Testar fluxo de atualização de portfólio."""
        
        # Criar portfólio
        portfolio_data = {
            "name": "Portfólio Original",
            "description": "Descrição original",
            "status": "active"
        }
        
        response = client.post(f"{settings.API_V1_STR}/portfolios", json=portfolio_data)
        assert response.status_code == 201
        portfolio = response.json()
        portfolio_id = portfolio["id"]
        
        # Atualizar portfólio
        update_data = {
            "name": "Portfólio Atualizado",
            "description": "Descrição atualizada",
            "status": "inactive",
            "budget": 500000.00
        }
        
        response = client.put(f"{settings.API_V1_STR}/portfolios/{portfolio_id}", json=update_data)
        assert response.status_code == 200
        
        updated_portfolio = response.json()
        assert updated_portfolio["name"] == update_data["name"]
        assert updated_portfolio["description"] == update_data["description"]
        assert updated_portfolio["status"] == update_data["status"]
        assert updated_portfolio["budget"] == update_data["budget"]
    
    async def test_portfolio_metrics(self, client: TestClient, db_session: AsyncSession):
        """Testar métricas de portfólio."""
        
        # Criar portfólio
        portfolio_data = {
            "name": "Portfólio para Métricas",
            "description": "Portfólio para testar métricas",
            "status": "active",
            "budget": 1000000.00
        }
        
        response = client.post(f"{settings.API_V1_STR}/portfolios", json=portfolio_data)
        assert response.status_code == 201
        portfolio = response.json()
        portfolio_id = portfolio["id"]
        
        # Criar projetos no portfólio
        projects_data = [
            {
                "name": "Projeto 1",
                "description": "Primeiro projeto",
                "municipio": "São Paulo",
                "entidade": "Prefeitura",
                "portfolio_id": portfolio_id,
                "status": "active",
                "budget": 300000.00
            },
            {
                "name": "Projeto 2", 
                "description": "Segundo projeto",
                "municipio": "Rio de Janeiro",
                "entidade": "Estado",
                "portfolio_id": portfolio_id,
                "status": "completed",
                "budget": 200000.00
            }
        ]
        
        for project_data in projects_data:
            response = client.post(f"{settings.API_V1_STR}/projects", json=project_data)
            assert response.status_code == 201
        
        # Testar métricas do portfólio
        response = client.get(f"{settings.API_V1_STR}/portfolios/{portfolio_id}/metrics")
        assert response.status_code == 200
        
        metrics = response.json()
        assert "total_projects" in metrics
        assert "total_budget" in metrics
        assert "active_projects" in metrics
        assert "completed_projects" in metrics
    
    async def test_portfolio_delete_flow(self, client: TestClient, db_session: AsyncSession):
        """Testar fluxo de exclusão de portfólio."""
        
        # Criar portfólio
        portfolio_data = {
            "name": "Portfólio para Exclusão",
            "description": "Portfólio que será excluído",
            "status": "active"
        }
        
        response = client.post(f"{settings.API_V1_STR}/portfolios", json=portfolio_data)
        assert response.status_code == 201
        portfolio = response.json()
        portfolio_id = portfolio["id"]
        
        # Verificar que o portfólio existe
        response = client.get(f"{settings.API_V1_STR}/portfolios/{portfolio_id}")
        assert response.status_code == 200
        
        # Excluir portfólio
        response = client.delete(f"{settings.API_V1_STR}/portfolios/{portfolio_id}")
        assert response.status_code == 200
        
        # Verificar que o portfólio foi excluído
        response = client.get(f"{settings.API_V1_STR}/portfolios/{portfolio_id}")
        assert response.status_code == 404
    
    async def test_portfolio_validation_errors(self, client: TestClient, db_session: AsyncSession):
        """Testar validação de dados de portfólio."""
        
        # Testar dados inválidos
        invalid_data = {
            "name": "",  # Nome vazio
            "description": "Descrição válida",
            "status": "invalid_status"  # Status inválido
        }
        
        response = client.post(f"{settings.API_V1_STR}/portfolios", json=invalid_data)
        assert response.status_code == 422  # Validation Error
        
        # Testar dados obrigatórios faltando
        incomplete_data = {
            "description": "Apenas descrição"
        }
        
        response = client.post(f"{settings.API_V1_STR}/portfolios", json=incomplete_data)
        assert response.status_code == 422  # Validation Error
    
    async def test_portfolio_not_found(self, client: TestClient, db_session: AsyncSession):
        """Testar cenários de portfólio não encontrado."""
        
        # Tentar buscar portfólio inexistente
        response = client.get(f"{settings.API_V1_STR}/portfolios/99999")
        assert response.status_code == 404
        
        # Tentar atualizar portfólio inexistente
        update_data = {"name": "Nome Atualizado"}
        response = client.put(f"{settings.API_V1_STR}/portfolios/99999", json=update_data)
        assert response.status_code == 404
        
        # Tentar excluir portfólio inexistente
        response = client.delete(f"{settings.API_V1_STR}/portfolios/99999")
        assert response.status_code == 404
