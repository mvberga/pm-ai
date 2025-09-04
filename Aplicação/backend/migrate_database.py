#!/usr/bin/env python3
"""
Script para migrar o banco de dados após atualização das dependências
"""

import asyncio
import sys
from pathlib import Path

# Adicionar o diretório do projeto ao path
sys.path.append(str(Path(__file__).parent))

from app.db.session import get_engine
from app.db.base import Base
from app.models import *  # Importar todos os modelos
from alembic.config import Config
from alembic import command

async def migrate_database():
    """Executar migração do banco de dados"""
    print("�� Iniciando migração do banco de dados...")
    
    try:
        # Criar todas as tabelas
        engine = get_engine()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        print("✅ Tabelas criadas com sucesso!")
        
        # Executar migrações do Alembic
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        
        print("✅ Migrações do Alembic executadas com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante a migração: {e}")
        sys.exit(1)
    
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(migrate_database())
