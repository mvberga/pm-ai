"""
ChecklistGroup repository for checklist data access operations.
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload

from app.models.checklist import ChecklistGroup
from app.models.project import Project
from .base_repository import BaseRepository

class ChecklistRepository(BaseRepository[ChecklistGroup]):
    """Repository for checklist data access operations."""
    
    def __init__(self, session: AsyncSession):
        super().__init__(ChecklistGroup, session)
    
    async def get_by_project(self, project_id: int, skip: int = 0, limit: int = 100) -> List[ChecklistGroup]:
        """
        Get checklists by project ID.
        
        Args:
            project_id: Project ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of checklist instances
        """
        try:
            stmt = select(ChecklistGroup).where(
                ChecklistGroup.project_id == project_id
            ).options(
                selectinload(ChecklistGroup.action_items)
            ).offset(skip).limit(limit)
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def get_by_user_project(self, project_id: int, user_id: int, skip: int = 0, limit: int = 100) -> List[ChecklistGroup]:
        """
        Get checklists by project ID for a specific user (verify ownership).
        
        Args:
            project_id: Project ID
            user_id: User ID (project owner)
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of checklist instances
        """
        try:
            stmt = select(ChecklistGroup).join(Project).where(
                and_(
                    ChecklistGroup.project_id == project_id,
                    Project.owner_id == user_id
                )
            ).options(
                selectinload(ChecklistGroup.action_items)
            ).offset(skip).limit(limit)
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def get_checklist_with_action_items(self, checklist_id: int, user_id: int) -> Optional[ChecklistGroup]:
        """
        Get checklist with all its action items (verify user access).
        
        Args:
            checklist_id: ChecklistGroup ID
            user_id: User ID (project owner)
            
        Returns:
            ChecklistGroup instance with action items if found, None otherwise
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
    
    async def search_checklists(self, query: str, project_id: int, user_id: int, skip: int = 0, limit: int = 100) -> List[ChecklistGroup]:
        """
        Search checklists by title or description for a specific project and user.
        
        Args:
            query: Search query
            project_id: Project ID
            user_id: User ID (project owner)
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching checklist instances
        """
        try:
            search_term = f"%{query}%"
            stmt = select(ChecklistGroup).join(Project).where(
                and_(
                    ChecklistGroup.project_id == project_id,
                    Project.owner_id == user_id,
                    or_(
                        ChecklistGroup.title.ilike(search_term),
                        ChecklistGroup.description.ilike(search_term)
                    )
                )
            ).options(
                selectinload(ChecklistGroup.action_items)
            ).offset(skip).limit(limit)
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def get_checklist_statistics(self, project_id: int, user_id: int) -> dict:
        """
        Get checklist statistics for a specific project.
        
        Args:
            project_id: Project ID
            user_id: User ID (project owner)
            
        Returns:
            Dictionary with checklist statistics
        """
        try:
            # Verify project ownership
            project_stmt = select(Project).where(
                and_(
                    Project.id == project_id,
                    Project.owner_id == user_id
                )
            )
            project_result = await self.session.execute(project_stmt)
            if not project_result.scalar_one_or_none():
                return {
                    "total_checklists": 0,
                    "completed_checklists": 0,
                    "completion_rate": 0
                }
            
            # Total checklists
            total_checklists = await self.count(project_id=project_id)
            
            # For now, we'll consider a checklist completed if all its action items are completed
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
    
    async def get_recent_checklists(self, project_id: int, user_id: int, limit: int = 5) -> List[ChecklistGroup]:
        """
        Get recently created checklists for a specific project.
        
        Args:
            project_id: Project ID
            user_id: User ID (project owner)
            limit: Maximum number of records to return
            
        Returns:
            List of recent checklist instances
        """
        try:
            stmt = select(ChecklistGroup).join(Project).where(
                and_(
                    ChecklistGroup.project_id == project_id,
                    Project.owner_id == user_id
                )
            ).order_by(
                ChecklistGroup.created_at.desc()
            ).limit(limit)
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def delete_by_project(self, project_id: int, user_id: int) -> int:
        """
        Delete all checklists for a specific project (verify ownership).
        
        Args:
            project_id: Project ID
            user_id: User ID (project owner)
            
        Returns:
            Number of deleted checklists
        """
        try:
            # Verify project ownership
            project_stmt = select(Project).where(
                and_(
                    Project.id == project_id,
                    Project.owner_id == user_id
                )
            )
            project_result = await self.session.execute(project_stmt)
            if not project_result.scalar_one_or_none():
                return 0
            
            # Get checklists to delete
            checklists_stmt = select(ChecklistGroup).where(ChecklistGroup.project_id == project_id)
            checklists_result = await self.session.execute(checklists_stmt)
            checklists = checklists_result.scalars().all()
            
            # Delete checklists
            for checklist in checklists:
                await self.session.delete(checklist)
            
            await self.session.commit()
            return len(checklists)
        except Exception as e:
            await self.session.rollback()
            raise e
