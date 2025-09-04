"""
Team member repository for data access operations.
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.models.team_member import TeamMember
from app.models.project import Project
from .base_repository import BaseRepository

class TeamMemberRepository(BaseRepository[TeamMember]):
    """Repository for team member data access operations."""
    
    def __init__(self, session: AsyncSession):
        super().__init__(TeamMember, session)
    
    async def get_by_project(self, project_id: int) -> List[TeamMember]:
        """Get all team members for a project."""
        query = select(TeamMember).where(TeamMember.project_id == project_id)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_user(self, user_id: int) -> List[TeamMember]:
        """Get all team members for a user."""
        query = select(TeamMember).where(TeamMember.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_project_and_user(self, project_id: int, user_id: int) -> Optional[TeamMember]:
        """Get team member by project and user."""
        query = select(TeamMember).where(
            and_(TeamMember.project_id == project_id, TeamMember.user_id == user_id)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
