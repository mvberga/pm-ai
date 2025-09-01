import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

class TestFixtureDebug:
    """Testes para debugar o problema com o fixture"""
    
    @pytest.mark.asyncio
    async def test_fixture_creates_tables(self, db_session: AsyncSession):
        """Testa se o fixture está criando as tabelas corretamente"""
        try:
            # Verificar se as tabelas existem
            result = await db_session.execute(
                text("SELECT name FROM sqlite_master WHERE type='table'")
            )
            tables = result.fetchall()
            table_names = [t[0] for t in tables]
            
            print(f"✅ Tabelas criadas pelo fixture: {table_names}")
            
            # Verificar tabelas específicas
            expected_tables = ['users', 'projects', 'checklist_groups', 'action_items']
            for table in expected_tables:
                if table in table_names:
                    print(f"   ✅ {table}")
                else:
                    print(f"   ❌ {table}")
            
            # Tentar inserir um usuário
            from app.models.user import User
            user = User(email="test@fixture.com", name="Fixture Test User")
            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)
            
            print(f"✅ Usuário inserido com sucesso: ID {user.id}")
            
            assert user.id is not None
            
        except Exception as e:
            print(f"❌ Erro no teste do fixture: {e}")
            raise
    
    @pytest.mark.asyncio
    async def test_fixture_isolation(self, db_session: AsyncSession):
        """Testa se o fixture está isolando corretamente"""
        try:
            # Verificar se as tabelas existem
            result = await db_session.execute(
                text("SELECT name FROM sqlite_master WHERE type='table'")
            )
            tables = result.fetchall()
            table_names = [t[0] for t in tables]
            
            print(f"✅ Tabelas no teste de isolamento: {table_names}")
            
            # Tentar inserir um usuário
            from app.models.user import User
            user = User(email="isolation@test.com", name="Isolation Test User")
            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)
            
            print(f"✅ Usuário inserido no teste de isolamento: ID {user.id}")
            
            assert user.id is not None
            
        except Exception as e:
            print(f"❌ Erro no teste de isolamento: {e}")
            raise
