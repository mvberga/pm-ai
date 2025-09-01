import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.user import User
from datetime import datetime

class TestAuthAPI:
    """Testes para a API de autenticação (Google OAuth)"""
    
    @pytest.mark.asyncio
    async def test_google_login_new_user(self, client: TestClient, db_session: AsyncSession):
        """Teste de login Google para usuário novo"""
        # Dados do usuário Google
        google_data = {
            "id_token": "fake_google_token_123",
            "email": "novo@gmail.com",
            "name": "Usuário Google"
        }

        # Fazer requisição POST para login Google
        response = client.post("/api/v1/auth/google/login", json=google_data)

        # Verificar resposta
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == "novo@gmail.com"
        assert data["user"]["name"] == "Usuário Google"

    @pytest.mark.asyncio
    async def test_google_login_existing_user(self, client: TestClient, db_session: AsyncSession):
        """Teste de login Google para usuário existente"""
        # Criar usuário primeiro
        user = User(
            name="Usuário Existente",
            email="existente@gmail.com"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        # Dados do usuário Google
        google_data = {
            "id_token": "fake_google_token_456",
            "email": "existente@gmail.com",
            "name": "Usuário Existente"
        }

        # Fazer requisição POST para login Google
        response = client.post("/api/v1/auth/google/login", json=google_data)

        # Verificar resposta
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["id"] == user.id
        assert data["user"]["email"] == "existente@gmail.com"

    @pytest.mark.asyncio
    async def test_google_login_invalid_data(self, client: TestClient, db_session: AsyncSession):
        """Teste de login Google com dados inválidos"""
        # Dados inválidos (sem email)
        invalid_data = {
            "id_token": "fake_token",
            "name": "Usuário Sem Email"
        }

        # Fazer requisição POST para login Google
        response = client.post("/api/v1/auth/google/login", json=invalid_data)

        # Verificar resposta de erro (422 - validação falhou)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_google_login_empty_data(self, client: TestClient, db_session: AsyncSession):
        """Teste de login Google com dados vazios"""
        # Dados vazios
        empty_data = {}

        # Fazer requisição POST para login Google
        response = client.post("/api/v1/auth/google/login", json=empty_data)

        # Verificar resposta de erro (422 - validação falhou)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_google_login_creates_user_automatically(self, client: TestClient, db_session: AsyncSession):
        """Teste de que o login Google cria usuário automaticamente se não existir"""
        # Verificar que não há usuário com este email usando SQLAlchemy
        result = await db_session.execute(
            select(func.count(User.id)).where(User.email == "auto@gmail.com")
        )
        initial_count = result.scalar()

        # Dados do usuário Google
        google_data = {
            "id_token": "fake_google_token_789",
            "email": "auto@gmail.com",
            "name": "Usuário Automático"
        }

        # Fazer requisição POST para login Google
        response = client.post("/api/v1/auth/google/login", json=google_data)

        # Verificar resposta
        assert response.status_code == 200
        
        # Verificar que o usuário foi criado usando SQLAlchemy
        result = await db_session.execute(
            select(func.count(User.id)).where(User.email == "auto@gmail.com")
        )
        final_count = result.scalar()
        assert final_count == initial_count + 1
