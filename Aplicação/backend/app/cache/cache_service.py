"""
Cache service for managing application caching.
"""

from typing import Any, Optional, Callable, Union
import asyncio
import logging
from datetime import timedelta
import hashlib
import json

from .redis_client import RedisClient

logger = logging.getLogger(__name__)

class CacheService:
    """Service for managing application caching."""
    
    def __init__(self, redis_client: RedisClient):
        self.redis = redis_client
        self.default_ttl = 3600  # 1 hour
        self.cache_prefix = "pm_ai:"
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key from prefix and arguments."""
        # Create a hash of the arguments for consistent key generation
        key_data = {
            'args': args,
            'kwargs': sorted(kwargs.items()) if kwargs else {}
        }
        key_hash = hashlib.md5(json.dumps(key_data, sort_keys=True).encode()).hexdigest()[:8]
        return f"{self.cache_prefix}{prefix}:{key_hash}"
    
    async def get_or_set(
        self, 
        key_prefix: str, 
        fetch_func: Callable, 
        ttl: Optional[int] = None,
        *args, 
        **kwargs
    ) -> Any:
        """
        Get value from cache or fetch and cache it.
        
        Args:
            key_prefix: Cache key prefix
            fetch_func: Function to fetch data if not in cache
            ttl: Time to live in seconds
            *args: Arguments for fetch function
            **kwargs: Keyword arguments for fetch function
            
        Returns:
            Cached or fetched value
        """
        cache_key = self._generate_key(key_prefix, *args, **kwargs)
        
        # Try to get from cache
        cached_value = await self.redis.get(cache_key)
        if cached_value is not None:
            logger.debug(f"Cache hit for key: {cache_key}")
            return cached_value
        
        # Fetch from source
        logger.debug(f"Cache miss for key: {cache_key}, fetching from source")
        try:
            if asyncio.iscoroutinefunction(fetch_func):
                value = await fetch_func(*args, **kwargs)
            else:
                value = fetch_func(*args, **kwargs)
            
            # Cache the value
            await self.set(cache_key, value, ttl)
            return value
            
        except Exception as e:
            logger.error(f"Error fetching data for cache key {cache_key}: {str(e)}")
            raise
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set a value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if ttl is None:
            ttl = self.default_ttl
        
        cache_key = f"{self.cache_prefix}{key}"
        return await self.redis.set(cache_key, value, ttl)
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Get a value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        cache_key = f"{self.cache_prefix}{key}"
        return await self.redis.get(cache_key)
    
    async def delete(self, key: str) -> bool:
        """
        Delete a value from cache.
        
        Args:
            key: Cache key to delete
            
        Returns:
            True if successful, False otherwise
        """
        cache_key = f"{self.cache_prefix}{key}"
        return await self.redis.delete(cache_key)
    
    async def exists(self, key: str) -> bool:
        """
        Check if a key exists in cache.
        
        Args:
            key: Cache key to check
            
        Returns:
            True if key exists, False otherwise
        """
        cache_key = f"{self.cache_prefix}{key}"
        return await self.redis.exists(cache_key)
    
    async def invalidate_pattern(self, pattern: str) -> int:
        """
        Invalidate all keys matching a pattern.
        
        Args:
            pattern: Key pattern to match
            
        Returns:
            Number of keys deleted
        """
        cache_pattern = f"{self.cache_prefix}{pattern}"
        keys = await self.redis.keys(cache_pattern)
        
        if not keys:
            return 0
        
        deleted_count = 0
        for key in keys:
            if await self.redis.delete(key):
                deleted_count += 1
        
        logger.info(f"Invalidated {deleted_count} cache keys matching pattern: {pattern}")
        return deleted_count
    
    async def invalidate_user_cache(self, user_id: int) -> int:
        """Invalidate all cache entries for a specific user."""
        patterns = [
            f"user:{user_id}:*",
            f"projects:user:{user_id}:*",
            f"portfolios:user:{user_id}:*",
            f"team_members:user:{user_id}:*",
            f"clients:user:{user_id}:*",
            f"risks:user:{user_id}:*"
        ]
        
        total_deleted = 0
        for pattern in patterns:
            deleted = await self.invalidate_pattern(pattern)
            total_deleted += deleted
        
        return total_deleted
    
    async def invalidate_project_cache(self, project_id: int) -> int:
        """Invalidate all cache entries for a specific project."""
        patterns = [
            f"project:{project_id}:*",
            f"team_members:project:{project_id}:*",
            f"clients:project:{project_id}:*",
            f"risks:project:{project_id}:*",
            f"lessons:project:{project_id}:*",
            f"next_steps:project:{project_id}:*"
        ]
        
        total_deleted = 0
        for pattern in patterns:
            deleted = await self.invalidate_pattern(pattern)
            total_deleted += deleted
        
        return total_deleted
    
    async def invalidate_portfolio_cache(self, portfolio_id: int) -> int:
        """Invalidate all cache entries for a specific portfolio."""
        patterns = [
            f"portfolio:{portfolio_id}:*",
            f"projects:portfolio:{portfolio_id}:*"
        ]
        
        total_deleted = 0
        for pattern in patterns:
            deleted = await self.invalidate_pattern(pattern)
            total_deleted += deleted
        
        return total_deleted
    
    async def get_user_projects(self, user_id: int, skip: int = 0, limit: int = 100) -> Optional[list]:
        """Get cached user projects."""
        cache_key = f"projects:user:{user_id}:skip:{skip}:limit:{limit}"
        return await self.get(cache_key)
    
    async def set_user_projects(self, user_id: int, projects: list, skip: int = 0, limit: int = 100, ttl: int = 1800) -> bool:
        """Cache user projects."""
        cache_key = f"projects:user:{user_id}:skip:{skip}:limit:{limit}"
        return await self.set(cache_key, projects, ttl)
    
    async def get_project_details(self, project_id: int, user_id: int) -> Optional[dict]:
        """Get cached project details."""
        cache_key = f"project:{project_id}:user:{user_id}"
        return await self.get(cache_key)
    
    async def set_project_details(self, project_id: int, user_id: int, project_data: dict, ttl: int = 1800) -> bool:
        """Cache project details."""
        cache_key = f"project:{project_id}:user:{user_id}"
        return await self.set(cache_key, project_data, ttl)
    
    async def get_portfolio_projects(self, portfolio_id: int, user_id: int) -> Optional[list]:
        """Get cached portfolio projects."""
        cache_key = f"projects:portfolio:{portfolio_id}:user:{user_id}"
        return await self.get(cache_key)
    
    async def set_portfolio_projects(self, portfolio_id: int, user_id: int, projects: list, ttl: int = 1800) -> bool:
        """Cache portfolio projects."""
        cache_key = f"projects:portfolio:{portfolio_id}:user:{user_id}"
        return await self.set(cache_key, projects, ttl)
    
    async def get_team_members(self, project_id: int, user_id: int) -> Optional[list]:
        """Get cached team members."""
        cache_key = f"team_members:project:{project_id}:user:{user_id}"
        return await self.get(cache_key)
    
    async def set_team_members(self, project_id: int, user_id: int, team_members: list, ttl: int = 1800) -> bool:
        """Cache team members."""
        cache_key = f"team_members:project:{project_id}:user:{user_id}"
        return await self.set(cache_key, team_members, ttl)
    
    async def get_clients(self, project_id: int, user_id: int) -> Optional[list]:
        """Get cached clients."""
        cache_key = f"clients:project:{project_id}:user:{user_id}"
        return await self.get(cache_key)
    
    async def set_clients(self, project_id: int, user_id: int, clients: list, ttl: int = 1800) -> bool:
        """Cache clients."""
        cache_key = f"clients:project:{project_id}:user:{user_id}"
        return await self.set(cache_key, clients, ttl)
    
    async def get_risks(self, project_id: int, user_id: int) -> Optional[list]:
        """Get cached risks."""
        cache_key = f"risks:project:{project_id}:user:{user_id}"
        return await self.get(cache_key)
    
    async def set_risks(self, project_id: int, user_id: int, risks: list, ttl: int = 1800) -> bool:
        """Cache risks."""
        cache_key = f"risks:project:{project_id}:user:{user_id}"
        return await self.set(cache_key, risks, ttl)
    
    async def get_project_statistics(self, project_id: int, user_id: int) -> Optional[dict]:
        """Get cached project statistics."""
        cache_key = f"stats:project:{project_id}:user:{user_id}"
        return await self.get(cache_key)
    
    async def set_project_statistics(self, project_id: int, user_id: int, stats: dict, ttl: int = 900) -> bool:
        """Cache project statistics."""
        cache_key = f"stats:project:{project_id}:user:{user_id}"
        return await self.set(cache_key, stats, ttl)
    
    async def get_user_statistics(self, user_id: int) -> Optional[dict]:
        """Get cached user statistics."""
        cache_key = f"stats:user:{user_id}"
        return await self.get(cache_key)
    
    async def set_user_statistics(self, user_id: int, stats: dict, ttl: int = 900) -> bool:
        """Cache user statistics."""
        cache_key = f"stats:user:{user_id}"
        return await self.set(cache_key, stats, ttl)
    
    async def get_ai_analysis(self, entity_type: str, entity_id: int, analysis_type: str) -> Optional[dict]:
        """Get cached AI analysis."""
        cache_key = f"ai:{entity_type}:{entity_id}:{analysis_type}"
        return await self.get(cache_key)
    
    async def set_ai_analysis(self, entity_type: str, entity_id: int, analysis_type: str, analysis: dict, ttl: int = 3600) -> bool:
        """Cache AI analysis."""
        cache_key = f"ai:{entity_type}:{entity_id}:{analysis_type}"
        return await self.set(cache_key, analysis, ttl)
    
    async def get_cache_info(self) -> dict:
        """Get cache information and statistics."""
        try:
            redis_info = await self.redis.info()
            cache_keys = await self.redis.keys(f"{self.cache_prefix}*")
            
            return {
                'redis_connected': await self.redis.is_connected(),
                'total_keys': len(cache_keys),
                'redis_info': {
                    'used_memory': redis_info.get('used_memory_human', 'N/A'),
                    'connected_clients': redis_info.get('connected_clients', 0),
                    'total_commands_processed': redis_info.get('total_commands_processed', 0),
                    'keyspace_hits': redis_info.get('keyspace_hits', 0),
                    'keyspace_misses': redis_info.get('keyspace_misses', 0)
                },
                'cache_prefix': self.cache_prefix,
                'default_ttl': self.default_ttl
            }
        except Exception as e:
            logger.error(f"Error getting cache info: {str(e)}")
            return {
                'redis_connected': False,
                'error': str(e)
            }
    
    async def clear_all_cache(self) -> bool:
        """Clear all application cache."""
        try:
            await self.redis.flushdb()
            logger.info("All cache cleared successfully")
            return True
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
            return False
