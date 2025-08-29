import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.action_item import ActionItem
from app.models.user import User
from app.models.project import Project, ProjectStatus, ProjectType
from datetime import datetime

class TestActionItemsAPI:
    """Testes para a API de action items"""
    
    @pytest.mark.asyncio
    async def test_create_action_item_api(self, client: TestClient, db_session: AsyncSession):
        """Teste de criação de action item via API"""
        # Criar usuário e projeto primeiro
        user = User(
            name="Test User",
            email="test@example.com"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        project = Project(
            name="Projeto Action Item",
            municipio="São Paulo",
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

        # Dados do action item (usando campos corretos do schema)
        action_data = {
            "title": "Action Item Test",
            "type": "Ação Pontual",
            "assignee_id": user.id,
            "project_id": project.id,  # Adicionado project_id
            "status": "open",
            "description": "Descrição do action item"
        }

        # Fazer requisição POST
        response = client.post("/api/v1/action-items", json=action_data)

        # Verificar resposta (aceitar 200 ou 201)
        assert response.status_code in (200, 201)
        data = response.json()
        assert "id" in data
        assert data["title"] == "Action Item Test"

    @pytest.mark.asyncio
    async def test_create_action_item_directly(self, db_session: AsyncSession):
        """Teste de criação direta de action item no banco"""
        # Criar usuário e projeto primeiro
        user = User(
            name="Test User",
            email="test@example.com"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        project = Project(
            name="Projeto Action Item",
            municipio="São Paulo",
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

        # Criar action item diretamente
        action = ActionItem(
            title="Action Item Test",
            type="Ação Pontual",
            assignee_id=user.id,
            project_id=project.id,
            status="open",
            description="Descrição do action item"
        )
        db_session.add(action)
        await db_session.commit()
        await db_session.refresh(action)

        # Verificar se foi criado
        assert action.id is not None
        assert action.title == "Action Item Test"
        assert action.project_id == project.id

    @pytest.mark.asyncio
    async def test_list_action_items_api(self, client: TestClient, db_session: AsyncSession):
        """Teste de listagem de action items via API"""
        # Criar usuário e projeto primeiro
        user = User(
            name="Test User",
            email="test@example.com"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        project = Project(
            name="Projeto Action Item",
            municipio="São Paulo",
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

        # Criar action item diretamente
        action = ActionItem(
            title="Action Item Test",
            type="Ação Pontual",
            assignee_id=user.id,
            project_id=project.id,
            status="open",
            description="Descrição do action item"
        )
        db_session.add(action)
        await db_session.commit()

        # Fazer requisição GET
        response = client.get("/api/v1/action-items")
        
        # Verificar resposta
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    @pytest.mark.asyncio
    async def test_get_action_item_api(self, client: TestClient, db_session: AsyncSession):
        """Teste de obtenção de action item específico via API"""
        # Criar usuário e projeto primeiro
        user = User(
            name="Test User",
            email="test@example.com"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        project = Project(
            name="Projeto Action Item",
            municipio="São Paulo",
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

        # Criar action item diretamente
        action = ActionItem(
            title="Action Item Test",
            type="Ação Pontual",
            assignee_id=user.id,
            project_id=project.id,
            status="open",
            description="Descrição do action item"
        )
        db_session.add(action)
        await db_session.commit()
        await db_session.refresh(action)

        # Fazer requisição GET
        response = client.get(f"/api/v1/action-items/{action.id}")
        
        # Verificar resposta
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == action.id
        assert data["title"] == "Action Item Test"

    @pytest.mark.asyncio
    async def test_action_item_not_found_api(self, client: TestClient):
        """Teste de action item não encontrado via API"""
        # Fazer requisição GET para ID inexistente
        response = client.get("/api/v1/action-items/99999")
        
        # Verificar resposta
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Action item not found"
