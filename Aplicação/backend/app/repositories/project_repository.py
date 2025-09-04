"""
Project repository for project data access operations.
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload

from app.models.project import Project
from app.models.user import User
from .base_repository import BaseRepository

class ProjectRepository(BaseRepository[Project]):
    """Repository for project data access operations."""
    
    def __init__(self, session: AsyncSession):
        super().__init__(Project, session)
    
    async def get_by_owner(self, owner_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        """
        Get projects by owner ID.
        
        Args:
            owner_id: Owner user ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of project instances
        """
        try:
            stmt = select(Project).where(
                Project.owner_id == owner_id
            ).options(
                selectinload(Project.checklists)
            ).offset(skip).limit(limit)
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def get_by_status(self, status: str, owner_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        """
        Get projects by status for a specific owner.
        
        Args:
            status: Project status
            owner_id: Owner user ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of project instances
        """
        try:
            stmt = select(Project).where(
                and_(
                    Project.status == status,
                    Project.owner_id == owner_id
                )
            ).options(
                selectinload(Project.checklists)
            ).offset(skip).limit(limit)
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def search_projects(self, query: str, owner_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        """
        Search projects by name or description for a specific owner.
        
        Args:
            query: Search query
            owner_id: Owner user ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching project instances
        """
        try:
            search_term = f"%{query}%"
            stmt = select(Project).where(
                and_(
                    Project.owner_id == owner_id,
                    or_(
                        Project.name.ilike(search_term),
                        Project.description.ilike(search_term)
                    )
                )
            ).options(
                selectinload(Project.checklists)
            ).offset(skip).limit(limit)
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def get_project_with_checklists(self, project_id: int, owner_id: int) -> Optional[Project]:
        """
        Get project with all its checklists.
        
        Args:
            project_id: Project ID
            owner_id: Owner user ID
            
        Returns:
            Project instance with checklists if found, None otherwise
        """
        try:
            stmt = select(Project).where(
                and_(
                    Project.id == project_id,
                    Project.owner_id == owner_id
                )
            ).options(
                selectinload(Project.checklists).selectinload(Project.checklists.property.mapper.class_.action_items)
            )
            
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception:
            return None
    
    async def get_active_projects(self, owner_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        """
        Get active projects for a specific owner.
        
        Args:
            owner_id: Owner user ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of active project instances
        """
        return await self.get_by_status("active", owner_id, skip, limit)
    
    async def get_completed_projects(self, owner_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        """
        Get completed projects for a specific owner.
        
        Args:
            owner_id: Owner user ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of completed project instances
        """
        return await self.get_by_status("completed", owner_id, skip, limit)
    
    async def get_project_statistics(self, owner_id: int) -> dict:
        """
        Get project statistics for a specific owner.
        
        Args:
            owner_id: Owner user ID
            
        Returns:
            Dictionary with project statistics
        """
        try:
            # Total projects
            total_projects = await self.count(owner_id=owner_id)
            
            # Active projects
            active_projects = await self.count(owner_id=owner_id, status="active")
            
            # Completed projects
            completed_projects = await self.count(owner_id=owner_id, status="completed")
            
            # On hold projects
            on_hold_projects = await self.count(owner_id=owner_id, status="on_hold")
            
            return {
                "total_projects": total_projects,
                "active_projects": active_projects,
                "completed_projects": completed_projects,
                "on_hold_projects": on_hold_projects,
                "completion_rate": (completed_projects / total_projects * 100) if total_projects > 0 else 0
            }
        except Exception:
            return {
                "total_projects": 0,
                "active_projects": 0,
                "completed_projects": 0,
                "on_hold_projects": 0,
                "completion_rate": 0
            }
    
    async def get_recent_projects(self, owner_id: int, limit: int = 5) -> List[Project]:
        """
        Get recently created projects for a specific owner.
        
        Args:
            owner_id: Owner user ID
            limit: Maximum number of records to return
            
        Returns:
            List of recent project instances
        """
        try:
            stmt = select(Project).where(
                Project.owner_id == owner_id
            ).order_by(
                Project.created_at.desc()
            ).limit(limit)
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def update_project_status(self, project_id: int, owner_id: int, status: str) -> bool:
        """
        Update project status.
        
        Args:
            project_id: Project ID
            owner_id: Owner user ID
            status: New status
            
        Returns:
            True if successful, False otherwise
        """
        try:
            project = await self.get_by_id(project_id)
            if not project or project.owner_id != owner_id:
                return False
            
            project.status = status
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            raise e
