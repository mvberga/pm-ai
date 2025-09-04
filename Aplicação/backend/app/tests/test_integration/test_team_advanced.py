"""
Testes de integração avançados para endpoints de equipe.
"""

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.team_member import TeamMember, TeamRole
from app.models.project import Project
from app.models.user import User


class TestTeamAdvanced:
    """Testes de integração avançados para equipe."""
    
    async def test_create_team_member_complete_flow(self, client: TestClient, db_session: AsyncSession):
        """Testar fluxo completo de criação de membro da equipe."""
        
        # Primeiro criar um projeto para associar o membro
        project_data = {
            "name": "Projeto para Equipe",
            "description": "Projeto para testar membros da equipe",
            "municipio": "São Paulo",
            "entidade": "Prefeitura",
            "status": "active"
        }
        
        response = client.post(f"{settings.API_V1_STR}/projects", json=project_data)
        assert response.status_code == 201
        project = response.json()
        project_id = project["id"]
        
        # Dados do membro da equipe
        team_member_data = {
            "name": "João Silva",
            "email": "joao.silva@example.com",
            "role": "developer",
            "project_id": project_id,
            "skills": ["Python", "FastAPI", "SQLAlchemy"],
            "availability": 0.8,
            "hourly_rate": 150.00,
            "start_date": "2024-01-01",
            "end_date": "2024-12-31"
        }
        
        # Criar membro da equipe
        response = client.post(f"{settings.API_V1_STR}/team-members", json=team_member_data)
        assert response.status_code == 201
        
        team_member = response.json()
        assert team_member["name"] == team_member_data["name"]
        assert team_member["email"] == team_member_data["email"]
        assert team_member["role"] == team_member_data["role"]
        assert team_member["project_id"] == project_id
        assert team_member["skills"] == team_member_data["skills"]
        assert team_member["availability"] == team_member_data["availability"]
        assert team_member["hourly_rate"] == team_member_data["hourly_rate"]
        
        team_member_id = team_member["id"]
        
        # Verificar se o membro foi criado no banco
        from sqlalchemy import select
        result = await db_session.execute(select(TeamMember).where(TeamMember.id == team_member_id))
        db_member = result.scalar_one_or_none()
        assert db_member is not None
        assert db_member.name == team_member_data["name"]
    
    async def test_team_member_roles_and_permissions(self, client: TestClient, db_session: AsyncSession):
        """Testar diferentes roles e permissões de membros da equipe."""
        
        # Criar projeto
        project_data = {
            "name": "Projeto para Roles",
            "description": "Projeto para testar roles da equipe",
            "municipio": "São Paulo",
            "entidade": "Prefeitura",
            "status": "active"
        }
        
        response = client.post(f"{settings.API_V1_STR}/projects", json=project_data)
        assert response.status_code == 201
        project = response.json()
        project_id = project["id"]
        
        # Criar membros com diferentes roles
        team_members_data = [
            {
                "name": "Gerente de Projeto",
                "email": "gerente@example.com",
                "role": "project_manager",
                "project_id": project_id,
                "skills": ["Gestão", "Planejamento"],
                "availability": 1.0,
                "hourly_rate": 200.00
            },
            {
                "name": "Desenvolvedor Senior",
                "email": "dev.senior@example.com",
                "role": "senior_developer",
                "project_id": project_id,
                "skills": ["Python", "FastAPI", "Docker"],
                "availability": 0.9,
                "hourly_rate": 180.00
            },
            {
                "name": "Desenvolvedor Junior",
                "email": "dev.junior@example.com",
                "role": "junior_developer",
                "project_id": project_id,
                "skills": ["Python", "SQL"],
                "availability": 0.7,
                "hourly_rate": 120.00
            },
            {
                "name": "Analista de QA",
                "email": "qa@example.com",
                "role": "qa_analyst",
                "project_id": project_id,
                "skills": ["Testes", "Automação"],
                "availability": 0.8,
                "hourly_rate": 140.00
            }
        ]
        
        created_members = []
        for member_data in team_members_data:
            response = client.post(f"{settings.API_V1_STR}/team-members", json=member_data)
            assert response.status_code == 201
            created_members.append(response.json())
        
        # Testar listagem de membros por role
        response = client.get(f"{settings.API_V1_STR}/team-members?project_id={project_id}&role=developer")
        assert response.status_code == 200
        
        developers = response.json()
        assert len(developers) == 2  # Senior e Junior
        
        # Testar listagem de membros por disponibilidade
        response = client.get(f"{settings.API_V1_STR}/team-members?project_id={project_id}&min_availability=0.8")
        assert response.status_code == 200
        
        available_members = response.json()
        assert len(available_members) == 3  # Gerente, Senior e QA
    
    async def test_team_member_workload_management(self, client: TestClient, db_session: AsyncSession):
        """Testar gerenciamento de carga de trabalho da equipe."""
        
        # Criar projeto
        project_data = {
            "name": "Projeto para Workload",
            "description": "Projeto para testar carga de trabalho",
            "municipio": "São Paulo",
            "entidade": "Prefeitura",
            "status": "active"
        }
        
        response = client.post(f"{settings.API_V1_STR}/projects", json=project_data)
        assert response.status_code == 201
        project = response.json()
        project_id = project["id"]
        
        # Criar membros com diferentes cargas de trabalho
        team_members_data = [
            {
                "name": "Membro Sobrecarregado",
                "email": "sobrecarregado@example.com",
                "role": "developer",
                "project_id": project_id,
                "skills": ["Python"],
                "availability": 0.3,  # Baixa disponibilidade
                "hourly_rate": 150.00,
                "current_workload": 0.9  # Alta carga
            },
            {
                "name": "Membro Disponível",
                "email": "disponivel@example.com",
                "role": "developer",
                "project_id": project_id,
                "skills": ["Python", "FastAPI"],
                "availability": 0.8,  # Alta disponibilidade
                "hourly_rate": 150.00,
                "current_workload": 0.2  # Baixa carga
            }
        ]
        
        for member_data in team_members_data:
            response = client.post(f"{settings.API_V1_STR}/team-members", json=member_data)
            assert response.status_code == 201
        
        # Testar analytics de carga de trabalho
        response = client.get(f"{settings.API_V1_STR}/team-members/analytics?project_id={project_id}")
        assert response.status_code == 200
        
        analytics = response.json()
        assert "total_members" in analytics
        assert "average_availability" in analytics
        assert "average_workload" in analytics
        assert "overloaded_members" in analytics
        
        # Verificar se os dados estão corretos
        assert analytics["total_members"] == 2
        assert analytics["overloaded_members"] == 1
    
    async def test_team_member_skill_matching(self, client: TestClient, db_session: AsyncSession):
        """Testar correspondência de habilidades da equipe."""
        
        # Criar projeto
        project_data = {
            "name": "Projeto para Skills",
            "description": "Projeto para testar habilidades",
            "municipio": "São Paulo",
            "entidade": "Prefeitura",
            "status": "active"
        }
        
        response = client.post(f"{settings.API_V1_STR}/projects", json=project_data)
        assert response.status_code == 201
        project = response.json()
        project_id = project["id"]
        
        # Criar membros com diferentes habilidades
        team_members_data = [
            {
                "name": "Especialista Python",
                "email": "python@example.com",
                "role": "developer",
                "project_id": project_id,
                "skills": ["Python", "FastAPI", "SQLAlchemy", "Docker"],
                "availability": 0.8,
                "hourly_rate": 180.00
            },
            {
                "name": "Especialista Frontend",
                "email": "frontend@example.com",
                "role": "developer",
                "project_id": project_id,
                "skills": ["React", "TypeScript", "CSS", "HTML"],
                "availability": 0.7,
                "hourly_rate": 160.00
            },
            {
                "name": "Full Stack",
                "email": "fullstack@example.com",
                "role": "developer",
                "project_id": project_id,
                "skills": ["Python", "React", "FastAPI", "TypeScript"],
                "availability": 0.9,
                "hourly_rate": 200.00
            }
        ]
        
        for member_data in team_members_data:
            response = client.post(f"{settings.API_V1_STR}/team-members", json=member_data)
            assert response.status_code == 201
        
        # Testar busca por habilidades específicas
        response = client.get(f"{settings.API_V1_STR}/team-members?project_id={project_id}&skills=Python")
        assert response.status_code == 200
        
        python_members = response.json()
        assert len(python_members) == 2  # Especialista Python e Full Stack
        
        # Testar busca por múltiplas habilidades
        response = client.get(f"{settings.API_V1_STR}/team-members?project_id={project_id}&skills=React,TypeScript")
        assert response.status_code == 200
        
        frontend_members = response.json()
        assert len(frontend_members) == 2  # Especialista Frontend e Full Stack
    
    async def test_team_member_update_flow(self, client: TestClient, db_session: AsyncSession):
        """Testar fluxo de atualização de membro da equipe."""
        
        # Criar projeto
        project_data = {
            "name": "Projeto para Atualização",
            "description": "Projeto para testar atualizações",
            "municipio": "São Paulo",
            "entidade": "Prefeitura",
            "status": "active"
        }
        
        response = client.post(f"{settings.API_V1_STR}/projects", json=project_data)
        assert response.status_code == 201
        project = response.json()
        project_id = project["id"]
        
        # Criar membro da equipe
        team_member_data = {
            "name": "Membro Original",
            "email": "original@example.com",
            "role": "developer",
            "project_id": project_id,
            "skills": ["Python"],
            "availability": 0.5,
            "hourly_rate": 100.00
        }
        
        response = client.post(f"{settings.API_V1_STR}/team-members", json=team_member_data)
        assert response.status_code == 201
        team_member = response.json()
        team_member_id = team_member["id"]
        
        # Atualizar membro da equipe
        update_data = {
            "name": "Membro Atualizado",
            "email": "atualizado@example.com",
            "role": "senior_developer",
            "skills": ["Python", "FastAPI", "Docker"],
            "availability": 0.8,
            "hourly_rate": 150.00
        }
        
        response = client.put(f"{settings.API_V1_STR}/team-members/{team_member_id}", json=update_data)
        assert response.status_code == 200
        
        updated_member = response.json()
        assert updated_member["name"] == update_data["name"]
        assert updated_member["email"] == update_data["email"]
        assert updated_member["role"] == update_data["role"]
        assert updated_member["skills"] == update_data["skills"]
        assert updated_member["availability"] == update_data["availability"]
        assert updated_member["hourly_rate"] == update_data["hourly_rate"]
    
    async def test_team_member_validation_errors(self, client: TestClient, db_session: AsyncSession):
        """Testar validação de dados de membro da equipe."""
        
        # Testar dados inválidos
        invalid_data = {
            "name": "",  # Nome vazio
            "email": "email_invalido",  # Email inválido
            "role": "invalid_role",  # Role inválido
            "availability": 1.5,  # Disponibilidade > 1
            "hourly_rate": -50.00  # Taxa negativa
        }
        
        response = client.post(f"{settings.API_V1_STR}/team-members", json=invalid_data)
        assert response.status_code == 422  # Validation Error
        
        # Testar dados obrigatórios faltando
        incomplete_data = {
            "email": "teste@example.com"
        }
        
        response = client.post(f"{settings.API_V1_STR}/team-members", json=incomplete_data)
        assert response.status_code == 422  # Validation Error
    
    async def test_team_member_not_found(self, client: TestClient, db_session: AsyncSession):
        """Testar cenários de membro da equipe não encontrado."""
        
        # Tentar buscar membro inexistente
        response = client.get(f"{settings.API_V1_STR}/team-members/99999")
        assert response.status_code == 404
        
        # Tentar atualizar membro inexistente
        update_data = {"name": "Nome Atualizado"}
        response = client.put(f"{settings.API_V1_STR}/team-members/99999", json=update_data)
        assert response.status_code == 404
        
        # Tentar excluir membro inexistente
        response = client.delete(f"{settings.API_V1_STR}/team-members/99999")
        assert response.status_code == 404
