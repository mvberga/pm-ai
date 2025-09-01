import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

class TestTableCreation:
    """Testes para validar a criação de tabelas"""
    
    @pytest.mark.asyncio
    async def test_create_tables_manually(self, db_session: AsyncSession):
        """Testa criação manual de tabelas"""
        from app.db.session import Base
        from app.tests.conftest import test_engine
        
        print(f"🔍 Antes de criar: {len(Base.metadata.tables)} tabelas no metadata")
        
        # Criar tabelas manualmente
        async with test_engine.begin() as conn:
            print("🛠️ Criando tabelas...")
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Tabelas criadas!")
        
        # Verificar se as tabelas foram criadas
        result = await db_session.execute(
            text("SELECT name FROM sqlite_master WHERE type='table'")
        )
        db_tables = result.fetchall()
        table_names = [t[0] for t in db_tables]
        
        print(f"📋 Tabelas no banco após criação: {table_names}")
        
        # Verificar tabelas específicas
        expected_tables = ['users', 'projects', 'checklist_groups', 'action_items']
        for expected_table in expected_tables:
            assert expected_table in table_names, f"Tabela '{expected_table}' não foi criada"
        
        print("🎉 Todas as tabelas esperadas foram criadas!")
    
    @pytest.mark.asyncio
    async def test_project_table_after_creation(self, db_session: AsyncSession):
        """Testa se a tabela projects está funcionando após criação"""
        # Verificar estrutura da tabela projects
        result = await db_session.execute(
            text("PRAGMA table_info(projects)")
        )
        columns = result.fetchall()
        
        print(f"�� Estrutura da tabela projects: {len(columns)} colunas")
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")
        
        # Verificar se temos as colunas principais
        column_names = [col[1] for col in columns]
        expected_columns = ['id', 'name', 'description', 'municipio', 'data_inicio', 'data_fim']
        
        for expected_col in expected_columns:
            assert expected_col in column_names, f"Coluna '{expected_col}' não encontrada"
        
        print("✅ Estrutura da tabela projects está correta!")
