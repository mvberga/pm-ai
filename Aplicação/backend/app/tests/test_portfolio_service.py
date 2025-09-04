"""
Testes unitários para PortfolioService
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.portfolio_service import PortfolioService
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate
from app.models.portfolio import Portfolio
from app.models.user import User
from app.core.exceptions import ValidationError, NotFoundError


@pytest.fixture
def mock_db():
    """Mock do banco de dados"""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def portfolio_service(mock_db):
    """Instância do PortfolioService com mocks"""
    return PortfolioService(mock_db)


@pytest.fixture
def sample_user():
    """Usuário de exemplo"""
    user = MagicMock(spec=User)
    user.id = 1
    user.email = "test@example.com"
    user.full_name = "Test User"
    return user


@pytest.fixture
def sample_portfolio():
    """Portfólio de exemplo"""
    portfolio = MagicMock(spec=Portfolio)
    portfolio.id = 1
    portfolio.name = "Test Portfolio"
    portfolio.description = "Test Description"
    portfolio.owner_id = 1
    portfolio.is_active = True
    portfolio.created_at = "2025-01-01T00:00:00"
    portfolio.updated_at = "2025-01-01T00:00:00"
    return portfolio


@pytest.fixture
def portfolio_create_data():
    """Dados para criação de portfólio"""
    return PortfolioCreate(
        name="New Portfolio",
        description="New Description",
        is_active=True
    )


class TestPortfolioService:
    """Testes para PortfolioService"""
    
    @pytest.mark.asyncio
    async def test_create_portfolio_success(self, portfolio_service, sample_user, portfolio_create_data):
        """Testa criação de portfólio com sucesso"""
        # Arrange
        portfolio_service.user_repo.get.return_value = sample_user
        portfolio_service.portfolio_repo.get_by_name_and_owner.return_value = None
        portfolio_service.portfolio_repo.create.return_value = MagicMock()
        
        # Act
        result = await portfolio_service.create_portfolio(portfolio_create_data, sample_user.id)
        
        # Assert
        assert result is not None
        portfolio_service.user_repo.get.assert_called_once_with(sample_user.id)
        portfolio_service.portfolio_repo.get_by_name_and_owner.assert_called_once_with(
            portfolio_create_data.name, sample_user.id
        )
        portfolio_service.portfolio_repo.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_portfolio_user_not_found(self, portfolio_service, portfolio_create_data):
        """Testa criação de portfólio com usuário não encontrado"""
        # Arrange
        portfolio_service.user_repo.get.return_value = None
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            await portfolio_service.create_portfolio(portfolio_create_data, 999)
        
        assert "Usuário com ID 999 não encontrado" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_create_portfolio_duplicate_name(self, portfolio_service, sample_user, portfolio_create_data):
        """Testa criação de portfólio com nome duplicado"""
        # Arrange
        portfolio_service.user_repo.get.return_value = sample_user
        portfolio_service.portfolio_repo.get_by_name_and_owner.return_value = MagicMock()
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            await portfolio_service.create_portfolio(portfolio_create_data, sample_user.id)
        
        assert f"Já existe um portfólio com o nome '{portfolio_create_data.name}'" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_get_portfolio_success(self, portfolio_service, sample_portfolio):
        """Testa busca de portfólio com sucesso"""
        # Arrange
        portfolio_service.portfolio_repo.get.return_value = sample_portfolio
        portfolio_service.project_repo.get.return_value = MagicMock()
        
        # Act
        result = await portfolio_service.get_portfolio(sample_portfolio.id, sample_portfolio.owner_id)
        
        # Assert
        assert result == sample_portfolio
        portfolio_service.portfolio_repo.get.assert_called_once_with(sample_portfolio.id)
    
    @pytest.mark.asyncio
    async def test_get_portfolio_not_found(self, portfolio_service):
        """Testa busca de portfólio não encontrado"""
        # Arrange
        portfolio_service.portfolio_repo.get.return_value = None
        
        # Act
        result = await portfolio_service.get_portfolio(999, 1)
        
        # Assert
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_portfolio_no_permission(self, portfolio_service, sample_portfolio):
        """Testa busca de portfólio sem permissão"""
        # Arrange
        portfolio_service.portfolio_repo.get.return_value = sample_portfolio
        portfolio_service.project_repo.get.return_value = None
        
        # Act
        result = await portfolio_service.get_portfolio(sample_portfolio.id, 999)
        
        # Assert
        assert result is None
    
    @pytest.mark.asyncio
    async def test_update_portfolio_success(self, portfolio_service, sample_portfolio):
        """Testa atualização de portfólio com sucesso"""
        # Arrange
        portfolio_service.portfolio_repo.get.return_value = sample_portfolio
        portfolio_service.project_repo.get.return_value = MagicMock()
        portfolio_service.portfolio_repo.get_by_name_and_owner.return_value = None
        portfolio_service.portfolio_repo.update.return_value = sample_portfolio
        
        update_data = PortfolioUpdate(name="Updated Portfolio")
        
        # Act
        result = await portfolio_service.update_portfolio(
            sample_portfolio.id, update_data, sample_portfolio.owner_id
        )
        
        # Assert
        assert result == sample_portfolio
        portfolio_service.portfolio_repo.update.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_update_portfolio_not_found(self, portfolio_service):
        """Testa atualização de portfólio não encontrado"""
        # Arrange
        portfolio_service.portfolio_repo.get.return_value = None
        
        update_data = PortfolioUpdate(name="Updated Portfolio")
        
        # Act
        result = await portfolio_service.update_portfolio(999, update_data, 1)
        
        # Assert
        assert result is None
    
    @pytest.mark.asyncio
    async def test_delete_portfolio_success(self, portfolio_service, sample_portfolio):
        """Testa exclusão de portfólio com sucesso"""
        # Arrange
        portfolio_service.portfolio_repo.get.return_value = sample_portfolio
        portfolio_service.project_repo.get.return_value = MagicMock()
        portfolio_service.portfolio_repo.delete.return_value = True
        
        # Act
        result = await portfolio_service.delete_portfolio(sample_portfolio.id, sample_portfolio.owner_id)
        
        # Assert
        assert result is True
        portfolio_service.portfolio_repo.delete.assert_called_once_with(sample_portfolio.id)
    
    @pytest.mark.asyncio
    async def test_delete_portfolio_not_found(self, portfolio_service):
        """Testa exclusão de portfólio não encontrado"""
        # Arrange
        portfolio_service.portfolio_repo.get.return_value = None
        
        # Act
        result = await portfolio_service.delete_portfolio(999, 1)
        
        # Assert
        assert result is False
    
    @pytest.mark.asyncio
    async def test_get_user_portfolios(self, portfolio_service, sample_portfolio):
        """Testa listagem de portfólios do usuário"""
        # Arrange
        portfolios = [sample_portfolio]
        portfolio_service.portfolio_repo.get_by_owner.return_value = portfolios
        portfolio_service.portfolio_repo.count_projects.return_value = 5
        
        # Act
        result = await portfolio_service.get_user_portfolios(sample_portfolio.owner_id)
        
        # Assert
        assert len(result) == 1
        assert result[0].id == sample_portfolio.id
        assert result[0].name == sample_portfolio.name
        assert result[0].projects_count == 5
    
    @pytest.mark.asyncio
    async def test_activate_portfolio(self, portfolio_service, sample_portfolio):
        """Testa ativação de portfólio"""
        # Arrange
        portfolio_service.portfolio_repo.get.return_value = sample_portfolio
        portfolio_service.project_repo.get.return_value = MagicMock()
        portfolio_service.portfolio_repo.get_by_name_and_owner.return_value = None
        portfolio_service.portfolio_repo.update.return_value = sample_portfolio
        
        # Act
        result = await portfolio_service.activate_portfolio(sample_portfolio.id, sample_portfolio.owner_id)
        
        # Assert
        assert result == sample_portfolio
        portfolio_service.portfolio_repo.update.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_deactivate_portfolio(self, portfolio_service, sample_portfolio):
        """Testa desativação de portfólio"""
        # Arrange
        portfolio_service.portfolio_repo.get.return_value = sample_portfolio
        portfolio_service.project_repo.get.return_value = MagicMock()
        portfolio_service.portfolio_repo.get_by_name_and_owner.return_value = None
        portfolio_service.portfolio_repo.update.return_value = sample_portfolio
        
        # Act
        result = await portfolio_service.deactivate_portfolio(sample_portfolio.id, sample_portfolio.owner_id)
        
        # Assert
        assert result == sample_portfolio
        portfolio_service.portfolio_repo.update.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_portfolio_statistics(self, portfolio_service, sample_portfolio):
        """Testa obtenção de estatísticas do portfólio"""
        # Arrange
        portfolio_service.portfolio_repo.get.return_value = sample_portfolio
        portfolio_service.project_repo.get.return_value = MagicMock()
        portfolio_service.portfolio_repo.count_projects.return_value = 10
        portfolio_service.portfolio_repo.count_active_projects.return_value = 8
        
        # Act
        result = await portfolio_service.get_portfolio_statistics(sample_portfolio.id, sample_portfolio.owner_id)
        
        # Assert
        assert result["portfolio_id"] == sample_portfolio.id
        assert result["portfolio_name"] == sample_portfolio.name
        assert result["total_projects"] == 10
        assert result["active_projects"] == 8
        assert result["inactive_projects"] == 2
    
    @pytest.mark.asyncio
    async def test_get_portfolio_statistics_not_found(self, portfolio_service):
        """Testa obtenção de estatísticas de portfólio não encontrado"""
        # Arrange
        portfolio_service.portfolio_repo.get.return_value = None
        
        # Act & Assert
        with pytest.raises(NotFoundError) as exc_info:
            await portfolio_service.get_portfolio_statistics(999, 1)
        
        assert "Portfólio não encontrado" in str(exc_info.value)
