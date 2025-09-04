"""
Script para validar a migração de dados.

Este script verifica se:
1. Todas as novas tabelas foram criadas
2. Os dados foram migrados corretamente
3. Os relacionamentos estão funcionando
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Dict, Any

# Adicionar o diretório raiz ao path para imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy import text, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.models.portfolio import Portfolio
from app.models.team_member import TeamMember
from app.models.client import Client
from app.models.risk import Risk
from app.models.lesson_learned import LessonLearned
from app.models.next_step import NextStep
from app.models.project import Project

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MigrationValidator:
    """Classe para validar a migração."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.validation_results = {
            'tables_created': False,
            'portfolios_migrated': False,
            'team_members_migrated': False,
            'clients_migrated': False,
            'risks_migrated': False,
            'relationships_working': False,
            'errors': []
        }
    
    async def validate_migration(self):
        """Executa toda a validação."""
        logger.info("Iniciando validação da migração...")
        
        try:
            # 1. Validar criação das tabelas
            await self.validate_tables_created()
            
            # 2. Validar migração de portfólios
            await self.validate_portfolios_migration()
            
            # 3. Validar migração de membros da equipe
            await self.validate_team_members_migration()
            
            # 4. Validar migração de clientes
            await self.validate_clients_migration()
            
            # 5. Validar migração de riscos
            await self.validate_risks_migration()
            
            # 6. Validar relacionamentos
            await self.validate_relationships()
            
            # Imprimir resultados
            self.print_validation_results()
            
        except Exception as e:
            logger.error(f"Erro durante a validação: {e}")
            self.validation_results['errors'].append(str(e))
            raise
    
    async def validate_tables_created(self):
        """Valida se todas as novas tabelas foram criadas."""
        logger.info("Validando criação das tabelas...")
        
        required_tables = [
            'portfolios',
            'team_members', 
            'clients',
            'risks',
            'lessons_learned',
            'next_steps'
        ]
        
        for table in required_tables:
            result = await self.session.execute(
                text(f"""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = '{table}'
                    );
                """)
            )
            exists = result.scalar()
            
            if not exists:
                error_msg = f"Tabela '{table}' não foi criada"
                logger.error(error_msg)
                self.validation_results['errors'].append(error_msg)
                return
        
        self.validation_results['tables_created'] = True
        logger.info("✅ Todas as tabelas foram criadas com sucesso!")
    
    async def validate_portfolios_migration(self):
        """Valida a migração de portfólios."""
        logger.info("Validando migração de portfólios...")
        
        # Contar portfólios criados
        result = await self.session.execute(select(func.count(Portfolio.id)))
        portfolio_count = result.scalar()
        
        if portfolio_count == 0:
            error_msg = "Nenhum portfólio foi migrado"
            logger.error(error_msg)
            self.validation_results['errors'].append(error_msg)
            return
        
        # Verificar se há projetos com portfolio definido
        result = await self.session.execute(
            select(func.count(Project.id))
            .where(Project.portfolio.isnot(None))
            .where(Project.portfolio != "")
        )
        projects_with_portfolio = result.scalar()
        
        if projects_with_portfolio > 0 and portfolio_count == 0:
            error_msg = "Projetos com portfolio definido mas nenhum portfólio migrado"
            logger.error(error_msg)
            self.validation_results['errors'].append(error_msg)
            return
        
        self.validation_results['portfolios_migrated'] = True
        logger.info(f"✅ {portfolio_count} portfólios migrados com sucesso!")
    
    async def validate_team_members_migration(self):
        """Valida a migração de membros da equipe."""
        logger.info("Validando migração de membros da equipe...")
        
        # Contar team members criados
        result = await self.session.execute(select(func.count(TeamMember.id)))
        team_member_count = result.scalar()
        
        # Contar project members existentes
        result = await self.session.execute(
            text("SELECT COUNT(*) FROM project_members")
        )
        project_member_count = result.scalar()
        
        if project_member_count > 0 and team_member_count == 0:
            error_msg = "Project members existem mas nenhum team member foi migrado"
            logger.error(error_msg)
            self.validation_results['errors'].append(error_msg)
            return
        
        self.validation_results['team_members_migrated'] = True
        logger.info(f"✅ {team_member_count} membros da equipe migrados com sucesso!")
    
    async def validate_clients_migration(self):
        """Valida a migração de clientes."""
        logger.info("Validando migração de clientes...")
        
        # Contar clientes criados
        result = await self.session.execute(select(func.count(Client.id)))
        client_count = result.scalar()
        
        # Contar projetos existentes
        result = await self.session.execute(select(func.count(Project.id)))
        project_count = result.scalar()
        
        if project_count > 0 and client_count == 0:
            error_msg = "Projetos existem mas nenhum cliente foi criado"
            logger.error(error_msg)
            self.validation_results['errors'].append(error_msg)
            return
        
        self.validation_results['clients_migrated'] = True
        logger.info(f"✅ {client_count} clientes criados com sucesso!")
    
    async def validate_risks_migration(self):
        """Valida a migração de riscos."""
        logger.info("Validando migração de riscos...")
        
        # Contar riscos criados
        result = await self.session.execute(select(func.count(Risk.id)))
        risk_count = result.scalar()
        
        # Contar projetos existentes
        result = await self.session.execute(select(func.count(Project.id)))
        project_count = result.scalar()
        
        if project_count > 0 and risk_count == 0:
            error_msg = "Projetos existem mas nenhum risco foi criado"
            logger.error(error_msg)
            self.validation_results['errors'].append(error_msg)
            return
        
        self.validation_results['risks_migrated'] = True
        logger.info(f"✅ {risk_count} riscos criados com sucesso!")
    
    async def validate_relationships(self):
        """Valida se os relacionamentos estão funcionando."""
        logger.info("Validando relacionamentos...")
        
        try:
            # Testar relacionamento Portfolio -> Projects
            result = await self.session.execute(
                select(Portfolio)
                .options(selectinload(Portfolio.projects))
                .limit(1)
            )
            portfolio = result.scalar_one_or_none()
            
            if portfolio and hasattr(portfolio, 'projects'):
                logger.info("✅ Relacionamento Portfolio -> Projects funcionando")
            
            # Testar relacionamento Project -> TeamMembers
            result = await self.session.execute(
                select(Project)
                .options(selectinload(Project.team_members))
                .limit(1)
            )
            project = result.scalar_one_or_none()
            
            if project and hasattr(project, 'team_members'):
                logger.info("✅ Relacionamento Project -> TeamMembers funcionando")
            
            # Testar relacionamento Project -> Clients
            if project and hasattr(project, 'clients'):
                logger.info("✅ Relacionamento Project -> Clients funcionando")
            
            # Testar relacionamento Project -> Risks
            if project and hasattr(project, 'risks'):
                logger.info("✅ Relacionamento Project -> Risks funcionando")
            
            self.validation_results['relationships_working'] = True
            logger.info("✅ Todos os relacionamentos estão funcionando!")
            
        except Exception as e:
            error_msg = f"Erro ao validar relacionamentos: {e}"
            logger.error(error_msg)
            self.validation_results['errors'].append(error_msg)
    
    def print_validation_results(self):
        """Imprime os resultados da validação."""
        logger.info("=== RESULTADOS DA VALIDAÇÃO ===")
        
        checks = [
            ('Tabelas criadas', self.validation_results['tables_created']),
            ('Portfólios migrados', self.validation_results['portfolios_migrated']),
            ('Membros da equipe migrados', self.validation_results['team_members_migrated']),
            ('Clientes migrados', self.validation_results['clients_migrated']),
            ('Riscos migrados', self.validation_results['risks_migrated']),
            ('Relacionamentos funcionando', self.validation_results['relationships_working'])
        ]
        
        for check_name, status in checks:
            status_icon = "✅" if status else "❌"
            logger.info(f"{status_icon} {check_name}: {'PASSOU' if status else 'FALHOU'}")
        
        if self.validation_results['errors']:
            logger.warning(f"❌ {len(self.validation_results['errors'])} erros encontrados:")
            for error in self.validation_results['errors']:
                logger.warning(f"  - {error}")
        else:
            logger.info("🎉 Validação concluída sem erros!")

async def run_validation():
    """Função principal para executar a validação."""
    async for session in get_async_session():
        validator = MigrationValidator(session)
        await validator.validate_migration()
        break

if __name__ == "__main__":
    asyncio.run(run_validation())
