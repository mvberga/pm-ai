import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

class TestDebug:
    """Testes de debug para entender o problema"""
    
    @pytest.mark.asyncio
    async def test_metadata_debug(self, db_session: AsyncSession):
        """Debug: ver o que está no metadata do SQLAlchemy"""
        from app.db.session import Base
        
        print(f"�� Metadata tables: {list(Base.metadata.tables.keys())}")
        print(f"🔍 Total tables in metadata: {len(Base.metadata.tables)}")
        
        # Verificar se temos algum modelo registrado
        if Base.metadata.tables:
            for table_name in Base.metadata.tables:
                table = Base.metadata.tables[table_name]
                print(f"📋 Tabela: {table_name}")
                print(f"   Colunas: {[col.name for col in table.columns]}")
        else:
            print("❌ NENHUMA TABELA encontrada no metadata!")
        
        # Verificar se o banco tem alguma tabela
        result = await db_session.execute(
            text("SELECT name FROM sqlite_master WHERE type='table'")
        )
        db_tables = result.fetchall()
        print(f"��️ Tabelas no banco: {[t[0] for t in db_tables]}")
        
        # Sempre passar para não quebrar o teste
        assert True, "Debug apenas"
    
    @pytest.mark.asyncio
    async def test_model_import_debug(self, db_session: AsyncSession):
        """Debug: ver se os modelos estão sendo importados"""
        try:
            # Tentar importar modelos
            from app.models.user import User
            print(f"✅ User model: {User.__tablename__}")
        except Exception as e:
            print(f"❌ Erro importando User: {e}")
        
        try:
            from app.models.project import Project
            print(f"✅ Project model: {Project.__tablename__}")
        except Exception as e:
            print(f"❌ Erro importando Project: {e}")
        
        try:
            from app.models.checklist import ChecklistGroup
            print(f"✅ ChecklistGroup model: {ChecklistGroup.__tablename__}")
        except Exception as e:
            print(f"❌ Erro importando ChecklistGroup: {e}")
        
        try:
            from app.models.action_item import ActionItem
            print(f"✅ ActionItem model: {ActionItem.__tablename__}")
        except Exception as e:
            print(f"❌ Erro importando ActionItem: {e}")
        
        # Sempre passar para não quebrar o teste
        assert True, "Debug apenas"
