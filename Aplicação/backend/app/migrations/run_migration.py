"""
Script principal para executar toda a migração de dados.

Este script executa:
1. Criação das novas tabelas
2. Migração dos dados existentes
3. Validação da migração
"""

import asyncio
import logging
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path para imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.migrations.create_new_tables import run_database_migration
from app.migrations.data_migration import run_data_migration

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def run_complete_migration():
    """Executa a migração completa."""
    logger.info("=== INICIANDO MIGRAÇÃO COMPLETA ===")
    
    try:
        # Passo 1: Criar novas tabelas
        logger.info("Passo 1: Criando novas tabelas...")
        await run_database_migration()
        logger.info("✅ Novas tabelas criadas com sucesso!")
        
        # Passo 2: Migrar dados
        logger.info("Passo 2: Migrando dados existentes...")
        await run_data_migration()
        logger.info("✅ Dados migrados com sucesso!")
        
        logger.info("=== MIGRAÇÃO COMPLETA FINALIZADA COM SUCESSO! ===")
        
    except Exception as e:
        logger.error(f"❌ Erro durante a migração: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(run_complete_migration())
