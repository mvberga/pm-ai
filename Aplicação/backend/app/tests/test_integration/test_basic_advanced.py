"""
Testes de integração básicos avançados para verificar se os endpoints estão funcionando.
"""

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings


class TestBasicAdvanced:
    """Testes de integração básicos avançados."""
    
    async def test_all_endpoints_are_accessible(self, client: TestClient, db_session: AsyncSession):
        """Testar se todos os endpoints estão acessíveis."""
        
        # Testar endpoints básicos
        endpoints_to_test = [
            ("/health", "GET"),
            ("/", "GET"),
            (f"{settings.API_V1_STR}/auth/google/login", "POST"),
            (f"{settings.API_V1_STR}/projects/", "GET"),
            (f"{settings.API_V1_STR}/projects/", "POST"),
            (f"{settings.API_V1_STR}/checklists", "GET"),
            (f"{settings.API_V1_STR}/action-items", "GET"),
            (f"{settings.API_V1_STR}/portfolios", "GET"),
            (f"{settings.API_V1_STR}/portfolios", "POST"),
            (f"{settings.API_V1_STR}/risks", "GET"),
            (f"{settings.API_V1_STR}/risks", "POST"),
            (f"{settings.API_V1_STR}/team-members", "GET"),
            (f"{settings.API_V1_STR}/team-members", "POST"),
            (f"{settings.API_V1_STR}/clients", "GET"),
            (f"{settings.API_V1_STR}/clients", "POST"),
            (f"{settings.API_V1_STR}/analytics/dashboard", "GET"),
            (f"{settings.API_V1_STR}/security/health", "GET"),
        ]
        
        for endpoint, method in endpoints_to_test:
            if method == "GET":
                response = client.get(endpoint)
            elif method == "POST":
                response = client.post(endpoint, json={})
            
            # Verificar se o endpoint existe (não deve retornar 404)
            assert response.status_code != 404, f"Endpoint {method} {endpoint} não encontrado (404)"
            
            # Verificar se não é erro de servidor interno
            assert response.status_code != 500, f"Endpoint {method} {endpoint} retornou erro interno (500)"
            
            print(f"[OK] {method} {endpoint} - Status: {response.status_code}")
    
    async def test_portfolio_endpoint_basic(self, client: TestClient, db_session: AsyncSession):
        """Testar endpoint básico de portfólio."""
        
        # Testar GET (deve retornar lista vazia ou erro de validação, mas não 404)
        response = client.get(f"{settings.API_V1_STR}/portfolios")
        assert response.status_code != 404, "Endpoint GET /portfolios não encontrado"
        print(f"[OK] GET /portfolios - Status: {response.status_code}")
        
        # Testar POST com dados mínimos
        minimal_data = {
            "name": "Teste Básico",
            "description": "Teste básico de portfólio"
        }
        response = client.post(f"{settings.API_V1_STR}/portfolios", json=minimal_data)
        assert response.status_code != 404, "Endpoint POST /portfolios não encontrado"
        print(f"[OK] POST /portfolios - Status: {response.status_code}")
    
    async def test_risks_endpoint_basic(self, client: TestClient, db_session: AsyncSession):
        """Testar endpoint básico de riscos."""
        
        # Testar GET
        response = client.get(f"{settings.API_V1_STR}/risks")
        assert response.status_code != 404, "Endpoint GET /risks não encontrado"
        print(f"[OK] GET /risks - Status: {response.status_code}")
        
        # Testar POST com dados mínimos
        minimal_data = {
            "title": "Risco de Teste",
            "description": "Risco básico para teste"
        }
        response = client.post(f"{settings.API_V1_STR}/risks", json=minimal_data)
        assert response.status_code != 404, "Endpoint POST /risks não encontrado"
        print(f"[OK] POST /risks - Status: {response.status_code}")
    
    async def test_team_members_endpoint_basic(self, client: TestClient, db_session: AsyncSession):
        """Testar endpoint básico de membros da equipe."""
        
        # Testar GET
        response = client.get(f"{settings.API_V1_STR}/team-members")
        assert response.status_code != 404, "Endpoint GET /team-members não encontrado"
        print(f"[OK] GET /team-members - Status: {response.status_code}")
        
        # Testar POST com dados mínimos
        minimal_data = {
            "name": "Membro Teste",
            "email": "teste@example.com",
            "role": "developer"
        }
        response = client.post(f"{settings.API_V1_STR}/team-members", json=minimal_data)
        assert response.status_code != 404, "Endpoint POST /team-members não encontrado"
        print(f"[OK] POST /team-members - Status: {response.status_code}")
    
    async def test_clients_endpoint_basic(self, client: TestClient, db_session: AsyncSession):
        """Testar endpoint básico de clientes."""
        
        # Testar GET
        response = client.get(f"{settings.API_V1_STR}/clients")
        assert response.status_code != 404, "Endpoint GET /clients não encontrado"
        print(f"[OK] GET /clients - Status: {response.status_code}")
        
        # Testar POST com dados mínimos
        minimal_data = {
            "name": "Cliente Teste",
            "type": "private",
            "contact_person": "Contato Teste",
            "email": "contato@cliente.com"
        }
        response = client.post(f"{settings.API_V1_STR}/clients", json=minimal_data)
        assert response.status_code != 404, "Endpoint POST /clients não encontrado"
        print(f"[OK] POST /clients - Status: {response.status_code}")
    
    async def test_analytics_endpoint_basic(self, client: TestClient, db_session: AsyncSession):
        """Testar endpoint básico de analytics."""
        
        # Testar dashboard
        response = client.get(f"{settings.API_V1_STR}/analytics/dashboard")
        assert response.status_code != 404, "Endpoint GET /analytics/dashboard não encontrado"
        print(f"[OK] GET /analytics/dashboard - Status: {response.status_code}")
        
        # Testar analytics de projetos
        response = client.get(f"{settings.API_V1_STR}/analytics/projects")
        assert response.status_code != 404, "Endpoint GET /analytics/projects não encontrado"
        print(f"[OK] GET /analytics/projects - Status: {response.status_code}")
    
    async def test_security_endpoint_basic(self, client: TestClient, db_session: AsyncSession):
        """Testar endpoint básico de segurança."""
        
        # Testar health check
        response = client.get(f"{settings.API_V1_STR}/security/health")
        assert response.status_code != 404, "Endpoint GET /security/health não encontrado"
        print(f"[OK] GET /security/health - Status: {response.status_code}")
        
        # Testar eventos de segurança
        response = client.get(f"{settings.API_V1_STR}/security/events")
        assert response.status_code != 404, "Endpoint GET /security/events não encontrado"
        print(f"[OK] GET /security/events - Status: {response.status_code}")
