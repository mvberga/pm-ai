import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

class TestDatabaseSetup:
    """Testes para validar a configuração do banco de teste"""
    
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
        
        print("✅ Todas as tabelas foram criadas com sucesso!")
    
    @pytest.mark.asyncio
    async def test_project_table_structure(self, db_session: AsyncSession):
        """Testa a estrutura da tabela projects"""
        result = await db_session.execute(
            text("PRAGMA table_info(projects)")
        )
        columns = result.fetchall()
        
        # Verificar se temos as colunas principais
        column_names = [col[1] for col in columns]
        expected_columns = ['id', 'name', 'description', 'municipio', 'data_inicio', 'data_fim']
        
        for expected_col in expected_columns:
            assert expected_col in column_names, f"Coluna '{expected_col}' não encontrada na tabela projects"
        
        print(f"✅ Estrutura da tabela projects: {len(columns)} colunas encontradas")
