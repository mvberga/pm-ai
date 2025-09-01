import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.models.project import Project, ProjectStatus, ProjectType
from app.models.user import User
from datetime import datetime

class TestProjectsAPI:
    """Testes para a API de projetos"""
    
    @pytest.mark.asyncio
    async def test_create_project_api(self, client: TestClient, db_session: AsyncSession):
        """Teste de criação de projeto via API"""
        # Criar usuário primeiro
        user = User(
            name="Test User",
            email="test@example.com"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        # Dados do projeto para a API (incluindo updated_at obrigatório)
        project_data = {
            "name": "Projeto API Test",
            "description": "Projeto criado via API",
            "municipio": "São Paulo",
            "entidade": "Prefeitura",
            "data_inicio": datetime.now().isoformat(),
            "data_fim": datetime.now().isoformat(),
            "gerente_projeto_id": user.id,
            "gerente_portfolio_id": user.id,
            "updated_at": datetime.now().isoformat()  # Campo obrigatório no modelo
        }

        # Fazer requisição POST com o prefixo correto da API
        response = client.post("/api/v1/projects/", json=project_data)

        # Verificar resposta (FastAPI retorna 200 para criação bem-sucedida)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Projeto API Test"
        assert data["municipio"] == "São Paulo"
        assert data["gerente_projeto_id"] == user.id

    @pytest.mark.asyncio
    async def test_get_project_api(self, client: TestClient, db_session: AsyncSession):
        """Teste de busca de projeto via API"""
        # Criar usuário
        user = User(
            name="Test User",
            email="test@example.com"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        # Criar projeto
        project = Project(
            name="Projeto para Buscar",
            municipio="Rio de Janeiro",
            data_inicio=datetime.now(),
            data_fim=datetime.now(),
            gerente_projeto_id=user.id,
            gerente_portfolio_id=user.id,
            owner_id=user.id,
            status=ProjectStatus.NOT_STARTED,
            updated_at=datetime.now()
        )
        db_session.add(project)
        await db_session.commit()
        await db_session.refresh(project)

        # Fazer requisição GET com o prefixo correto da API
        response = client.get(f"/api/v1/projects/{project.id}")

        # Verificar resposta
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Projeto para Buscar"
        assert data["municipio"] == "Rio de Janeiro"

    @pytest.mark.asyncio
    async def test_list_projects_api(self, client: TestClient, db_session: AsyncSession):
        """Teste de listagem de projetos via API"""
        # Criar usuário
        user = User(
            name="Test User",
            email="test@example.com"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        # Criar múltiplos projetos
        projects = [
            Project(
                name=f"Projeto {i}",
                municipio=f"Cidade {i}",
                data_inicio=datetime.now(),
                data_fim=datetime.now(),
                gerente_projeto_id=user.id,
                gerente_portfolio_id=user.id,
                owner_id=user.id,
                status=ProjectStatus.NOT_STARTED,
                updated_at=datetime.now()
            )
            for i in range(3)
        ]

        for project in projects:
            db_session.add(project)
        await db_session.commit()

        # Fazer requisição GET para listar com o prefixo correto da API
        response = client.get("/api/v1/projects/")

        # Verificar resposta
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3  # Pode ter mais projetos se houver dados existentes

    @pytest.mark.asyncio
    async def test_update_project_api(self, client: TestClient, db_session: AsyncSession):
        """Teste de atualização de projeto via API"""
        # Criar usuário
        user = User(
            name="Test User",
            email="test@example.com"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        # Criar projeto
        project = Project(
            name="Projeto para Atualizar",
            municipio="Brasília",
            data_inicio=datetime.now(),
            data_fim=datetime.now(),
            gerente_projeto_id=user.id,
            gerente_portfolio_id=user.id,
            owner_id=user.id,
            status=ProjectStatus.NOT_STARTED,
            updated_at=datetime.now()
        )
        db_session.add(project)
        await db_session.commit()
        await db_session.refresh(project)

        # Dados de atualização (precisam ser completos para ProjectIn)
        update_data = {
            "name": "Projeto Atualizado",
            "description": "Descrição atualizada",
            "municipio": "São Paulo",
            "entidade": "Prefeitura",
            "data_inicio": datetime.now().isoformat(),
            "data_fim": datetime.now().isoformat(),
            "gerente_projeto_id": user.id,
            "gerente_portfolio_id": user.id,
            "updated_at": datetime.now().isoformat()  # Campo obrigatório
        }

        # Fazer requisição PUT com o prefixo correto da API
        response = client.put(f"/api/v1/projects/{project.id}", json=update_data)

        # Verificar resposta
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Projeto Atualizado"
        assert data["municipio"] == "São Paulo"

    @pytest.mark.asyncio
    async def test_project_metrics_api(self, client: TestClient, db_session: AsyncSession):
        """Teste de métricas de projetos via API"""
        # Criar usuário
        user = User(
            name="Test User",
            email="test@example.com"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        # Criar alguns projetos para testar métricas
        projects = [
            Project(
                name=f"Projeto Métricas {i}",
                municipio=f"Cidade {i}",
                data_inicio=datetime.now(),
                data_fim=datetime.now(),
                gerente_projeto_id=user.id,
                gerente_portfolio_id=user.id,
                owner_id=user.id,
                status=ProjectStatus.NOT_STARTED,
                updated_at=datetime.now()
            )
            for i in range(2)
        ]

        for project in projects:
            db_session.add(project)
        await db_session.commit()

        # Fazer requisição GET para métricas
        response = client.get("/api/v1/projects/metrics")

        # Verificar resposta
        assert response.status_code == 200
        data = response.json()
        assert "total_projects" in data
        assert "projects_by_status" in data
        assert "projects_by_municipio" in data
