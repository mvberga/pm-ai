"""
Redis client for cache operations.
"""

import redis.asyncio as redis
from typing import Optional, Any, Union
import json
import logging
from datetime import timedelta

from app.core.config import settings

logger = logging.getLogger(__name__)

class RedisClient:
    """Redis client for cache operations."""
    
    def __init__(self):
        self.redis_url = getattr(settings, 'REDIS_URL', 'redis://localhost:6379/0')
        self.client: Optional[redis.Redis] = None
        self._connected = False
    
    async def connect(self):
        """Connect to Redis server."""
        try:
            self.client = redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True
            )
            
            # Test connection
            await self.client.ping()
            self._connected = True
            logger.info("Connected to Redis successfully")
            
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            self._connected = False
            self.client = None
    
    async def disconnect(self):
        """Disconnect from Redis server."""
        if self.client:
            await self.client.close()
            self._connected = False
            logger.info("Disconnected from Redis")
    
    async def is_connected(self) -> bool:
        """Check if connected to Redis."""
        if not self.client:
            return False
        
        try:
            await self.client.ping()
            return True
        except Exception:
            return False
    
    async def set(self, key: str, value: Any, expire: Optional[Union[int, timedelta]] = None) -> bool:
        """
        Set a key-value pair in Redis.
        
        Args:
            key: Cache key
            value: Value to cache
            expire: Expiration time in seconds or timedelta
            
        Returns:
            True if successful, False otherwise
        """
        if not self._connected or not self.client:
            return False
        
        try:
            # Serialize value to JSON
            serialized_value = json.dumps(value, default=str)
            
            if expire:
                if isinstance(expire, timedelta):
                    expire = int(expire.total_seconds())
                await self.client.setex(key, expire, serialized_value)
            else:
                await self.client.set(key, serialized_value)
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting cache key {key}: {str(e)}")
            return False
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Get a value from Redis.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        if not self._connected or not self.client:
            return None
        
        try:
            value = await self.client.get(key)
            if value is None:
                return None
            
            # Deserialize from JSON
            return json.loads(value)
            
        except Exception as e:
            logger.error(f"Error getting cache key {key}: {str(e)}")
            return None
    
    async def delete(self, key: str) -> bool:
        """
        Delete a key from Redis.
        
        Args:
            key: Cache key to delete
            
        Returns:
            True if successful, False otherwise
        """
        if not self._connected or not self.client:
            return False
        
        try:
            result = await self.client.delete(key)
            return result > 0
            
        except Exception as e:
            logger.error(f"Error deleting cache key {key}: {str(e)}")
            return False
    
    async def exists(self, key: str) -> bool:
        """
        Check if a key exists in Redis.
        
        Args:
            key: Cache key to check
            
        Returns:
            True if key exists, False otherwise
        """
        if not self._connected or not self.client:
            return False
        
        try:
            result = await self.client.exists(key)
            return result > 0
            
        except Exception as e:
            logger.error(f"Error checking cache key {key}: {str(e)}")
            return False
    
    async def expire(self, key: str, seconds: int) -> bool:
        """
        Set expiration time for a key.
        
        Args:
            key: Cache key
            seconds: Expiration time in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self._connected or not self.client:
            return False
        
        try:
            result = await self.client.expire(key, seconds)
            return result
            
        except Exception as e:
            logger.error(f"Error setting expiration for cache key {key}: {str(e)}")
            return False
    
    async def ttl(self, key: str) -> int:
        """
        Get time to live for a key.
        
        Args:
            key: Cache key
            
        Returns:
            TTL in seconds, -1 if no expiration, -2 if key doesn't exist
        """
        if not self._connected or not self.client:
            return -2
        
        try:
            return await self.client.ttl(key)
            
        except Exception as e:
            logger.error(f"Error getting TTL for cache key {key}: {str(e)}")
            return -2
    
    async def keys(self, pattern: str = "*") -> list:
        """
        Get keys matching a pattern.
        
        Args:
            pattern: Key pattern (default: all keys)
            
        Returns:
            List of matching keys
        """
        if not self._connected or not self.client:
            return []
        
        try:
            keys = await self.client.keys(pattern)
            return keys
            
        except Exception as e:
            logger.error(f"Error getting keys with pattern {pattern}: {str(e)}")
            return []
    
    async def flushdb(self) -> bool:
        """
        Flush all keys from the current database.
        
        Returns:
            True if successful, False otherwise
        """
        if not self._connected or not self.client:
            return False
        
        try:
            await self.client.flushdb()
            return True
            
        except Exception as e:
            logger.error(f"Error flushing database: {str(e)}")
            return False
    
    async def info(self) -> dict:
        """
        Get Redis server information.
        
        Returns:
            Dictionary with server information
        """
        if not self._connected or not self.client:
            return {}
        
        try:
            info = await self.client.info()
            return info
            
        except Exception as e:
            logger.error(f"Error getting Redis info: {str(e)}")
            return {}
    
    async def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """
        Increment a numeric value in Redis.
        
        Args:
            key: Cache key
            amount: Amount to increment by
            
        Returns:
            New value after increment or None if error
        """
        if not self._connected or not self.client:
            return None
        
        try:
            return await self.client.incrby(key, amount)
            
        except Exception as e:
            logger.error(f"Error incrementing cache key {key}: {str(e)}")
            return None
    
    async def decrement(self, key: str, amount: int = 1) -> Optional[int]:
        """
        Decrement a numeric value in Redis.
        
        Args:
            key: Cache key
            amount: Amount to decrement by
            
        Returns:
            New value after decrement or None if error
        """
        if not self._connected or not self.client:
            return None
        
        try:
            return await self.client.decrby(key, amount)
            
        except Exception as e:
            logger.error(f"Error decrementing cache key {key}: {str(e)}")
            return None
    
    async def hset(self, name: str, mapping: dict) -> bool:
        """
        Set hash fields in Redis.
        
        Args:
            name: Hash name
            mapping: Dictionary of field-value pairs
            
        Returns:
            True if successful, False otherwise
        """
        if not self._connected or not self.client:
            return False
        
        try:
            # Serialize values
            serialized_mapping = {k: json.dumps(v, default=str) for k, v in mapping.items()}
            await self.client.hset(name, mapping=serialized_mapping)
            return True
            
        except Exception as e:
            logger.error(f"Error setting hash {name}: {str(e)}")
            return False
    
    async def hget(self, name: str, key: str) -> Optional[Any]:
        """
        Get hash field value from Redis.
        
        Args:
            name: Hash name
            key: Field key
            
        Returns:
            Field value or None if not found
        """
        if not self._connected or not self.client:
            return None
        
        try:
            value = await self.client.hget(name, key)
            if value is None:
                return None
            
            return json.loads(value)
            
        except Exception as e:
            logger.error(f"Error getting hash field {name}:{key}: {str(e)}")
            return None
    
    async def hgetall(self, name: str) -> dict:
        """
        Get all hash fields from Redis.
        
        Args:
            name: Hash name
            
        Returns:
            Dictionary of all field-value pairs
        """
        if not self._connected or not self.client:
            return {}
        
        try:
            hash_data = await self.client.hgetall(name)
            return {k: json.loads(v) for k, v in hash_data.items()}
            
        except Exception as e:
            logger.error(f"Error getting hash {name}: {str(e)}")
            return {}
    
    async def hdel(self, name: str, *keys: str) -> int:
        """
        Delete hash fields from Redis.
        
        Args:
            name: Hash name
            *keys: Field keys to delete
            
        Returns:
            Number of fields deleted
        """
        if not self._connected or not self.client:
            return 0
        
        try:
            return await self.client.hdel(name, *keys)
            
        except Exception as e:
            logger.error(f"Error deleting hash fields {name}:{keys}: {str(e)}")
            return 0
