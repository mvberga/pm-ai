"""
Portfolio router for portfolio management endpoints.

Este router fornece endpoints para gestão completa de portfólios,
incluindo criação, atualização, exclusão e consulta de estatísticas.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import Session, CurrentUser
from app.schemas.portfolio import (
    Portfolio, PortfolioCreate, PortfolioUpdate, PortfolioSummary,
    PortfolioWithProjects
)
from app.services.portfolio_service import PortfolioService
# from app.core.exceptions import ValidationError, NotFoundError

router = APIRouter(
    prefix="/portfolios",
    tags=["portfolios"],
    responses={
        404: {"description": "Portfólio não encontrado"},
        400: {"description": "Dados inválidos"},
        401: {"description": "Não autorizado"},
        403: {"description": "Sem permissão"},
        500: {"description": "Erro interno do servidor"}
    }
)

@router.post(
    "/", 
    response_model=Portfolio, 
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo portfólio",
    description="""
    Cria um novo portfólio para o usuário autenticado.
    
    **Validações:**
    - Nome do portfólio é obrigatório e único por usuário
    - Usuário deve estar autenticado
    - Descrição é opcional
    
    **Retorna:**
    - Portfólio criado com ID gerado automaticamente
    - Timestamps de criação e atualização
    """
)
async def create_portfolio(
    portfolio_data: PortfolioCreate,
    session: Session,
    current_user: CurrentUser
):
    """Criar um novo portfólio."""
    try:
        service = PortfolioService(session)
        portfolio = await service.create_portfolio(portfolio_data, current_user.id)
        return portfolio
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

@router.get(
    "/", 
    response_model=List[PortfolioSummary],
    summary="Listar portfólios do usuário",
    description="""
    Lista todos os portfólios do usuário autenticado.
    
    **Parâmetros:**
    - include_inactive: Se deve incluir portfólios inativos (padrão: False)
    
    **Retorna:**
    - Lista de portfólios com informações resumidas
    - Contagem de projetos por portfólio
    - Status de ativação
    """
)
async def get_portfolios(
    session: Session,
    current_user: CurrentUser,
    include_inactive: bool = Query(False, description="Incluir portfólios inativos")
):
    """Listar todos os portfólios do usuário."""
    try:
        service = PortfolioService(session)
        portfolios = await service.get_user_portfolios(current_user.id, include_inactive)
        return portfolios
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

@router.get(
    "/{portfolio_id}", 
    response_model=Portfolio,
    summary="Buscar portfólio por ID",
    description="""
    Busca um portfólio específico por ID.
    
    **Validações:**
    - Portfólio deve existir
    - Usuário deve ter permissão para acessar o portfólio
    
    **Retorna:**
    - Dados completos do portfólio
    - Timestamps de criação e atualização
    """
)
async def get_portfolio(
    portfolio_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Buscar portfólio específico por ID."""
    try:
        service = PortfolioService(session)
        portfolio = await service.get_portfolio(portfolio_id, current_user.id)
        if not portfolio:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfólio não encontrado")
        return portfolio
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

@router.put(
    "/{portfolio_id}", 
    response_model=Portfolio,
    summary="Atualizar portfólio",
    description="""
    Atualiza um portfólio existente.
    
    **Validações:**
    - Portfólio deve existir
    - Usuário deve ter permissão para atualizar o portfólio
    - Nome deve ser único por usuário (se alterado)
    
    **Retorna:**
    - Portfólio atualizado com novos dados
    - Timestamp de atualização modificado
    """
)
async def update_portfolio(
    portfolio_id: int,
    portfolio_data: PortfolioUpdate,
    session: Session,
    current_user: CurrentUser
):
    """Atualizar portfólio existente."""
    try:
        service = PortfolioService(session)
        portfolio = await service.update_portfolio(portfolio_id, portfolio_data, current_user.id)
        if not portfolio:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfólio não encontrado")
        return portfolio
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

@router.delete(
    "/{portfolio_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir portfólio",
    description="""
    Exclui um portfólio permanentemente.
    
    **Validações:**
    - Portfólio deve existir
    - Usuário deve ter permissão para excluir o portfólio
    
    **Atenção:**
    - Esta operação é irreversível
    - Todos os projetos do portfólio serão afetados
    """
)
async def delete_portfolio(
    portfolio_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Excluir portfólio permanentemente."""
    try:
        service = PortfolioService(session)
        success = await service.delete_portfolio(portfolio_id, current_user.id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfólio não encontrado")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

@router.get(
    "/{portfolio_id}/statistics",
    summary="Obter estatísticas do portfólio",
    description="""
    Obtém estatísticas detalhadas de um portfólio.
    
    **Retorna:**
    - Total de projetos
    - Projetos ativos e inativos
    - Status do portfólio
    - Timestamps de criação e atualização
    
    **Validações:**
    - Portfólio deve existir
    - Usuário deve ter permissão para acessar o portfólio
    """
)
async def get_portfolio_statistics(
    portfolio_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Obter estatísticas detalhadas do portfólio."""
    try:
        service = PortfolioService(session)
        stats = await service.get_portfolio_statistics(portfolio_id, current_user.id)
        return stats
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

@router.post(
    "/{portfolio_id}/activate",
    response_model=Portfolio,
    summary="Ativar portfólio",
    description="""
    Ativa um portfólio inativo.
    
    **Validações:**
    - Portfólio deve existir
    - Usuário deve ter permissão para ativar o portfólio
    
    **Retorna:**
    - Portfólio ativado com status atualizado
    """
)
async def activate_portfolio(
    portfolio_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Ativar portfólio."""
    try:
        service = PortfolioService(session)
        portfolio = await service.activate_portfolio(portfolio_id, current_user.id)
        if not portfolio:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfólio não encontrado")
        return portfolio
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

@router.post(
    "/{portfolio_id}/deactivate",
    response_model=Portfolio,
    summary="Desativar portfólio",
    description="""
    Desativa um portfólio ativo.
    
    **Validações:**
    - Portfólio deve existir
    - Usuário deve ter permissão para desativar o portfólio
    
    **Retorna:**
    - Portfólio desativado com status atualizado
    """
)
async def deactivate_portfolio(
    portfolio_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Desativar portfólio."""
    try:
        service = PortfolioService(session)
        portfolio = await service.deactivate_portfolio(portfolio_id, current_user.id)
        if not portfolio:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfólio não encontrado")
        return portfolio
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")
