"""
Base repository class with common database operations.
"""

from typing import TypeVar, Generic, Type, Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import DeclarativeBase

from app.db.session import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """Base repository class with common CRUD operations."""
    
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session
    
    async def create(self, **kwargs) -> ModelType:
        """
        Create a new record.
        
        Args:
            **kwargs: Model attributes
            
        Returns:
            Created model instance
        """
        try:
            instance = self.model(**kwargs)
            self.session.add(instance)
            await self.session.commit()
            await self.session.refresh(instance)
            return instance
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        Get record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            Model instance if found, None otherwise
        """
        try:
            stmt = select(self.model).where(self.model.id == id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception:
            return None
    
    async def get_all(self, skip: int = 0, limit: int = 100, **filters) -> List[ModelType]:
        """
        Get all records with optional filtering and pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            **filters: Filter conditions
            
        Returns:
            List of model instances
        """
        try:
            stmt = select(self.model)
            
            # Apply filters
            for field, value in filters.items():
                if hasattr(self.model, field):
                    stmt = stmt.where(getattr(self.model, field) == value)
            
            stmt = stmt.offset(skip).limit(limit)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def update(self, id: int, **kwargs) -> Optional[ModelType]:
        """
        Update record by ID.
        
        Args:
            id: Record ID
            **kwargs: Fields to update
            
        Returns:
            Updated model instance if found, None otherwise
        """
        try:
            # Get the record first
            instance = await self.get_by_id(id)
            if not instance:
                return None
            
            # Update fields
            for field, value in kwargs.items():
                if hasattr(instance, field):
                    setattr(instance, field, value)
            
            await self.session.commit()
            await self.session.refresh(instance)
            return instance
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def delete(self, id: int) -> bool:
        """
        Delete record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            True if deleted, False if not found
        """
        try:
            instance = await self.get_by_id(id)
            if not instance:
                return False
            
            await self.session.delete(instance)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def count(self, **filters) -> int:
        """
        Count records with optional filtering.
        
        Args:
            **filters: Filter conditions
            
        Returns:
            Number of matching records
        """
        try:
            stmt = select(func.count(self.model.id))
            
            # Apply filters
            for field, value in filters.items():
                if hasattr(self.model, field):
                    stmt = stmt.where(getattr(self.model, field) == value)
            
            result = await self.session.execute(stmt)
            return result.scalar() or 0
        except Exception:
            return 0
    
    async def exists(self, id: int) -> bool:
        """
        Check if record exists by ID.
        
        Args:
            id: Record ID
            
        Returns:
            True if exists, False otherwise
        """
        try:
            stmt = select(self.model.id).where(self.model.id == id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none() is not None
        except Exception:
            return False
    
    async def search(self, query: str, fields: List[str], skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Search records by text in specified fields.
        
        Args:
            query: Search query
            fields: List of field names to search in
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching model instances
        """
        try:
            if not fields:
                return []
            
            stmt = select(self.model)
            search_term = f"%{query}%"
            
            # Build search conditions
            conditions = []
            for field in fields:
                if hasattr(self.model, field):
                    conditions.append(getattr(self.model, field).ilike(search_term))
            
            if conditions:
                from sqlalchemy import or_
                stmt = stmt.where(or_(*conditions))
            
            stmt = stmt.offset(skip).limit(limit)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception:
            return []
    
    async def bulk_create(self, data_list: List[Dict[str, Any]]) -> List[ModelType]:
        """
        Create multiple records in bulk.
        
        Args:
            data_list: List of dictionaries with model attributes
            
        Returns:
            List of created model instances
        """
        try:
            instances = [self.model(**data) for data in data_list]
            self.session.add_all(instances)
            await self.session.commit()
            
            # Refresh all instances
            for instance in instances:
                await self.session.refresh(instance)
            
            return instances
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def bulk_update(self, updates: List[Dict[str, Any]]) -> int:
        """
        Update multiple records in bulk.
        
        Args:
            updates: List of dictionaries with id and fields to update
            
        Returns:
            Number of updated records
        """
        try:
            updated_count = 0
            for update_data in updates:
                record_id = update_data.pop('id', None)
                if record_id:
                    result = await self.update(record_id, **update_data)
                    if result:
                        updated_count += 1
            
            return updated_count
        except Exception as e:
            await self.session.rollback()
            raise e
