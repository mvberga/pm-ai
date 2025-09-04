"""
Service para lógica de negócio de TeamMember
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.team_member import TeamMember, TeamRole
from app.schemas.team_member import (
    TeamMemberCreate, TeamMemberUpdate, TeamMemberSummary, 
    TeamMemberBulkCreate, TeamMemberBulkUpdate
)
from app.repositories.team_member_repository import TeamMemberRepository
from app.repositories.project_repository import ProjectRepository
from app.core.exceptions import NotFoundError, ValidationError


class TeamMemberService:
    """Service para operações de TeamMember"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.team_member_repo = TeamMemberRepository(db)
        self.project_repo = ProjectRepository(db)
    
    async def create_team_member(self, team_member_data: TeamMemberCreate, user_id: int) -> TeamMember:
        """
        Cria um novo membro da equipe
        
        Args:
            team_member_data: Dados do membro da equipe
            user_id: ID do usuário (para verificar permissão no projeto)
            
        Returns:
            TeamMember criado
            
        Raises:
            ValidationError: Se o projeto não existe ou usuário não tem permissão
        """
        # Verificar se o projeto existe e o usuário tem permissão
        project = await self.project_repo.get(team_member_data.project_id)
        if not project:
            raise ValidationError(f"Projeto com ID {team_member_data.project_id} não encontrado")
        
        # Verificar se o usuário tem permissão no projeto (simplificado - pode ser expandido)
        if project.owner_id != user_id:
            raise ValidationError("Usuário não tem permissão para adicionar membros a este projeto")
        
        # Verificar se já existe um membro com o mesmo email no projeto
        existing_member = await self.team_member_repo.get_by_email_and_project(
            team_member_data.email, team_member_data.project_id
        )
        if existing_member:
            raise ValidationError(f"Já existe um membro com o email '{team_member_data.email}' neste projeto")
        
        # Criar o membro da equipe
        member_dict = team_member_data.model_dump()
        return await self.team_member_repo.create(member_dict)
    
    async def get_team_member(self, member_id: int, user_id: int) -> Optional[TeamMember]:
        """
        Busca um membro da equipe por ID
        
        Args:
            member_id: ID do membro da equipe
            user_id: ID do usuário (para verificar permissão)
            
        Returns:
            TeamMember encontrado ou None
        """
        member = await self.team_member_repo.get(member_id)
        if not member:
            return None
        
        # Verificar se o usuário tem permissão no projeto
        project = await self.project_repo.get(member.project_id)
        if not project or project.owner_id != user_id:
            return None
        
        return member
    
    async def update_team_member(self, member_id: int, member_data: TeamMemberUpdate, user_id: int) -> Optional[TeamMember]:
        """
        Atualiza um membro da equipe
        
        Args:
            member_id: ID do membro da equipe
            member_data: Dados para atualização
            user_id: ID do usuário
            
        Returns:
            TeamMember atualizado ou None
        """
        member = await self.get_team_member(member_id, user_id)
        if not member:
            return None
        
        # Verificar se o email não conflita com outros membros do projeto
        if member_data.email and member_data.email != member.email:
            existing_member = await self.team_member_repo.get_by_email_and_project(
                member_data.email, member.project_id
            )
            if existing_member and existing_member.id != member_id:
                raise ValidationError(f"Já existe um membro com o email '{member_data.email}' neste projeto")
        
        # Atualizar o membro da equipe
        update_data = member_data.model_dump(exclude_unset=True)
        return await self.team_member_repo.update(member_id, update_data)
    
    async def delete_team_member(self, member_id: int, user_id: int) -> bool:
        """
        Exclui um membro da equipe
        
        Args:
            member_id: ID do membro da equipe
            user_id: ID do usuário
            
        Returns:
            True se excluído com sucesso
        """
        member = await self.get_team_member(member_id, user_id)
        if not member:
            return False
        
        return await self.team_member_repo.delete(member_id)
    
    async def get_project_team_members(self, project_id: int, user_id: int, include_inactive: bool = False) -> List[TeamMemberSummary]:
        """
        Lista membros da equipe de um projeto
        
        Args:
            project_id: ID do projeto
            user_id: ID do usuário
            include_inactive: Se deve incluir membros inativos
            
        Returns:
            Lista de membros da equipe
        """
        # Verificar se o usuário tem permissão no projeto
        project = await self.project_repo.get(project_id)
        if not project or project.owner_id != user_id:
            return []
        
        members = await self.team_member_repo.get_by_project(project_id, include_inactive)
        
        return [
            TeamMemberSummary(
                id=member.id,
                name=member.name,
                email=member.email,
                role=member.role,
                is_active=member.is_active
            )
            for member in members
        ]
    
    async def bulk_create_team_members(self, bulk_data: TeamMemberBulkCreate, user_id: int) -> List[TeamMember]:
        """
        Cria múltiplos membros da equipe
        
        Args:
            bulk_data: Dados para criação em lote
            user_id: ID do usuário
            
        Returns:
            Lista de membros criados
        """
        # Verificar se o projeto existe e o usuário tem permissão
        project = await self.project_repo.get(bulk_data.project_id)
        if not project:
            raise ValidationError(f"Projeto com ID {bulk_data.project_id} não encontrado")
        
        if project.owner_id != user_id:
            raise ValidationError("Usuário não tem permissão para adicionar membros a este projeto")
        
        created_members = []
        
        for member_data in bulk_data.members:
            try:
                # Verificar se já existe um membro com o mesmo email
                existing_member = await self.team_member_repo.get_by_email_and_project(
                    member_data.email, bulk_data.project_id
                )
                if existing_member:
                    continue  # Pular membro duplicado
                
                # Criar o membro
                member_dict = member_data.model_dump()
                member_dict["project_id"] = bulk_data.project_id
                member = await self.team_member_repo.create(member_dict)
                created_members.append(member)
                
            except Exception as e:
                # Log do erro e continuar com os próximos membros
                print(f"Erro ao criar membro {member_data.email}: {e}")
                continue
        
        return created_members
    
    async def bulk_update_team_members(self, bulk_data: TeamMemberBulkUpdate, user_id: int) -> List[TeamMember]:
        """
        Atualiza múltiplos membros da equipe
        
        Args:
            bulk_data: Dados para atualização em lote
            user_id: ID do usuário
            
        Returns:
            Lista de membros atualizados
        """
        updated_members = []
        
        for member_update in bulk_data.members:
            try:
                member_id = member_update.get("id")
                if not member_id:
                    continue
                
                # Verificar se o membro existe e o usuário tem permissão
                member = await self.get_team_member(member_id, user_id)
                if not member:
                    continue
                
                # Atualizar o membro
                update_data = {k: v for k, v in member_update.items() if k != "id"}
                updated_member = await self.team_member_repo.update(member_id, update_data)
                if updated_member:
                    updated_members.append(updated_member)
                
            except Exception as e:
                # Log do erro e continuar com os próximos membros
                print(f"Erro ao atualizar membro {member_update.get('id')}: {e}")
                continue
        
        return updated_members
    
    async def get_team_members_by_role(self, project_id: int, role: TeamRole, user_id: int) -> List[TeamMemberSummary]:
        """
        Lista membros da equipe por função
        
        Args:
            project_id: ID do projeto
            role: Função dos membros
            user_id: ID do usuário
            
        Returns:
            Lista de membros da equipe
        """
        # Verificar se o usuário tem permissão no projeto
        project = await self.project_repo.get(project_id)
        if not project or project.owner_id != user_id:
            return []
        
        members = await self.team_member_repo.get_by_project_and_role(project_id, role)
        
        return [
            TeamMemberSummary(
                id=member.id,
                name=member.name,
                email=member.email,
                role=member.role,
                is_active=member.is_active
            )
            for member in members
        ]
    
    async def activate_team_member(self, member_id: int, user_id: int) -> Optional[TeamMember]:
        """
        Ativa um membro da equipe
        
        Args:
            member_id: ID do membro da equipe
            user_id: ID do usuário
            
        Returns:
            TeamMember ativado ou None
        """
        return await self.update_team_member(
            member_id, 
            TeamMemberUpdate(is_active=True), 
            user_id
        )
    
    async def deactivate_team_member(self, member_id: int, user_id: int) -> Optional[TeamMember]:
        """
        Desativa um membro da equipe
        
        Args:
            member_id: ID do membro da equipe
            user_id: ID do usuário
            
        Returns:
            TeamMember desativado ou None
        """
        return await self.update_team_member(
            member_id, 
            TeamMemberUpdate(is_active=False), 
            user_id
        )
