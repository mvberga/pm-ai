"""
Action item service for action item management operations.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.models.action_item import ActionItem
from app.models.checklist import ChecklistGroup
from app.models.project import Project
from app.schemas.action_item import ActionItemCreate, ActionItemUpdate

class ActionItemService:
    """Service for action item management operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_action_item(self, action_item_data: ActionItemCreate, user_id: int) -> ActionItem:
        """
        Create a new action item.
        
        Args:
            action_item_data: Action item creation data
            user_id: ID of the user creating the action item
            
        Returns:
            Created action item object
        """
        try:
            # Verify checklist access
            checklist = await self._get_user_checklist(action_item_data.checklist_id, user_id)
            if not checklist:
                raise ValueError("ChecklistGroup not found or access denied")
            
            action_item = ActionItem(
                title=action_item_data.title,
                description=action_item_data.description,
                checklist_id=action_item_data.checklist_id,
                assigned_to=action_item_data.assigned_to,
                due_date=action_item_data.due_date,
                priority=action_item_data.priority,
                status=action_item_data.status or "pending",
                created_by=user_id
            )
            
            self.session.add(action_item)
            await self.session.commit()
            await self.session.refresh(action_item)
            
            return action_item
            
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def get_action_item_by_id(self, action_item_id: int, user_id: int) -> Optional[ActionItem]:
        """
        Get action item by ID for a specific user.
        
        Args:
            action_item_id: Action item ID
            user_id: User ID
            
        Returns:
            Action item object if found and accessible, None otherwise
        """
        try:
            stmt = select(ActionItem).join(ChecklistGroup).join(Project).where(
                and_(
                    ActionItem.id == action_item_id,
                    Project.owner_id == user_id
                )
            )
            
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
            
        except Exception:
            return None
    
    async def get_checklist_action_items(self, checklist_id: int, user_id: int) -> List[ActionItem]:
        """
        Get all action items for a checklist.
        
        Args:
            checklist_id: ChecklistGroup ID
            user_id: User ID
            
        Returns:
            List of action item objects
        """
        try:
            # Verify checklist access
            checklist = await self._get_user_checklist(checklist_id, user_id)
            if not checklist:
                return []
            
            stmt = select(ActionItem).where(
                ActionItem.checklist_id == checklist_id
            ).order_by(ActionItem.created_at.desc())
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
            
        except Exception:
            return []
    
    async def update_action_item(self, action_item_id: int, user_id: int, action_item_data: ActionItemUpdate) -> Optional[ActionItem]:
        """
        Update action item information.
        
        Args:
            action_item_id: Action item ID
            user_id: User ID
            action_item_data: Action item update data
            
        Returns:
            Updated action item object if successful, None otherwise
        """
        try:
            action_item = await self.get_action_item_by_id(action_item_id, user_id)
            if not action_item:
                return None
            
            # Update fields
            update_data = action_item_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(action_item, field):
                    setattr(action_item, field, value)
            
            await self.session.commit()
            await self.session.refresh(action_item)
            
            return action_item
            
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def delete_action_item(self, action_item_id: int, user_id: int) -> bool:
        """
        Delete an action item.
        
        Args:
            action_item_id: Action item ID
            user_id: User ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            action_item = await self.get_action_item_by_id(action_item_id, user_id)
            if not action_item:
                return False
            
            await self.session.delete(action_item)
            await self.session.commit()
            
            return True
            
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def mark_action_item_complete(self, action_item_id: int, user_id: int) -> Optional[ActionItem]:
        """
        Mark an action item as completed.
        
        Args:
            action_item_id: Action item ID
            user_id: User ID
            
        Returns:
            Updated action item object if successful, None otherwise
        """
        try:
            action_item = await self.get_action_item_by_id(action_item_id, user_id)
            if not action_item:
                return None
            
            action_item.status = "completed"
            await self.session.commit()
            await self.session.refresh(action_item)
            
            return action_item
            
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def get_action_item_statistics(self, checklist_id: int, user_id: int) -> dict:
        """
        Get action item statistics for a checklist.
        
        Args:
            checklist_id: ChecklistGroup ID
            user_id: User ID
            
        Returns:
            Dictionary with action item statistics
        """
        try:
            # Verify checklist access
            checklist = await self._get_user_checklist(checklist_id, user_id)
            if not checklist:
                return {
                    "total_items": 0,
                    "completed_items": 0,
                    "pending_items": 0,
                    "overdue_items": 0,
                    "completion_rate": 0
                }
            
            # Total action items
            total_stmt = select(ActionItem).where(ActionItem.checklist_id == checklist_id)
            total_result = await self.session.execute(total_stmt)
            all_items = total_result.scalars().all()
            
            total_items = len(all_items)
            completed_items = len([item for item in all_items if item.status == "completed"])
            pending_items = len([item for item in all_items if item.status == "pending"])
            
            # Overdue items (items past due date with pending status)
            from datetime import datetime
            overdue_items = len([
                item for item in all_items 
                if item.status == "pending" and item.due_date and item.due_date < datetime.now()
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
    
    async def get_user_action_items(self, user_id: int, status: Optional[str] = None) -> List[ActionItem]:
        """
        Get all action items assigned to a user.
        
        Args:
            user_id: User ID
            status: Optional status filter
            
        Returns:
            List of action item objects
        """
        try:
            stmt = select(ActionItem).join(ChecklistGroup).join(Project).where(
                and_(
                    ActionItem.assigned_to == user_id,
                    Project.owner_id == user_id
                )
            )
            
            if status:
                stmt = stmt.where(ActionItem.status == status)
            
            stmt = stmt.order_by(ActionItem.due_date.asc())
            
            result = await self.session.execute(stmt)
            return result.scalars().all()
            
        except Exception:
            return []
    
    async def _get_user_checklist(self, checklist_id: int, user_id: int) -> Optional[ChecklistGroup]:
        """
        Get checklist if user has access to it.
        
        Args:
            checklist_id: ChecklistGroup ID
            user_id: User ID
            
        Returns:
            ChecklistGroup object if accessible, None otherwise
        """
        try:
            stmt = select(ChecklistGroup).join(Project).where(
                and_(
                    ChecklistGroup.id == checklist_id,
                    Project.owner_id == user_id
                )
            )
            
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
            
        except Exception:
            return None
