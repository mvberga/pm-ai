"""
Testes de integração específicos para endpoints de autenticação.
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient

from app.core.config import settings
from app.models.user import User


class TestAuthIntegration:
    """Testes de integração para autenticação."""
    
    async def test_google_login_flow(self, client: TestClient, db_session: AsyncSession):
        """Testar fluxo completo de login do Google."""
        
        # Dados de login
        login_data = {
            "id_token": "test_token_123",
            "email": "integration@example.com",
            "name": "Integration Test User"
        }
        
        # Verificar que o usuário não existe inicialmente
        user_before = await db_session.execute(
            "SELECT * FROM users WHERE email = :email",
            {"email": login_data["email"]}
        )
        assert user_before.fetchone() is None
        
        # Fazer login
        response = client.post(f"{settings.API_V1_STR}/auth/google/login", json=login_data)
        assert response.status_code == 200
        
        # Verificar resposta
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert "user" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == login_data["email"]
        assert data["user"]["name"] == login_data["name"]
        assert "id" in data["user"]
        
        # Verificar que o usuário foi criado no banco
        user_after = await db_session.execute(
            "SELECT * FROM users WHERE email = :email",
            {"email": login_data["email"]}
        )
        user_row = user_after.fetchone()
        assert user_row is not None
        assert user_row[1] == login_data["email"]  # email é a segunda coluna
        assert user_row[2] == login_data["name"]   # name é a terceira coluna

    async def test_google_login_existing_user(self, client: TestClient, db_session: AsyncSession):
        """Testar login com usuário existente."""
        
        # Criar usuário existente
        from app.utils.auth import hash_password
        existing_user = User(
            email="existing@example.com",
            name="Existing User",
            hashed_password=hash_password("testpassword")
        )
        db_session.add(existing_user)
        await db_session.commit()
        await db_session.refresh(existing_user)
        
        # Dados de login
        login_data = {
            "id_token": "test_token_456",
            "email": existing_user.email,
            "name": existing_user.name
        }
        
        # Fazer login
        response = client.post(f"{settings.API_V1_STR}/auth/google/login", json=login_data)
        assert response.status_code == 200
        
        # Verificar resposta
        data = response.json()
        assert data["user"]["id"] == existing_user.id
        assert data["user"]["email"] == existing_user.email
        assert data["user"]["name"] == existing_user.name

    async def test_google_login_invalid_data(self, client: TestClient):
        """Testar login com dados inválidos."""
        
        # Teste 1: Dados vazios
        response = client.post(f"{settings.API_V1_STR}/auth/google/login", json={})
        assert response.status_code == 422
        
        # Teste 2: Email inválido
        invalid_data = {
            "id_token": "test_token",
            "email": "invalid-email",
            "name": "Test User"
        }
        response = client.post(f"{settings.API_V1_STR}/auth/google/login", json=invalid_data)
        assert response.status_code == 422
        
        # Teste 3: Campos obrigatórios ausentes
        incomplete_data = {
            "email": "test@example.com"
            # Faltam id_token e name
        }
        response = client.post(f"{settings.API_V1_STR}/auth/google/login", json=incomplete_data)
        assert response.status_code == 422

    async def test_google_login_database_consistency(self, client: TestClient, db_session: AsyncSession):
        """Testar consistência do banco de dados durante login."""
        
        # Contar usuários antes
        count_before = await db_session.execute("SELECT COUNT(*) FROM users")
        count_before_value = count_before.scalar()
        
        # Fazer login
        login_data = {
            "id_token": "test_token_789",
            "email": "consistency@example.com",
            "name": "Consistency Test User"
        }
        
        response = client.post(f"{settings.API_V1_STR}/auth/google/login", json=login_data)
        assert response.status_code == 200
        
        # Verificar que o usuário foi adicionado
        count_after = await db_session.execute("SELECT COUNT(*) FROM users")
        count_after_value = count_after.scalar()
        assert count_after_value == count_before_value + 1
        
        # Fazer login novamente com o mesmo usuário
        response = client.post(f"{settings.API_V1_STR}/auth/google/login", json=login_data)
        assert response.status_code == 200
        
        # Verificar que não foi criado usuário duplicado
        count_final = await db_session.execute("SELECT COUNT(*) FROM users")
        count_final_value = count_final.scalar()
        assert count_final_value == count_after_value

    async def test_token_format(self, client: TestClient):
        """Testar formato do token retornado."""
        
        login_data = {
            "id_token": "test_token_format",
            "email": "token@example.com",
            "name": "Token Test User"
        }
        
        response = client.post(f"{settings.API_V1_STR}/auth/google/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()
        access_token = data["access_token"]
        
        # Verificar que o token não está vazio
        assert access_token is not None
        assert len(access_token) > 0
        
        # Verificar que é uma string
        assert isinstance(access_token, str)
        
        # Verificar que contém pontos (formato JWT típico)
        assert "." in access_token

    async def test_concurrent_logins(self, client: TestClient, db_session: AsyncSession):
        """Testar logins concorrentes."""
        
        # Dados para múltiplos usuários
        users_data = [
            {
                "id_token": f"token_{i}",
                "email": f"concurrent{i}@example.com",
                "name": f"Concurrent User {i}"
            }
            for i in range(5)
        ]
        
        # Fazer logins simultâneos (simulado sequencialmente)
        responses = []
        for user_data in users_data:
            response = client.post(f"{settings.API_V1_STR}/auth/google/login", json=user_data)
            responses.append(response)
        
        # Verificar que todos os logins foram bem-sucedidos
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert "access_token" in data
            assert "user" in data
        
        # Verificar que todos os usuários foram criados
        count_after = await db_session.execute("SELECT COUNT(*) FROM users")
        count_after_value = count_after.scalar()
        assert count_after_value >= 5  # Pelo menos 5 usuários

    async def test_user_data_validation(self, client: TestClient):
        """Testar validação de dados do usuário."""
        
        # Teste com nome muito longo
        long_name_data = {
            "id_token": "test_token",
            "email": "longname@example.com",
            "name": "A" * 1000  # Nome muito longo
        }
        
        response = client.post(f"{settings.API_V1_STR}/auth/google/login", json=long_name_data)
        # Pode ser 200 (aceito) ou 422 (rejeitado), dependendo da validação
        assert response.status_code in [200, 422]
        
        # Teste com email muito longo
        long_email_data = {
            "id_token": "test_token",
            "email": "a" * 300 + "@example.com",  # Email muito longo
            "name": "Test User"
        }
        
        response = client.post(f"{settings.API_V1_STR}/auth/google/login", json=long_email_data)
        assert response.status_code in [200, 422]

    async def test_special_characters_in_data(self, client: TestClient):
        """Testar caracteres especiais nos dados."""
        
        special_data = {
            "id_token": "test_token_special",
            "email": "test+special@example.com",
            "name": "José da Silva-Santos & Cia."
        }
        
        response = client.post(f"{settings.API_V1_STR}/auth/google/login", json=special_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["user"]["email"] == special_data["email"]
        assert data["user"]["name"] == special_data["name"]
