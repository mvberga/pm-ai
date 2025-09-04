"""
Client repository for data access operations.
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.models.client import Client
from app.models.project import Project
from .base_repository import BaseRepository

class ClientRepository(BaseRepository[Client]):
    """Repository for client data access operations."""
    
    def __init__(self, session: AsyncSession):
        super().__init__(Client, session)
    
    async def get_by_project(self, project_id: int) -> List[Client]:
        """Get all clients for a project."""
        query = select(Client).where(Client.project_id == project_id)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_email(self, email: str) -> Optional[Client]:
        """Get client by email."""
        query = select(Client).where(Client.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
