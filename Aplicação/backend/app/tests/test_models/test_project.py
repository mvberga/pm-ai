import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.project import Project, ProjectStatus, ProjectType
from app.models.user import User
from app.schemas.project import ProjectIn, ProjectOut
from datetime import datetime

class TestProjectModel:
    """Testes para o modelo Project"""
    
    @pytest.mark.asyncio
    async def test_create_project(self, db_session: AsyncSession):
        """Teste de criação de projeto"""
        # Criar usuário primeiro (sem o campo 'role' que não existe)
        user = User(
            name="Test User",
            email="test@example.com"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        # Criar projeto com updated_at
        project = Project(
            name="Projeto Teste",
            description="Descrição do projeto teste",
            municipio="São Paulo",
            entidade="Prefeitura",
            chamado_jira="TEST-123",
            portfolio="Portfolio Teste",
            vertical="Saúde",
            product="Produto Teste",
            tipo=ProjectType.IMPLANTACAO,
            data_inicio=datetime.now(),
            data_fim=datetime.now(),
            etapa_atual="Início",
            valor_implantacao=10000.0,
            valor_recorrente=1000.0,
            status=ProjectStatus.NOT_STARTED,
            recursos=5,
            gerente_projeto_id=user.id,
            gerente_portfolio_id=user.id,
            owner_id=user.id,
            updated_at=datetime.now()  # Adicionar este campo obrigatório
        )
        
        db_session.add(project)
        await db_session.commit()
        await db_session.refresh(project)
        
        assert project.id is not None
        assert project.name == "Projeto Teste"
        assert project.gerente_projeto_id == user.id
        assert project.created_at is not None
        assert project.updated_at is not None
    
    @pytest.mark.asyncio
    async def test_project_relationships(self, db_session: AsyncSession):
        """Teste de relacionamentos do projeto"""
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
            description="Teste de relacionamentos",
            municipio="Rio de Janeiro",
            entidade="Estado",
            data_inicio=datetime.now(),
            data_fim=datetime.now(),
            gerente_projeto_id=user.id,
            gerente_portfolio_id=user.id,
            owner_id=user.id,
            status=ProjectStatus.NOT_STARTED,
            updated_at=datetime.now()  # Adicionar este campo obrigatório
        )
        
        db_session.add(project)
        await db_session.commit()
        await db_session.refresh(project)
        
        # Verificar relacionamentos
        assert project.gerente_projeto_id == user.id
        assert project.owner_id == user.id
    
    @pytest.mark.asyncio
    async def test_project_validation(self, db_session: AsyncSession):
        """Teste de validação de dados do projeto"""
        # Criar usuário
        user = User(
            name="Test User",
            email="test@example.com"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        # Teste com dados válidos
        project = Project(
            name="Projeto Válido",
            description="Descrição válida",
            municipio="Brasília",
            entidade="Governo Federal",
            data_inicio=datetime.now(),
            data_fim=datetime.now(),
            gerente_projeto_id=user.id,
            gerente_portfolio_id=user.id,
            owner_id=user.id,
            status=ProjectStatus.NOT_STARTED,
            updated_at=datetime.now()  # Adicionar este campo obrigatório
        )
        
        db_session.add(project)
        await db_session.commit()
        await db_session.refresh(project)
        
        # Verificar enums válidos
        assert project.status in [status.value for status in ProjectStatus]
        assert project.tipo in [tipo.value for tipo in ProjectType]
    
    @pytest.mark.asyncio
    async def test_project_schema_validation(self, db_session: AsyncSession):
        """Teste de validação usando schemas Pydantic"""
        # Criar usuário
        user = User(
            name="Test User",
            email="test@example.com"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        # Teste do schema ProjectIn
        project_data = ProjectIn(
            name="Projeto Schema Test",
            description="Teste de schema",
            municipio="Curitiba",
            entidade="Prefeitura",
            data_inicio=datetime.now(),
            data_fim=datetime.now(),
            gerente_projeto_id=user.id,
            gerente_portfolio_id=user.id
        )
        
        # Verificar se o schema é válido
        assert project_data.name == "Projeto Schema Test"
        assert project_data.municipio == "Curitiba"
        assert project_data.tipo == ProjectType.IMPLANTACAO  # valor padrão
