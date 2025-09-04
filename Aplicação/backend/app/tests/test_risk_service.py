"""
Testes unitários para RiskService
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.risk_service import RiskService
from app.schemas.risk import RiskCreate, RiskUpdate
from app.models.risk import Risk, RiskCategory, RiskStatus, RiskPriority
from app.models.project import Project
from app.core.exceptions import ValidationError, NotFoundError


@pytest.fixture
def mock_db():
    """Mock do banco de dados"""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def risk_service(mock_db):
    """Instância do RiskService com mocks"""
    return RiskService(mock_db)


@pytest.fixture
def sample_project():
    """Projeto de exemplo"""
    project = MagicMock(spec=Project)
    project.id = 1
    project.name = "Test Project"
    project.owner_id = 1
    return project


@pytest.fixture
def sample_risk():
    """Risco de exemplo"""
    risk = MagicMock(spec=Risk)
    risk.id = 1
    risk.title = "Test Risk"
    risk.description = "Test Description"
    risk.category = RiskCategory.TECHNICAL
    risk.status = RiskStatus.ACTIVE
    risk.priority = RiskPriority.HIGH
    risk.probability = 0.8
    risk.impact = 0.9
    risk.project_id = 1
    risk.created_at = "2025-01-01T00:00:00"
    risk.updated_at = "2025-01-01T00:00:00"
    return risk


@pytest.fixture
def risk_create_data():
    """Dados para criação de risco"""
    return RiskCreate(
        title="New Risk",
        description="New Description",
        category=RiskCategory.TECHNICAL,
        status=RiskStatus.ACTIVE,
        priority=RiskPriority.HIGH,
        probability=0.7,
        impact=0.8,
        project_id=1
    )


class TestRiskService:
    """Testes para RiskService"""
    
    @pytest.mark.asyncio
    async def test_create_risk_success(self, risk_service, sample_project, risk_create_data):
        """Testa criação de risco com sucesso"""
        # Arrange
        risk_service.project_repo.get.return_value = sample_project
        created_risk = MagicMock()
        created_risk.id = 1
        created_risk.probability = risk_create_data.probability
        created_risk.impact = risk_create_data.impact
        risk_service.risk_repo.create.return_value = created_risk
        risk_service.risk_repo.update.return_value = created_risk
        
        # Act
        result = await risk_service.create_risk(risk_create_data, sample_project.owner_id)
        
        # Assert
        assert result is not None
        risk_service.project_repo.get.assert_called_once_with(risk_create_data.project_id)
        risk_service.risk_repo.create.assert_called_once()
        risk_service.risk_repo.update.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_risk_project_not_found(self, risk_service, risk_create_data):
        """Testa criação de risco com projeto não encontrado"""
        # Arrange
        risk_service.project_repo.get.return_value = None
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            await risk_service.create_risk(risk_create_data, 1)
        
        assert f"Projeto com ID {risk_create_data.project_id} não encontrado" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_create_risk_no_permission(self, risk_service, sample_project, risk_create_data):
        """Testa criação de risco sem permissão"""
        # Arrange
        sample_project.owner_id = 999  # Diferente do user_id
        risk_service.project_repo.get.return_value = sample_project
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            await risk_service.create_risk(risk_create_data, 1)
        
        assert "Usuário não tem permissão para adicionar riscos a este projeto" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_get_risk_success(self, risk_service, sample_risk, sample_project):
        """Testa busca de risco com sucesso"""
        # Arrange
        risk_service.risk_repo.get.return_value = sample_risk
        risk_service.project_repo.get.return_value = sample_project
        
        # Act
        result = await risk_service.get_risk(sample_risk.id, sample_project.owner_id)
        
        # Assert
        assert result == sample_risk
        risk_service.risk_repo.get.assert_called_once_with(sample_risk.id)
    
    @pytest.mark.asyncio
    async def test_get_risk_not_found(self, risk_service):
        """Testa busca de risco não encontrado"""
        # Arrange
        risk_service.risk_repo.get.return_value = None
        
        # Act
        result = await risk_service.get_risk(999, 1)
        
        # Assert
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_risk_no_permission(self, risk_service, sample_risk):
        """Testa busca de risco sem permissão"""
        # Arrange
        risk_service.risk_repo.get.return_value = sample_risk
        risk_service.project_repo.get.return_value = None
        
        # Act
        result = await risk_service.get_risk(sample_risk.id, 999)
        
        # Assert
        assert result is None
    
    @pytest.mark.asyncio
    async def test_update_risk_success(self, risk_service, sample_risk, sample_project):
        """Testa atualização de risco com sucesso"""
        # Arrange
        risk_service.risk_repo.get.return_value = sample_risk
        risk_service.project_repo.get.return_value = sample_project
        risk_service.risk_repo.update.return_value = sample_risk
        
        update_data = RiskUpdate(title="Updated Risk")
        
        # Act
        result = await risk_service.update_risk(sample_risk.id, update_data, sample_project.owner_id)
        
        # Assert
        assert result == sample_risk
        risk_service.risk_repo.update.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_update_risk_recalculate_score(self, risk_service, sample_risk, sample_project):
        """Testa atualização de risco com recálculo de score"""
        # Arrange
        risk_service.risk_repo.get.return_value = sample_risk
        risk_service.project_repo.get.return_value = sample_project
        risk_service.risk_repo.update.return_value = sample_risk
        
        update_data = RiskUpdate(probability=0.9, impact=0.8)
        
        # Act
        result = await risk_service.update_risk(sample_risk.id, update_data, sample_project.owner_id)
        
        # Assert
        assert result == sample_risk
        # Verificar se o risk_score foi calculado corretamente
        call_args = risk_service.risk_repo.update.call_args[0]
        assert call_args[1]["risk_score"] == 0.9 * 0.8
    
    @pytest.mark.asyncio
    async def test_delete_risk_success(self, risk_service, sample_risk, sample_project):
        """Testa exclusão de risco com sucesso"""
        # Arrange
        risk_service.risk_repo.get.return_value = sample_risk
        risk_service.project_repo.get.return_value = sample_project
        risk_service.risk_repo.delete.return_value = True
        
        # Act
        result = await risk_service.delete_risk(sample_risk.id, sample_project.owner_id)
        
        # Assert
        assert result is True
        risk_service.risk_repo.delete.assert_called_once_with(sample_risk.id)
    
    @pytest.mark.asyncio
    async def test_get_project_risks(self, risk_service, sample_risk, sample_project):
        """Testa listagem de riscos do projeto"""
        # Arrange
        risks = [sample_risk]
        risk_service.project_repo.get.return_value = sample_project
        risk_service.risk_repo.get_by_project.return_value = risks
        
        # Act
        result = await risk_service.get_project_risks(sample_project.id, sample_project.owner_id)
        
        # Assert
        assert len(result) == 1
        assert result[0].id == sample_risk.id
        assert result[0].title == sample_risk.title
        assert result[0].risk_score == sample_risk.probability * sample_risk.impact
    
    @pytest.mark.asyncio
    async def test_get_risks_by_category(self, risk_service, sample_risk, sample_project):
        """Testa listagem de riscos por categoria"""
        # Arrange
        risks = [sample_risk]
        risk_service.project_repo.get.return_value = sample_project
        risk_service.risk_repo.get_by_project_and_category.return_value = risks
        
        # Act
        result = await risk_service.get_risks_by_category(
            sample_project.id, RiskCategory.TECHNICAL, sample_project.owner_id
        )
        
        # Assert
        assert len(result) == 1
        assert result[0].category == RiskCategory.TECHNICAL
    
    @pytest.mark.asyncio
    async def test_get_risks_by_priority(self, risk_service, sample_risk, sample_project):
        """Testa listagem de riscos por prioridade"""
        # Arrange
        risks = [sample_risk]
        risk_service.project_repo.get.return_value = sample_project
        risk_service.risk_repo.get_by_project_and_priority.return_value = risks
        
        # Act
        result = await risk_service.get_risks_by_priority(
            sample_project.id, RiskPriority.HIGH, sample_project.owner_id
        )
        
        # Assert
        assert len(result) == 1
        assert result[0].priority == RiskPriority.HIGH
    
    @pytest.mark.asyncio
    async def test_get_high_risk_risks(self, risk_service, sample_risk, sample_project):
        """Testa listagem de riscos de alta pontuação"""
        # Arrange
        risks = [sample_risk]
        risk_service.project_repo.get.return_value = sample_project
        risk_service.risk_repo.get_high_risk_risks.return_value = risks
        
        # Act
        result = await risk_service.get_high_risk_risks(sample_project.id, sample_project.owner_id, 0.7)
        
        # Assert
        assert len(result) == 1
        risk_service.risk_repo.get_high_risk_risks.assert_called_once_with(sample_project.id, 0.7)
    
    @pytest.mark.asyncio
    async def test_get_risk_analysis(self, risk_service, sample_project):
        """Testa obtenção de análise de riscos"""
        # Arrange
        risk_service.project_repo.get.return_value = sample_project
        risk_service.risk_repo.count_by_project.return_value = 10
        risk_service.risk_repo.count_by_priority.return_value = 3
        risk_service.risk_repo.count_by_status.return_value = 8
        risk_service.risk_repo.get_average_risk_score.return_value = 0.65
        risk_service.risk_repo.count_by_category.return_value = {"TECHNICAL": 5, "BUSINESS": 5}
        risk_service.risk_repo.count_by_status_all.return_value = {"ACTIVE": 8, "MITIGATED": 2}
        
        # Act
        result = await risk_service.get_risk_analysis(sample_project.id, sample_project.owner_id)
        
        # Assert
        assert result.total_risks == 10
        assert result.high_priority_risks == 3
        assert result.active_risks == 8
        assert result.average_risk_score == 0.65
        assert result.risks_by_category == {"TECHNICAL": 5, "BUSINESS": 5}
        assert result.risks_by_status == {"ACTIVE": 8, "MITIGATED": 2}
    
    @pytest.mark.asyncio
    async def test_get_risk_analysis_not_found(self, risk_service):
        """Testa obtenção de análise de riscos de projeto não encontrado"""
        # Arrange
        risk_service.project_repo.get.return_value = None
        
        # Act & Assert
        with pytest.raises(NotFoundError) as exc_info:
            await risk_service.get_risk_analysis(999, 1)
        
        assert "Projeto não encontrado" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_update_risk_status(self, risk_service, sample_risk, sample_project):
        """Testa atualização de status do risco"""
        # Arrange
        risk_service.risk_repo.get.return_value = sample_risk
        risk_service.project_repo.get.return_value = sample_project
        risk_service.risk_repo.update.return_value = sample_risk
        
        # Act
        result = await risk_service.update_risk_status(
            sample_risk.id, RiskStatus.MITIGATED, sample_project.owner_id
        )
        
        # Assert
        assert result == sample_risk
        risk_service.risk_repo.update.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_update_risk_priority(self, risk_service, sample_risk, sample_project):
        """Testa atualização de prioridade do risco"""
        # Arrange
        risk_service.risk_repo.get.return_value = sample_risk
        risk_service.project_repo.get.return_value = sample_project
        risk_service.risk_repo.update.return_value = sample_risk
        
        # Act
        result = await risk_service.update_risk_priority(
            sample_risk.id, RiskPriority.MEDIUM, sample_project.owner_id
        )
        
        # Assert
        assert result == sample_risk
        risk_service.risk_repo.update.assert_called_once()
