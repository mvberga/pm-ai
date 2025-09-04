"""
Analytics router for advanced reporting and analysis endpoints.
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import Session, CurrentUser
from app.services.analytics_service import AnalyticsService

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
    responses={
        404: {"description": "Recurso não encontrado"},
        400: {"description": "Dados inválidos"},
        401: {"description": "Não autorizado"},
        403: {"description": "Sem permissão"},
        500: {"description": "Erro interno do servidor"}
    }
)

@router.get(
    "/portfolio/{portfolio_id}/dashboard",
    response_model=Dict[str, Any],
    summary="Dashboard do Portfólio",
    description="""
    Obtém dashboard completo de um portfólio com:
    - Estatísticas gerais
    - Projetos recentes
    - Riscos críticos
    - Tendências
    """
)
async def get_portfolio_dashboard(
    portfolio_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Obtém dashboard completo de um portfólio."""
    try:
        service = AnalyticsService(session)
        dashboard = await service.get_portfolio_dashboard(portfolio_id, current_user.id)
        return dashboard
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get(
    "/project/{project_id}/health-score",
    response_model=Dict[str, Any],
    summary="Score de Saúde do Projeto",
    description="""
    Calcula score de saúde de um projeto baseado em:
    - Cronograma
    - Orçamento
    - Riscos
    - Equipe
    - Cliente
    """
)
async def get_project_health_score(
    project_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Calcula score de saúde de um projeto."""
    try:
        service = AnalyticsService(session)
        health_score = await service.get_project_health_score(project_id, current_user.id)
        return health_score
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get(
    "/portfolio/{portfolio_id}/risk-heatmap",
    response_model=Dict[str, Any],
    summary="Mapa de Calor de Riscos",
    description="""
    Gera mapa de calor de riscos do portfólio com:
    - Distribuição por categoria
    - Pontuações de risco
    - Estatísticas por projeto
    """
)
async def get_risk_heatmap(
    portfolio_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Gera mapa de calor de riscos."""
    try:
        service = AnalyticsService(session)
        heatmap = await service.get_risk_heatmap(portfolio_id, current_user.id)
        return heatmap
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get(
    "/project/{project_id}/team-performance",
    response_model=Dict[str, Any],
    summary="Análise de Performance da Equipe",
    description="""
    Analisa performance da equipe com:
    - Métricas por função
    - Diversidade de roles
    - Status de atividade
    - Recomendações
    """
)
async def get_team_performance_analysis(
    project_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Analisa performance da equipe."""
    try:
        service = AnalyticsService(session)
        analysis = await service.get_team_performance_analysis(project_id, current_user.id)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get(
    "/project/{project_id}/client-satisfaction",
    response_model=Dict[str, Any],
    summary="Relatório de Satisfação do Cliente",
    description="""
    Gera relatório de satisfação do cliente com:
    - Métricas de satisfação
    - Análise por tipo de cliente
    - Níveis de comunicação
    - Recomendações
    """
)
async def get_client_satisfaction_report(
    project_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Gera relatório de satisfação do cliente."""
    try:
        service = AnalyticsService(session)
        report = await service.get_client_satisfaction_report(project_id, current_user.id)
        return report
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get(
    "/portfolio/{portfolio_id}/summary",
    response_model=Dict[str, Any],
    summary="Resumo Executivo do Portfólio",
    description="""
    Obtém resumo executivo do portfólio com:
    - Métricas consolidadas
    - Indicadores-chave
    - Alertas e recomendações
    """
)
async def get_portfolio_summary(
    portfolio_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Obtém resumo executivo do portfólio."""
    try:
        service = AnalyticsService(session)
        
        # Obter dados do dashboard
        dashboard = await service.get_portfolio_dashboard(portfolio_id, current_user.id)
        
        # Calcular métricas consolidadas
        total_projects = dashboard["statistics"]["total_projects"]
        active_projects = dashboard["statistics"]["active_projects"]
        critical_risks_count = len(dashboard["critical_risks"])
        
        # Calcular score médio de saúde dos projetos
        health_scores = []
        for project in dashboard["statistics"].get("projects", []):
            try:
                health_score = await service.get_project_health_score(project["id"], current_user.id)
                health_scores.append(health_score["overall_score"])
            except:
                continue
        
        avg_health_score = sum(health_scores) / len(health_scores) if health_scores else 0
        
        # Gerar alertas
        alerts = []
        if critical_risks_count > 5:
            alerts.append("Alto número de riscos críticos - requer atenção imediata")
        
        if avg_health_score < 60:
            alerts.append("Score médio de saúde dos projetos baixo")
        
        if active_projects / total_projects < 0.7:
            alerts.append("Baixa taxa de projetos ativos")
        
        return {
            "portfolio": dashboard["portfolio"],
            "key_metrics": {
                "total_projects": total_projects,
                "active_projects": active_projects,
                "inactive_projects": total_projects - active_projects,
                "critical_risks": critical_risks_count,
                "avg_health_score": round(avg_health_score, 2),
                "completion_rate": dashboard["trends"]["completion_rate"]
            },
            "alerts": alerts,
            "recommendations": [
                "Monitorar riscos críticos regularmente",
                "Revisar projetos com baixo score de saúde",
                "Implementar melhorias baseadas nas análises"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
