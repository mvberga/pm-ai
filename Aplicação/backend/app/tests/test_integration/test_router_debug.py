"""
Teste para debugar problemas com routers.
"""

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings


class TestRouterDebug:
    """Teste para debugar problemas com routers."""
    
    async def test_router_inclusion_debug(self, client: TestClient, db_session: AsyncSession):
        """Testar se os routers estão sendo incluídos corretamente."""
        
        # Testar endpoints que sabemos que funcionam
        working_endpoints = [
            "/health",
            "/",
            f"{settings.API_V1_STR}/projects/",
            f"{settings.API_V1_STR}/checklists",
            f"{settings.API_V1_STR}/action-items",
        ]
        
        print("=== Testando endpoints que funcionam ===")
        for endpoint in working_endpoints:
            response = client.get(endpoint)
            print(f"[OK] {endpoint} - Status: {response.status_code}")
        
        # Testar endpoints que não estão funcionando
        problematic_endpoints = [
            f"{settings.API_V1_STR}/portfolios",
            f"{settings.API_V1_STR}/risks",
            f"{settings.API_V1_STR}/team-members",
            f"{settings.API_V1_STR}/clients",
            f"{settings.API_V1_STR}/analytics/dashboard",
            f"{settings.API_V1_STR}/security/health",
        ]
        
        print("\n=== Testando endpoints problemáticos ===")
        for endpoint in problematic_endpoints:
            response = client.get(endpoint)
            print(f"{'[OK]' if response.status_code != 404 else '[ERROR]'} {endpoint} - Status: {response.status_code}")
            if response.status_code == 404:
                print(f"   Erro: {response.text}")
    
    async def test_specific_portfolio_debug(self, client: TestClient, db_session: AsyncSession):
        """Testar especificamente o endpoint de portfólio."""
        
        # Testar diferentes variações do endpoint
        portfolio_endpoints = [
            f"{settings.API_V1_STR}/portfolios",
            f"{settings.API_V1_STR}/portfolios/",
            "/api/v1/portfolios",
            "/api/v1/portfolios/",
        ]
        
        print("=== Testando variações do endpoint de portfólio ===")
        for endpoint in portfolio_endpoints:
            response = client.get(endpoint)
            print(f"{'[OK]' if response.status_code != 404 else '[ERROR]'} {endpoint} - Status: {response.status_code}")
            if response.status_code == 404:
                print(f"   Erro: {response.text}")
    
    async def test_router_import_debug(self, client: TestClient, db_session: AsyncSession):
        """Testar se os routers estão sendo importados corretamente."""
        
        try:
            from app.routers import portfolios
            print("[OK] Router de portfólio importado com sucesso")
            print(f"   Rotas: {[route.path for route in portfolios.router.routes]}")
        except Exception as e:
            print(f"[ERROR] Erro ao importar router de portfólio: {e}")
        
        try:
            from app.routers import risks
            print("[OK] Router de riscos importado com sucesso")
            print(f"   Rotas: {[route.path for route in risks.router.routes]}")
        except Exception as e:
            print(f"[ERROR] Erro ao importar router de riscos: {e}")
        
        try:
            from app.routers import team_members
            print("[OK] Router de team_members importado com sucesso")
            print(f"   Rotas: {[route.path for route in team_members.router.routes]}")
        except Exception as e:
            print(f"[ERROR] Erro ao importar router de team_members: {e}")
        
        try:
            from app.routers import clients
            print("[OK] Router de clientes importado com sucesso")
            print(f"   Rotas: {[route.path for route in clients.router.routes]}")
        except Exception as e:
            print(f"[ERROR] Erro ao importar router de clientes: {e}")
        
        try:
            from app.routers import analytics
            print("[OK] Router de analytics importado com sucesso")
            print(f"   Rotas: {[route.path for route in analytics.router.routes]}")
        except Exception as e:
            print(f"[ERROR] Erro ao importar router de analytics: {e}")
        
        try:
            from app.routers import security
            print("[OK] Router de security importado com sucesso")
            print(f"   Rotas: {[route.path for route in security.router.routes]}")
        except Exception as e:
            print(f"[ERROR] Erro ao importar router de security: {e}")
