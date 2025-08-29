import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.checklist import ChecklistGroup, ChecklistItem
from app.models.user import User
from app.models.project import Project, ProjectStatus, ProjectType
from datetime import datetime

class TestChecklistsAPI:
    """Testes para a API de checklists"""
    
    @pytest.mark.asyncio
    async def test_create_checklist_group_api(self, client: TestClient, db_session: AsyncSession):
        """Teste de criação de grupo de checklist via API"""
        # Criar usuário e projeto primeiro
        user = User(
            name="Test User",
            email="test@example.com"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        project = Project(
            name="Projeto Checklist",
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

        # Dados do grupo de checklist (incluindo project_id obrigatório)
        checklist_data = {
            "name": "Grupo de Checklist",
            "project_id": project.id
        }

        # Fazer requisição POST (rota correta: /checklists)
        response = client.post("/api/v1/checklists", json=checklist_data)

        # Verificar resposta (aceitar 200 ou 201)
        assert response.status_code in (200, 201)
        data = response.json()
        assert data["name"] == "Grupo de Checklist"
        assert data["project_id"] == project.id

    @pytest.mark.asyncio
    async def test_create_checklist_item_directly(self, client: TestClient, db_session: AsyncSession):
        """Teste de criação de item de checklist diretamente no banco"""
        # Criar usuário, projeto e grupo
        user = User(
            name="Test User",
            email="test@example.com"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        project = Project(
            name="Projeto Item",
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

        group = ChecklistGroup(
            name="Grupo para Item",
            project_id=project.id
        )
        db_session.add(group)
        await db_session.commit()
        await db_session.refresh(group)

        # Criar item diretamente no banco (sem API)
        item = ChecklistItem(
            title="Item de Checklist",
            group_id=group.id,
            type="Ação",
            notes="Notas do item",
            is_done=False
        )
        db_session.add(item)
        await db_session.commit()
        await db_session.refresh(item)

        # Verificar que o item foi criado
        assert item.id is not None
        assert item.title == "Item de Checklist"
        assert item.group_id == group.id
        assert item.type == "Ação"
        assert item.is_done == False

    @pytest.mark.asyncio
    async def test_get_checklist_group_api(self, client: TestClient, db_session: AsyncSession):
        """Teste de busca de grupo de checklist via API"""
        # Criar usuário, projeto e grupo
        user = User(
            name="Test User",
            email="test@example.com"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        project = Project(
            name="Projeto Buscar",
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

        group = ChecklistGroup(
            name="Grupo para Buscar",
            project_id=project.id
        )
        db_session.add(group)
        await db_session.commit()
        await db_session.refresh(group)

        # Fazer requisição GET (rota correta: /checklists/{id})
        response = client.get(f"/api/v1/checklists/{group.id}")

        # Verificar resposta
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Grupo para Buscar"
        assert data["project_id"] == project.id

    @pytest.mark.asyncio
    async def test_list_checklist_groups_api(self, client: TestClient, db_session: AsyncSession):
        """Teste de listagem de grupos de checklist via API"""
        # Criar usuário e projeto
        user = User(
            name="Test User",
            email="test@example.com"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        project = Project(
            name="Projeto Listar",
            municipio="Curitiba",
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

        # Criar múltiplos grupos
        groups = [
            ChecklistGroup(
                name=f"Grupo {i}",
                project_id=project.id
            )
            for i in range(3)
        ]

        for group in groups:
            db_session.add(group)
        await db_session.commit()

        # Fazer requisição GET para listar todos os grupos
        response = client.get("/api/v1/checklists")

        # Verificar resposta
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3

    @pytest.mark.asyncio
    async def test_checklist_not_found_api(self, client: TestClient, db_session: AsyncSession):
        """Teste de busca de checklist inexistente via API"""
        # Fazer requisição GET para ID inexistente
        response = client.get("/api/v1/checklists/99999")

        # Verificar resposta de erro
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Checklist not found"
