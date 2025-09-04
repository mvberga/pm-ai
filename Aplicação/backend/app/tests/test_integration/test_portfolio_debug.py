import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.user import User
from app.models.portfolio import Portfolio
from app.utils.auth import hash_password
from app.schemas.portfolio import PortfolioCreate
from app.services.portfolio_service import PortfolioService


class TestPortfolioDebug:
    """Testes para debugar o serviço de portfólio."""

    async def test_portfolio_service_direct(self, db_session: AsyncSession):
        """Testar o serviço de portfólio diretamente."""
        
        # Criar usuário
        test_user = User(
            id=1,
            email="test@example.com",
            name="Test User",
            hashed_password=hash_password("testpassword")
        )
        db_session.add(test_user)
        await db_session.commit()
        await db_session.refresh(test_user)
        
        # Criar dados do portfólio
        portfolio_data = PortfolioCreate(
            name="Portfólio de Teste Debug",
            description="Portfólio para debug",
            owner_id=1
        )
        
        # Testar serviço diretamente
        try:
            service = PortfolioService(db_session)
            portfolio = await service.create_portfolio(portfolio_data, 1)
            print(f"Portfolio criado: {portfolio}")
            assert portfolio is not None
            assert portfolio.name == "Portfólio de Teste Debug"
        except Exception as e:
            print(f"Erro no serviço: {e}")
            print(f"Tipo do erro: {type(e)}")
            import traceback
            traceback.print_exc()
            raise

    async def test_portfolio_model_direct(self, db_session: AsyncSession):
        """Testar criação direta do modelo Portfolio."""
        
        # Criar usuário
        test_user = User(
            id=1,
            email="test@example.com",
            name="Test User",
            hashed_password=hash_password("testpassword")
        )
        db_session.add(test_user)
        await db_session.commit()
        await db_session.refresh(test_user)
        
        # Criar portfólio diretamente
        try:
            portfolio = Portfolio(
                name="Portfólio de Teste Direto",
                description="Portfólio criado diretamente",
                owner_id=1
            )
            db_session.add(portfolio)
            await db_session.commit()
            await db_session.refresh(portfolio)
            print(f"Portfolio criado diretamente: {portfolio}")
            assert portfolio is not None
            assert portfolio.name == "Portfólio de Teste Direto"
        except Exception as e:
            print(f"Erro na criação direta: {e}")
            print(f"Tipo do erro: {type(e)}")
            import traceback
            traceback.print_exc()
            raise
