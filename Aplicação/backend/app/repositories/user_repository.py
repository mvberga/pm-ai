"""
User repository for user data access operations.
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.user import User
from .base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    """Repository for user data access operations."""
    
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email address.
        
        Args:
            email: User email address
            
        Returns:
            User instance if found, None otherwise
        """
        try:
            stmt = select(User).where(User.email == email)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception:
            return None
    
    async def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all active users.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of active user instances
        """
        try:
            stmt = select(User).where(
                User.is_active == True
            ).offset(skip).limit(limit)
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def get_inactive_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all inactive users.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of inactive user instances
        """
        try:
            stmt = select(User).where(
                User.is_active == False
            ).offset(skip).limit(limit)
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def search_users(self, query: str, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Search users by name or email.
        
        Args:
            query: Search query
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching user instances
        """
        try:
            search_term = f"%{query}%"
            stmt = select(User).where(
                (User.full_name.ilike(search_term) | User.email.ilike(search_term))
            ).offset(skip).limit(limit)
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def activate_user(self, user_id: int) -> bool:
        """
        Activate a user account.
        
        Args:
            user_id: User ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user = await self.get_by_id(user_id)
            if not user:
                return False
            
            user.is_active = True
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def deactivate_user(self, user_id: int) -> bool:
        """
        Deactivate a user account.
        
        Args:
            user_id: User ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user = await self.get_by_id(user_id)
            if not user:
                return False
            
            user.is_active = False
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def update_password(self, user_id: int, hashed_password: str) -> bool:
        """
        Update user password.
        
        Args:
            user_id: User ID
            hashed_password: New hashed password
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user = await self.get_by_id(user_id)
            if not user:
                return False
            
            user.hashed_password = hashed_password
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def get_user_statistics(self) -> dict:
        """
        Get user statistics.
        
        Returns:
            Dictionary with user statistics
        """
        try:
            # Total users
            total_users = await self.count()
            
            # Active users
            active_users = await self.count(is_active=True)
            
            # Inactive users
            inactive_users = await self.count(is_active=False)
            
            return {
                "total_users": total_users,
                "active_users": active_users,
                "inactive_users": inactive_users,
                "activation_rate": (active_users / total_users * 100) if total_users > 0 else 0
            }
        except Exception:
            return {
                "total_users": 0,
                "active_users": 0,
                "inactive_users": 0,
                "activation_rate": 0
            }
