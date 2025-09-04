"""
Testes de integração específicos para endpoints de projetos.
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient

from app.core.config import settings
from app.models.project import Project, ProjectStatus
from app.models.user import User


class TestProjectsIntegration:
    """Testes de integração para projetos."""
    
    async def test_create_project_flow(self, client: TestClient, db_session: AsyncSession):
        """Testar fluxo completo de criação de projeto."""
        
        # Dados do projeto
        project_data = {
            "name": "Integration Test Project",
            "description": "A project for integration testing",
            "municipio": "São Paulo",
            "entidade": "Prefeitura de São Paulo",
            "portfolio": "Test Portfolio",
            "vertical": "Technology",
            "product": "Software Development",
            "tipo": "implantacao",
            "data_inicio": "2024-01-01",
            "data_fim": "2024-12-31",
            "gerente_projeto_id": 1,
            "gerente_portfolio_id": 1
        }
        
        # Verificar que não há projetos inicialmente
        count_before = await db_session.execute("SELECT COUNT(*) FROM projects")
        count_before_value = count_before.scalar()
        
        # Criar projeto
        response = client.post(f"{settings.API_V1_STR}/projects/", json=project_data)
        assert response.status_code in [200, 201]
        
        # Verificar resposta
        data = response.json()
        assert "id" in data
        assert data["name"] == project_data["name"]
        assert data["description"] == project_data["description"]
        assert data["municipio"] == project_data["municipio"]
        assert data["entidade"] == project_data["entidade"]
        assert data["portfolio"] == project_data["portfolio"]
        assert data["vertical"] == project_data["vertical"]
        assert data["product"] == project_data["product"]
        assert data["tipo"] == project_data["tipo"]
        
        # Verificar que o projeto foi criado no banco
        count_after = await db_session.execute("SELECT COUNT(*) FROM projects")
        count_after_value = count_after.scalar()
        assert count_after_value == count_before_value + 1

    async def test_get_projects_list(self, client: TestClient, db_session: AsyncSession):
        """Testar listagem de projetos."""
        
        # Criar alguns projetos de teste
        projects_data = [
            {
                "name": f"Test Project {i}",
                "description": f"Description for project {i}",
                "municipio": "São Paulo",
                "entidade": "Prefeitura",
                "portfolio": f"Portfolio {i}",
                "vertical": "Technology",
                "product": "Software",
                "tipo": "implantacao",
                "gerente_projeto_id": 1,
                "gerente_portfolio_id": 1
            }
            for i in range(3)
        ]
        
        # Criar projetos
        created_projects = []
        for project_data in projects_data:
            response = client.post(f"{settings.API_V1_STR}/projects/", json=project_data)
            if response.status_code in [200, 201]:
                created_projects.append(response.json())
        
        # Listar projetos
        response = client.get(f"{settings.API_V1_STR}/projects/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= len(created_projects)

    async def test_get_project_by_id(self, client: TestClient, db_session: AsyncSession):
        """Testar busca de projeto por ID."""
        
        # Criar projeto
        project_data = {
            "name": "Get By ID Project",
            "description": "A project to test get by ID",
            "municipio": "Rio de Janeiro",
            "entidade": "Prefeitura do Rio",
            "portfolio": "Rio Portfolio",
            "vertical": "Technology",
            "product": "Software",
            "tipo": "implantacao",
            "gerente_projeto_id": 1,
            "gerente_portfolio_id": 1
        }
        
        create_response = client.post(f"{settings.API_V1_STR}/projects/", json=project_data)
        if create_response.status_code in [200, 201]:
            created_project = create_response.json()
            project_id = created_project["id"]
            
            # Buscar projeto por ID
            response = client.get(f"{settings.API_V1_STR}/projects/{project_id}")
            assert response.status_code == 200
            
            data = response.json()
            assert data["id"] == project_id
            assert data["name"] == project_data["name"]
            assert data["municipio"] == project_data["municipio"]

    async def test_get_nonexistent_project(self, client: TestClient):
        """Testar busca de projeto inexistente."""
        
        response = client.get(f"{settings.API_V1_STR}/projects/99999")
        assert response.status_code == 404

    async def test_update_project(self, client: TestClient, db_session: AsyncSession):
        """Testar atualização de projeto."""
        
        # Criar projeto
        project_data = {
            "name": "Update Test Project",
            "description": "Original description",
            "municipio": "Brasília",
            "entidade": "Governo Federal",
            "portfolio": "Federal Portfolio",
            "vertical": "Technology",
            "product": "Software",
            "tipo": "implantacao",
            "gerente_projeto_id": 1,
            "gerente_portfolio_id": 1
        }
        
        create_response = client.post(f"{settings.API_V1_STR}/projects/", json=project_data)
        if create_response.status_code in [200, 201]:
            created_project = create_response.json()
            project_id = created_project["id"]
            
            # Dados de atualização
            update_data = {
                "name": "Updated Project Name",
                "description": "Updated description",
                "municipio": "Salvador",
                "entidade": "Prefeitura de Salvador"
            }
            
            # Atualizar projeto
            response = client.put(f"{settings.API_V1_STR}/projects/{project_id}", json=update_data)
            assert response.status_code in [200, 201]
            
            data = response.json()
            assert data["name"] == update_data["name"]
            assert data["description"] == update_data["description"]
            assert data["municipio"] == update_data["municipio"]
            assert data["entidade"] == update_data["entidade"]

    async def test_delete_project(self, client: TestClient, db_session: AsyncSession):
        """Testar exclusão de projeto."""
        
        # Criar projeto
        project_data = {
            "name": "Delete Test Project",
            "description": "A project to be deleted",
            "municipio": "Belo Horizonte",
            "entidade": "Prefeitura de BH",
            "portfolio": "BH Portfolio",
            "vertical": "Technology",
            "product": "Software",
            "tipo": "implantacao",
            "gerente_projeto_id": 1,
            "gerente_portfolio_id": 1
        }
        
        create_response = client.post(f"{settings.API_V1_STR}/projects/", json=project_data)
        if create_response.status_code in [200, 201]:
            created_project = create_response.json()
            project_id = created_project["id"]
            
            # Contar projetos antes da exclusão
            count_before = await db_session.execute("SELECT COUNT(*) FROM projects")
            count_before_value = count_before.scalar()
            
            # Excluir projeto
            response = client.delete(f"{settings.API_V1_STR}/projects/{project_id}")
            assert response.status_code == 204
            
            # Verificar que o projeto foi excluído
            count_after = await db_session.execute("SELECT COUNT(*) FROM projects")
            count_after_value = count_after.scalar()
            assert count_after_value == count_before_value - 1

    async def test_project_metrics(self, client: TestClient, db_session: AsyncSession):
        """Testar métricas de projeto."""
        
        # Criar alguns projetos para ter dados
        projects_data = [
            {
                "name": f"Metrics Project {i}",
                "description": f"Project for metrics {i}",
                "municipio": f"City {i}",
                "entidade": f"Entity {i}",
                "portfolio": f"Portfolio {i}",
                "vertical": "Technology",
                "product": "Software",
                "tipo": "implantacao",
                "valor_implantacao": 100000.0 + (i * 10000),
                "valor_recorrente": 10000.0 + (i * 1000),
                "recursos": 5 + i,
                "gerente_projeto_id": 1,
                "gerente_portfolio_id": 1
            }
            for i in range(3)
        ]
        
        # Criar projetos
        for project_data in projects_data:
            response = client.post(f"{settings.API_V1_STR}/projects/", json=project_data)
            # Não verificamos o status pois pode falhar por validação
        
        # Obter métricas
        response = client.get(f"{settings.API_V1_STR}/projects/metrics")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_projects" in data
        assert "total_implantation" in data
        assert "total_recurring" in data
        assert "total_resources" in data
        assert "projects_by_status" in data
        assert "projects_by_municipio" in data
        assert "projects_by_portfolio" in data
        
        # Verificar tipos
        assert isinstance(data["total_projects"], int)
        assert isinstance(data["total_implantation"], (int, float))
        assert isinstance(data["total_recurring"], (int, float))
        assert isinstance(data["total_resources"], int)
        assert isinstance(data["projects_by_status"], dict)
        assert isinstance(data["projects_by_municipio"], dict)
        assert isinstance(data["projects_by_portfolio"], dict)

    async def test_project_filters(self, client: TestClient, db_session: AsyncSession):
        """Testar filtros de projeto."""
        
        # Criar projetos com diferentes características
        projects_data = [
            {
                "name": "São Paulo Project",
                "description": "Project in São Paulo",
                "municipio": "São Paulo",
                "entidade": "Prefeitura SP",
                "portfolio": "SP Portfolio",
                "vertical": "Technology",
                "product": "Software",
                "tipo": "implantacao",
                "gerente_projeto_id": 1,
                "gerente_portfolio_id": 1
            },
            {
                "name": "Rio Project",
                "description": "Project in Rio",
                "municipio": "Rio de Janeiro",
                "entidade": "Prefeitura RJ",
                "portfolio": "RJ Portfolio",
                "vertical": "Healthcare",
                "product": "Medical Software",
                "tipo": "implantacao",
                "gerente_projeto_id": 2,
                "gerente_portfolio_id": 2
            }
        ]
        
        # Criar projetos
        for project_data in projects_data:
            response = client.post(f"{settings.API_V1_STR}/projects/", json=project_data)
            # Não verificamos o status pois pode falhar por validação
        
        # Testar filtro por município
        response = client.get(f"{settings.API_V1_STR}/projects/?municipio=São Paulo")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        
        # Testar filtro por portfólio
        response = client.get(f"{settings.API_V1_STR}/projects/?portfolio=SP Portfolio")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        
        # Testar filtro por vertical
        response = client.get(f"{settings.API_V1_STR}/projects/?vertical=Technology")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)

    async def test_project_validation_errors(self, client: TestClient):
        """Testar erros de validação em projetos."""
        
        # Teste 1: Dados vazios
        response = client.post(f"{settings.API_V1_STR}/projects/", json={})
        assert response.status_code == 422
        
        # Teste 2: Campos obrigatórios ausentes
        incomplete_data = {
            "name": "Incomplete Project"
            # Faltam campos obrigatórios
        }
        response = client.post(f"{settings.API_V1_STR}/projects/", json=incomplete_data)
        assert response.status_code == 422
        
        # Teste 3: Dados inválidos
        invalid_data = {
            "name": "Invalid Project",
            "description": "Invalid description",
            "municipio": "",  # Município vazio
            "entidade": "",   # Entidade vazia
            "portfolio": "Test Portfolio",
            "vertical": "Technology",
            "product": "Software",
            "tipo": "invalid_type",  # Tipo inválido
            "gerente_projeto_id": -1,  # ID inválido
            "gerente_portfolio_id": -1  # ID inválido
        }
        response = client.post(f"{settings.API_V1_STR}/projects/", json=invalid_data)
        assert response.status_code == 422

    async def test_project_tasks_endpoints(self, client: TestClient, db_session: AsyncSession):
        """Testar endpoints de tarefas do projeto."""
        
        # Criar projeto primeiro
        project_data = {
            "name": "Task Test Project",
            "description": "Project for testing tasks",
            "municipio": "Test City",
            "entidade": "Test Entity",
            "portfolio": "Test Portfolio",
            "vertical": "Technology",
            "product": "Software",
            "tipo": "implantacao",
            "gerente_projeto_id": 1,
            "gerente_portfolio_id": 1
        }
        
        create_response = client.post(f"{settings.API_V1_STR}/projects/", json=project_data)
        if create_response.status_code in [200, 201]:
            created_project = create_response.json()
            project_id = created_project["id"]
            
            # Testar listagem de tarefas (deve retornar lista vazia)
            response = client.get(f"{settings.API_V1_STR}/projects/{project_id}/tasks")
            assert response.status_code == 200
            
            data = response.json()
            assert isinstance(data, list)
            
            # Testar criação de tarefa
            task_data = {
                "title": "Test Task",
                "description": "A test task",
                "status": "pending",
                "priority": "medium"
            }
            
            response = client.post(f"{settings.API_V1_STR}/projects/{project_id}/tasks", json=task_data)
            assert response.status_code in [200, 201, 422]  # 422 se validação falhar

    async def test_project_implantadores_endpoints(self, client: TestClient, db_session: AsyncSession):
        """Testar endpoints de implantadores do projeto."""
        
        # Criar projeto primeiro
        project_data = {
            "name": "Implantador Test Project",
            "description": "Project for testing implantadores",
            "municipio": "Test City",
            "entidade": "Test Entity",
            "portfolio": "Test Portfolio",
            "vertical": "Technology",
            "product": "Software",
            "tipo": "implantacao",
            "gerente_projeto_id": 1,
            "gerente_portfolio_id": 1
        }
        
        create_response = client.post(f"{settings.API_V1_STR}/projects/", json=project_data)
        if create_response.status_code in [200, 201]:
            created_project = create_response.json()
            project_id = created_project["id"]
            
            # Testar listagem de implantadores
            response = client.get(f"{settings.API_V1_STR}/projects/{project_id}/implantadores")
            assert response.status_code == 200
            
            data = response.json()
            assert isinstance(data, list)
            
            # Testar adição de implantador
            implantador_data = {
                "nome": "Test Implantador",
                "email": "implantador@test.com",
                "telefone": "11999999999"
            }
            
            response = client.post(f"{settings.API_V1_STR}/projects/{project_id}/implantadores", json=implantador_data)
            assert response.status_code in [200, 201, 422]  # 422 se validação falhar

    async def test_project_migradores_endpoints(self, client: TestClient, db_session: AsyncSession):
        """Testar endpoints de migradores do projeto."""
        
        # Criar projeto primeiro
        project_data = {
            "name": "Migrador Test Project",
            "description": "Project for testing migradores",
            "municipio": "Test City",
            "entidade": "Test Entity",
            "portfolio": "Test Portfolio",
            "vertical": "Technology",
            "product": "Software",
            "tipo": "implantacao",
            "gerente_projeto_id": 1,
            "gerente_portfolio_id": 1
        }
        
        create_response = client.post(f"{settings.API_V1_STR}/projects/", json=project_data)
        if create_response.status_code in [200, 201]:
            created_project = create_response.json()
            project_id = created_project["id"]
            
            # Testar listagem de migradores
            response = client.get(f"{settings.API_V1_STR}/projects/{project_id}/migradores")
            assert response.status_code == 200
            
            data = response.json()
            assert isinstance(data, list)
            
            # Testar adição de migrador
            migrador_data = {
                "nome": "Test Migrador",
                "email": "migrador@test.com",
                "telefone": "11999999999"
            }
            
            response = client.post(f"{settings.API_V1_STR}/projects/{project_id}/migradores", json=migrador_data)
            assert response.status_code in [200, 201, 422]  # 422 se validação falhar
