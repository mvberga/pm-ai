"""
Repository para operações de Portfolio
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload

from app.models.portfolio import Portfolio
from app.models.project import Project
from app.repositories.base_repository import BaseRepository


class PortfolioRepository(BaseRepository[Portfolio]):
    """Repository para operações de Portfolio"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(Portfolio, db)
    
    async def get_by_name_and_owner(self, name: str, owner_id: int) -> Optional[Portfolio]:
        """
        Busca um portfólio por nome e proprietário
        
        Args:
            name: Nome do portfólio
            owner_id: ID do proprietário
            
        Returns:
            Portfolio encontrado ou None
        """
        result = await self.session.execute(
            select(Portfolio)
            .where(and_(
                Portfolio.name == name,
                Portfolio.owner_id == owner_id
            ))
        )
        return result.scalar_one_or_none()
    
    async def get_by_owner(self, owner_id: int, include_inactive: bool = False) -> List[Portfolio]:
        """
        Lista portfólios de um proprietário
        
        Args:
            owner_id: ID do proprietário
            include_inactive: Se deve incluir portfólios inativos
            
        Returns:
            Lista de portfólios
        """
        query = select(Portfolio).where(Portfolio.owner_id == owner_id)
        
        if not include_inactive:
            query = query.where(Portfolio.is_active == True)
        
        query = query.order_by(Portfolio.created_at.desc())
        
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_projects(self, portfolio_id: int) -> List[Project]:
        """
        Busca projetos de um portfólio
        
        Args:
            portfolio_id: ID do portfólio
            
        Returns:
            Lista de projetos
        """
        result = await self.session.execute(
            select(Project)
            .where(Project.portfolio_id == portfolio_id)
            .options(selectinload(Project.gerente_projeto))
            .options(selectinload(Project.gerente_portfolio))
            .options(selectinload(Project.owner))
            .order_by(Project.created_at.desc())
        )
        return result.scalars().all()
    
    async def count_projects(self, portfolio_id: int) -> int:
        """
        Conta projetos de um portfólio
        
        Args:
            portfolio_id: ID do portfólio
            
        Returns:
            Número de projetos
        """
        result = await self.session.execute(
            select(func.count(Project.id))
            .where(Project.portfolio_id == portfolio_id)
        )
        return result.scalar() or 0
    
    async def count_active_projects(self, portfolio_id: int) -> int:
        """
        Conta projetos ativos de um portfólio
        
        Args:
            portfolio_id: ID do portfólio
            
        Returns:
            Número de projetos ativos
        """
        result = await self.session.execute(
            select(func.count(Project.id))
            .where(and_(
                Project.portfolio_id == portfolio_id,
                Project.status.in_(['on_track', 'warning', 'delayed'])
            ))
        )
        return result.scalar() or 0
    
    async def get_portfolio_with_projects(self, portfolio_id: int) -> Optional[Portfolio]:
        """
        Busca um portfólio com seus projetos
        
        Args:
            portfolio_id: ID do portfólio
            
        Returns:
            Portfolio com projetos ou None
        """
        result = await self.session.execute(
            select(Portfolio)
            .where(Portfolio.id == portfolio_id)
            .options(selectinload(Portfolio.projects))
        )
        return result.scalar_one_or_none()
    
    async def get_portfolio_statistics(self, portfolio_id: int) -> dict:
        """
        Obtém estatísticas de um portfólio
        
        Args:
            portfolio_id: ID do portfólio
            
        Returns:
            Dicionário com estatísticas
        """
        # Buscar o portfólio
        portfolio = await self.get(portfolio_id)
        if not portfolio:
            return {}
        
        # Contar projetos por status
        result = await self.session.execute(
            select(
                Project.status,
                func.count(Project.id).label('count')
            )
            .where(Project.portfolio_id == portfolio_id)
            .group_by(Project.status)
        )
        projects_by_status = {row.status: row.count for row in result.fetchall()}
        
        # Contar projetos por tipo
        result = await self.session.execute(
            select(
                Project.tipo,
                func.count(Project.id).label('count')
            )
            .where(Project.portfolio_id == portfolio_id)
            .group_by(Project.tipo)
        )
        projects_by_type = {row.tipo: row.count for row in result.fetchall()}
        
        # Calcular valores totais
        result = await self.session.execute(
            select(
                func.sum(Project.valor_implantacao).label('total_implantacao'),
                func.sum(Project.valor_recorrente).label('total_recorrente'),
                func.sum(Project.recursos).label('total_recursos')
            )
            .where(Project.portfolio_id == portfolio_id)
        )
        totals = result.fetchone()
        
        return {
            "portfolio_id": portfolio_id,
            "portfolio_name": portfolio.name,
            "total_projects": sum(projects_by_status.values()),
            "projects_by_status": projects_by_status,
            "projects_by_type": projects_by_type,
            "total_implantacao": float(totals.total_implantacao or 0),
            "total_recorrente": float(totals.total_recorrente or 0),
            "total_recursos": int(totals.total_recursos or 0),
            "is_active": portfolio.is_active,
            "created_at": portfolio.created_at,
            "updated_at": portfolio.updated_at
        }
