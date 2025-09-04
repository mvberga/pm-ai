"""
Advanced caching system with intelligent invalidation strategies.
"""

from typing import Any, Optional, Dict, List, Callable, Union
import asyncio
import logging
from datetime import datetime, timedelta
import json
from enum import Enum

from .cache_service import CacheService
from .redis_client import RedisClient

logger = logging.getLogger(__name__)

class CacheStrategy(Enum):
    """Cache invalidation strategies."""
    WRITE_THROUGH = "write_through"
    WRITE_BEHIND = "write_behind"
    WRITE_AROUND = "write_around"
    REFRESH_AHEAD = "refresh_ahead"

class CacheLevel(Enum):
    """Cache levels for hierarchical caching."""
    L1 = "l1"  # In-memory cache
    L2 = "l2"  # Redis cache
    L3 = "l3"  # Database

class AdvancedCacheService(CacheService):
    """Advanced cache service with intelligent invalidation and hierarchical caching."""
    
    def __init__(self, redis_client: RedisClient):
        super().__init__(redis_client)
        self.l1_cache = {}  # In-memory cache
        self.l1_ttl = {}    # TTL for L1 cache
        self.cache_strategies = {}
        self.dependency_graph = {}  # Cache dependency tracking
        self.access_patterns = {}   # Access pattern tracking
        self.cache_stats = {
            'hits': {'l1': 0, 'l2': 0, 'l3': 0},
            'misses': {'l1': 0, 'l2': 0, 'l3': 0},
            'invalidations': 0,
            'evictions': 0
        }
    
    def _is_l1_expired(self, key: str) -> bool:
        """Check if L1 cache entry is expired."""
        if key not in self.l1_ttl:
            return True
        return datetime.now() > self.l1_ttl[key]
    
    def _set_l1_cache(self, key: str, value: Any, ttl: int = 300):
        """Set value in L1 cache."""
        self.l1_cache[key] = value
        self.l1_ttl[key] = datetime.now() + timedelta(seconds=ttl)
    
    def _get_l1_cache(self, key: str) -> Optional[Any]:
        """Get value from L1 cache."""
        if key in self.l1_cache and not self._is_l1_expired(key):
            self.cache_stats['hits']['l1'] += 1
            return self.l1_cache[key]
        
        if key in self.l1_cache:
            del self.l1_cache[key]
            del self.l1_ttl[key]
        
        self.cache_stats['misses']['l1'] += 1
        return None
    
    def _evict_l1_cache(self, pattern: str = None):
        """Evict entries from L1 cache."""
        if pattern:
            keys_to_remove = [k for k in self.l1_cache.keys() if pattern in k]
        else:
            keys_to_remove = list(self.l1_cache.keys())
        
        for key in keys_to_remove:
            if key in self.l1_cache:
                del self.l1_cache[key]
            if key in self.l1_ttl:
                del self.l1_ttl[key]
        
        self.cache_stats['evictions'] += len(keys_to_remove)
        logger.debug(f"Evicted {len(keys_to_remove)} entries from L1 cache")
    
    async def get_hierarchical(
        self, 
        key: str, 
        fetch_func: Callable = None,
        ttl: int = None,
        *args, 
        **kwargs
    ) -> Any:
        """
        Get value using hierarchical caching (L1 -> L2 -> L3).
        
        Args:
            key: Cache key
            fetch_func: Function to fetch data if not in any cache
            ttl: Time to live in seconds
            *args: Arguments for fetch function
            **kwargs: Keyword arguments for fetch function
            
        Returns:
            Cached or fetched value
        """
        # Try L1 cache first
        l1_value = self._get_l1_cache(key)
        if l1_value is not None:
            return l1_value
        
        # Try L2 cache (Redis)
        l2_value = await self.get(key)
        if l2_value is not None:
            self.cache_stats['hits']['l2'] += 1
            # Populate L1 cache
            self._set_l1_cache(key, l2_value, ttl or 300)
            return l2_value
        
        self.cache_stats['misses']['l2'] += 1
        
        # Fetch from L3 (database) if fetch function provided
        if fetch_func:
            try:
                if asyncio.iscoroutinefunction(fetch_func):
                    value = await fetch_func(*args, **kwargs)
                else:
                    value = fetch_func(*args, **kwargs)
                
                # Store in both L1 and L2
                self._set_l1_cache(key, value, ttl or 300)
                await self.set(key, value, ttl)
                
                self.cache_stats['hits']['l3'] += 1
                return value
            except Exception as e:
                self.cache_stats['misses']['l3'] += 1
                logger.error(f"Error fetching data for key {key}: {str(e)}")
                raise
        
        return None
    
    async def set_hierarchical(self, key: str, value: Any, ttl: int = None):
        """Set value in both L1 and L2 cache."""
        self._set_l1_cache(key, value, ttl or 300)
        await self.set(key, value, ttl)
    
    async def invalidate_hierarchical(self, key: str):
        """Invalidate key from both L1 and L2 cache."""
        if key in self.l1_cache:
            del self.l1_cache[key]
        if key in self.l1_ttl:
            del self.l1_ttl[key]
        
        await self.delete(key)
        self.cache_stats['invalidations'] += 1
    
    def add_dependency(self, parent_key: str, child_key: str):
        """Add cache dependency relationship."""
        if parent_key not in self.dependency_graph:
            self.dependency_graph[parent_key] = []
        
        if child_key not in self.dependency_graph[parent_key]:
            self.dependency_graph[parent_key].append(child_key)
    
    async def invalidate_dependencies(self, key: str):
        """Invalidate all dependent cache entries."""
        if key not in self.dependency_graph:
            return
        
        dependencies = self.dependency_graph[key]
        for dep_key in dependencies:
            await self.invalidate_hierarchical(dep_key)
            # Recursively invalidate dependencies of dependencies
            await self.invalidate_dependencies(dep_key)
    
    def track_access_pattern(self, key: str, access_type: str = "read"):
        """Track access patterns for cache optimization."""
        if key not in self.access_patterns:
            self.access_patterns[key] = {
                'read_count': 0,
                'write_count': 0,
                'last_access': datetime.now(),
                'access_frequency': 0
            }
        
        pattern = self.access_patterns[key]
        pattern['last_access'] = datetime.now()
        
        if access_type == "read":
            pattern['read_count'] += 1
        elif access_type == "write":
            pattern['write_count'] += 1
        
        # Calculate access frequency (accesses per hour)
        time_diff = datetime.now() - pattern['last_access']
        if time_diff.total_seconds() > 0:
            pattern['access_frequency'] = (pattern['read_count'] + pattern['write_count']) / (time_diff.total_seconds() / 3600)
    
    async def optimize_cache(self):
        """Optimize cache based on access patterns."""
        logger.info("Starting cache optimization...")
        
        # Evict rarely accessed entries from L1
        current_time = datetime.now()
        keys_to_evict = []
        
        for key, pattern in self.access_patterns.items():
            # Evict if not accessed in last hour and low frequency
            time_since_access = current_time - pattern['last_access']
            if (time_since_access.total_seconds() > 3600 and 
                pattern['access_frequency'] < 0.1):
                keys_to_evict.append(key)
        
        for key in keys_to_evict:
            if key in self.l1_cache:
                del self.l1_cache[key]
            if key in self.l1_ttl:
                del self.l1_ttl[key]
        
        logger.info(f"Optimized cache: evicted {len(keys_to_evict)} rarely accessed entries")
    
    async def get_cache_analytics(self) -> Dict[str, Any]:
        """Get comprehensive cache analytics."""
        total_hits = sum(self.cache_stats['hits'].values())
        total_misses = sum(self.cache_stats['misses'].values())
        total_requests = total_hits + total_misses
        
        hit_rate = (total_hits / total_requests * 100) if total_requests > 0 else 0
        
        # Calculate hit rates by level
        l1_hit_rate = (self.cache_stats['hits']['l1'] / total_requests * 100) if total_requests > 0 else 0
        l2_hit_rate = (self.cache_stats['hits']['l2'] / total_requests * 100) if total_requests > 0 else 0
        l3_hit_rate = (self.cache_stats['hits']['l3'] / total_requests * 100) if total_requests > 0 else 0
        
        # Get most accessed keys
        most_accessed = sorted(
            self.access_patterns.items(),
            key=lambda x: x[1]['read_count'] + x[1]['write_count'],
            reverse=True
        )[:10]
        
        return {
            'performance': {
                'total_requests': total_requests,
                'total_hits': total_hits,
                'total_misses': total_misses,
                'overall_hit_rate': round(hit_rate, 2),
                'l1_hit_rate': round(l1_hit_rate, 2),
                'l2_hit_rate': round(l2_hit_rate, 2),
                'l3_hit_rate': round(l3_hit_rate, 2)
            },
            'cache_size': {
                'l1_entries': len(self.l1_cache),
                'l2_entries': len(await self.redis.keys(f"{self.cache_prefix}*"))
            },
            'operations': {
                'invalidations': self.cache_stats['invalidations'],
                'evictions': self.cache_stats['evictions']
            },
            'most_accessed_keys': [
                {
                    'key': key,
                    'read_count': pattern['read_count'],
                    'write_count': pattern['write_count'],
                    'access_frequency': round(pattern['access_frequency'], 2),
                    'last_access': pattern['last_access'].isoformat()
                }
                for key, pattern in most_accessed
            ],
            'dependencies': {
                'total_dependencies': sum(len(deps) for deps in self.dependency_graph.values()),
                'dependency_chains': len(self.dependency_graph)
            }
        }
    
    async def warm_cache(self, warmup_functions: List[Callable]):
        """Warm up cache with frequently accessed data."""
        logger.info("Starting cache warmup...")
        
        warmup_tasks = []
        for func in warmup_functions:
            if asyncio.iscoroutinefunction(func):
                warmup_tasks.append(func())
            else:
                warmup_tasks.append(asyncio.create_task(asyncio.to_thread(func)))
        
        try:
            await asyncio.gather(*warmup_tasks)
            logger.info(f"Cache warmup completed: {len(warmup_functions)} functions executed")
        except Exception as e:
            logger.error(f"Error during cache warmup: {str(e)}")
    
    async def get_optimized_user_projects(
        self, 
        user_id: int, 
        fetch_func: Callable,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get user projects with optimized caching."""
        cache_key = f"projects:user:{user_id}:skip:{skip}:limit:{limit}"
        
        # Track access pattern
        self.track_access_pattern(cache_key, "read")
        
        # Use hierarchical caching
        return await self.get_hierarchical(
            cache_key,
            fetch_func,
            ttl=1800,  # 30 minutes
            user_id=user_id,
            skip=skip,
            limit=limit
        )
    
    async def get_optimized_project_details(
        self, 
        project_id: int, 
        user_id: int,
        fetch_func: Callable
    ) -> Dict[str, Any]:
        """Get project details with optimized caching."""
        cache_key = f"project:{project_id}:user:{user_id}"
        
        # Track access pattern
        self.track_access_pattern(cache_key, "read")
        
        # Add dependencies
        self.add_dependency(f"projects:user:{user_id}", cache_key)
        
        # Use hierarchical caching
        return await self.get_hierarchical(
            cache_key,
            fetch_func,
            ttl=1800,  # 30 minutes
            project_id=project_id,
            user_id=user_id
        )
    
    async def invalidate_project_related_cache(self, project_id: int, user_id: int):
        """Invalidate all cache entries related to a project."""
        patterns = [
            f"project:{project_id}:*",
            f"team_members:project:{project_id}:*",
            f"clients:project:{project_id}:*",
            f"risks:project:{project_id}:*",
            f"stats:project:{project_id}:*"
        ]
        
        total_invalidated = 0
        for pattern in patterns:
            # Invalidate L1 cache
            self._evict_l1_cache(pattern.replace("*", ""))
            
            # Invalidate L2 cache
            invalidated = await self.invalidate_pattern(pattern)
            total_invalidated += invalidated
        
        # Invalidate dependencies
        await self.invalidate_dependencies(f"project:{project_id}:user:{user_id}")
        
        logger.info(f"Invalidated {total_invalidated} cache entries for project {project_id}")
        return total_invalidated
