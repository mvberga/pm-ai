"""
Risk repository for data access operations.
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.models.risk import Risk
from app.models.project import Project
from .base_repository import BaseRepository

class RiskRepository(BaseRepository[Risk]):
    """Repository for risk data access operations."""
    
    def __init__(self, session: AsyncSession):
        super().__init__(Risk, session)
    
    async def get_by_project(self, project_id: int) -> List[Risk]:
        """Get all risks for a project."""
        query = select(Risk).where(Risk.project_id == project_id)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_level(self, risk_level: str) -> List[Risk]:
        """Get risks by level."""
        query = select(Risk).where(Risk.risk_level == risk_level)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_status(self, status: str) -> List[Risk]:
        """Get risks by status."""
        query = select(Risk).where(Risk.status == status)
        result = await self.session.execute(query)
        return result.scalars().all()