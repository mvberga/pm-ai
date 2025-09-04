"""
Testes de integração avançados para endpoints de riscos.
"""

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.risk import Risk, RiskStatus, RiskPriority
from app.models.project import Project
from app.models.user import User


class TestRisksAdvanced:
    """Testes de integração avançados para riscos."""
    
    async def test_create_risk_complete_flow(self, client: TestClient, db_session: AsyncSession):
        """Testar fluxo completo de criação de risco."""
        
        # Primeiro criar um projeto para associar o risco
        project_data = {
            "name": "Projeto para Risco",
            "description": "Projeto para testar riscos",
            "municipio": "São Paulo",
            "entidade": "Prefeitura",
            "status": "active"
        }
        
        response = client.post(f"{settings.API_V1_STR}/projects", json=project_data)
        assert response.status_code == 201
        project = response.json()
        project_id = project["id"]
        
        # Dados do risco
        risk_data = {
            "title": "Risco de Atraso no Projeto",
            "description": "Possível atraso na entrega do projeto devido a problemas técnicos",
            "project_id": project_id,
            "severity": "high",
            "probability": 0.7,
            "impact": 0.8,
            "status": "open",
            "category": "technical",
            "owner_id": 1,
            "mitigation_plan": "Implementar revisões técnicas mais frequentes",
            "contingency_plan": "Contratar consultor externo se necessário"
        }
        
        # Criar risco
        response = client.post(f"{settings.API_V1_STR}/risks", json=risk_data)
        assert response.status_code == 201
        
        risk = response.json()
        assert risk["title"] == risk_data["title"]
        assert risk["description"] == risk_data["description"]
        assert risk["project_id"] == project_id
        assert risk["severity"] == risk_data["severity"]
        assert risk["probability"] == risk_data["probability"]
        assert risk["impact"] == risk_data["impact"]
        assert risk["status"] == risk_data["status"]
        
        risk_id = risk["id"]
        
        # Verificar se o risco foi criado no banco
        from sqlalchemy import select
        result = await db_session.execute(select(Risk).where(Risk.id == risk_id))
        db_risk = result.scalar_one_or_none()
        assert db_risk is not None
        assert db_risk.title == risk_data["title"]
    
    async def test_risk_calculation_and_prioritization(self, client: TestClient, db_session: AsyncSession):
        """Testar cálculo de prioridade e classificação de riscos."""
        
        # Criar projeto
        project_data = {
            "name": "Projeto para Priorização",
            "description": "Projeto para testar priorização de riscos",
            "municipio": "São Paulo",
            "entidade": "Prefeitura",
            "status": "active"
        }
        
        response = client.post(f"{settings.API_V1_STR}/projects", json=project_data)
        assert response.status_code == 201
        project = response.json()
        project_id = project["id"]
        
        # Criar riscos com diferentes níveis de severidade
        risks_data = [
            {
                "title": "Risco Crítico",
                "description": "Risco de alta severidade",
                "project_id": project_id,
                "severity": "critical",
                "probability": 0.9,
                "impact": 0.9,
                "status": "open",
                "category": "technical"
            },
            {
                "title": "Risco Médio",
                "description": "Risco de média severidade", 
                "project_id": project_id,
                "severity": "medium",
                "probability": 0.5,
                "impact": 0.5,
                "status": "open",
                "category": "schedule"
            },
            {
                "title": "Risco Baixo",
                "description": "Risco de baixa severidade",
                "project_id": project_id,
                "severity": "low",
                "probability": 0.2,
                "impact": 0.3,
                "status": "open",
                "category": "budget"
            }
        ]
        
        created_risks = []
        for risk_data in risks_data:
            response = client.post(f"{settings.API_V1_STR}/risks", json=risk_data)
            assert response.status_code == 201
            created_risks.append(response.json())
        
        # Testar listagem de riscos por prioridade
        response = client.get(f"{settings.API_V1_STR}/risks?project_id={project_id}&sort_by=priority")
        assert response.status_code == 200
        
        risks = response.json()
        assert len(risks) == 3
        
        # Verificar se os riscos estão ordenados por prioridade (crítico primeiro)
        assert risks[0]["severity"] == "critical"
    
    async def test_risk_status_workflow(self, client: TestClient, db_session: AsyncSession):
        """Testar fluxo de mudança de status de risco."""
        
        # Criar projeto
        project_data = {
            "name": "Projeto para Workflow",
            "description": "Projeto para testar workflow de riscos",
            "municipio": "São Paulo",
            "entidade": "Prefeitura",
            "status": "active"
        }
        
        response = client.post(f"{settings.API_V1_STR}/projects", json=project_data)
        assert response.status_code == 201
        project = response.json()
        project_id = project["id"]
        
        # Criar risco
        risk_data = {
            "title": "Risco para Workflow",
            "description": "Risco para testar mudanças de status",
            "project_id": project_id,
            "severity": "medium",
            "probability": 0.6,
            "impact": 0.7,
            "status": "open",
            "category": "technical"
        }
        
        response = client.post(f"{settings.API_V1_STR}/risks", json=risk_data)
        assert response.status_code == 201
        risk = response.json()
        risk_id = risk["id"]
        
        # Mudar status para "in_progress"
        response = client.post(f"{settings.API_V1_STR}/risks/{risk_id}/update-status?status=in_progress")
        assert response.status_code == 200
        
        updated_risk = response.json()
        assert updated_risk["status"] == "in_progress"
        
        # Mudar status para "mitigated"
        response = client.post(f"{settings.API_V1_STR}/risks/{risk_id}/update-status?status=mitigated")
        assert response.status_code == 200
        
        updated_risk = response.json()
        assert updated_risk["status"] == "mitigated"
        
        # Mudar status para "closed"
        response = client.post(f"{settings.API_V1_STR}/risks/{risk_id}/update-status?status=closed")
        assert response.status_code == 200
        
        updated_risk = response.json()
        assert updated_risk["status"] == "closed"
    
    async def test_risk_review_scheduling(self, client: TestClient, db_session: AsyncSession):
        """Testar agendamento de revisões de risco."""
        
        # Criar projeto
        project_data = {
            "name": "Projeto para Revisão",
            "description": "Projeto para testar agendamento de revisões",
            "municipio": "São Paulo",
            "entidade": "Prefeitura",
            "status": "active"
        }
        
        response = client.post(f"{settings.API_V1_STR}/projects", json=project_data)
        assert response.status_code == 201
        project = response.json()
        project_id = project["id"]
        
        # Criar risco
        risk_data = {
            "title": "Risco para Revisão",
            "description": "Risco que precisa de revisão agendada",
            "project_id": project_id,
            "severity": "high",
            "probability": 0.8,
            "impact": 0.7,
            "status": "open",
            "category": "technical"
        }
        
        response = client.post(f"{settings.API_V1_STR}/risks", json=risk_data)
        assert response.status_code == 201
        risk = response.json()
        risk_id = risk["id"]
        
        # Agendar revisão
        review_data = {
            "review_date": "2024-02-15",
            "reviewer_id": 1,
            "notes": "Revisão agendada para avaliar progresso da mitigação"
        }
        
        response = client.post(f"{settings.API_V1_STR}/risks/{risk_id}/schedule-review", json=review_data)
        assert response.status_code == 200
        
        updated_risk = response.json()
        assert "next_review_date" in updated_risk
        assert updated_risk["next_review_date"] == review_data["review_date"]
    
    async def test_risk_analytics_and_reporting(self, client: TestClient, db_session: AsyncSession):
        """Testar analytics e relatórios de riscos."""
        
        # Criar projeto
        project_data = {
            "name": "Projeto para Analytics",
            "description": "Projeto para testar analytics de riscos",
            "municipio": "São Paulo",
            "entidade": "Prefeitura",
            "status": "active"
        }
        
        response = client.post(f"{settings.API_V1_STR}/projects", json=project_data)
        assert response.status_code == 201
        project = response.json()
        project_id = project["id"]
        
        # Criar múltiplos riscos para analytics
        risks_data = [
            {
                "title": "Risco Técnico 1",
                "description": "Primeiro risco técnico",
                "project_id": project_id,
                "severity": "high",
                "probability": 0.7,
                "impact": 0.8,
                "status": "open",
                "category": "technical"
            },
            {
                "title": "Risco de Cronograma",
                "description": "Risco de atraso no cronograma",
                "project_id": project_id,
                "severity": "medium",
                "probability": 0.6,
                "impact": 0.5,
                "status": "in_progress",
                "category": "schedule"
            },
            {
                "title": "Risco Orçamentário",
                "description": "Risco de estouro de orçamento",
                "project_id": project_id,
                "severity": "low",
                "probability": 0.3,
                "impact": 0.4,
                "status": "mitigated",
                "category": "budget"
            }
        ]
        
        for risk_data in risks_data:
            response = client.post(f"{settings.API_V1_STR}/risks", json=risk_data)
            assert response.status_code == 201
        
        # Testar analytics de riscos
        response = client.get(f"{settings.API_V1_STR}/risks/analytics?project_id={project_id}")
        assert response.status_code == 200
        
        analytics = response.json()
        assert "total_risks" in analytics
        assert "risks_by_severity" in analytics
        assert "risks_by_status" in analytics
        assert "risks_by_category" in analytics
        
        # Verificar se os dados estão corretos
        assert analytics["total_risks"] == 3
        assert analytics["risks_by_severity"]["high"] == 1
        assert analytics["risks_by_severity"]["medium"] == 1
        assert analytics["risks_by_severity"]["low"] == 1
    
    async def test_risk_validation_errors(self, client: TestClient, db_session: AsyncSession):
        """Testar validação de dados de risco."""
        
        # Testar dados inválidos
        invalid_data = {
            "title": "",  # Título vazio
            "description": "Descrição válida",
            "severity": "invalid_severity",  # Severidade inválida
            "probability": 1.5,  # Probabilidade > 1
            "impact": -0.1  # Impacto negativo
        }
        
        response = client.post(f"{settings.API_V1_STR}/risks", json=invalid_data)
        assert response.status_code == 422  # Validation Error
        
        # Testar dados obrigatórios faltando
        incomplete_data = {
            "description": "Apenas descrição"
        }
        
        response = client.post(f"{settings.API_V1_STR}/risks", json=incomplete_data)
        assert response.status_code == 422  # Validation Error
    
    async def test_risk_not_found(self, client: TestClient, db_session: AsyncSession):
        """Testar cenários de risco não encontrado."""
        
        # Tentar buscar risco inexistente
        response = client.get(f"{settings.API_V1_STR}/risks/99999")
        assert response.status_code == 404
        
        # Tentar atualizar risco inexistente
        update_data = {"title": "Título Atualizado"}
        response = client.put(f"{settings.API_V1_STR}/risks/99999", json=update_data)
        assert response.status_code == 404
        
        # Tentar excluir risco inexistente
        response = client.delete(f"{settings.API_V1_STR}/risks/99999")
        assert response.status_code == 404
