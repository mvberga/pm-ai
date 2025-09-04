"""
Service para lógica de negócio de Risk
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.risk import Risk, RiskCategory, RiskStatus, RiskPriority
from app.schemas.risk import (
    RiskCreate, RiskUpdate, RiskSummary, RiskAnalysis,
    RiskBulkCreate, RiskBulkUpdate
)
from app.repositories.risk_repository import RiskRepository
from app.repositories.project_repository import ProjectRepository
from app.core.exceptions import NotFoundError, ValidationError


class RiskService:
    """Service para operações de Risk"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.risk_repo = RiskRepository(db)
        self.project_repo = ProjectRepository(db)
    
    async def create_risk(self, risk_data: RiskCreate, user_id: int) -> Risk:
        """
        Cria um novo risco
        
        Args:
            risk_data: Dados do risco
            user_id: ID do usuário (para verificar permissão no projeto)
            
        Returns:
            Risk criado
            
        Raises:
            ValidationError: Se o projeto não existe ou usuário não tem permissão
        """
        # Verificar se o projeto existe e o usuário tem permissão
        project = await self.project_repo.get(risk_data.project_id)
        if not project:
            raise ValidationError(f"Projeto com ID {risk_data.project_id} não encontrado")
        
        # Verificar se o usuário tem permissão no projeto
        if project.owner_id != user_id:
            raise ValidationError("Usuário não tem permissão para adicionar riscos a este projeto")
        
        # Criar o risco
        risk_dict = risk_data.model_dump()
        risk = await self.risk_repo.create(risk_dict)
        
        # Calcular e atualizar o risk score
        risk_score = risk.probability * risk.impact
        await self.risk_repo.update(risk.id, {"risk_score": risk_score})
        
        return risk
    
    async def get_risk(self, risk_id: int, user_id: int) -> Optional[Risk]:
        """
        Busca um risco por ID
        
        Args:
            risk_id: ID do risco
            user_id: ID do usuário (para verificar permissão)
            
        Returns:
            Risk encontrado ou None
        """
        risk = await self.risk_repo.get(risk_id)
        if not risk:
            return None
        
        # Verificar se o usuário tem permissão no projeto
        project = await self.project_repo.get(risk.project_id)
        if not project or project.owner_id != user_id:
            return None
        
        return risk
    
    async def update_risk(self, risk_id: int, risk_data: RiskUpdate, user_id: int) -> Optional[Risk]:
        """
        Atualiza um risco
        
        Args:
            risk_id: ID do risco
            risk_data: Dados para atualização
            user_id: ID do usuário
            
        Returns:
            Risk atualizado ou None
        """
        risk = await self.get_risk(risk_id, user_id)
        if not risk:
            return None
        
        # Atualizar o risco
        update_data = risk_data.model_dump(exclude_unset=True)
        
        # Recalcular risk score se probability ou impact foram alterados
        if "probability" in update_data or "impact" in update_data:
            new_probability = update_data.get("probability", risk.probability)
            new_impact = update_data.get("impact", risk.impact)
            update_data["risk_score"] = new_probability * new_impact
        
        return await self.risk_repo.update(risk_id, update_data)
    
    async def delete_risk(self, risk_id: int, user_id: int) -> bool:
        """
        Exclui um risco
        
        Args:
            risk_id: ID do risco
            user_id: ID do usuário
            
        Returns:
            True se excluído com sucesso
        """
        risk = await self.get_risk(risk_id, user_id)
        if not risk:
            return False
        
        return await self.risk_repo.delete(risk_id)
    
    async def get_project_risks(self, project_id: int, user_id: int, include_inactive: bool = False) -> List[RiskSummary]:
        """
        Lista riscos de um projeto
        
        Args:
            project_id: ID do projeto
            user_id: ID do usuário
            include_inactive: Se deve incluir riscos inativos
            
        Returns:
            Lista de riscos
        """
        # Verificar se o usuário tem permissão no projeto
        project = await self.project_repo.get(project_id)
        if not project or project.owner_id != user_id:
            return []
        
        risks = await self.risk_repo.get_by_project(project_id, include_inactive)
        
        return [
            RiskSummary(
                id=risk.id,
                title=risk.title,
                category=risk.category,
                status=risk.status,
                priority=risk.priority,
                risk_score=risk.probability * risk.impact
            )
            for risk in risks
        ]
    
    async def bulk_create_risks(self, bulk_data: RiskBulkCreate, user_id: int) -> List[Risk]:
        """
        Cria múltiplos riscos
        
        Args:
            bulk_data: Dados para criação em lote
            user_id: ID do usuário
            
        Returns:
            Lista de riscos criados
        """
        # Verificar se o projeto existe e o usuário tem permissão
        project = await self.project_repo.get(bulk_data.project_id)
        if not project:
            raise ValidationError(f"Projeto com ID {bulk_data.project_id} não encontrado")
        
        if project.owner_id != user_id:
            raise ValidationError("Usuário não tem permissão para adicionar riscos a este projeto")
        
        created_risks = []
        
        for risk_data in bulk_data.risks:
            try:
                # Criar o risco
                risk_dict = risk_data.model_dump()
                risk_dict["project_id"] = bulk_data.project_id
                risk = await self.risk_repo.create(risk_dict)
                
                # Calcular e atualizar o risk score
                risk_score = risk.probability * risk.impact
                await self.risk_repo.update(risk.id, {"risk_score": risk_score})
                
                created_risks.append(risk)
                
            except Exception as e:
                # Log do erro e continuar com os próximos riscos
                print(f"Erro ao criar risco {risk_data.title}: {e}")
                continue
        
        return created_risks
    
    async def bulk_update_risks(self, bulk_data: RiskBulkUpdate, user_id: int) -> List[Risk]:
        """
        Atualiza múltiplos riscos
        
        Args:
            bulk_data: Dados para atualização em lote
            user_id: ID do usuário
            
        Returns:
            Lista de riscos atualizados
        """
        updated_risks = []
        
        for risk_update in bulk_data.risks:
            try:
                risk_id = risk_update.get("id")
                if not risk_id:
                    continue
                
                # Verificar se o risco existe e o usuário tem permissão
                risk = await self.get_risk(risk_id, user_id)
                if not risk:
                    continue
                
                # Atualizar o risco
                update_data = {k: v for k, v in risk_update.items() if k != "id"}
                
                # Recalcular risk score se necessário
                if "probability" in update_data or "impact" in update_data:
                    new_probability = update_data.get("probability", risk.probability)
                    new_impact = update_data.get("impact", risk.impact)
                    update_data["risk_score"] = new_probability * new_impact
                
                updated_risk = await self.risk_repo.update(risk_id, update_data)
                if updated_risk:
                    updated_risks.append(updated_risk)
                
            except Exception as e:
                # Log do erro e continuar com os próximos riscos
                print(f"Erro ao atualizar risco {risk_update.get('id')}: {e}")
                continue
        
        return updated_risks
    
    async def get_risks_by_category(self, project_id: int, category: RiskCategory, user_id: int) -> List[RiskSummary]:
        """
        Lista riscos por categoria
        
        Args:
            project_id: ID do projeto
            category: Categoria dos riscos
            user_id: ID do usuário
            
        Returns:
            Lista de riscos
        """
        # Verificar se o usuário tem permissão no projeto
        project = await self.project_repo.get(project_id)
        if not project or project.owner_id != user_id:
            return []
        
        risks = await self.risk_repo.get_by_project_and_category(project_id, category)
        
        return [
            RiskSummary(
                id=risk.id,
                title=risk.title,
                category=risk.category,
                status=risk.status,
                priority=risk.priority,
                risk_score=risk.probability * risk.impact
            )
            for risk in risks
        ]
    
    async def get_risks_by_priority(self, project_id: int, priority: RiskPriority, user_id: int) -> List[RiskSummary]:
        """
        Lista riscos por prioridade
        
        Args:
            project_id: ID do projeto
            priority: Prioridade dos riscos
            user_id: ID do usuário
            
        Returns:
            Lista de riscos
        """
        # Verificar se o usuário tem permissão no projeto
        project = await self.project_repo.get(project_id)
        if not project or project.owner_id != user_id:
            return []
        
        risks = await self.risk_repo.get_by_project_and_priority(project_id, priority)
        
        return [
            RiskSummary(
                id=risk.id,
                title=risk.title,
                category=risk.category,
                status=risk.status,
                priority=risk.priority,
                risk_score=risk.probability * risk.impact
            )
            for risk in risks
        ]
    
    async def get_risks_by_status(self, project_id: int, status: RiskStatus, user_id: int) -> List[RiskSummary]:
        """
        Lista riscos por status
        
        Args:
            project_id: ID do projeto
            status: Status dos riscos
            user_id: ID do usuário
            
        Returns:
            Lista de riscos
        """
        # Verificar se o usuário tem permissão no projeto
        project = await self.project_repo.get(project_id)
        if not project or project.owner_id != user_id:
            return []
        
        risks = await self.risk_repo.get_by_project_and_status(project_id, status)
        
        return [
            RiskSummary(
                id=risk.id,
                title=risk.title,
                category=risk.category,
                status=risk.status,
                priority=risk.priority,
                risk_score=risk.probability * risk.impact
            )
            for risk in risks
        ]
    
    async def get_high_risk_risks(self, project_id: int, user_id: int, threshold: float = 0.7) -> List[RiskSummary]:
        """
        Lista riscos de alta pontuação
        
        Args:
            project_id: ID do projeto
            user_id: ID do usuário
            threshold: Limite para considerar risco alto (padrão: 0.7)
            
        Returns:
            Lista de riscos de alta pontuação
        """
        # Verificar se o usuário tem permissão no projeto
        project = await self.project_repo.get(project_id)
        if not project or project.owner_id != user_id:
            return []
        
        risks = await self.risk_repo.get_high_risk_risks(project_id, threshold)
        
        return [
            RiskSummary(
                id=risk.id,
                title=risk.title,
                category=risk.category,
                status=risk.status,
                priority=risk.priority,
                risk_score=risk.probability * risk.impact
            )
            for risk in risks
        ]
    
    async def get_risk_analysis(self, project_id: int, user_id: int) -> RiskAnalysis:
        """
        Obtém análise de riscos de um projeto
        
        Args:
            project_id: ID do projeto
            user_id: ID do usuário
            
        Returns:
            Análise de riscos
        """
        # Verificar se o usuário tem permissão no projeto
        project = await self.project_repo.get(project_id)
        if not project or project.owner_id != user_id:
            raise NotFoundError("Projeto não encontrado")
        
        # Obter estatísticas
        total_risks = await self.risk_repo.count_by_project(project_id)
        high_priority_risks = await self.risk_repo.count_by_priority(project_id, RiskPriority.HIGH)
        active_risks = await self.risk_repo.count_by_status(project_id, RiskStatus.ACTIVE)
        average_risk_score = await self.risk_repo.get_average_risk_score(project_id)
        
        # Obter contagens por categoria e status
        risks_by_category = await self.risk_repo.count_by_category(project_id)
        risks_by_status = await self.risk_repo.count_by_status_all(project_id)
        
        return RiskAnalysis(
            total_risks=total_risks,
            high_priority_risks=high_priority_risks,
            active_risks=active_risks,
            average_risk_score=average_risk_score,
            risks_by_category=risks_by_category,
            risks_by_status=risks_by_status
        )
    
    async def update_risk_status(self, risk_id: int, status: RiskStatus, user_id: int) -> Optional[Risk]:
        """
        Atualiza o status de um risco
        
        Args:
            risk_id: ID do risco
            status: Novo status
            user_id: ID do usuário
            
        Returns:
            Risk atualizado ou None
        """
        return await self.update_risk(
            risk_id, 
            RiskUpdate(status=status), 
            user_id
        )
    
    async def update_risk_priority(self, risk_id: int, priority: RiskPriority, user_id: int) -> Optional[Risk]:
        """
        Atualiza a prioridade de um risco
        
        Args:
            risk_id: ID do risco
            priority: Nova prioridade
            user_id: ID do usuário
            
        Returns:
            Risk atualizado ou None
        """
        return await self.update_risk(
            risk_id, 
            RiskUpdate(priority=priority), 
            user_id
        )
