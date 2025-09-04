"""
Script para criar as novas tabelas da arquitetura expandida.

Este script cria as tabelas para os novos modelos:
- portfolios
- team_members
- clients
- risks
- lessons_learned
- next_steps
"""

import asyncio
import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseMigration:
    """Classe para executar migração do banco de dados."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_new_tables(self):
        """Cria as novas tabelas da arquitetura expandida."""
        logger.info("Iniciando criação das novas tabelas...")
        
        # SQL para criar as novas tabelas
        create_tables_sql = [
            # Tabela portfolios
            """
            CREATE TABLE IF NOT EXISTS portfolios (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                status VARCHAR(50) DEFAULT 'active' NOT NULL,
                start_date TIMESTAMP WITH TIME ZONE,
                end_date TIMESTAMP WITH TIME ZONE,
                owner_id INTEGER NOT NULL REFERENCES users(id),
                created_by INTEGER NOT NULL REFERENCES users(id),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
            );
            """,
            
            # Tabela team_members
            """
            CREATE TABLE IF NOT EXISTS team_members (
                id SERIAL PRIMARY KEY,
                project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
            );
            """,
            
            # Tabela clients
            """
            CREATE TABLE IF NOT EXISTS clients (
                id SERIAL PRIMARY KEY,
                project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                name VARCHAR(255) NOT NULL,
                company VARCHAR(255),
                client_type VARCHAR(50) NOT NULL DEFAULT 'corporate',
                email VARCHAR(255),
                phone VARCHAR(50),
                address TEXT,
                website VARCHAR(255),
                primary_contact VARCHAR(255),
                communication_level VARCHAR(50) NOT NULL DEFAULT 'managerial',
                preferred_communication VARCHAR(50) DEFAULT 'email' NOT NULL,
                communication_frequency VARCHAR(50) DEFAULT 'weekly' NOT NULL,
                industry VARCHAR(255),
                company_size VARCHAR(50),
                annual_revenue VARCHAR(100),
                satisfaction_score INTEGER,
                last_contact_date TIMESTAMP WITH TIME ZONE,
                next_contact_date TIMESTAMP WITH TIME ZONE,
                is_active BOOLEAN DEFAULT TRUE NOT NULL,
                notes TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
            );
            """,
            
            # Tabela risks
            """
            CREATE TABLE IF NOT EXISTS risks (
                id SERIAL PRIMARY KEY,
                project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                title VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                category VARCHAR(50) NOT NULL,
                status VARCHAR(50) NOT NULL DEFAULT 'identified',
                priority VARCHAR(50) NOT NULL,
                probability DECIMAL(3,2) NOT NULL,
                impact DECIMAL(3,2) NOT NULL,
                mitigation_plan TEXT,
                owner_id INTEGER REFERENCES users(id),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
            );
            """,
            
            # Tabela lessons_learned
            """
            CREATE TABLE IF NOT EXISTS lessons_learned (
                id SERIAL PRIMARY KEY,
                project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                title VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                category VARCHAR(50) NOT NULL,
                lesson_type VARCHAR(50) NOT NULL,
                impact TEXT NOT NULL,
                recommendations TEXT NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
            );
            """,
            
            # Tabela next_steps
            """
            CREATE TABLE IF NOT EXISTS next_steps (
                id SERIAL PRIMARY KEY,
                project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                title VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                status VARCHAR(50) NOT NULL DEFAULT 'pending',
                priority VARCHAR(50) NOT NULL,
                step_type VARCHAR(50) NOT NULL,
                due_date TIMESTAMP WITH TIME ZONE,
                assignee_id INTEGER REFERENCES users(id),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
            );
            """
        ]
        
        # Criar índices para melhor performance
        create_indexes_sql = [
            "CREATE INDEX IF NOT EXISTS idx_portfolios_owner_id ON portfolios(owner_id);",
            "CREATE INDEX IF NOT EXISTS idx_portfolios_name ON portfolios(name);",
            "CREATE INDEX IF NOT EXISTS idx_team_members_project_id ON team_members(project_id);",
            "CREATE INDEX IF NOT EXISTS idx_team_members_email ON team_members(email);",
            "CREATE INDEX IF NOT EXISTS idx_clients_project_id ON clients(project_id);",
            "CREATE INDEX IF NOT EXISTS idx_clients_name ON clients(name);",
            "CREATE INDEX IF NOT EXISTS idx_risks_project_id ON risks(project_id);",
            "CREATE INDEX IF NOT EXISTS idx_risks_priority ON risks(priority);",
            "CREATE INDEX IF NOT EXISTS idx_risks_status ON risks(status);",
            "CREATE INDEX IF NOT EXISTS idx_lessons_learned_project_id ON lessons_learned(project_id);",
            "CREATE INDEX IF NOT EXISTS idx_lessons_learned_category ON lessons_learned(category);",
            "CREATE INDEX IF NOT EXISTS idx_next_steps_project_id ON next_steps(project_id);",
            "CREATE INDEX IF NOT EXISTS idx_next_steps_status ON next_steps(status);",
            "CREATE INDEX IF NOT EXISTS idx_next_steps_due_date ON next_steps(due_date);"
        ]
        
        try:
            # Executar criação das tabelas
            for sql in create_tables_sql:
                logger.info(f"Executando: {sql[:50]}...")
                await self.session.execute(text(sql))
            
            # Executar criação dos índices
            for sql in create_indexes_sql:
                logger.info(f"Executando: {sql[:50]}...")
                await self.session.execute(text(sql))
            
            await self.session.commit()
            logger.info("Todas as tabelas e índices foram criados com sucesso!")
            
        except Exception as e:
            logger.error(f"Erro ao criar tabelas: {e}")
            await self.session.rollback()
            raise
    
    async def add_foreign_key_constraints(self):
        """Adiciona constraints de chave estrangeira se necessário."""
        logger.info("Adicionando constraints de chave estrangeira...")
        
        constraints_sql = [
            # Adicionar portfolio_id aos projetos se não existir
            """
            DO $$ 
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'projects' AND column_name = 'portfolio_id'
                ) THEN
                    ALTER TABLE projects ADD COLUMN portfolio_id INTEGER REFERENCES portfolios(id);
                END IF;
            END $$;
            """,
            
            # Adicionar is_active aos portfolios se não existir
            """
            DO $$ 
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'portfolios' AND column_name = 'is_active'
                ) THEN
                    ALTER TABLE portfolios ADD COLUMN is_active BOOLEAN DEFAULT TRUE NOT NULL;
                END IF;
            END $$;
            """
        ]
        
        try:
            for sql in constraints_sql:
                logger.info("Executando constraint...")
                await self.session.execute(text(sql))
            
            await self.session.commit()
            logger.info("Constraints adicionadas com sucesso!")
            
        except Exception as e:
            logger.error(f"Erro ao adicionar constraints: {e}")
            await self.session.rollback()
            raise

async def run_database_migration():
    """Função principal para executar a migração do banco."""
    async for session in get_async_session():
        migration = DatabaseMigration(session)
        await migration.create_new_tables()
        await migration.add_foreign_key_constraints()
        break

if __name__ == "__main__":
    asyncio.run(run_database_migration())
