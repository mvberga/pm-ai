#!/usr/bin/env python3
"""
Script para recriar o banco de dados com os relacionamentos corretos.
"""

import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text

# Importar todos os modelos para garantir que o metadata seja populado
from app.models import user, project, portfolio, checklist, action_item, team_member, client, risk, lesson_learned, next_step
from app.db.session import Base

async def recreate_database():
    """Recriar o banco de dados com os relacionamentos corretos."""
    
    # URL do banco de dados SQLite
    database_url = "sqlite+aiosqlite:///./pmdb.db"
    
    # Remover arquivo do banco se existir
    if os.path.exists("pmdb.db"):
        os.remove("pmdb.db")
        print("Arquivo do banco de dados removido.")
    
    # Criar engine
    engine = create_async_engine(
        database_url,
        echo=True,
        connect_args={"check_same_thread": False}
    )
    
    try:
        # Criar todas as tabelas
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("Todas as tabelas foram criadas com sucesso!")
            
            # Verificar se as tabelas foram criadas
            result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            tables = result.fetchall()
            print(f"Tabelas criadas: {[table[0] for table in tables]}")
            
    except Exception as e:
        print(f"Erro ao criar banco de dados: {e}")
        raise
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(recreate_database())
