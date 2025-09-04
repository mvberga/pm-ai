"""
Query optimization system for database performance.
"""

from typing import List, Dict, Any, Optional, Union
import logging
from datetime import datetime, timedelta
from sqlalchemy import text, select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.sql import Select

logger = logging.getLogger(__name__)

class QueryOptimizer:
    """Query optimization system for database performance."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.query_stats = {
            'total_queries': 0,
            'slow_queries': 0,
            'optimized_queries': 0,
            'cache_hits': 0,
            'cache_misses': 0
        }
        self.slow_query_threshold = 1.0  # seconds
    
    async def optimize_project_query(
        self, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Optimized query for fetching user projects with eager loading.
        
        Args:
            user_id: ID do usuário
            skip: Número de registros para pular
            limit: Número máximo de registros
            filters: Filtros opcionais
            
        Returns:
            Lista de projetos otimizada
        """
        start_time = datetime.now()
        
        try:
            # Build optimized query with eager loading
            query = select(Project).options(
                selectinload(Project.gerente_projeto),
                selectinload(Project.gerente_portfolio),
                selectinload(Project.owner),
                selectinload(Project.portfolio)
            ).where(Project.owner_id == user_id)
            
            # Apply filters
            if filters:
                if filters.get('status'):
                    query = query.where(Project.status == filters['status'])
                if filters.get('portfolio'):
                    query = query.where(Project.portfolio.has(name=filters['portfolio']))
                if filters.get('municipio'):
                    query = query.where(Project.municipio.ilike(f"%{filters['municipio']}%"))
                if filters.get('search'):
                    search_term = f"%{filters['search']}%"
                    query = query.where(
                        or_(
                            Project.name.ilike(search_term),
                            Project.description.ilike(search_term)
                        )
                    )
            
            # Apply pagination
            query = query.offset(skip).limit(limit)
            
            # Execute query
            result = await self.session.execute(query)
            projects = result.scalars().all()
            
            # Convert to dict format
            optimized_projects = []
            for project in projects:
                project_dict = {
                    'id': project.id,
                    'name': project.name,
                    'description': project.description,
                    'municipio': project.municipio,
                    'entidade': project.entidade,
                    'status': project.status.value,
                    'tipo': project.tipo.value,
                    'data_inicio': project.data_inicio,
                    'data_fim': project.data_fim,
                    'valor_implantacao': project.valor_implantacao,
                    'valor_recorrente': project.valor_recorrente,
                    'recursos': project.recursos,
                    'gerente_projeto': {
                        'id': project.gerente_projeto.id,
                        'name': project.gerente_projeto.full_name,
                        'email': project.gerente_projeto.email
                    } if project.gerente_projeto else None,
                    'gerente_portfolio': {
                        'id': project.gerente_portfolio.id,
                        'name': project.gerente_portfolio.full_name,
                        'email': project.gerente_portfolio.email
                    } if project.gerente_portfolio else None,
                    'portfolio': {
                        'id': project.portfolio.id,
                        'name': project.portfolio.name
                    } if project.portfolio else None,
                    'created_at': project.created_at,
                    'updated_at': project.updated_at
                }
                optimized_projects.append(project_dict)
            
            # Track performance
            execution_time = (datetime.now() - start_time).total_seconds()
            self._track_query_performance('optimized_project_query', execution_time)
            
            return optimized_projects
            
        except Exception as e:
            logger.error(f"Error in optimized project query: {str(e)}")
            raise
    
    async def optimize_portfolio_with_projects_query(
        self, 
        portfolio_id: int, 
        user_id: int
    ) -> Optional[Dict[str, Any]]:
        """
        Optimized query for fetching portfolio with projects.
        
        Args:
            portfolio_id: ID do portfólio
            user_id: ID do usuário
            
        Returns:
            Portfólio com projetos ou None
        """
        start_time = datetime.now()
        
        try:
            # Build optimized query with eager loading
            query = select(Portfolio).options(
                selectinload(Portfolio.projects).selectinload(Project.gerente_projeto),
                selectinload(Portfolio.projects).selectinload(Project.gerente_portfolio),
                selectinload(Portfolio.owner)
            ).where(
                and_(
                    Portfolio.id == portfolio_id,
                    Portfolio.owner_id == user_id
                )
            )
            
            result = await self.session.execute(query)
            portfolio = result.scalar_one_or_none()
            
            if not portfolio:
                return None
            
            # Convert to dict format
            portfolio_dict = {
                'id': portfolio.id,
                'name': portfolio.name,
                'description': portfolio.description,
                'is_active': portfolio.is_active,
                'owner': {
                    'id': portfolio.owner.id,
                    'name': portfolio.owner.full_name,
                    'email': portfolio.owner.email
                },
                'projects': [
                    {
                        'id': project.id,
                        'name': project.name,
                        'status': project.status.value,
                        'municipio': project.municipio,
                        'data_inicio': project.data_inicio,
                        'data_fim': project.data_fim,
                        'gerente_projeto': {
                            'id': project.gerente_projeto.id,
                            'name': project.gerente_projeto.full_name
                        } if project.gerente_projeto else None
                    }
                    for project in portfolio.projects
                ],
                'created_at': portfolio.created_at,
                'updated_at': portfolio.updated_at
            }
            
            # Track performance
            execution_time = (datetime.now() - start_time).total_seconds()
            self._track_query_performance('optimized_portfolio_with_projects', execution_time)
            
            return portfolio_dict
            
        except Exception as e:
            logger.error(f"Error in optimized portfolio query: {str(e)}")
            raise
    
    async def optimize_risk_analysis_query(
        self, 
        project_id: int, 
        user_id: int
    ) -> Dict[str, Any]:
        """
        Optimized query for risk analysis with aggregated data.
        
        Args:
            project_id: ID do projeto
            user_id: ID do usuário
            
        Returns:
            Análise de riscos otimizada
        """
        start_time = datetime.now()
        
        try:
            # Verify user has access to project
            project_query = select(Project).where(
                and_(
                    Project.id == project_id,
                    Project.owner_id == user_id
                )
            )
            project_result = await self.session.execute(project_query)
            project = project_result.scalar_one_or_none()
            
            if not project:
                raise ValueError("Project not found or access denied")
            
            # Build optimized aggregation query
            risk_stats_query = select(
                func.count(Risk.id).label('total_risks'),
                func.avg(Risk.probability * Risk.impact).label('avg_risk_score'),
                func.count(func.case(
                    (Risk.priority == 'high', 1),
                    (Risk.priority == 'critical', 1)
                )).label('high_priority_risks'),
                func.count(func.case(
                    (Risk.status == 'identified', 1),
                    (Risk.status == 'assessed', 1)
                )).label('active_risks')
            ).where(Risk.project_id == project_id)
            
            result = await self.session.execute(risk_stats_query)
            stats = result.fetchone()
            
            # Get risks by category
            category_query = select(
                Risk.category,
                func.count(Risk.id).label('count'),
                func.avg(Risk.probability * Risk.impact).label('avg_score')
            ).where(Risk.project_id == project_id).group_by(Risk.category)
            
            category_result = await self.session.execute(category_query)
            risks_by_category = {
                row.category.value: {
                    'count': row.count,
                    'avg_score': float(row.avg_score or 0)
                }
                for row in category_result.fetchall()
            }
            
            # Get risks by status
            status_query = select(
                Risk.status,
                func.count(Risk.id).label('count')
            ).where(Risk.project_id == project_id).group_by(Risk.status)
            
            status_result = await self.session.execute(status_query)
            risks_by_status = {
                row.status.value: row.count
                for row in status_result.fetchall()
            }
            
            # Get high-risk risks
            high_risk_query = select(Risk).where(
                and_(
                    Risk.project_id == project_id,
                    (Risk.probability * Risk.impact) >= 0.7
                )
            ).order_by((Risk.probability * Risk.impact).desc()).limit(10)
            
            high_risk_result = await self.session.execute(high_risk_query)
            high_risk_risks = [
                {
                    'id': risk.id,
                    'title': risk.title,
                    'category': risk.category.value,
                    'priority': risk.priority.value,
                    'risk_score': risk.probability * risk.impact
                }
                for risk in high_risk_result.scalars().all()
            ]
            
            analysis = {
                'project_id': project_id,
                'total_risks': stats.total_risks or 0,
                'avg_risk_score': float(stats.avg_risk_score or 0),
                'high_priority_risks': stats.high_priority_risks or 0,
                'active_risks': stats.active_risks or 0,
                'risks_by_category': risks_by_category,
                'risks_by_status': risks_by_status,
                'high_risk_risks': high_risk_risks
            }
            
            # Track performance
            execution_time = (datetime.now() - start_time).total_seconds()
            self._track_query_performance('optimized_risk_analysis', execution_time)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in optimized risk analysis query: {str(e)}")
            raise
    
    async def optimize_team_performance_query(
        self, 
        project_id: int, 
        user_id: int
    ) -> Dict[str, Any]:
        """
        Optimized query for team performance analysis.
        
        Args:
            project_id: ID do projeto
            user_id: ID do usuário
            
        Returns:
            Análise de performance da equipe
        """
        start_time = datetime.now()
        
        try:
            # Verify user has access to project
            project_query = select(Project).where(
                and_(
                    Project.id == project_id,
                    Project.owner_id == user_id
                )
            )
            project_result = await self.session.execute(project_query)
            project = project_result.scalar_one_or_none()
            
            if not project:
                raise ValueError("Project not found or access denied")
            
            # Build optimized team analysis query
            team_stats_query = select(
                TeamMember.role,
                func.count(TeamMember.id).label('total_count'),
                func.count(func.case(
                    (TeamMember.is_active == True, 1)
                )).label('active_count')
            ).where(TeamMember.project_id == project_id).group_by(TeamMember.role)
            
            result = await self.session.execute(team_stats_query)
            role_analysis = {}
            
            for row in result.fetchall():
                role_analysis[row.role.value] = {
                    'total_count': row.total_count,
                    'active_count': row.active_count,
                    'inactive_count': row.total_count - row.active_count
                }
            
            # Get total team metrics
            total_query = select(
                func.count(TeamMember.id).label('total_members'),
                func.count(func.case(
                    (TeamMember.is_active == True, 1)
                )).label('active_members')
            ).where(TeamMember.project_id == project_id)
            
            total_result = await self.session.execute(total_query)
            total_stats = total_result.fetchone()
            
            total_members = total_stats.total_members or 0
            active_members = total_stats.active_members or 0
            
            analysis = {
                'project_id': project_id,
                'project_name': project.name,
                'team_metrics': {
                    'total_members': total_members,
                    'active_members': active_members,
                    'inactive_members': total_members - active_members,
                    'role_diversity': len(role_analysis),
                    'active_percentage': (active_members / total_members * 100) if total_members > 0 else 0
                },
                'role_analysis': role_analysis
            }
            
            # Track performance
            execution_time = (datetime.now() - start_time).total_seconds()
            self._track_query_performance('optimized_team_performance', execution_time)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in optimized team performance query: {str(e)}")
            raise
    
    async def optimize_dashboard_query(
        self, 
        portfolio_id: int, 
        user_id: int
    ) -> Dict[str, Any]:
        """
        Optimized query for portfolio dashboard with all related data.
        
        Args:
            portfolio_id: ID do portfólio
            user_id: ID do usuário
            
        Returns:
            Dashboard data otimizado
        """
        start_time = datetime.now()
        
        try:
            # Build comprehensive dashboard query with multiple CTEs
            dashboard_query = text("""
                WITH portfolio_stats AS (
                    SELECT 
                        p.id,
                        p.name,
                        p.description,
                        p.is_active,
                        p.created_at,
                        COUNT(pr.id) as total_projects,
                        COUNT(CASE WHEN pr.status IN ('on_track', 'warning', 'delayed') THEN 1 END) as active_projects
                    FROM portfolios p
                    LEFT JOIN projects pr ON p.id = pr.portfolio_id
                    WHERE p.id = :portfolio_id AND p.owner_id = :user_id
                    GROUP BY p.id, p.name, p.description, p.is_active, p.created_at
                ),
                recent_projects AS (
                    SELECT 
                        pr.id,
                        pr.name,
                        pr.status,
                        pr.updated_at,
                        pr.municipio
                    FROM projects pr
                    WHERE pr.portfolio_id = :portfolio_id
                    ORDER BY pr.updated_at DESC
                    LIMIT 5
                ),
                critical_risks AS (
                    SELECT 
                        r.id,
                        r.title,
                        r.project_id,
                        pr.name as project_name,
                        (r.probability * r.impact) as risk_score,
                        r.priority,
                        r.status
                    FROM risks r
                    JOIN projects pr ON r.project_id = pr.id
                    WHERE pr.portfolio_id = :portfolio_id
                    AND (r.probability * r.impact) >= 0.7
                    ORDER BY risk_score DESC
                    LIMIT 10
                )
                SELECT 
                    ps.*,
                    COALESCE(
                        json_agg(
                            json_build_object(
                                'id', rp.id,
                                'name', rp.name,
                                'status', rp.status,
                                'updated_at', rp.updated_at,
                                'municipio', rp.municipio
                            )
                        ) FILTER (WHERE rp.id IS NOT NULL),
                        '[]'::json
                    ) as recent_projects,
                    COALESCE(
                        json_agg(
                            json_build_object(
                                'id', cr.id,
                                'title', cr.title,
                                'project_id', cr.project_id,
                                'project_name', cr.project_name,
                                'risk_score', cr.risk_score,
                                'priority', cr.priority,
                                'status', cr.status
                            )
                        ) FILTER (WHERE cr.id IS NOT NULL),
                        '[]'::json
                    ) as critical_risks
                FROM portfolio_stats ps
                LEFT JOIN recent_projects rp ON true
                LEFT JOIN critical_risks cr ON true
                GROUP BY ps.id, ps.name, ps.description, ps.is_active, ps.created_at, ps.total_projects, ps.active_projects
            """)
            
            result = await self.session.execute(
                dashboard_query, 
                {"portfolio_id": portfolio_id, "user_id": user_id}
            )
            dashboard_data = result.fetchone()
            
            if not dashboard_data:
                raise ValueError("Portfolio not found or access denied")
            
            # Calculate trends (simplified)
            trends_query = text("""
                SELECT 
                    COUNT(CASE WHEN created_at >= NOW() - INTERVAL '30 days' THEN 1 END) as projects_created_30d,
                    COUNT(CASE WHEN status = 'completed' AND updated_at >= NOW() - INTERVAL '30 days' THEN 1 END) as projects_completed_30d
                FROM projects
                WHERE portfolio_id = :portfolio_id
            """)
            
            trends_result = await self.session.execute(
                trends_query, 
                {"portfolio_id": portfolio_id}
            )
            trends_data = trends_result.fetchone()
            
            dashboard = {
                'portfolio': {
                    'id': dashboard_data.id,
                    'name': dashboard_data.name,
                    'description': dashboard_data.description,
                    'is_active': dashboard_data.is_active,
                    'created_at': dashboard_data.created_at
                },
                'statistics': {
                    'total_projects': dashboard_data.total_projects,
                    'active_projects': dashboard_data.active_projects,
                    'inactive_projects': dashboard_data.total_projects - dashboard_data.active_projects
                },
                'recent_projects': dashboard_data.recent_projects,
                'critical_risks': dashboard_data.critical_risks,
                'trends': {
                    'projects_created_30d': trends_data.projects_created_30d,
                    'projects_completed_30d': trends_data.projects_completed_30d,
                    'completion_rate': (
                        trends_data.projects_completed_30d / trends_data.projects_created_30d * 100
                        if trends_data.projects_created_30d > 0 else 0
                    )
                }
            }
            
            # Track performance
            execution_time = (datetime.now() - start_time).total_seconds()
            self._track_query_performance('optimized_dashboard', execution_time)
            
            return dashboard
            
        except Exception as e:
            logger.error(f"Error in optimized dashboard query: {str(e)}")
            raise
    
    def _track_query_performance(self, query_name: str, execution_time: float):
        """Track query performance metrics."""
        self.query_stats['total_queries'] += 1
        
        if execution_time > self.slow_query_threshold:
            self.query_stats['slow_queries'] += 1
            logger.warning(f"Slow query detected: {query_name} took {execution_time:.2f}s")
        else:
            self.query_stats['optimized_queries'] += 1
        
        logger.debug(f"Query {query_name} executed in {execution_time:.3f}s")
    
    def get_query_stats(self) -> Dict[str, Any]:
        """Get query performance statistics."""
        total_queries = self.query_stats['total_queries']
        
        return {
            'total_queries': total_queries,
            'slow_queries': self.query_stats['slow_queries'],
            'optimized_queries': self.query_stats['optimized_queries'],
            'slow_query_percentage': (
                self.query_stats['slow_queries'] / total_queries * 100
                if total_queries > 0 else 0
            ),
            'optimization_rate': (
                self.query_stats['optimized_queries'] / total_queries * 100
                if total_queries > 0 else 0
            ),
            'slow_query_threshold': self.slow_query_threshold
        }
