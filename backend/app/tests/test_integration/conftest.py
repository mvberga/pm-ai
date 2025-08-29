import pytest
from datetime import datetime, timezone

@pytest.fixture
def test_project_data():
    """Dados de teste para projetos"""
    return {
        "name": "Test Project",
        "description": "A test project for testing purposes",
        "municipio": "São Paulo",  # ✅ Campo obrigatório
        "entidade": "Prefeitura",  # ✅ Campo obrigatório
        "portfolio": "Test Portfolio",
        "vertical": "Technology",
        "product": "Software",
        "tipo": "implantacao",  # ✅ CORRIGIDO: minúsculo
        "data_inicio": "2024-01-01",
        "data_fim": "2024-12-31",
        "gerente_projeto_id": 1,  # ✅ NOVO: campo obrigatório
        "gerente_portfolio_id": 1  # ✅ NOVO: campo obrigatório
    }

@pytest.fixture
def test_user_data():
    """Dados de teste para usuários"""
    return {
        "email": "test@example.com",
        "id_token": "test_token_123",
        "name": "Test User"
    }


