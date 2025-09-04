"""
Service para lógica de negócio de Client
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.client import Client, ClientType, CommunicationLevel
from app.schemas.client import (
    ClientCreate, ClientUpdate, ClientSummary, 
    ClientBulkCreate, ClientBulkUpdate
)
from app.repositories.client_repository import ClientRepository
from app.repositories.project_repository import ProjectRepository
from app.core.exceptions import NotFoundError, ValidationError


class ClientService:
    """Service para operações de Client"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.client_repo = ClientRepository(db)
        self.project_repo = ProjectRepository(db)
    
    async def create_client(self, client_data: ClientCreate, user_id: int) -> Client:
        """
        Cria um novo cliente
        
        Args:
            client_data: Dados do cliente
            user_id: ID do usuário (para verificar permissão no projeto)
            
        Returns:
            Client criado
            
        Raises:
            ValidationError: Se o projeto não existe ou usuário não tem permissão
        """
        # Verificar se o projeto existe e o usuário tem permissão
        project = await self.project_repo.get(client_data.project_id)
        if not project:
            raise ValidationError(f"Projeto com ID {client_data.project_id} não encontrado")
        
        # Verificar se o usuário tem permissão no projeto
        if project.owner_id != user_id:
            raise ValidationError("Usuário não tem permissão para adicionar clientes a este projeto")
        
        # Verificar se já existe um cliente com o mesmo email no projeto
        existing_client = await self.client_repo.get_by_email_and_project(
            client_data.email, client_data.project_id
        )
        if existing_client:
            raise ValidationError(f"Já existe um cliente com o email '{client_data.email}' neste projeto")
        
        # Criar o cliente
        client_dict = client_data.model_dump()
        return await self.client_repo.create(client_dict)
    
    async def get_client(self, client_id: int, user_id: int) -> Optional[Client]:
        """
        Busca um cliente por ID
        
        Args:
            client_id: ID do cliente
            user_id: ID do usuário (para verificar permissão)
            
        Returns:
            Client encontrado ou None
        """
        client = await self.client_repo.get(client_id)
        if not client:
            return None
        
        # Verificar se o usuário tem permissão no projeto
        project = await self.project_repo.get(client.project_id)
        if not project or project.owner_id != user_id:
            return None
        
        return client
    
    async def update_client(self, client_id: int, client_data: ClientUpdate, user_id: int) -> Optional[Client]:
        """
        Atualiza um cliente
        
        Args:
            client_id: ID do cliente
            client_data: Dados para atualização
            user_id: ID do usuário
            
        Returns:
            Client atualizado ou None
        """
        client = await self.get_client(client_id, user_id)
        if not client:
            return None
        
        # Verificar se o email não conflita com outros clientes do projeto
        if client_data.email and client_data.email != client.email:
            existing_client = await self.client_repo.get_by_email_and_project(
                client_data.email, client.project_id
            )
            if existing_client and existing_client.id != client_id:
                raise ValidationError(f"Já existe um cliente com o email '{client_data.email}' neste projeto")
        
        # Atualizar o cliente
        update_data = client_data.model_dump(exclude_unset=True)
        return await self.client_repo.update(client_id, update_data)
    
    async def delete_client(self, client_id: int, user_id: int) -> bool:
        """
        Exclui um cliente
        
        Args:
            client_id: ID do cliente
            user_id: ID do usuário
            
        Returns:
            True se excluído com sucesso
        """
        client = await self.get_client(client_id, user_id)
        if not client:
            return False
        
        return await self.client_repo.delete(client_id)
    
    async def get_project_clients(self, project_id: int, user_id: int) -> List[ClientSummary]:
        """
        Lista clientes de um projeto
        
        Args:
            project_id: ID do projeto
            user_id: ID do usuário
            
        Returns:
            Lista de clientes
        """
        # Verificar se o usuário tem permissão no projeto
        project = await self.project_repo.get(project_id)
        if not project or project.owner_id != user_id:
            return []
        
        clients = await self.client_repo.get_by_project(project_id)
        
        return [
            ClientSummary(
                id=client.id,
                name=client.name,
                email=client.email,
                client_type=client.client_type,
                communication_level=client.communication_level
            )
            for client in clients
        ]
    
    async def bulk_create_clients(self, bulk_data: ClientBulkCreate, user_id: int) -> List[Client]:
        """
        Cria múltiplos clientes
        
        Args:
            bulk_data: Dados para criação em lote
            user_id: ID do usuário
            
        Returns:
            Lista de clientes criados
        """
        # Verificar se o projeto existe e o usuário tem permissão
        project = await self.project_repo.get(bulk_data.project_id)
        if not project:
            raise ValidationError(f"Projeto com ID {bulk_data.project_id} não encontrado")
        
        if project.owner_id != user_id:
            raise ValidationError("Usuário não tem permissão para adicionar clientes a este projeto")
        
        created_clients = []
        
        for client_data in bulk_data.clients:
            try:
                # Verificar se já existe um cliente com o mesmo email
                existing_client = await self.client_repo.get_by_email_and_project(
                    client_data.email, bulk_data.project_id
                )
                if existing_client:
                    continue  # Pular cliente duplicado
                
                # Criar o cliente
                client_dict = client_data.model_dump()
                client_dict["project_id"] = bulk_data.project_id
                client = await self.client_repo.create(client_dict)
                created_clients.append(client)
                
            except Exception as e:
                # Log do erro e continuar com os próximos clientes
                print(f"Erro ao criar cliente {client_data.email}: {e}")
                continue
        
        return created_clients
    
    async def bulk_update_clients(self, bulk_data: ClientBulkUpdate, user_id: int) -> List[Client]:
        """
        Atualiza múltiplos clientes
        
        Args:
            bulk_data: Dados para atualização em lote
            user_id: ID do usuário
            
        Returns:
            Lista de clientes atualizados
        """
        updated_clients = []
        
        for client_update in bulk_data.clients:
            try:
                client_id = client_update.get("id")
                if not client_id:
                    continue
                
                # Verificar se o cliente existe e o usuário tem permissão
                client = await self.get_client(client_id, user_id)
                if not client:
                    continue
                
                # Atualizar o cliente
                update_data = {k: v for k, v in client_update.items() if k != "id"}
                updated_client = await self.client_repo.update(client_id, update_data)
                if updated_client:
                    updated_clients.append(updated_client)
                
            except Exception as e:
                # Log do erro e continuar com os próximos clientes
                print(f"Erro ao atualizar cliente {client_update.get('id')}: {e}")
                continue
        
        return updated_clients
    
    async def get_clients_by_type(self, project_id: int, client_type: ClientType, user_id: int) -> List[ClientSummary]:
        """
        Lista clientes por tipo
        
        Args:
            project_id: ID do projeto
            client_type: Tipo dos clientes
            user_id: ID do usuário
            
        Returns:
            Lista de clientes
        """
        # Verificar se o usuário tem permissão no projeto
        project = await self.project_repo.get(project_id)
        if not project or project.owner_id != user_id:
            return []
        
        clients = await self.client_repo.get_by_project_and_type(project_id, client_type)
        
        return [
            ClientSummary(
                id=client.id,
                name=client.name,
                email=client.email,
                client_type=client.client_type,
                communication_level=client.communication_level
            )
            for client in clients
        ]
    
    async def get_clients_by_communication_level(self, project_id: int, communication_level: CommunicationLevel, user_id: int) -> List[ClientSummary]:
        """
        Lista clientes por nível de comunicação
        
        Args:
            project_id: ID do projeto
            communication_level: Nível de comunicação
            user_id: ID do usuário
            
        Returns:
            Lista de clientes
        """
        # Verificar se o usuário tem permissão no projeto
        project = await self.project_repo.get(project_id)
        if not project or project.owner_id != user_id:
            return []
        
        clients = await self.client_repo.get_by_project_and_communication_level(project_id, communication_level)
        
        return [
            ClientSummary(
                id=client.id,
                name=client.name,
                email=client.email,
                client_type=client.client_type,
                communication_level=client.communication_level
            )
            for client in clients
        ]
    
    async def get_client_statistics(self, project_id: int, user_id: int) -> dict:
        """
        Obtém estatísticas de clientes de um projeto
        
        Args:
            project_id: ID do projeto
            user_id: ID do usuário
            
        Returns:
            Dicionário com estatísticas
        """
        # Verificar se o usuário tem permissão no projeto
        project = await self.project_repo.get(project_id)
        if not project or project.owner_id != user_id:
            raise NotFoundError("Projeto não encontrado")
        
        # Contar clientes por tipo
        clients_by_type = await self.client_repo.count_by_type(project_id)
        
        # Contar clientes por nível de comunicação
        clients_by_communication = await self.client_repo.count_by_communication_level(project_id)
        
        # Total de clientes
        total_clients = await self.client_repo.count_by_project(project_id)
        
        return {
            "project_id": project_id,
            "total_clients": total_clients,
            "clients_by_type": clients_by_type,
            "clients_by_communication_level": clients_by_communication
        }
