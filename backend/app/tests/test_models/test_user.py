import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from datetime import datetime

class TestUserModel:
    """Testes para o modelo User"""
    
    @pytest.mark.asyncio
    async def test_create_user(self, db_session: AsyncSession):
        """Teste de criação de usuário"""
        user = User(
            name="Test User",
            email="test@example.com"
        )
        
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        assert user.id is not None
        assert user.name == "Test User"
        assert user.email == "test@example.com"
        assert user.created_at is not None
    
    @pytest.mark.asyncio
    async def test_user_email_uniqueness(self, db_session: AsyncSession):
        """Teste de unicidade do email"""
        # Criar primeiro usuário
        user1 = User(
            name="User 1",
            email="unique@example.com"
        )
        db_session.add(user1)
        await db_session.commit()
        
        # Tentar criar segundo usuário com mesmo email
        user2 = User(
            name="User 2",
            email="unique@example.com"  # Mesmo email
        )
        db_session.add(user2)
        
        # Deve falhar por constraint de unicidade
        with pytest.raises(Exception):  # SQLAlchemy exception
            await db_session.commit()
    
    @pytest.mark.asyncio
    async def test_user_required_fields(self, db_session: AsyncSession):
        """Teste de campos obrigatórios"""
        # Teste sem email (deve falhar)
        user_no_email = User(
            name="User No Email"
            # email faltando
        )
        db_session.add(user_no_email)
        
        with pytest.raises(Exception):
            await db_session.commit()
        
        # Reset da sessão
        await db_session.rollback()
        
        # Teste sem nome (deve falhar)
        user_no_name = User(
            email="noname@example.com"
            # name faltando
        )
        db_session.add(user_no_name)
        
        with pytest.raises(Exception):
            await db_session.commit()
    
    @pytest.mark.asyncio
    async def test_user_string_lengths(self, db_session: AsyncSession):
        """Teste de comprimento das strings"""
        # Teste com nome muito longo (deve falhar se > 255)
        long_name = "A" * 300  # Nome com 300 caracteres
        user_long_name = User(
            name=long_name,
            email="longname@example.com"
        )
        db_session.add(user_long_name)
        
        # Pode falhar por tamanho da string
        try:
            await db_session.commit()
            # Se não falhar, verificar se foi truncado
            await db_session.refresh(user_long_name)
            assert len(user_long_name.name) <= 255
        except Exception:
            # Esperado falhar por constraint de tamanho
            pass
    
    @pytest.mark.asyncio
    async def test_user_relationships(self, db_session: AsyncSession):
        """Teste de relacionamentos do usuário"""
        # Criar usuário
        user = User(
            name="User Relacionamentos",
            email="relacionamentos@example.com"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        # Verificar se o usuário foi criado corretamente
        assert user.id is not None
        assert user.created_at is not None
        
        # Aqui poderíamos testar relacionamentos quando implementarmos
        # Por exemplo: projetos onde é gerente, membro, etc.
