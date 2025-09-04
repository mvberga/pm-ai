"""
Testes de integração avançados para endpoints de clientes.
"""

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.client import Client, ClientType
from app.models.project import Project


class TestClientsAdvanced:
    """Testes de integração avançados para clientes."""
    
    async def test_create_client_complete_flow(self, client: TestClient, db_session: AsyncSession):
        """Testar fluxo completo de criação de cliente."""
        
        # Dados do cliente
        client_data = {
            "name": "Prefeitura de São Paulo",
            "type": "government",
            "contact_person": "João Silva",
            "email": "joao.silva@prefeitura.sp.gov.br",
            "phone": "+55 11 1234-5678",
            "address": "Viaduto do Chá, 15 - Centro, São Paulo - SP",
            "cnpj": "12.345.678/0001-90",
            "description": "Prefeitura Municipal de São Paulo",
            "status": "active"
        }
        
        # Criar cliente
        response = client.post(f"{settings.API_V1_STR}/clients", json=client_data)
        assert response.status_code == 201
        
        created_client = response.json()
        assert created_client["name"] == client_data["name"]
        assert created_client["type"] == client_data["type"]
        assert created_client["contact_person"] == client_data["contact_person"]
        assert created_client["email"] == client_data["email"]
        assert created_client["phone"] == client_data["phone"]
        assert created_client["address"] == client_data["address"]
        assert created_client["cnpj"] == client_data["cnpj"]
        assert created_client["status"] == client_data["status"]
        
        client_id = created_client["id"]
        
        # Verificar se o cliente foi criado no banco
        from sqlalchemy import select
        result = await db_session.execute(select(Client).where(Client.id == client_id))
        db_client = result.scalar_one_or_none()
        assert db_client is not None
        assert db_client.name == client_data["name"]
    
    async def test_client_types_and_categorization(self, client: TestClient, db_session: AsyncSession):
        """Testar diferentes tipos de clientes e categorização."""
        
        # Criar clientes de diferentes tipos
        clients_data = [
            {
                "name": "Prefeitura Municipal",
                "type": "government",
                "contact_person": "Maria Santos",
                "email": "maria@prefeitura.gov.br",
                "phone": "+55 11 1111-1111",
                "cnpj": "11.111.111/0001-11",
                "status": "active"
            },
            {
                "name": "Empresa Privada Ltda",
                "type": "private",
                "contact_person": "Carlos Oliveira",
                "email": "carlos@empresa.com.br",
                "phone": "+55 11 2222-2222",
                "cnpj": "22.222.222/0001-22",
                "status": "active"
            },
            {
                "name": "ONG Social",
                "type": "non_profit",
                "contact_person": "Ana Costa",
                "email": "ana@ong.org.br",
                "phone": "+55 11 3333-3333",
                "cnpj": "33.333.333/0001-33",
                "status": "active"
            },
            {
                "name": "Universidade Federal",
                "type": "educational",
                "contact_person": "Prof. Roberto",
                "email": "roberto@universidade.edu.br",
                "phone": "+55 11 4444-4444",
                "cnpj": "44.444.444/0001-44",
                "status": "active"
            }
        ]
        
        created_clients = []
        for client_data in clients_data:
            response = client.post(f"{settings.API_V1_STR}/clients", json=client_data)
            assert response.status_code == 201
            created_clients.append(response.json())
        
        # Testar listagem por tipo
        response = client.get(f"{settings.API_V1_STR}/clients?type=government")
        assert response.status_code == 200
        
        government_clients = response.json()
        assert len(government_clients) == 1
        assert government_clients[0]["type"] == "government"
        
        # Testar listagem por status
        response = client.get(f"{settings.API_V1_STR}/clients?status=active")
        assert response.status_code == 200
        
        active_clients = response.json()
        assert len(active_clients) == 4
    
    async def test_client_project_relationship(self, client: TestClient, db_session: AsyncSession):
        """Testar relacionamento entre cliente e projetos."""
        
        # Criar cliente
        client_data = {
            "name": "Cliente para Projetos",
            "type": "private",
            "contact_person": "Pedro Santos",
            "email": "pedro@cliente.com.br",
            "phone": "+55 11 5555-5555",
            "cnpj": "55.555.555/0001-55",
            "status": "active"
        }
        
        response = client.post(f"{settings.API_V1_STR}/clients", json=client_data)
        assert response.status_code == 201
        created_client = response.json()
        client_id = created_client["id"]
        
        # Criar projetos para o cliente
        projects_data = [
            {
                "name": "Projeto 1 do Cliente",
                "description": "Primeiro projeto do cliente",
                "municipio": "São Paulo",
                "entidade": created_client["name"],
                "status": "active"
            },
            {
                "name": "Projeto 2 do Cliente",
                "description": "Segundo projeto do cliente",
                "municipio": "São Paulo",
                "entidade": created_client["name"],
                "status": "completed"
            }
        ]
        
        created_projects = []
        for project_data in projects_data:
            response = client.post(f"{settings.API_V1_STR}/projects", json=project_data)
            assert response.status_code == 201
            created_projects.append(response.json())
        
        # Testar analytics do cliente
        response = client.get(f"{settings.API_V1_STR}/clients/{client_id}/analytics")
        assert response.status_code == 200
        
        analytics = response.json()
        assert "total_projects" in analytics
        assert "active_projects" in analytics
        assert "completed_projects" in analytics
        
        # Verificar se os dados estão corretos
        assert analytics["total_projects"] == 2
        assert analytics["active_projects"] == 1
        assert analytics["completed_projects"] == 1
    
    async def test_client_contact_management(self, client: TestClient, db_session: AsyncSession):
        """Testar gerenciamento de contatos do cliente."""
        
        # Criar cliente
        client_data = {
            "name": "Cliente com Contatos",
            "type": "private",
            "contact_person": "Contato Principal",
            "email": "principal@cliente.com.br",
            "phone": "+55 11 6666-6666",
            "cnpj": "66.666.666/0001-66",
            "status": "active"
        }
        
        response = client.post(f"{settings.API_V1_STR}/clients", json=client_data)
        assert response.status_code == 201
        created_client = response.json()
        client_id = created_client["id"]
        
        # Atualizar informações de contato
        contact_update = {
            "contact_person": "Novo Contato Principal",
            "email": "novo.contato@cliente.com.br",
            "phone": "+55 11 7777-7777",
            "address": "Nova Rua, 123 - Centro, São Paulo - SP"
        }
        
        response = client.put(f"{settings.API_V1_STR}/clients/{client_id}", json=contact_update)
        assert response.status_code == 200
        
        updated_client = response.json()
        assert updated_client["contact_person"] == contact_update["contact_person"]
        assert updated_client["email"] == contact_update["email"]
        assert updated_client["phone"] == contact_update["phone"]
        assert updated_client["address"] == contact_update["address"]
    
    async def test_client_status_workflow(self, client: TestClient, db_session: AsyncSession):
        """Testar fluxo de mudança de status do cliente."""
        
        # Criar cliente ativo
        client_data = {
            "name": "Cliente para Status",
            "type": "private",
            "contact_person": "Status Test",
            "email": "status@cliente.com.br",
            "phone": "+55 11 8888-8888",
            "cnpj": "88.888.888/0001-88",
            "status": "active"
        }
        
        response = client.post(f"{settings.API_V1_STR}/clients", json=client_data)
        assert response.status_code == 201
        created_client = response.json()
        client_id = created_client["id"]
        
        # Mudar status para inativo
        status_update = {"status": "inactive"}
        response = client.put(f"{settings.API_V1_STR}/clients/{client_id}", json=status_update)
        assert response.status_code == 200
        
        updated_client = response.json()
        assert updated_client["status"] == "inactive"
        
        # Mudar status para suspenso
        status_update = {"status": "suspended"}
        response = client.put(f"{settings.API_V1_STR}/clients/{client_id}", json=status_update)
        assert response.status_code == 200
        
        updated_client = response.json()
        assert updated_client["status"] == "suspended"
        
        # Voltar para ativo
        status_update = {"status": "active"}
        response = client.put(f"{settings.API_V1_STR}/clients/{client_id}", json=status_update)
        assert response.status_code == 200
        
        updated_client = response.json()
        assert updated_client["status"] == "active"
    
    async def test_client_search_and_filtering(self, client: TestClient, db_session: AsyncSession):
        """Testar busca e filtros de clientes."""
        
        # Criar clientes para busca
        clients_data = [
            {
                "name": "Prefeitura de São Paulo",
                "type": "government",
                "contact_person": "João Silva",
                "email": "joao@prefeitura.sp.gov.br",
                "phone": "+55 11 1111-1111",
                "cnpj": "11.111.111/0001-11",
                "status": "active"
            },
            {
                "name": "Prefeitura de Santos",
                "type": "government",
                "contact_person": "Maria Santos",
                "email": "maria@prefeitura.santos.gov.br",
                "phone": "+55 13 2222-2222",
                "cnpj": "22.222.222/0001-22",
                "status": "active"
            },
            {
                "name": "Empresa ABC Ltda",
                "type": "private",
                "contact_person": "Carlos ABC",
                "email": "carlos@abc.com.br",
                "phone": "+55 11 3333-3333",
                "cnpj": "33.333.333/0001-33",
                "status": "inactive"
            }
        ]
        
        for client_data in clients_data:
            response = client.post(f"{settings.API_V1_STR}/clients", json=client_data)
            assert response.status_code == 201
        
        # Testar busca por nome
        response = client.get(f"{settings.API_V1_STR}/clients?search=Prefeitura")
        assert response.status_code == 200
        
        prefeitura_clients = response.json()
        assert len(prefeitura_clients) == 2
        
        # Testar busca por email
        response = client.get(f"{settings.API_V1_STR}/clients?search=abc.com.br")
        assert response.status_code == 200
        
        abc_clients = response.json()
        assert len(abc_clients) == 1
        
        # Testar filtro combinado
        response = client.get(f"{settings.API_V1_STR}/clients?type=government&status=active")
        assert response.status_code == 200
        
        active_government_clients = response.json()
        assert len(active_government_clients) == 2
    
    async def test_client_validation_errors(self, client: TestClient, db_session: AsyncSession):
        """Testar validação de dados de cliente."""
        
        # Testar dados inválidos
        invalid_data = {
            "name": "",  # Nome vazio
            "type": "invalid_type",  # Tipo inválido
            "email": "email_invalido",  # Email inválido
            "phone": "telefone_invalido",  # Telefone inválido
            "cnpj": "cnpj_invalido"  # CNPJ inválido
        }
        
        response = client.post(f"{settings.API_V1_STR}/clients", json=invalid_data)
        assert response.status_code == 422  # Validation Error
        
        # Testar dados obrigatórios faltando
        incomplete_data = {
            "email": "teste@example.com"
        }
        
        response = client.post(f"{settings.API_V1_STR}/clients", json=incomplete_data)
        assert response.status_code == 422  # Validation Error
    
    async def test_client_not_found(self, client: TestClient, db_session: AsyncSession):
        """Testar cenários de cliente não encontrado."""
        
        # Tentar buscar cliente inexistente
        response = client.get(f"{settings.API_V1_STR}/clients/99999")
        assert response.status_code == 404
        
        # Tentar atualizar cliente inexistente
        update_data = {"name": "Nome Atualizado"}
        response = client.put(f"{settings.API_V1_STR}/clients/99999", json=update_data)
        assert response.status_code == 404
        
        # Tentar excluir cliente inexistente
        response = client.delete(f"{settings.API_V1_STR}/clients/99999")
        assert response.status_code == 404
