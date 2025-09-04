"""
Service para lógica de negócio de Portfolio
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.models.portfolio import Portfolio
from app.models.user import User
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate, PortfolioWithProjects, PortfolioSummary
from app.repositories.portfolio_repository import PortfolioRepository
from app.repositories.user_repository import UserRepository
from app.core.exceptions import NotFoundError, ValidationError


class PortfolioService:
    """Service para operações de Portfolio"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.portfolio_repo = PortfolioRepository(db)
        self.user_repo = UserRepository(db)
    
    async def create_portfolio(self, portfolio_data: PortfolioCreate, owner_id: int) -> Portfolio:
        """
        Cria um novo portfólio
        
        Args:
            portfolio_data: Dados do portfólio
            owner_id: ID do proprietário
            
        Returns:
            Portfolio criado
            
        Raises:
            ValidationError: Se o usuário não existe
        """
        # Verificar se o usuário existe
        owner = await self.user_repo.get_by_id(owner_id)
        if not owner:
            raise ValidationError(f"Usuário com ID {owner_id} não encontrado")
        
        # Verificar se já existe um portfólio com o mesmo nome para o usuário
        existing_portfolio = await self.portfolio_repo.get_by_name_and_owner(
            portfolio_data.name, owner_id
        )
        if existing_portfolio:
            raise ValidationError(f"Já existe um portfólio com o nome '{portfolio_data.name}' para este usuário")
        
        # Criar o portfólio
        portfolio_dict = portfolio_data.model_dump()
        portfolio_dict["owner_id"] = owner_id
        portfolio_dict["created_by"] = owner_id  # O criador é o mesmo que o proprietário
        
        return await self.portfolio_repo.create(**portfolio_dict)
    
    async def get_portfolio(self, portfolio_id: int, user_id: int) -> Optional[Portfolio]:
        """
        Busca um portfólio por ID
        
        Args:
            portfolio_id: ID do portfólio
            user_id: ID do usuário (para verificar permissão)
            
        Returns:
            Portfolio encontrado ou None
        """
        portfolio = await self.portfolio_repo.get_by_id(portfolio_id)
        
        if not portfolio:
            return None
        
        # Verificar se o usuário tem permissão para acessar o portfólio
        if portfolio.owner_id != user_id:
            return None
        
        return portfolio
    
    async def get_portfolio_with_projects(self, portfolio_id: int, user_id: int) -> Optional[PortfolioWithProjects]:
        """
        Busca um portfólio com seus projetos
        
        Args:
            portfolio_id: ID do portfólio
            user_id: ID do usuário
            
        Returns:
            Portfolio com projetos ou None
        """
        portfolio = await self.get_portfolio(portfolio_id, user_id)
        if not portfolio:
            return None
        
        # Buscar projetos do portfólio
        projects = await self.portfolio_repo.get_projects(portfolio_id)
        
        # Converter para schema com projetos
        portfolio_dict = portfolio.__dict__.copy()
        portfolio_dict["projects"] = projects
        
        return PortfolioWithProjects(**portfolio_dict)
    
    async def update_portfolio(self, portfolio_id: int, portfolio_data: PortfolioUpdate, user_id: int) -> Optional[Portfolio]:
        """
        Atualiza um portfólio
        
        Args:
            portfolio_id: ID do portfólio
            portfolio_data: Dados para atualização
            user_id: ID do usuário
            
        Returns:
            Portfolio atualizado ou None
        """
        portfolio = await self.get_portfolio(portfolio_id, user_id)
        if not portfolio:
            return None
        
        # Verificar se o nome não conflita com outros portfólios do usuário
        if portfolio_data.name and portfolio_data.name != portfolio.name:
            existing_portfolio = await self.portfolio_repo.get_by_name_and_owner(
                portfolio_data.name, user_id
            )
            if existing_portfolio and existing_portfolio.id != portfolio_id:
                raise ValidationError(f"Já existe um portfólio com o nome '{portfolio_data.name}' para este usuário")
        
        # Atualizar o portfólio
        update_data = portfolio_data.model_dump(exclude_unset=True)
        return await self.portfolio_repo.update(portfolio_id, update_data)
    
    async def delete_portfolio(self, portfolio_id: int, user_id: int) -> bool:
        """
        Exclui um portfólio
        
        Args:
            portfolio_id: ID do portfólio
            user_id: ID do usuário
            
        Returns:
            True se excluído com sucesso
        """
        portfolio = await self.get_portfolio(portfolio_id, user_id)
        if not portfolio:
            return False
        
        return await self.portfolio_repo.delete(portfolio_id)
    
    async def get_user_portfolios(self, user_id: int, include_inactive: bool = False) -> List[PortfolioSummary]:
        """
        Lista portfólios de um usuário
        
        Args:
            user_id: ID do usuário
            include_inactive: Se deve incluir portfólios inativos
            
        Returns:
            Lista de portfólios
        """
        portfolios = await self.portfolio_repo.get_by_owner(user_id, include_inactive)
        
        result = []
        for portfolio in portfolios:
            # Contar projetos
            projects_count = await self.portfolio_repo.count_projects(portfolio.id)
            
            portfolio_summary = PortfolioSummary(
                id=portfolio.id,
                name=portfolio.name,
                is_active=portfolio.is_active,
                projects_count=projects_count
            )
            result.append(portfolio_summary)
        
        return result
    
    async def activate_portfolio(self, portfolio_id: int, user_id: int) -> Optional[Portfolio]:
        """
        Ativa um portfólio
        
        Args:
            portfolio_id: ID do portfólio
            user_id: ID do usuário
            
        Returns:
            Portfolio ativado ou None
        """
        return await self.update_portfolio(
            portfolio_id, 
            PortfolioUpdate(is_active=True), 
            user_id
        )
    
    async def deactivate_portfolio(self, portfolio_id: int, user_id: int) -> Optional[Portfolio]:
        """
        Desativa um portfólio
        
        Args:
            portfolio_id: ID do portfólio
            user_id: ID do usuário
            
        Returns:
            Portfolio desativado ou None
        """
        return await self.update_portfolio(
            portfolio_id, 
            PortfolioUpdate(is_active=False), 
            user_id
        )
    
    async def get_portfolio_statistics(self, portfolio_id: int, user_id: int) -> dict:
        """
        Obtém estatísticas de um portfólio
        
        Args:
            portfolio_id: ID do portfólio
            user_id: ID do usuário
            
        Returns:
            Dicionário com estatísticas
        """
        portfolio = await self.get_portfolio(portfolio_id, user_id)
        if not portfolio:
            raise NotFoundError("Portfólio não encontrado")
        
        # Contar projetos
        total_projects = await self.portfolio_repo.count_projects(portfolio_id)
        active_projects = await self.portfolio_repo.count_active_projects(portfolio_id)
        
        return {
            "portfolio_id": portfolio_id,
            "portfolio_name": portfolio.name,
            "total_projects": total_projects,
            "active_projects": active_projects,
            "inactive_projects": total_projects - active_projects,
            "is_active": portfolio.is_active,
            "created_at": portfolio.created_at,
            "updated_at": portfolio.updated_at
        }
