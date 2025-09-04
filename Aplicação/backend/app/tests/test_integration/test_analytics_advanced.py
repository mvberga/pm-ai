"""
Testes de integração avançados para endpoints de analytics.
"""

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.project import Project, ProjectStatus
from app.models.portfolio import Portfolio
from app.models.risk import Risk, RiskPriority
from app.models.team_member import TeamMember
from app.models.client import Client


class TestAnalyticsAdvanced:
    """Testes de integração avançados para analytics."""
    
    async def test_dashboard_overview_analytics(self, client: TestClient, db_session: AsyncSession):
        """Testar analytics do dashboard geral."""
        
        # Criar dados de teste para analytics
        await self._create_test_data_for_analytics(client, db_session)
        
        # Testar analytics do dashboard
        response = client.get(f"{settings.API_V1_STR}/analytics/dashboard")
        assert response.status_code == 200
        
        dashboard_data = response.json()
        
        # Verificar se todas as métricas estão presentes
        assert "projects" in dashboard_data
        assert "portfolios" in dashboard_data
        assert "risks" in dashboard_data
        assert "team" in dashboard_data
        assert "clients" in dashboard_data
        
        # Verificar estrutura dos dados de projetos
        projects_data = dashboard_data["projects"]
        assert "total" in projects_data
        assert "by_status" in projects_data
        assert "by_priority" in projects_data
        assert "budget_summary" in projects_data
        
        # Verificar estrutura dos dados de riscos
        risks_data = dashboard_data["risks"]
        assert "total" in risks_data
        assert "by_severity" in risks_data
        assert "by_status" in risks_data
        assert "trending_up" in risks_data
    
    async def test_project_analytics_detailed(self, client: TestClient, db_session: AsyncSession):
        """Testar analytics detalhados de projetos."""
        
        # Criar dados de teste
        await self._create_test_data_for_analytics(client, db_session)
        
        # Testar analytics de projetos
        response = client.get(f"{settings.API_V1_STR}/analytics/projects")
        assert response.status_code == 200
        
        projects_analytics = response.json()
        
        # Verificar métricas básicas
        assert "total_projects" in projects_analytics
        assert "active_projects" in projects_analytics
        assert "completed_projects" in projects_analytics
        assert "total_budget" in projects_analytics
        
        # Verificar distribuição por status
        assert "status_distribution" in projects_analytics
        status_dist = projects_analytics["status_distribution"]
        assert "active" in status_dist
        assert "completed" in status_dist
        assert "planning" in status_dist
        
        # Verificar distribuição por portfólio
        assert "portfolio_distribution" in projects_analytics
        
        # Verificar métricas de orçamento
        assert "budget_metrics" in projects_analytics
        budget_metrics = projects_analytics["budget_metrics"]
        assert "total_budget" in budget_metrics
        assert "average_budget" in budget_metrics
        assert "budget_variance" in budget_metrics
    
    async def test_risk_analytics_detailed(self, client: TestClient, db_session: AsyncSession):
        """Testar analytics detalhados de riscos."""
        
        # Criar dados de teste
        await self._create_test_data_for_analytics(client, db_session)
        
        # Testar analytics de riscos
        response = client.get(f"{settings.API_V1_STR}/analytics/risks")
        assert response.status_code == 200
        
        risks_analytics = response.json()
        
        # Verificar métricas básicas
        assert "total_risks" in risks_analytics
        assert "open_risks" in risks_analytics
        assert "mitigated_risks" in risks_analytics
        assert "closed_risks" in risks_analytics
        
        # Verificar distribuição por severidade
        assert "severity_distribution" in risks_analytics
        severity_dist = risks_analytics["severity_distribution"]
        assert "critical" in severity_dist
        assert "high" in severity_dist
        assert "medium" in severity_dist
        assert "low" in severity_dist
        
        # Verificar distribuição por categoria
        assert "category_distribution" in risks_analytics
        
        # Verificar métricas de tendência
        assert "trend_analysis" in risks_analytics
        trend = risks_analytics["trend_analysis"]
        assert "new_risks_this_month" in trend
        assert "resolved_risks_this_month" in trend
        assert "trend_direction" in trend
    
    async def test_team_analytics_detailed(self, client: TestClient, db_session: AsyncSession):
        """Testar analytics detalhados da equipe."""
        
        # Criar dados de teste
        await self._create_test_data_for_analytics(client, db_session)
        
        # Testar analytics da equipe
        response = client.get(f"{settings.API_V1_STR}/analytics/team")
        assert response.status_code == 200
        
        team_analytics = response.json()
        
        # Verificar métricas básicas
        assert "total_members" in team_analytics
        assert "active_members" in team_analytics
        assert "average_availability" in team_analytics
        assert "total_hourly_rate" in team_analytics
        
        # Verificar distribuição por role
        assert "role_distribution" in team_analytics
        role_dist = team_analytics["role_distribution"]
        assert "developer" in role_dist
        assert "project_manager" in role_dist
        assert "qa_analyst" in role_dist
        
        # Verificar métricas de carga de trabalho
        assert "workload_metrics" in team_analytics
        workload = team_analytics["workload_metrics"]
        assert "average_workload" in workload
        assert "overloaded_members" in workload
        assert "underutilized_members" in workload
        
        # Verificar distribuição de habilidades
        assert "skills_distribution" in team_analytics
    
    async def test_client_analytics_detailed(self, client: TestClient, db_session: AsyncSession):
        """Testar analytics detalhados de clientes."""
        
        # Criar dados de teste
        await self._create_test_data_for_analytics(client, db_session)
        
        # Testar analytics de clientes
        response = client.get(f"{settings.API_V1_STR}/analytics/clients")
        assert response.status_code == 200
        
        clients_analytics = response.json()
        
        # Verificar métricas básicas
        assert "total_clients" in clients_analytics
        assert "active_clients" in clients_analytics
        assert "inactive_clients" in clients_analytics
        
        # Verificar distribuição por tipo
        assert "type_distribution" in clients_analytics
        type_dist = clients_analytics["type_distribution"]
        assert "government" in type_dist
        assert "private" in type_dist
        assert "non_profit" in type_dist
        
        # Verificar distribuição por status
        assert "status_distribution" in clients_analytics
        
        # Verificar métricas de projetos por cliente
        assert "projects_per_client" in clients_analytics
        projects_per_client = clients_analytics["projects_per_client"]
        assert "average_projects" in projects_per_client
        assert "max_projects" in projects_per_client
        assert "min_projects" in projects_per_client
    
    async def test_portfolio_analytics_detailed(self, client: TestClient, db_session: AsyncSession):
        """Testar analytics detalhados de portfólios."""
        
        # Criar dados de teste
        await self._create_test_data_for_analytics(client, db_session)
        
        # Testar analytics de portfólios
        response = client.get(f"{settings.API_V1_STR}/analytics/portfolios")
        assert response.status_code == 200
        
        portfolios_analytics = response.json()
        
        # Verificar métricas básicas
        assert "total_portfolios" in portfolios_analytics
        assert "active_portfolios" in portfolios_analytics
        assert "total_budget" in portfolios_analytics
        
        # Verificar distribuição por status
        assert "status_distribution" in portfolios_analytics
        
        # Verificar métricas de projetos por portfólio
        assert "projects_per_portfolio" in portfolios_analytics
        
        # Verificar métricas de orçamento
        assert "budget_metrics" in portfolios_analytics
        budget_metrics = portfolios_analytics["budget_metrics"]
        assert "total_budget" in budget_metrics
        assert "average_budget" in budget_metrics
        assert "budget_utilization" in budget_metrics
    
    async def test_analytics_with_filters(self, client: TestClient, db_session: AsyncSession):
        """Testar analytics com filtros específicos."""
        
        # Criar dados de teste
        await self._create_test_data_for_analytics(client, db_session)
        
        # Testar analytics com filtro de data
        response = client.get(f"{settings.API_V1_STR}/analytics/projects?start_date=2024-01-01&end_date=2024-12-31")
        assert response.status_code == 200
        
        filtered_analytics = response.json()
        assert "total_projects" in filtered_analytics
        
        # Testar analytics com filtro de status
        response = client.get(f"{settings.API_V1_STR}/analytics/risks?status=open")
        assert response.status_code == 200
        
        open_risks_analytics = response.json()
        assert "total_risks" in open_risks_analytics
        
        # Testar analytics com filtro de severidade
        response = client.get(f"{settings.API_V1_STR}/analytics/risks?severity=high")
        assert response.status_code == 200
        
        high_risks_analytics = response.json()
        assert "total_risks" in high_risks_analytics
    
    async def test_analytics_export_functionality(self, client: TestClient, db_session: AsyncSession):
        """Testar funcionalidade de exportação de analytics."""
        
        # Criar dados de teste
        await self._create_test_data_for_analytics(client, db_session)
        
        # Testar exportação de relatório de projetos
        response = client.get(f"{settings.API_V1_STR}/analytics/projects/export?format=pdf")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        
        # Testar exportação de relatório de riscos
        response = client.get(f"{settings.API_V1_STR}/analytics/risks/export?format=excel")
        assert response.status_code == 200
        assert "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in response.headers["content-type"]
        
        # Testar exportação de dashboard completo
        response = client.get(f"{settings.API_V1_STR}/analytics/dashboard/export?format=pdf")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
    
    async def _create_test_data_for_analytics(self, client: TestClient, db_session: AsyncSession):
        """Criar dados de teste para analytics."""
        
        # Criar portfólio
        portfolio_data = {
            "name": "Portfólio de Teste Analytics",
            "description": "Portfólio para testes de analytics",
            "status": "active",
            "budget": 1000000.00
        }
        
        response = client.post(f"{settings.API_V1_STR}/portfolios", json=portfolio_data)
        assert response.status_code == 201
        portfolio = response.json()
        portfolio_id = portfolio["id"]
        
        # Criar cliente
        client_data = {
            "name": "Cliente para Analytics",
            "type": "government",
            "contact_person": "Analytics Test",
            "email": "analytics@cliente.gov.br",
            "phone": "+55 11 9999-9999",
            "cnpj": "99.999.999/0001-99",
            "status": "active"
        }
        
        response = client.post(f"{settings.API_V1_STR}/clients", json=client_data)
        assert response.status_code == 201
        created_client = response.json()
        client_id = created_client["id"]
        
        # Criar projetos
        projects_data = [
            {
                "name": "Projeto Ativo 1",
                "description": "Primeiro projeto ativo",
                "municipio": "São Paulo",
                "entidade": created_client["name"],
                "portfolio_id": portfolio_id,
                "status": "active",
                "budget": 300000.00
            },
            {
                "name": "Projeto Ativo 2",
                "description": "Segundo projeto ativo",
                "municipio": "Rio de Janeiro",
                "entidade": created_client["name"],
                "portfolio_id": portfolio_id,
                "status": "active",
                "budget": 200000.00
            },
            {
                "name": "Projeto Concluído",
                "description": "Projeto já concluído",
                "municipio": "Brasília",
                "entidade": created_client["name"],
                "portfolio_id": portfolio_id,
                "status": "completed",
                "budget": 150000.00
            }
        ]
        
        created_projects = []
        for project_data in projects_data:
            response = client.post(f"{settings.API_V1_STR}/projects", json=project_data)
            assert response.status_code == 201
            created_projects.append(response.json())
        
        # Criar riscos
        risks_data = [
            {
                "title": "Risco Crítico",
                "description": "Risco de alta severidade",
                "project_id": created_projects[0]["id"],
                "severity": "critical",
                "probability": 0.9,
                "impact": 0.9,
                "status": "open",
                "category": "technical"
            },
            {
                "title": "Risco Alto",
                "description": "Risco de severidade alta",
                "project_id": created_projects[1]["id"],
                "severity": "high",
                "probability": 0.7,
                "impact": 0.8,
                "status": "open",
                "category": "schedule"
            },
            {
                "title": "Risco Médio",
                "description": "Risco de severidade média",
                "project_id": created_projects[2]["id"],
                "severity": "medium",
                "probability": 0.5,
                "impact": 0.5,
                "status": "mitigated",
                "category": "budget"
            }
        ]
        
        for risk_data in risks_data:
            response = client.post(f"{settings.API_V1_STR}/risks", json=risk_data)
            assert response.status_code == 201
        
        # Criar membros da equipe
        team_members_data = [
            {
                "name": "Desenvolvedor 1",
                "email": "dev1@equipe.com",
                "role": "developer",
                "project_id": created_projects[0]["id"],
                "skills": ["Python", "FastAPI"],
                "availability": 0.8,
                "hourly_rate": 150.00
            },
            {
                "name": "Gerente de Projeto",
                "email": "gerente@equipe.com",
                "role": "project_manager",
                "project_id": created_projects[1]["id"],
                "skills": ["Gestão", "Planejamento"],
                "availability": 1.0,
                "hourly_rate": 200.00
            },
            {
                "name": "Analista QA",
                "email": "qa@equipe.com",
                "role": "qa_analyst",
                "project_id": created_projects[2]["id"],
                "skills": ["Testes", "Automação"],
                "availability": 0.7,
                "hourly_rate": 140.00
            }
        ]
        
        for member_data in team_members_data:
            response = client.post(f"{settings.API_V1_STR}/team-members", json=member_data)
            assert response.status_code == 201
