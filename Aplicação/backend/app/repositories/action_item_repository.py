"""
Action item repository for action item data access operations.
"""

from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload

from app.models.action_item import ActionItem
from app.models.checklist import ChecklistGroup
from app.models.project import Project
from .base_repository import BaseRepository

class ActionItemRepository(BaseRepository[ActionItem]):
    """Repository for action item data access operations."""
    
    def __init__(self, session: AsyncSession):
        super().__init__(ActionItem, session)
    
    async def get_by_checklist(self, checklist_id: int, skip: int = 0, limit: int = 100) -> List[ActionItem]:
        """
        Get action items by checklist ID.
        
        Args:
            checklist_id: ChecklistGroup ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of action item instances
        """
        try:
            stmt = select(ActionItem).where(
                ActionItem.checklist_id == checklist_id
            ).order_by(
                ActionItem.created_at.desc()
            ).offset(skip).limit(limit)
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def get_by_user_checklist(self, checklist_id: int, user_id: int, skip: int = 0, limit: int = 100) -> List[ActionItem]:
        """
        Get action items by checklist ID for a specific user (verify access).
        
        Args:
            checklist_id: ChecklistGroup ID
            user_id: User ID (project owner)
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of action item instances
        """
        try:
            stmt = select(ActionItem).join(ChecklistGroup).join(Project).where(
                and_(
                    ActionItem.checklist_id == checklist_id,
                    Project.owner_id == user_id
                )
            ).order_by(
                ActionItem.created_at.desc()
            ).offset(skip).limit(limit)
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def get_by_status(self, status: str, user_id: int, skip: int = 0, limit: int = 100) -> List[ActionItem]:
        """
        Get action items by status for a specific user.
        
        Args:
            status: Action item status
            user_id: User ID (project owner)
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of action item instances
        """
        try:
            stmt = select(ActionItem).join(ChecklistGroup).join(Project).where(
                and_(
                    ActionItem.status == status,
                    Project.owner_id == user_id
                )
            ).order_by(
                ActionItem.due_date.asc()
            ).offset(skip).limit(limit)
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def get_by_assignee(self, assigned_to: int, user_id: int, skip: int = 0, limit: int = 100) -> List[ActionItem]:
        """
        Get action items assigned to a specific user.
        
        Args:
            assigned_to: Assigned user ID
            user_id: Project owner ID (for access verification)
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of action item instances
        """
        try:
            stmt = select(ActionItem).join(ChecklistGroup).join(Project).where(
                and_(
                    ActionItem.assigned_to == assigned_to,
                    Project.owner_id == user_id
                )
            ).order_by(
                ActionItem.due_date.asc()
            ).offset(skip).limit(limit)
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def get_overdue_items(self, user_id: int, skip: int = 0, limit: int = 100) -> List[ActionItem]:
        """
        Get overdue action items for a specific user.
        
        Args:
            user_id: User ID (project owner)
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of overdue action item instances
        """
        try:
            now = datetime.now()
            stmt = select(ActionItem).join(ChecklistGroup).join(Project).where(
                and_(
                    Project.owner_id == user_id,
                    ActionItem.status == "pending",
                    ActionItem.due_date < now
                )
            ).order_by(
                ActionItem.due_date.asc()
            ).offset(skip).limit(limit)
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def get_upcoming_items(self, user_id: int, days_ahead: int = 7, skip: int = 0, limit: int = 100) -> List[ActionItem]:
        """
        Get upcoming action items for a specific user.
        
        Args:
            user_id: User ID (project owner)
            days_ahead: Number of days ahead to look
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of upcoming action item instances
        """
        try:
            now = datetime.now()
            future_date = datetime.now().replace(hour=23, minute=59, second=59) + timedelta(days=days_ahead)
            
            stmt = select(ActionItem).join(ChecklistGroup).join(Project).where(
                and_(
                    Project.owner_id == user_id,
                    ActionItem.status == "pending",
                    ActionItem.due_date >= now,
                    ActionItem.due_date <= future_date
                )
            ).order_by(
                ActionItem.due_date.asc()
            ).offset(skip).limit(limit)
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def search_action_items(self, query: str, user_id: int, skip: int = 0, limit: int = 100) -> List[ActionItem]:
        """
        Search action items by title or description for a specific user.
        
        Args:
            query: Search query
            user_id: User ID (project owner)
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching action item instances
        """
        try:
            search_term = f"%{query}%"
            stmt = select(ActionItem).join(ChecklistGroup).join(Project).where(
                and_(
                    Project.owner_id == user_id,
                    or_(
                        ActionItem.title.ilike(search_term),
                        ActionItem.description.ilike(search_term)
                    )
                )
            ).order_by(
                ActionItem.due_date.asc()
            ).offset(skip).limit(limit)
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def get_action_item_statistics(self, checklist_id: int, user_id: int) -> dict:
        """
        Get action item statistics for a specific checklist.
        
        Args:
            checklist_id: ChecklistGroup ID
            user_id: User ID (project owner)
            
        Returns:
            Dictionary with action item statistics
        """
        try:
            # Verify checklist access
            checklist_stmt = select(ChecklistGroup).join(Project).where(
                and_(
                    ChecklistGroup.id == checklist_id,
                    Project.owner_id == user_id
                )
            )
            checklist_result = await self.session.execute(checklist_stmt)
            if not checklist_result.scalar_one_or_none():
                return {
                    "total_items": 0,
                    "completed_items": 0,
                    "pending_items": 0,
                    "overdue_items": 0,
                    "completion_rate": 0
                }
            
            # Get all action items for the checklist
            items_stmt = select(ActionItem).where(ActionItem.checklist_id == checklist_id)
            items_result = await self.session.execute(items_stmt)
            all_items = items_result.scalars().all()
            
            total_items = len(all_items)
            completed_items = len([item for item in all_items if item.status == "completed"])
            pending_items = len([item for item in all_items if item.status == "pending"])
            
            # Count overdue items
            now = datetime.now()
            overdue_items = len([
                item for item in all_items 
                if item.status == "pending" and item.due_date and item.due_date < now
            ])
            
            return {
                "total_items": total_items,
                "completed_items": completed_items,
                "pending_items": pending_items,
                "overdue_items": overdue_items,
                "completion_rate": (completed_items / total_items * 100) if total_items > 0 else 0
            }
        except Exception:
            return {
                "total_items": 0,
                "completed_items": 0,
                "pending_items": 0,
                "overdue_items": 0,
                "completion_rate": 0
            }
    
    async def update_status(self, action_item_id: int, user_id: int, status: str) -> bool:
        """
        Update action item status.
        
        Args:
            action_item_id: Action item ID
            user_id: User ID (project owner)
            status: New status
            
        Returns:
            True if successful, False otherwise
        """
        try:
            stmt = select(ActionItem).join(ChecklistGroup).join(Project).where(
                and_(
                    ActionItem.id == action_item_id,
                    Project.owner_id == user_id
                )
            )
            result = await self.session.execute(stmt)
            action_item = result.scalar_one_or_none()
            
            if not action_item:
                return False
            
            action_item.status = status
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            raise e
