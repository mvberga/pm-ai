#!/usr/bin/env python3
"""
Script para criar usuário de teste para o sistema de login.
"""

import asyncio
import sys
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.utils.auth import hash_password

async def create_test_user():
    """Cria um usuário de teste para desenvolvimento."""
    
    async with AsyncSessionLocal() as session:
        try:
            # Verificar se o usuário já existe
            from sqlalchemy import select
            result = await session.execute(
                select(User).where(User.email == "admin@betha.com.br")
            )
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print("🔄 Usuário de teste já existe! Atualizando senha...")
                # Atualizar senha com hash correto
                existing_user.hashed_password = hash_password("admin123")
                await session.commit()
                print("✅ Senha do usuário de teste atualizada!")
                print(f"   Email: {existing_user.email}")
                print(f"   Nome: {existing_user.name}")
                print(f"   Senha: admin123")
                return
            
            # Criar usuário de teste
            test_user = User(
                email="admin@betha.com.br",
                name="Administrador",
                hashed_password=hash_password("admin123")
            )
            
            session.add(test_user)
            await session.commit()
            await session.refresh(test_user)
            
            print("✅ Usuário de teste criado com sucesso!")
            print(f"   Email: {test_user.email}")
            print(f"   Nome: {test_user.name}")
            print(f"   Senha: admin123")
            print(f"   ID: {test_user.id}")
            
        except Exception as e:
            print(f"❌ Erro ao criar usuário de teste: {e}")
            await session.rollback()

if __name__ == "__main__":
    asyncio.run(create_test_user())
