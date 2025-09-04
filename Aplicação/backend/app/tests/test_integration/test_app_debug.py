"""
Teste para debugar a aplicação FastAPI.
"""

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings


class TestAppDebug:
    """Teste para debugar a aplicação FastAPI."""
    
    async def test_app_routes_debug(self, client: TestClient, db_session: AsyncSession):
        """Testar se as rotas estão sendo incluídas na aplicação."""
        
        # Obter a aplicação FastAPI do cliente
        app = client._tc.app
        
        # Listar todas as rotas da aplicação
        print("=== Rotas da aplicação ===")
        for route in app.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                print(f"[OK] {list(route.methods)} {route.path}")
        
        # Verificar se as rotas de portfólio estão presentes
        portfolio_routes = [route for route in app.routes if hasattr(route, 'path') and 'portfolio' in route.path]
        print(f"\n=== Rotas de portfólio encontradas: {len(portfolio_routes)} ===")
        for route in portfolio_routes:
            print(f"[OK] {list(route.methods)} {route.path}")
        
        # Verificar se as rotas de riscos estão presentes
        risk_routes = [route for route in app.routes if hasattr(route, 'path') and 'risk' in route.path]
        print(f"\n=== Rotas de riscos encontradas: {len(risk_routes)} ===")
        for route in risk_routes:
            print(f"[OK] {list(route.methods)} {route.path}")
        
        # Verificar se as rotas de team_members estão presentes
        team_routes = [route for route in app.routes if hasattr(route, 'path') and 'team' in route.path]
        print(f"\n=== Rotas de team_members encontradas: {len(team_routes)} ===")
        for route in team_routes:
            print(f"[OK] {list(route.methods)} {route.path}")
        
        # Verificar se as rotas de clientes estão presentes
        client_routes = [route for route in app.routes if hasattr(route, 'path') and 'client' in route.path]
        print(f"\n=== Rotas de clientes encontradas: {len(client_routes)} ===")
        for route in client_routes:
            print(f"[OK] {list(route.methods)} {route.path}")
        
        # Verificar se as rotas de analytics estão presentes
        analytics_routes = [route for route in app.routes if hasattr(route, 'path') and 'analytics' in route.path]
        print(f"\n=== Rotas de analytics encontradas: {len(analytics_routes)} ===")
        for route in analytics_routes:
            print(f"[OK] {list(route.methods)} {route.path}")
        
        # Verificar se as rotas de security estão presentes
        security_routes = [route for route in app.routes if hasattr(route, 'path') and 'security' in route.path]
        print(f"\n=== Rotas de security encontradas: {len(security_routes)} ===")
        for route in security_routes:
            print(f"[OK] {list(route.methods)} {route.path}")
    
    async def test_router_inclusion_debug(self, client: TestClient, db_session: AsyncSession):
        """Testar se os routers estão sendo incluídos corretamente."""
        
        # Testar se conseguimos acessar as rotas diretamente
        try:
            from app.routers.portfolios import router as portfolio_router
            print("[OK] Router de portfólio importado diretamente")
            print(f"   Rotas: {[route.path for route in portfolio_router.routes]}")
        except Exception as e:
            print(f"[ERROR] Erro ao importar router de portfólio: {e}")
        
        # Testar se conseguimos incluir o router manualmente
        try:
            from fastapi import FastAPI
            from app.routers.portfolios import router as portfolio_router
            
            test_app = FastAPI()
            test_app.include_router(portfolio_router, prefix=f"{settings.API_V1_STR}/portfolios", tags=["portfolios"])
            
            print("[OK] Router de portfólio incluído manualmente com sucesso")
            print(f"   Rotas na app de teste: {[route.path for route in test_app.routes]}")
        except Exception as e:
            print(f"[ERROR] Erro ao incluir router de portfólio manualmente: {e}")
