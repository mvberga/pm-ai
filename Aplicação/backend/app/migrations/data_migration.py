"""
Script de migração de dados para a arquitetura expandida.

Este script migra dados existentes para os novos modelos:
- Portfolio: Cria portfólios baseados nos valores únicos de 'portfolio' nos projetos
- TeamMember: Migra ProjectMember para TeamMember
- Client: Cria clientes baseados em dados existentes
- Risk: Cria riscos iniciais baseados em análise dos projetos
"""

import asyncio
import logging
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, distinct, func
from sqlalchemy.orm import selectinload

from app.db.session import get_async_session
from app.models.user import User
from app.models.project import Project, ProjectMember
from app.models.portfolio import Portfolio
from app.models.team_member import TeamMember, TeamRole
from app.models.client import Client, ClientType, CommunicationLevel
from app.models.risk import Risk, RiskCategory, RiskStatus, RiskPriority

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataMigration:
    """Classe para executar migração de dados."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.migration_stats = {
            'portfolios_created': 0,
            'team_members_migrated': 0,
            'clients_created': 0,
            'risks_created': 0,
            'errors': []
        }
    
    async def run_migration(self):
        """Executa toda a migração de dados."""
        logger.info("Iniciando migração de dados...")
        
        try:
            # 1. Migrar portfólios
            await self.migrate_portfolios()
            
            # 2. Migrar membros da equipe
            await self.migrate_team_members()
            
            # 3. Criar clientes
            await self.migrate_clients()
            
            # 4. Criar riscos iniciais
            await self.migrate_risks()
            
            # Commit das mudanças
            await self.session.commit()
            
            logger.info("Migração concluída com sucesso!")
            self.print_stats()
            
        except Exception as e:
            logger.error(f"Erro durante a migração: {e}")
            await self.session.rollback()
            raise
    
    async def migrate_portfolios(self):
        """Migra portfólios baseados nos valores únicos de 'portfolio' nos projetos."""
        logger.info("Migrando portfólios...")
        
        # Buscar valores únicos de portfolio nos projetos
        result = await self.session.execute(
            select(distinct(Project.portfolio))
            .where(Project.portfolio.isnot(None))
            .where(Project.portfolio != "")
        )
        portfolio_names = [row[0] for row in result.fetchall()]
        
        # Buscar o primeiro usuário como owner padrão
        first_user = await self.session.execute(select(User).limit(1))
        default_owner = first_user.scalar_one_or_none()
        
        if not default_owner:
            logger.warning("Nenhum usuário encontrado. Pulando migração de portfólios.")
            return
        
        for portfolio_name in portfolio_names:
            try:
                # Verificar se o portfólio já existe
                existing = await self.session.execute(
                    select(Portfolio).where(Portfolio.name == portfolio_name)
                )
                if existing.scalar_one_or_none():
                    logger.info(f"Portfólio '{portfolio_name}' já existe. Pulando...")
                    continue
                
                # Criar novo portfólio
                portfolio = Portfolio(
                    name=portfolio_name,
                    description=f"Portfólio migrado automaticamente: {portfolio_name}",
                    owner_id=default_owner.id,
                    created_by=default_owner.id,
                    status="active"
                )
                
                self.session.add(portfolio)
                self.migration_stats['portfolios_created'] += 1
                logger.info(f"Portfólio criado: {portfolio_name}")
                
            except Exception as e:
                error_msg = f"Erro ao criar portfólio '{portfolio_name}': {e}"
                logger.error(error_msg)
                self.migration_stats['errors'].append(error_msg)
        
        await self.session.flush()
    
    async def migrate_team_members(self):
        """Migra ProjectMember para TeamMember."""
        logger.info("Migrando membros da equipe...")
        
        # Buscar todos os ProjectMembers
        result = await self.session.execute(
            select(ProjectMember).options(selectinload(ProjectMember.project))
        )
        project_members = result.scalars().all()
        
        for pm in project_members:
            try:
                # Verificar se já existe um TeamMember para este projeto e usuário
                existing = await self.session.execute(
                    select(TeamMember)
                    .where(TeamMember.project_id == pm.project_id)
                    .where(TeamMember.name == pm.user.full_name)
                )
                if existing.scalar_one_or_none():
                    logger.info(f"TeamMember já existe para {pm.user.full_name} no projeto {pm.project_id}")
                    continue
                
                # Mapear role baseado no tipo de membro
                role = self._map_member_role(pm.role or "member")
                
                # Criar TeamMember
                team_member = TeamMember(
                    project_id=pm.project_id,
                    name=pm.user.full_name,
                    email=pm.user.email,
                    role=role,
                    is_active=True
                )
                
                self.session.add(team_member)
                self.migration_stats['team_members_migrated'] += 1
                logger.info(f"TeamMember criado: {pm.user.full_name} para projeto {pm.project_id}")
                
            except Exception as e:
                error_msg = f"Erro ao migrar TeamMember {pm.user.full_name}: {e}"
                logger.error(error_msg)
                self.migration_stats['errors'].append(error_msg)
        
        await self.session.flush()
    
    async def migrate_clients(self):
        """Cria clientes baseados em dados existentes dos projetos."""
        logger.info("Criando clientes...")
        
        # Buscar projetos que não têm clientes
        result = await self.session.execute(
            select(Project).where(~Project.clients.any())
        )
        projects = result.scalars().all()
        
        for project in projects:
            try:
                # Criar cliente baseado no projeto
                client = Client(
                    project_id=project.id,
                    name=f"Cliente - {project.entidade or project.municipio}",
                    email=f"contato@{project.entidade or project.municipio}.com".lower().replace(" ", ""),
                    client_type=ClientType.CORPORATE,
                    communication_level=CommunicationLevel.MANAGERIAL,
                    is_active=True
                )
                
                self.session.add(client)
                self.migration_stats['clients_created'] += 1
                logger.info(f"Cliente criado para projeto {project.id}: {client.name}")
                
            except Exception as e:
                error_msg = f"Erro ao criar cliente para projeto {project.id}: {e}"
                logger.error(error_msg)
                self.migration_stats['errors'].append(error_msg)
        
        await self.session.flush()
    
    async def migrate_risks(self):
        """Cria riscos iniciais baseados em análise dos projetos."""
        logger.info("Criando riscos iniciais...")
        
        # Buscar projetos que não têm riscos
        result = await self.session.execute(
            select(Project).where(~Project.risks.any())
        )
        projects = result.scalars().all()
        
        # Riscos padrão para cada projeto
        default_risks = [
            {
                "title": "Atraso no Cronograma",
                "description": "Risco de atraso no cronograma do projeto devido a imprevistos",
                "category": RiskCategory.OPERATIONAL,
                "priority": RiskPriority.MEDIUM,
                "probability": 0.6,
                "impact": 0.7,
                "mitigation_plan": "Monitorar progresso semanalmente e ajustar recursos conforme necessário"
            },
            {
                "title": "Mudança de Escopo",
                "description": "Risco de mudanças no escopo do projeto durante a execução",
                "category": RiskCategory.BUSINESS,
                "priority": RiskPriority.HIGH,
                "probability": 0.4,
                "impact": 0.8,
                "mitigation_plan": "Definir escopo claramente e implementar processo de controle de mudanças"
            },
            {
                "title": "Problemas Técnicos",
                "description": "Risco de problemas técnicos durante a implementação",
                "category": RiskCategory.TECHNICAL,
                "priority": RiskPriority.MEDIUM,
                "probability": 0.5,
                "impact": 0.6,
                "mitigation_plan": "Realizar testes extensivos e ter plano de contingência técnico"
            }
        ]
        
        for project in projects:
            for risk_data in default_risks:
                try:
                    risk = Risk(
                        project_id=project.id,
                        title=risk_data["title"],
                        description=risk_data["description"],
                        category=risk_data["category"],
                        status=RiskStatus.IDENTIFIED,
                        priority=risk_data["priority"],
                        probability=risk_data["probability"],
                        impact=risk_data["impact"],
                        mitigation_plan=risk_data["mitigation_plan"]
                    )
                    
                    self.session.add(risk)
                    self.migration_stats['risks_created'] += 1
                    logger.info(f"Risco criado para projeto {project.id}: {risk.title}")
                    
                except Exception as e:
                    error_msg = f"Erro ao criar risco para projeto {project.id}: {e}"
                    logger.error(error_msg)
                    self.migration_stats['errors'].append(error_msg)
        
        await self.session.flush()
    
    def _map_member_role(self, old_role: str) -> TeamRole:
        """Mapeia roles antigas para novas roles."""
        role_mapping = {
            "manager": TeamRole.PROJECT_MANAGER,
            "project_manager": TeamRole.PROJECT_MANAGER,
            "developer": TeamRole.DEVELOPER,
            "dev": TeamRole.DEVELOPER,
            "designer": TeamRole.DESIGNER,
            "analyst": TeamRole.ANALYST,
            "tester": TeamRole.TESTER,
            "test": TeamRole.TESTER,
            "consultant": TeamRole.CONSULTANT,
            "consultor": TeamRole.CONSULTANT,
        }
        
        return role_mapping.get(old_role.lower(), TeamRole.DEVELOPER)
    
    def print_stats(self):
        """Imprime estatísticas da migração."""
        logger.info("=== ESTATÍSTICAS DA MIGRAÇÃO ===")
        logger.info(f"Portfólios criados: {self.migration_stats['portfolios_created']}")
        logger.info(f"Membros da equipe migrados: {self.migration_stats['team_members_migrated']}")
        logger.info(f"Clientes criados: {self.migration_stats['clients_created']}")
        logger.info(f"Riscos criados: {self.migration_stats['risks_created']}")
        
        if self.migration_stats['errors']:
            logger.warning(f"Erros encontrados: {len(self.migration_stats['errors'])}")
            for error in self.migration_stats['errors']:
                logger.warning(f"  - {error}")
        else:
            logger.info("Nenhum erro encontrado!")

async def run_data_migration():
    """Função principal para executar a migração."""
    async for session in get_async_session():
        migration = DataMigration(session)
        await migration.run_migration()
        break

if __name__ == "__main__":
    asyncio.run(run_data_migration())
