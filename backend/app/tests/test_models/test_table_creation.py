import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

class TestTableCreation:
    """Testes para verificar se as tabelas estão sendo criadas corretamente"""
    
    @pytest.mark.asyncio
    async def test_tables_exist(self, db_session: AsyncSession):
        """Testa se as tabelas principais existem"""
        # Verificar se a tabela projects existe
        result = await db_session.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='projects'")
        )
        projects_table = result.fetchone()
        assert projects_table is not None, "Tabela 'projects' não foi criada"
        
        # Verificar se a tabela users existe
        result = await db_session.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        )
        users_table = result.fetchone()
        assert users_table is not None, "Tabela 'users' não foi criada"
        
        # Verificar se a tabela checklist_groups existe
        result = await db_session.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='checklist_groups'")
        )
        checklist_groups_table = result.fetchone()
        assert checklist_groups_table is not None, "Tabela 'checklist_groups' não foi criada"
        
        # Verificar se a tabela action_items existe
        result = await db_session.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='action_items'")
        )
        action_items_table = result.fetchone()
        assert action_items_table is not None, "Tabela 'action_items' não foi criada"
    
    @pytest.mark.asyncio
    async def test_can_insert_user(self, db_session: AsyncSession):
        """Testa se é possível inserir um usuário"""
        from app.models.user import User
        
        user = User(email="test@example.com", name="Test User")
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.name == "Test User"
    
    @pytest.mark.asyncio
    async def test_can_insert_project(self, db_session: AsyncSession):
        """Testa se é possível inserir um projeto"""
        from app.models.user import User
        from app.models.project import Project
        from datetime import datetime

        # Primeiro criar um usuário
        user = User(email="manager@example.com", name="Project Manager")
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        # Agora criar um projeto
        now = datetime.now()
        project = Project(
            name="Test Project",
            municipio="Test City",
            data_inicio=now,
            data_fim=now,
            gerente_projeto_id=user.id,
            gerente_portfolio_id=user.id,
            owner_id=user.id,  # ADICIONAR owner_id
            created_at=now,    # ADICIONAR timestamps
            updated_at=now
        )
        db_session.add(project)
        await db_session.commit()
        await db_session.refresh(project)

        # Assert
        assert project.id is not None
        assert project.name == "Test Project"
