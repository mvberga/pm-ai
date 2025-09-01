import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.action_item import ActionItem
from app.models.project import Project
from app.models.user import User
from datetime import datetime

class TestActionItemModel:
    """Testes para o modelo ActionItem"""
    
    @pytest.mark.asyncio
    async def test_create_action_item(self, db_session: AsyncSession):
        """Testa criação de um action item"""
        # Arrange - Criar usuários e projeto primeiro
        owner = User(email="action@example.com", name="Action Owner")
        gerente_projeto = User(email="action_gerente@example.com", name="Action Manager")
        gerente_portfolio = User(email="action_portfolio@example.com", name="Action Portfolio")
        
        db_session.add_all([owner, gerente_projeto, gerente_portfolio])
        await db_session.commit()
        await db_session.refresh(owner)
        await db_session.refresh(gerente_projeto)
        await db_session.refresh(gerente_portfolio)
        
        project = Project(
            name="Action Test Project",
            municipio="Test City",
            data_inicio=datetime.now(),
            data_fim=datetime.now(),
            gerente_projeto_id=gerente_projeto.id,
            gerente_portfolio_id=gerente_portfolio.id,
            owner_id=owner.id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db_session.add(project)
        await db_session.commit()
        await db_session.refresh(project)
        
        now = datetime.now()
        action_data = {
            "project_id": project.id,
            "title": "Test action item",
            "type": "task",
            "assignee_id": owner.id,
            "due_date": now,
            "status": "open",
            "description": "Test action item description",
            "created_at": now
        }
        
        # Act
        action = ActionItem(**action_data)
        db_session.add(action)
        await db_session.commit()
        await db_session.refresh(action)
        
        # Assert
        assert action.id is not None
        assert action.title == "Test action item"
        assert action.type == "task"
        assert action.assignee_id == owner.id
        assert action.due_date == now
        assert action.status == "open"
        assert action.description == "Test action item description"
        assert action.project_id == project.id
        assert action.created_at is not None
    
    @pytest.mark.asyncio
    async def test_update_action_item(self, db_session: AsyncSession):
        """Testa atualização de um action item"""
        # Arrange - Criar usuários, projeto e action item
        owner = User(email="update_action@example.com", name="Update Action Owner")
        gerente_projeto = User(email="update_action_gerente@example.com", name="Update Action Manager")
        gerente_portfolio = User(email="update_action_portfolio@example.com", name="Update Action Portfolio")
        
        db_session.add_all([owner, gerente_projeto, gerente_portfolio])
        await db_session.commit()
        await db_session.refresh(owner)
        await db_session.refresh(gerente_projeto)
        await db_session.refresh(gerente_portfolio)
        
        project = Project(
            name="Update Action Test Project",
            municipio="Test City",
            data_inicio=datetime.now(),
            data_fim=datetime.now(),
            gerente_projeto_id=gerente_projeto.id,
            gerente_portfolio_id=gerente_portfolio.id,
            owner_id=owner.id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db_session.add(project)
        await db_session.commit()
        await db_session.refresh(project)
        
        now = datetime.now()
        action = ActionItem(
            project_id=project.id,
            title="Original Title",
            type="task",
            assignee_id=owner.id,
            status="open",
            description="Original description",
            created_at=now
        )
        db_session.add(action)
        await db_session.commit()
        await db_session.refresh(action)
        
        # Act
        action.title = "Updated Title"
        action.status = "in_progress"
        action.description = "Updated description"
        await db_session.commit()
        await db_session.refresh(action)
        
        # Assert
        assert action.title == "Updated Title"
        assert action.status == "in_progress"
        assert action.description == "Updated description"
    
    @pytest.mark.asyncio
    async def test_delete_action_item(self, db_session: AsyncSession):
        """Testa exclusão de um action item"""
        # Arrange - Criar usuários, projeto e action item
        owner = User(email="delete_action@example.com", name="Delete Action Owner")
        gerente_projeto = User(email="delete_action_gerente@example.com", name="Delete Action Manager")
        gerente_portfolio = User(email="delete_action_portfolio@example.com", name="Delete Action Portfolio")
        
        db_session.add_all([owner, gerente_projeto, gerente_portfolio])
        await db_session.commit()
        await db_session.refresh(owner)
        await db_session.refresh(gerente_projeto)
        await db_session.refresh(gerente_portfolio)
        
        project = Project(
            name="Delete Action Test Project",
            municipio="Test City",
            data_inicio=datetime.now(),
            data_fim=datetime.now(),
            gerente_projeto_id=gerente_projeto.id,
            gerente_portfolio_id=gerente_portfolio.id,
            owner_id=owner.id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db_session.add(project)
        await db_session.commit()
        await db_session.refresh(project)
        
        now = datetime.now()
        action = ActionItem(
            project_id=project.id,
            title="Action to Delete",
            type="task",
            assignee_id=owner.id,
            status="open",
            description="Will be deleted",
            created_at=now
        )
        db_session.add(action)
        await db_session.commit()
        await db_session.refresh(action)
        action_id = action.id
        
        # Act
        await db_session.delete(action)
        await db_session.commit()
        
        # Assert
        result = await db_session.get(ActionItem, action_id)
        assert result is None
