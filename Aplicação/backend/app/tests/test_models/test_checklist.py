import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.checklist import ChecklistGroup, ChecklistItem
from app.models.user import User
from app.models.project import Project, ProjectStatus, ProjectType
from datetime import datetime

class TestChecklistModels:
    """Testes para os modelos de Checklist"""
    
    @pytest.mark.asyncio
    async def test_create_checklist_group(self, db_session: AsyncSession):
        """Teste de criação de grupo de checklist"""
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
        
        # Criar grupo de checklist (sem description, sem order_index)
        checklist_group = ChecklistGroup(
            name="Grupo de Teste",
            project_id=project.id
        )
        
        db_session.add(checklist_group)
        await db_session.commit()
        await db_session.refresh(checklist_group)
        
        assert checklist_group.id is not None
        assert checklist_group.name == "Grupo de Teste"
        assert checklist_group.project_id == project.id
        assert checklist_group.created_at is not None
    
    @pytest.mark.asyncio
    async def test_create_checklist_item(self, db_session: AsyncSession):
        """Teste de criação de item de checklist"""
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
        
        # Criar grupo de checklist
        checklist_group = ChecklistGroup(
            name="Grupo de Teste",
            project_id=project.id
        )
        db_session.add(checklist_group)
        await db_session.commit()
        await db_session.refresh(checklist_group)
        
        # Criar item de checklist (usando campos corretos)
        checklist_item = ChecklistItem(
            title="Item de Teste",
            type="Ação",  # Campo correto
            notes="Notas do item de teste",
            is_done=False,
            group_id=checklist_group.id  # Campo correto
        )
        
        db_session.add(checklist_item)
        await db_session.commit()
        await db_session.refresh(checklist_item)
        
        assert checklist_item.id is not None
        assert checklist_item.title == "Item de Teste"
        assert checklist_item.type == "Ação"
        assert checklist_item.group_id == checklist_group.id
        assert checklist_item.is_done is False
        assert checklist_item.created_at is not None
    
    @pytest.mark.asyncio
    async def test_checklist_relationships(self, db_session: AsyncSession):
        """Teste de relacionamentos dos checklists"""
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
            name="Projeto Relacionamentos",
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
        
        # Criar grupo de checklist
        group = ChecklistGroup(
            name="Grupo Principal",
            project_id=project.id
        )
        db_session.add(group)
        await db_session.commit()
        await db_session.refresh(group)
        
        # Criar múltiplos itens
        item1 = ChecklistItem(
            title="Item 1",
            type="Ação",
            notes="Primeiro item",
            is_done=False,
            group_id=group.id
        )
        
        item2 = ChecklistItem(
            title="Item 2",
            type="Documentação",
            notes="Segundo item",
            is_done=True,
            group_id=group.id
        )
        
        db_session.add_all([item1, item2])
        await db_session.commit()
        await db_session.refresh(item1)
        await db_session.refresh(item2)
        
        # Verificar relacionamentos
        assert item1.group_id == group.id
        assert item2.group_id == group.id
        assert group.project_id == project.id
    
    @pytest.mark.asyncio
    async def test_checklist_validation(self, db_session: AsyncSession):
        """Teste de validação dos checklists - Versão simplificada"""
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
            name="Projeto Validação",
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
        
        # Teste de grupo sem nome (deve falhar)
        group_no_name = ChecklistGroup(
            project_id=project.id
            # name faltando
        )
        db_session.add(group_no_name)
        
        # Deve falhar por constraint NOT NULL
        with pytest.raises(Exception):
            await db_session.commit()
        
        # SOLUÇÃO: Não usar rollback, apenas verificar que falhou
        # O fixture vai limpar automaticamente
