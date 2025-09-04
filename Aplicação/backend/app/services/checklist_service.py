"""
ChecklistGroup service for checklist management operations.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.models.checklist import ChecklistGroup
from app.models.project import Project
from app.schemas.checklist import ChecklistGroupCreate, ChecklistGroupUpdate

class ChecklistService:
    """Service for checklist management operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_checklist(self, checklist_data: ChecklistGroupCreate, user_id: int) -> ChecklistGroup:
        """
        Create a new checklist.
        
        Args:
            checklist_data: ChecklistGroup creation data
            user_id: ID of the user creating the checklist
            
        Returns:
            Created checklist object
        """
        try:
            # Verify project ownership
            project = await self._get_user_project(checklist_data.project_id, user_id)
            if not project:
                raise ValueError("Project not found or access denied")
            
            checklist = ChecklistGroup(
                title=checklist_data.title,
                description=checklist_data.description,
                project_id=checklist_data.project_id,
                created_by=user_id
            )
            
            self.session.add(checklist)
            await self.session.commit()
            await self.session.refresh(checklist)
            
            return checklist
            
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def get_checklist_by_id(self, checklist_id: int, user_id: int) -> Optional[ChecklistGroup]:
        """
        Get checklist by ID for a specific user.
        
        Args:
            checklist_id: ChecklistGroup ID
            user_id: User ID
            
        Returns:
            ChecklistGroup object if found and accessible, None otherwise
        """
        try:
            stmt = select(ChecklistGroup).join(Project).where(
                and_(
                    ChecklistGroup.id == checklist_id,
                    Project.owner_id == user_id
                )
            ).options(
                selectinload(ChecklistGroup.action_items)
            )
            
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
            
        except Exception:
            return None
    
    async def get_project_checklists(self, project_id: int, user_id: int) -> List[ChecklistGroup]:
        """
        Get all checklists for a project.
        
        Args:
            project_id: Project ID
            user_id: User ID
            
        Returns:
            List of checklist objects
        """
        try:
            # Verify project ownership
            project = await self._get_user_project(project_id, user_id)
            if not project:
                return []
            
            stmt = select(ChecklistGroup).where(
                ChecklistGroup.project_id == project_id
            ).options(
                selectinload(ChecklistGroup.action_items)
            )
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
            
        except Exception:
            return []
    
    async def update_checklist(self, checklist_id: int, user_id: int, checklist_data: ChecklistGroupUpdate) -> Optional[ChecklistGroup]:
        """
        Update checklist information.
        
        Args:
            checklist_id: ChecklistGroup ID
            user_id: User ID
            checklist_data: ChecklistGroup update data
            
        Returns:
            Updated checklist object if successful, None otherwise
        """
        try:
            checklist = await self.get_checklist_by_id(checklist_id, user_id)
            if not checklist:
                return None
            
            # Update fields
            update_data = checklist_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(checklist, field):
                    setattr(checklist, field, value)
            
            await self.session.commit()
            await self.session.refresh(checklist)
            
            return checklist
            
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def delete_checklist(self, checklist_id: int, user_id: int) -> bool:
        """
        Delete a checklist.
        
        Args:
            checklist_id: ChecklistGroup ID
            user_id: User ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            checklist = await self.get_checklist_by_id(checklist_id, user_id)
            if not checklist:
                return False
            
            await self.session.delete(checklist)
            await self.session.commit()
            
            return True
            
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def get_checklist_statistics(self, project_id: int, user_id: int) -> dict:
        """
        Get checklist statistics for a project.
        
        Args:
            project_id: Project ID
            user_id: User ID
            
        Returns:
            Dictionary with checklist statistics
        """
        try:
            # Verify project ownership
            project = await self._get_user_project(project_id, user_id)
            if not project:
                return {"total_checklists": 0, "completed_checklists": 0, "completion_rate": 0}
            
            # Total checklists
            total_stmt = select(ChecklistGroup).where(ChecklistGroup.project_id == project_id)
            total_result = await self.session.execute(total_stmt)
            total_checklists = len(total_result.scalars().all())
            
            # Completed checklists (assuming completion is based on action items)
            # This would need to be implemented based on business logic
            completed_checklists = 0  # Placeholder
            
            return {
                "total_checklists": total_checklists,
                "completed_checklists": completed_checklists,
                "completion_rate": (completed_checklists / total_checklists * 100) if total_checklists > 0 else 0
            }
            
        except Exception:
            return {
                "total_checklists": 0,
                "completed_checklists": 0,
                "completion_rate": 0
            }
    
    async def _get_user_project(self, project_id: int, user_id: int) -> Optional[Project]:
        """
        Get project if user has access to it.
        
        Args:
            project_id: Project ID
            user_id: User ID
            
        Returns:
            Project object if accessible, None otherwise
        """
        try:
            stmt = select(Project).where(
                and_(
                    Project.id == project_id,
                    Project.owner_id == user_id
                )
            )
            
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
            
        except Exception:
            return None
