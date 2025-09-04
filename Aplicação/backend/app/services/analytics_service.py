"""
Service para análise e relatórios avançados
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload

from app.models.project import Project, ProjectStatus, ProjectType
from app.models.portfolio import Portfolio
from app.models.risk import Risk, RiskCategory, RiskStatus, RiskPriority
from app.models.team_member import TeamMember, TeamRole
from app.models.client import Client, ClientType
from app.repositories.project_repository import ProjectRepository
from app.repositories.portfolio_repository import PortfolioRepository
from app.repositories.risk_repository import RiskRepository
from app.repositories.team_member_repository import TeamMemberRepository
from app.repositories.client_repository import ClientRepository
from app.core.exceptions import NotFoundError


class AnalyticsService:
    """Service para análise e relatórios avançados"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.project_repo = ProjectRepository(db)
        self.portfolio_repo = PortfolioRepository(db)
        self.risk_repo = RiskRepository(db)
        self.team_member_repo = TeamMemberRepository(db)
        self.client_repo = ClientRepository(db)
    
    async def get_portfolio_dashboard(self, portfolio_id: int, user_id: int) -> Dict[str, Any]:
        """
        Obtém dashboard completo de um portfólio
        
        Args:
            portfolio_id: ID do portfólio
            user_id: ID do usuário
            
        Returns:
            Dados do dashboard
        """
        # Verificar se o portfólio existe e o usuário tem permissão
        portfolio = await self.portfolio_repo.get(portfolio_id)
        if not portfolio or portfolio.owner_id != user_id:
            raise NotFoundError("Portfólio não encontrado")
        
        # Obter estatísticas básicas
        stats = await self.portfolio_repo.get_portfolio_statistics(portfolio_id)
        
        # Obter projetos recentes
        recent_projects = await self._get_recent_projects(portfolio_id, limit=5)
        
        # Obter riscos críticos
        critical_risks = await self._get_critical_risks(portfolio_id)
        
        # Obter tendências
        trends = await self._get_portfolio_trends(portfolio_id)
        
        return {
            "portfolio": {
                "id": portfolio.id,
                "name": portfolio.name,
                "description": portfolio.description,
                "is_active": portfolio.is_active,
                "created_at": portfolio.created_at
            },
            "statistics": stats,
            "recent_projects": recent_projects,
            "critical_risks": critical_risks,
            "trends": trends
        }
    
    async def get_project_health_score(self, project_id: int, user_id: int) -> Dict[str, Any]:
        """
        Calcula score de saúde de um projeto
        
        Args:
            project_id: ID do projeto
            user_id: ID do usuário
            
        Returns:
            Score de saúde e métricas
        """
        # Verificar se o projeto existe e o usuário tem permissão
        project = await self.project_repo.get(project_id)
        if not project or project.owner_id != user_id:
            raise NotFoundError("Projeto não encontrado")
        
        # Calcular componentes do score
        schedule_score = await self._calculate_schedule_score(project)
        budget_score = await self._calculate_budget_score(project)
        risk_score = await self._calculate_risk_score(project_id)
        team_score = await self._calculate_team_score(project_id)
        client_score = await self._calculate_client_score(project_id)
        
        # Calcular score geral (média ponderada)
        overall_score = (
            schedule_score * 0.3 +
            budget_score * 0.25 +
            risk_score * 0.25 +
            team_score * 0.1 +
            client_score * 0.1
        )
        
        # Determinar status de saúde
        if overall_score >= 80:
            health_status = "excellent"
        elif overall_score >= 60:
            health_status = "good"
        elif overall_score >= 40:
            health_status = "warning"
        else:
            health_status = "critical"
        
        return {
            "project_id": project_id,
            "overall_score": round(overall_score, 2),
            "health_status": health_status,
            "components": {
                "schedule": round(schedule_score, 2),
                "budget": round(budget_score, 2),
                "risk": round(risk_score, 2),
                "team": round(team_score, 2),
                "client": round(client_score, 2)
            },
            "recommendations": await self._get_health_recommendations(
                overall_score, schedule_score, budget_score, risk_score, team_score, client_score
            )
        }
    
    async def get_risk_heatmap(self, portfolio_id: int, user_id: int) -> Dict[str, Any]:
        """
        Gera mapa de calor de riscos
        
        Args:
            portfolio_id: ID do portfólio
            user_id: ID do usuário
            
        Returns:
            Dados do mapa de calor
        """
        # Verificar se o portfólio existe e o usuário tem permissão
        portfolio = await self.portfolio_repo.get(portfolio_id)
        if not portfolio or portfolio.owner_id != user_id:
            raise NotFoundError("Portfólio não encontrado")
        
        # Obter projetos do portfólio
        projects = await self.portfolio_repo.get_projects(portfolio_id)
        
        heatmap_data = []
        for project in projects:
            # Obter riscos do projeto
            risks = await self.risk_repo.get_by_project(project.id)
            
            for risk in risks:
                risk_score = risk.probability * risk.impact
                heatmap_data.append({
                    "project_id": project.id,
                    "project_name": project.name,
                    "risk_id": risk.id,
                    "risk_title": risk.title,
                    "category": risk.category.value,
                    "probability": risk.probability,
                    "impact": risk.impact,
                    "risk_score": risk_score,
                    "priority": risk.priority.value,
                    "status": risk.status.value
                })
        
        # Agrupar por categoria e calcular médias
        category_stats = {}
        for item in heatmap_data:
            category = item["category"]
            if category not in category_stats:
                category_stats[category] = {
                    "count": 0,
                    "total_score": 0,
                    "avg_score": 0,
                    "high_risk_count": 0
                }
            
            category_stats[category]["count"] += 1
            category_stats[category]["total_score"] += item["risk_score"]
            
            if item["risk_score"] >= 0.7:
                category_stats[category]["high_risk_count"] += 1
        
        # Calcular médias
        for category, stats in category_stats.items():
            stats["avg_score"] = stats["total_score"] / stats["count"] if stats["count"] > 0 else 0
        
        return {
            "portfolio_id": portfolio_id,
            "portfolio_name": portfolio.name,
            "heatmap_data": heatmap_data,
            "category_stats": category_stats,
            "total_risks": len(heatmap_data),
            "high_risk_count": sum(1 for item in heatmap_data if item["risk_score"] >= 0.7)
        }
    
    async def get_team_performance_analysis(self, project_id: int, user_id: int) -> Dict[str, Any]:
        """
        Analisa performance da equipe
        
        Args:
            project_id: ID do projeto
            user_id: ID do usuário
            
        Returns:
            Análise de performance da equipe
        """
        # Verificar se o projeto existe e o usuário tem permissão
        project = await self.project_repo.get(project_id)
        if not project or project.owner_id != user_id:
            raise NotFoundError("Projeto não encontrado")
        
        # Obter membros da equipe
        team_members = await self.team_member_repo.get_by_project(project_id)
        
        # Analisar por função
        role_analysis = {}
        for member in team_members:
            role = member.role.value
            if role not in role_analysis:
                role_analysis[role] = {
                    "count": 0,
                    "active_count": 0,
                    "roles": []
                }
            
            role_analysis[role]["count"] += 1
            if member.is_active:
                role_analysis[role]["active_count"] += 1
            
            role_analysis[role]["roles"].append({
                "id": member.id,
                "name": member.name,
                "email": member.email,
                "is_active": member.is_active,
                "created_at": member.created_at
            })
        
        # Calcular métricas
        total_members = len(team_members)
        active_members = sum(1 for member in team_members if member.is_active)
        inactive_members = total_members - active_members
        
        # Diversidade de funções
        role_diversity = len(role_analysis)
        
        return {
            "project_id": project_id,
            "project_name": project.name,
            "team_metrics": {
                "total_members": total_members,
                "active_members": active_members,
                "inactive_members": inactive_members,
                "role_diversity": role_diversity,
                "active_percentage": (active_members / total_members * 100) if total_members > 0 else 0
            },
            "role_analysis": role_analysis,
            "recommendations": await self._get_team_recommendations(role_analysis, total_members, active_members)
        }
    
    async def get_client_satisfaction_report(self, project_id: int, user_id: int) -> Dict[str, Any]:
        """
        Gera relatório de satisfação do cliente
        
        Args:
            project_id: ID do projeto
            user_id: ID do usuário
            
        Returns:
            Relatório de satisfação
        """
        # Verificar se o projeto existe e o usuário tem permissão
        project = await self.project_repo.get(project_id)
        if not project or project.owner_id != user_id:
            raise NotFoundError("Projeto não encontrado")
        
        # Obter clientes do projeto
        clients = await self.client_repo.get_by_project(project_id)
        
        # Analisar por tipo de cliente
        type_analysis = {}
        communication_analysis = {}
        
        for client in clients:
            # Análise por tipo
            client_type = client.client_type.value
            if client_type not in type_analysis:
                type_analysis[client_type] = {
                    "count": 0,
                    "active_count": 0,
                    "avg_satisfaction": 0,
                    "satisfaction_scores": []
                }
            
            type_analysis[client_type]["count"] += 1
            if client.is_active:
                type_analysis[client_type]["active_count"] += 1
            
            if client.satisfaction_score:
                type_analysis[client_type]["satisfaction_scores"].append(client.satisfaction_score)
            
            # Análise por nível de comunicação
            comm_level = client.communication_level.value
            if comm_level not in communication_analysis:
                communication_analysis[comm_level] = {
                    "count": 0,
                    "active_count": 0
                }
            
            communication_analysis[comm_level]["count"] += 1
            if client.is_active:
                communication_analysis[comm_level]["active_count"] += 1
        
        # Calcular médias de satisfação
        for client_type, data in type_analysis.items():
            if data["satisfaction_scores"]:
                data["avg_satisfaction"] = sum(data["satisfaction_scores"]) / len(data["satisfaction_scores"])
            else:
                data["avg_satisfaction"] = 0
        
        # Calcular métricas gerais
        total_clients = len(clients)
        active_clients = sum(1 for client in clients if client.is_active)
        clients_with_satisfaction = sum(1 for client in clients if client.satisfaction_score)
        avg_satisfaction = 0
        
        if clients_with_satisfaction > 0:
            satisfaction_scores = [client.satisfaction_score for client in clients if client.satisfaction_score]
            avg_satisfaction = sum(satisfaction_scores) / len(satisfaction_scores)
        
        return {
            "project_id": project_id,
            "project_name": project.name,
            "client_metrics": {
                "total_clients": total_clients,
                "active_clients": active_clients,
                "clients_with_satisfaction": clients_with_satisfaction,
                "avg_satisfaction": round(avg_satisfaction, 2),
                "satisfaction_percentage": (clients_with_satisfaction / total_clients * 100) if total_clients > 0 else 0
            },
            "type_analysis": type_analysis,
            "communication_analysis": communication_analysis,
            "recommendations": await self._get_client_recommendations(avg_satisfaction, clients_with_satisfaction, total_clients)
        }
    
    # Métodos auxiliares privados
    
    async def _get_recent_projects(self, portfolio_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Obtém projetos recentes do portfólio"""
        projects = await self.portfolio_repo.get_projects(portfolio_id)
        recent_projects = sorted(projects, key=lambda p: p.updated_at, reverse=True)[:limit]
        
        return [
            {
                "id": project.id,
                "name": project.name,
                "status": project.status.value,
                "updated_at": project.updated_at,
                "progress": self._calculate_project_progress(project)
            }
            for project in recent_projects
        ]
    
    async def _get_critical_risks(self, portfolio_id: int) -> List[Dict[str, Any]]:
        """Obtém riscos críticos do portfólio"""
        projects = await self.portfolio_repo.get_projects(portfolio_id)
        critical_risks = []
        
        for project in projects:
            risks = await self.risk_repo.get_high_risk_risks(project.id, threshold=0.7)
            for risk in risks:
                critical_risks.append({
                    "id": risk.id,
                    "title": risk.title,
                    "project_id": project.id,
                    "project_name": project.name,
                    "risk_score": risk.probability * risk.impact,
                    "priority": risk.priority.value,
                    "status": risk.status.value
                })
        
        return sorted(critical_risks, key=lambda r: r["risk_score"], reverse=True)[:10]
    
    async def _get_portfolio_trends(self, portfolio_id: int) -> Dict[str, Any]:
        """Obtém tendências do portfólio"""
        projects = await self.portfolio_repo.get_projects(portfolio_id)
        
        # Projetos criados nos últimos 30 dias
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_projects = [p for p in projects if p.created_at >= thirty_days_ago]
        
        # Projetos concluídos nos últimos 30 dias
        completed_recent = [p for p in projects if p.status == ProjectStatus.COMPLETED and p.updated_at >= thirty_days_ago]
        
        return {
            "projects_created_30d": len(recent_projects),
            "projects_completed_30d": len(completed_recent),
            "completion_rate": len(completed_recent) / len(recent_projects) * 100 if recent_projects else 0
        }
    
    def _calculate_schedule_score(self, project: Project) -> float:
        """Calcula score de cronograma"""
        if not project.data_inicio or not project.data_fim:
            return 50.0
        
        now = datetime.now()
        total_duration = (project.data_fim - project.data_inicio).days
        elapsed = (now - project.data_inicio).days
        
        if total_duration <= 0:
            return 50.0
        
        progress = elapsed / total_duration
        
        # Score baseado no progresso vs status
        if project.status == ProjectStatus.COMPLETED:
            return 100.0
        elif project.status == ProjectStatus.ON_TRACK:
            return min(90.0, 50.0 + progress * 40)
        elif project.status == ProjectStatus.WARNING:
            return min(70.0, 30.0 + progress * 40)
        elif project.status == ProjectStatus.DELAYED:
            return max(10.0, 50.0 - (progress - 1.0) * 40)
        else:
            return 50.0
    
    def _calculate_budget_score(self, project: Project) -> float:
        """Calcula score de orçamento"""
        if project.valor_implantacao <= 0:
            return 50.0
        
        # Score baseado no valor vs recursos
        if project.recursos <= 0:
            return 50.0
        
        # Razão valor/recursos (simplificado)
        ratio = project.valor_implantacao / project.recursos
        
        if ratio > 1000:
            return 90.0
        elif ratio > 500:
            return 80.0
        elif ratio > 100:
            return 70.0
        else:
            return 60.0
    
    async def _calculate_risk_score(self, project_id: int) -> float:
        """Calcula score de risco"""
        risks = await self.risk_repo.get_by_project(project_id)
        
        if not risks:
            return 100.0
        
        # Score baseado na média dos riscos
        total_risk_score = sum(risk.probability * risk.impact for risk in risks)
        avg_risk_score = total_risk_score / len(risks)
        
        # Converter para score (0-100, onde 100 é sem risco)
        return max(0.0, 100.0 - avg_risk_score * 100)
    
    async def _calculate_team_score(self, project_id: int) -> float:
        """Calcula score da equipe"""
        team_members = await self.team_member_repo.get_by_project(project_id)
        
        if not team_members:
            return 0.0
        
        active_members = sum(1 for member in team_members if member.is_active)
        return (active_members / len(team_members)) * 100
    
    async def _calculate_client_score(self, project_id: int) -> float:
        """Calcula score do cliente"""
        clients = await self.client_repo.get_by_project(project_id)
        
        if not clients:
            return 50.0
        
        active_clients = sum(1 for client in clients if client.is_active)
        clients_with_satisfaction = [client for client in clients if client.satisfaction_score]
        
        if not clients_with_satisfaction:
            return (active_clients / len(clients)) * 100
        
        avg_satisfaction = sum(client.satisfaction_score for client in clients_with_satisfaction) / len(clients_with_satisfaction)
        return avg_satisfaction * 10  # Converter de 1-10 para 0-100
    
    def _calculate_project_progress(self, project: Project) -> float:
        """Calcula progresso do projeto"""
        if not project.data_inicio or not project.data_fim:
            return 0.0
        
        now = datetime.now()
        total_duration = (project.data_fim - project.data_inicio).days
        elapsed = (now - project.data_inicio).days
        
        if total_duration <= 0:
            return 0.0
        
        progress = elapsed / total_duration
        
        # Ajustar baseado no status
        if project.status == ProjectStatus.COMPLETED:
            return 100.0
        elif project.status == ProjectStatus.ON_TRACK:
            return min(100.0, progress * 100)
        elif project.status == ProjectStatus.WARNING:
            return min(90.0, progress * 100)
        elif project.status == ProjectStatus.DELAYED:
            return min(80.0, progress * 100)
        else:
            return progress * 100
    
    async def _get_health_recommendations(self, overall_score: float, schedule_score: float, 
                                        budget_score: float, risk_score: float, 
                                        team_score: float, client_score: float) -> List[str]:
        """Gera recomendações baseadas no score de saúde"""
        recommendations = []
        
        if overall_score < 60:
            recommendations.append("Projeto em situação crítica - requer atenção imediata")
        
        if schedule_score < 50:
            recommendations.append("Cronograma atrasado - revisar prazos e recursos")
        
        if budget_score < 50:
            recommendations.append("Orçamento comprometido - revisar custos e recursos")
        
        if risk_score < 50:
            recommendations.append("Alto nível de risco - implementar planos de mitigação")
        
        if team_score < 70:
            recommendations.append("Equipe com problemas - revisar alocação e capacitação")
        
        if client_score < 70:
            recommendations.append("Satisfação do cliente baixa - melhorar comunicação")
        
        if not recommendations:
            recommendations.append("Projeto em boa situação - manter monitoramento")
        
        return recommendations
    
    async def _get_team_recommendations(self, role_analysis: Dict, total_members: int, active_members: int) -> List[str]:
        """Gera recomendações para a equipe"""
        recommendations = []
        
        if total_members < 3:
            recommendations.append("Equipe pequena - considerar adicionar mais membros")
        
        if active_members / total_members < 0.8:
            recommendations.append("Muitos membros inativos - revisar alocação")
        
        if len(role_analysis) < 3:
            recommendations.append("Baixa diversidade de funções - considerar especialistas")
        
        if not recommendations:
            recommendations.append("Equipe bem estruturada - manter composição atual")
        
        return recommendations
    
    async def _get_client_recommendations(self, avg_satisfaction: float, clients_with_satisfaction: int, total_clients: int) -> List[str]:
        """Gera recomendações para clientes"""
        recommendations = []
        
        if avg_satisfaction < 7:
            recommendations.append("Satisfação baixa - melhorar comunicação e entregas")
        
        if clients_with_satisfaction / total_clients < 0.5:
            recommendations.append("Poucos clientes com avaliação - implementar feedback regular")
        
        if not recommendations:
            recommendations.append("Clientes satisfeitos - manter qualidade atual")
        
        return recommendations
