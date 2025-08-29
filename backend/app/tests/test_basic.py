import pytest
from app.schemas.project import ProjectType, ProjectStatus

class TestBasicValidation:
    """Testes básicos para validar a infraestrutura"""
    
    def test_project_type_enum(self):
        """Testa se os enums estão funcionando"""
        assert ProjectType.IMPLANTACAO == "implantacao"
        assert ProjectType.MIGRACAO == "migracao"
        assert ProjectType.CONFIGURACAO == "configuracao"
        assert ProjectType.TREINAMENTO == "treinamento"
        assert ProjectType.SUPORTE == "suporte"
    
    def test_project_status_enum(self):
        """Testa se os enums de status estão funcionando"""
        assert ProjectStatus.NOT_STARTED == "not_started"
        assert ProjectStatus.ON_TRACK == "on_track"
        assert ProjectStatus.WARNING == "warning"
        assert ProjectStatus.DELAYED == "delayed"
        assert ProjectStatus.COMPLETED == "completed"
    
    def test_simple_math(self):
        """Teste simples de matemática para validar pytest"""
        assert 2 + 2 == 4
        assert 3 * 3 == 9
        assert 10 / 2 == 5
