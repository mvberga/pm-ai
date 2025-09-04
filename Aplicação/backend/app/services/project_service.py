"""
Project service for project management operations.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate

class ProjectService:
    """Service for project management operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_project(self, project_data: ProjectCreate, user_id: int) -> Project:
        """
        Create a new project.
        
        Args:
            project_data: Project creation data
            user_id: ID of the user creating the project
            
        Returns:
            Created project object
        """
        try:
            project = Project(
                name=project_data.name,
                description=project_data.description,
                status=project_data.status,
                start_date=project_data.start_date,
                end_date=project_data.end_date,
                owner_id=user_id
            )
            
            self.session.add(project)
            await self.session.commit()
            await self.session.refresh(project)
            
            return project
            
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def get_project_by_id(self, project_id: int, user_id: int) -> Optional[Project]:
        """
        Get project by ID for a specific user.
        
        Args:
            project_id: Project ID
            user_id: User ID
            
        Returns:
            Project object if found and accessible, None otherwise
        """
        try:
            stmt = select(Project).where(
                and_(
                    Project.id == project_id,
                    Project.owner_id == user_id
                )
            ).options(selectinload(Project.checklists))
            
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
            
        except Exception:
            return None
    
    async def get_user_projects(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        """
        Get all projects for a user with pagination.
        
        Args:
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of project objects
        """
        try:
            stmt = select(Project).where(
                Project.owner_id == user_id
            ).offset(skip).limit(limit).options(
                selectinload(Project.checklists)
            )
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
            
        except Exception:
            return []
    
    async def update_project(self, project_id: int, user_id: int, project_data: ProjectUpdate) -> Optional[Project]:
        """
        Update project information.
        
        Args:
            project_id: Project ID
            user_id: User ID
            project_data: Project update data
            
        Returns:
            Updated project object if successful, None otherwise
        """
        try:
            project = await self.get_project_by_id(project_id, user_id)
            if not project:
                return None
            
            # Update fields
            update_data = project_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(project, field):
                    setattr(project, field, value)
            
            await self.session.commit()
            await self.session.refresh(project)
            
            return project
            
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def delete_project(self, project_id: int, user_id: int) -> bool:
        """
        Delete a project.
        
        Args:
            project_id: Project ID
            user_id: User ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            project = await self.get_project_by_id(project_id, user_id)
            if not project:
                return False
            
            await self.session.delete(project)
            await self.session.commit()
            
            return True
            
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def get_project_statistics(self, user_id: int) -> dict:
        """
        Get project statistics for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with project statistics
        """
        try:
            # Total projects
            total_stmt = select(Project).where(Project.owner_id == user_id)
            total_result = await self.session.execute(total_stmt)
            total_projects = len(total_result.scalars().all())
            
            # Active projects
            active_stmt = select(Project).where(
                and_(
                    Project.owner_id == user_id,
                    Project.status == "active"
                )
            )
            active_result = await self.session.execute(active_stmt)
            active_projects = len(active_result.scalars().all())
            
            # Completed projects
            completed_stmt = select(Project).where(
                and_(
                    Project.owner_id == user_id,
                    Project.status == "completed"
                )
            )
            completed_result = await self.session.execute(completed_stmt)
            completed_projects = len(completed_result.scalars().all())
            
            return {
                "total_projects": total_projects,
                "active_projects": active_projects,
                "completed_projects": completed_projects,
                "completion_rate": (completed_projects / total_projects * 100) if total_projects > 0 else 0
            }
            
        except Exception:
            return {
                "total_projects": 0,
                "active_projects": 0,
                "completed_projects": 0,
                "completion_rate": 0
            }
    
    async def search_projects(self, user_id: int, query: str, skip: int = 0, limit: int = 100) -> List[Project]:
        """
        Search projects by name or description.
        
        Args:
            user_id: User ID
            query: Search query
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching project objects
        """
        try:
            search_term = f"%{query}%"
            stmt = select(Project).where(
                and_(
                    Project.owner_id == user_id,
                    (Project.name.ilike(search_term) | Project.description.ilike(search_term))
                )
            ).offset(skip).limit(limit).options(
                selectinload(Project.checklists)
            )
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
            
        except Exception:
            return []
