"""
Testes unitários para PortfolioRepository
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.portfolio_repository import PortfolioRepository
from app.models.portfolio import Portfolio


@pytest.fixture
def mock_db():
    """Mock do banco de dados"""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def portfolio_repository(mock_db):
    """Instância do PortfolioRepository com mocks"""
    return PortfolioRepository(mock_db)


@pytest.fixture
def sample_portfolio_data():
    """Dados de exemplo para portfólio"""
    return {
        "name": "Test Portfolio",
        "description": "Test Description",
        "owner_id": 1,
        "is_active": True
    }


class TestPortfolioRepository:
    """Testes para PortfolioRepository"""
    
    @pytest.mark.asyncio
    async def test_create_portfolio(self, portfolio_repository, sample_portfolio_data):
        """Testa criação de portfólio"""
        # Arrange
        mock_portfolio = MagicMock(spec=Portfolio)
        mock_portfolio.id = 1
        mock_portfolio.name = sample_portfolio_data["name"]
        
        portfolio_repository.db.add = MagicMock()
        portfolio_repository.db.commit = AsyncMock()
        portfolio_repository.db.refresh = AsyncMock()
        
        # Act
        result = await portfolio_repository.create(sample_portfolio_data)
        
        # Assert
        assert result is not None
        portfolio_repository.db.add.assert_called_once()
        portfolio_repository.db.commit.assert_called_once()
        portfolio_repository.db.refresh.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_portfolio(self, portfolio_repository):
        """Testa busca de portfólio por ID"""
        # Arrange
        mock_portfolio = MagicMock(spec=Portfolio)
        mock_portfolio.id = 1
        mock_portfolio.name = "Test Portfolio"
        
        portfolio_repository.db.execute = AsyncMock()
        portfolio_repository.db.execute.return_value.scalar_one_or_none.return_value = mock_portfolio
        
        # Act
        result = await portfolio_repository.get(1)
        
        # Assert
        assert result == mock_portfolio
        portfolio_repository.db.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_portfolio_not_found(self, portfolio_repository):
        """Testa busca de portfólio não encontrado"""
        # Arrange
        portfolio_repository.db.execute = AsyncMock()
        portfolio_repository.db.execute.return_value.scalar_one_or_none.return_value = None
        
        # Act
        result = await portfolio_repository.get(999)
        
        # Assert
        assert result is None
    
    @pytest.mark.asyncio
    async def test_update_portfolio(self, portfolio_repository):
        """Testa atualização de portfólio"""
        # Arrange
        mock_portfolio = MagicMock(spec=Portfolio)
        mock_portfolio.id = 1
        mock_portfolio.name = "Updated Portfolio"
        
        portfolio_repository.db.execute = AsyncMock()
        portfolio_repository.db.execute.return_value.scalar_one_or_none.return_value = mock_portfolio
        portfolio_repository.db.commit = AsyncMock()
        portfolio_repository.db.refresh = AsyncMock()
        
        update_data = {"name": "Updated Portfolio"}
        
        # Act
        result = await portfolio_repository.update(1, update_data)
        
        # Assert
        assert result == mock_portfolio
        portfolio_repository.db.commit.assert_called_once()
        portfolio_repository.db.refresh.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_delete_portfolio(self, portfolio_repository):
        """Testa exclusão de portfólio"""
        # Arrange
        mock_portfolio = MagicMock(spec=Portfolio)
        mock_portfolio.id = 1
        
        portfolio_repository.db.execute = AsyncMock()
        portfolio_repository.db.execute.return_value.scalar_one_or_none.return_value = mock_portfolio
        portfolio_repository.db.delete = MagicMock()
        portfolio_repository.db.commit = AsyncMock()
        
        # Act
        result = await portfolio_repository.delete(1)
        
        # Assert
        assert result is True
        portfolio_repository.db.delete.assert_called_once_with(mock_portfolio)
        portfolio_repository.db.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_delete_portfolio_not_found(self, portfolio_repository):
        """Testa exclusão de portfólio não encontrado"""
        # Arrange
        portfolio_repository.db.execute = AsyncMock()
        portfolio_repository.db.execute.return_value.scalar_one_or_none.return_value = None
        
        # Act
        result = await portfolio_repository.delete(999)
        
        # Assert
        assert result is False
    
    @pytest.mark.asyncio
    async def test_get_by_owner(self, portfolio_repository):
        """Testa busca de portfólios por proprietário"""
        # Arrange
        mock_portfolios = [
            MagicMock(spec=Portfolio, id=1, name="Portfolio 1"),
            MagicMock(spec=Portfolio, id=2, name="Portfolio 2")
        ]
        
        portfolio_repository.db.execute = AsyncMock()
        portfolio_repository.db.execute.return_value.scalars.return_value.all.return_value = mock_portfolios
        
        # Act
        result = await portfolio_repository.get_by_owner(1)
        
        # Assert
        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2
        portfolio_repository.db.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_by_name_and_owner(self, portfolio_repository):
        """Testa busca de portfólio por nome e proprietário"""
        # Arrange
        mock_portfolio = MagicMock(spec=Portfolio)
        mock_portfolio.id = 1
        mock_portfolio.name = "Test Portfolio"
        
        portfolio_repository.db.execute = AsyncMock()
        portfolio_repository.db.execute.return_value.scalar_one_or_none.return_value = mock_portfolio
        
        # Act
        result = await portfolio_repository.get_by_name_and_owner("Test Portfolio", 1)
        
        # Assert
        assert result == mock_portfolio
        portfolio_repository.db.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_count_projects(self, portfolio_repository):
        """Testa contagem de projetos do portfólio"""
        # Arrange
        portfolio_repository.db.execute = AsyncMock()
        portfolio_repository.db.execute.return_value.scalar.return_value = 5
        
        # Act
        result = await portfolio_repository.count_projects(1)
        
        # Assert
        assert result == 5
        portfolio_repository.db.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_count_active_projects(self, portfolio_repository):
        """Testa contagem de projetos ativos do portfólio"""
        # Arrange
        portfolio_repository.db.execute = AsyncMock()
        portfolio_repository.db.execute.return_value.scalar.return_value = 3
        
        # Act
        result = await portfolio_repository.count_active_projects(1)
        
        # Assert
        assert result == 3
        portfolio_repository.db.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_projects(self, portfolio_repository):
        """Testa busca de projetos do portfólio"""
        # Arrange
        mock_projects = [
            MagicMock(id=1, name="Project 1"),
            MagicMock(id=2, name="Project 2")
        ]
        
        portfolio_repository.db.execute = AsyncMock()
        portfolio_repository.db.execute.return_value.scalars.return_value.all.return_value = mock_projects
        
        # Act
        result = await portfolio_repository.get_projects(1)
        
        # Assert
        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2
        portfolio_repository.db.execute.assert_called_once()
