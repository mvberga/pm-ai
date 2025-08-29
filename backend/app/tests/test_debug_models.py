import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import text
import sys
import os

# Adicionar o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestDebugModels:
    """Testes de debug para entender o problema com criação de tabelas"""
    
    @pytest.mark.asyncio
    async def test_import_models(self):
        """Testa se os modelos podem ser importados corretamente"""
        try:
            # Importar os modelos
            from app.models.user import User
            from app.models.project import Project
            from app.models.checklist import ChecklistGroup, ChecklistItem
            from app.models.action_item import ActionItem
            
            print(f"✅ Modelos importados com sucesso:")
            print(f"   - User: {User}")
            print(f"   - Project: {Project}")
            print(f"   - ChecklistGroup: {ChecklistGroup}")
            print(f"   - ChecklistItem: {ChecklistItem}")
            print(f"   - ActionItem: {ActionItem}")
            
            # Verificar se estão no metadata
            from app.db.session import Base
            print(f"✅ Base metadata: {Base.metadata}")
            print(f"✅ Tabelas no metadata: {list(Base.metadata.tables.keys())}")
            
            assert len(Base.metadata.tables) > 0, "Metadata não contém tabelas"
            
        except Exception as e:
            print(f"❌ Erro ao importar modelos: {e}")
            raise
    
    @pytest.mark.asyncio
    async def test_create_tables_manually(self):
        """Testa criação manual de tabelas"""
        try:
            from app.db.session import Base
            
            # Criar engine de teste
            test_engine = create_async_engine(
                "sqlite+aiosqlite:///:memory:",
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
                echo=True  # Ativar echo para debug
            )
            
            print(f"✅ Engine de teste criado: {test_engine}")
            
            # Importar modelos para popular metadata
            from app.models.user import User
            from app.models.project import Project
            from app.models.checklist import ChecklistGroup, ChecklistItem
            from app.models.action_item import ActionItem
            
            print(f"✅ Modelos importados, metadata contém {len(Base.metadata.tables)} tabelas")
            print(f"✅ Tabelas: {list(Base.metadata.tables.keys())}")
            
            # Criar tabelas
            async with test_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                print("✅ Tabelas criadas com sucesso")
            
            # Verificar se as tabelas existem
            async with test_engine.begin() as conn:
                result = await conn.run_sync(lambda sync_conn: sync_conn.execute(
                    text("SELECT name FROM sqlite_master WHERE type='table'")
                ))
                tables = result.fetchall()
                print(f"✅ Tabelas criadas no banco: {[t[0] for t in tables]}")
                
                # Verificar tabelas específicas
                for table_name in ['users', 'projects', 'checklist_groups', 'action_items']:
                    result = await conn.run_sync(lambda sync_conn: sync_conn.execute(
                        text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
                    ))
                    table_exists = result.fetchone()
                    print(f"   - {table_name}: {'✅' if table_exists else '❌'}")
            
            await test_engine.dispose()
            
        except Exception as e:
            print(f"❌ Erro na criação manual: {e}")
            raise
    
    @pytest.mark.asyncio
    async def test_fixture_creation(self):
        """Testa se o fixture está funcionando corretamente"""
        try:
            from app.db.session import Base
            
            # Criar engine de teste
            test_engine = create_async_engine(
                "sqlite+aiosqlite:///:memory:",
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
                echo=True
            )
            
            # Importar modelos
            from app.models.user import User
            from app.models.project import Project
            from app.models.checklist import ChecklistGroup, ChecklistItem
            from app.models.action_item import ActionItem
            
            print(f"✅ Metadata antes de criar tabelas: {len(Base.metadata.tables)} tabelas")
            
            # Simular o que o fixture faz
            async with test_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                print("✅ Tabelas criadas pelo fixture")
            
            # Verificar tabelas
            async with test_engine.begin() as conn:
                result = await conn.run_sync(lambda sync_conn: sync_conn.execute(
                    text("SELECT name FROM sqlite_master WHERE type='table'")
                ))
                tables = result.fetchall()
                print(f"✅ Tabelas no banco: {[t[0] for t in tables]}")
            
            await test_engine.dispose()
            
        except Exception as e:
            print(f"❌ Erro no teste do fixture: {e}")
            raise
