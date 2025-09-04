"""
Cache decorators for automatic caching of function results.
"""

import functools
import asyncio
import logging
from typing import Any, Callable, Optional, Union
from datetime import timedelta

from .cache_service import CacheService

logger = logging.getLogger(__name__)

def cache_result(
    cache_service: CacheService,
    key_prefix: str,
    ttl: Optional[Union[int, timedelta]] = None,
    key_func: Optional[Callable] = None
):
    """
    Decorator to cache function results.
    
    Args:
        cache_service: Cache service instance
        key_prefix: Prefix for cache key
        ttl: Time to live in seconds or timedelta
        key_func: Function to generate cache key from function arguments
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = f"{key_prefix}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Try to get from cache
            cached_result = await cache_service.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__} with key: {cache_key}")
                return cached_result
            
            # Execute function and cache result
            logger.debug(f"Cache miss for {func.__name__} with key: {cache_key}")
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            # Cache the result
            await cache_service.set(cache_key, result, ttl)
            return result
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = f"{key_prefix}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # For sync functions, we need to run the async cache operations
            loop = asyncio.get_event_loop()
            
            # Try to get from cache
            cached_result = loop.run_until_complete(cache_service.get(cache_key))
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__} with key: {cache_key}")
                return cached_result
            
            # Execute function and cache result
            logger.debug(f"Cache miss for {func.__name__} with key: {cache_key}")
            result = func(*args, **kwargs)
            
            # Cache the result
            loop.run_until_complete(cache_service.set(cache_key, result, ttl))
            return result
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator

def invalidate_cache(
    cache_service: CacheService,
    key_patterns: list,
    key_func: Optional[Callable] = None
):
    """
    Decorator to invalidate cache after function execution.
    
    Args:
        cache_service: Cache service instance
        key_patterns: List of key patterns to invalidate
        key_func: Function to generate cache keys from function arguments
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Execute function
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            # Invalidate cache
            for pattern in key_patterns:
                if key_func:
                    cache_key = key_func(*args, **kwargs)
                    await cache_service.delete(cache_key)
                else:
                    await cache_service.invalidate_pattern(pattern)
            
            logger.debug(f"Cache invalidated for {func.__name__} with patterns: {key_patterns}")
            return result
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Execute function
            result = func(*args, **kwargs)
            
            # Invalidate cache
            loop = asyncio.get_event_loop()
            for pattern in key_patterns:
                if key_func:
                    cache_key = key_func(*args, **kwargs)
                    loop.run_until_complete(cache_service.delete(cache_key))
                else:
                    loop.run_until_complete(cache_service.invalidate_pattern(pattern))
            
            logger.debug(f"Cache invalidated for {func.__name__} with patterns: {key_patterns}")
            return result
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator

def cache_user_data(cache_service: CacheService, ttl: int = 1800):
    """Decorator to cache user-specific data."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Extract user_id from arguments (assuming it's the first argument after self)
            user_id = None
            if len(args) > 1:
                user_id = args[1]  # Assuming user_id is the second argument
            elif 'user_id' in kwargs:
                user_id = kwargs['user_id']
            
            if not user_id:
                # If no user_id found, execute function without caching
                return await func(*args, **kwargs)
            
            # Generate cache key
            cache_key = f"user:{user_id}:{func.__name__}:{hash(str(args[2:]) + str(sorted(kwargs.items())))}"
            
            # Try to get from cache
            cached_result = await cache_service.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for user {user_id} function {func.__name__}")
                return cached_result
            
            # Execute function and cache result
            logger.debug(f"Cache miss for user {user_id} function {func.__name__}")
            result = await func(*args, **kwargs)
            
            # Cache the result
            await cache_service.set(cache_key, result, ttl)
            return result
        
        return async_wrapper
    return decorator

def cache_project_data(cache_service: CacheService, ttl: int = 1800):
    """Decorator to cache project-specific data."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Extract project_id from arguments
            project_id = None
            if len(args) > 1:
                project_id = args[1]  # Assuming project_id is the second argument
            elif 'project_id' in kwargs:
                project_id = kwargs['project_id']
            
            if not project_id:
                # If no project_id found, execute function without caching
                return await func(*args, **kwargs)
            
            # Generate cache key
            cache_key = f"project:{project_id}:{func.__name__}:{hash(str(args[2:]) + str(sorted(kwargs.items())))}"
            
            # Try to get from cache
            cached_result = await cache_service.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for project {project_id} function {func.__name__}")
                return cached_result
            
            # Execute function and cache result
            logger.debug(f"Cache miss for project {project_id} function {func.__name__}")
            result = await func(*args, **kwargs)
            
            # Cache the result
            await cache_service.set(cache_key, result, ttl)
            return result
        
        return async_wrapper
    return decorator

def cache_portfolio_data(cache_service: CacheService, ttl: int = 1800):
    """Decorator to cache portfolio-specific data."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Extract portfolio_id from arguments
            portfolio_id = None
            if len(args) > 1:
                portfolio_id = args[1]  # Assuming portfolio_id is the second argument
            elif 'portfolio_id' in kwargs:
                portfolio_id = kwargs['portfolio_id']
            
            if not portfolio_id:
                # If no portfolio_id found, execute function without caching
                return await func(*args, **kwargs)
            
            # Generate cache key
            cache_key = f"portfolio:{portfolio_id}:{func.__name__}:{hash(str(args[2:]) + str(sorted(kwargs.items())))}"
            
            # Try to get from cache
            cached_result = await cache_service.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for portfolio {portfolio_id} function {func.__name__}")
                return cached_result
            
            # Execute function and cache result
            logger.debug(f"Cache miss for portfolio {portfolio_id} function {func.__name__}")
            result = await func(*args, **kwargs)
            
            # Cache the result
            await cache_service.set(cache_key, result, ttl)
            return result
        
        return async_wrapper
    return decorator

def invalidate_user_cache(cache_service: CacheService):
    """Decorator to invalidate user cache after function execution."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Execute function
            result = await func(*args, **kwargs)
            
            # Extract user_id from arguments
            user_id = None
            if len(args) > 1:
                user_id = args[1]
            elif 'user_id' in kwargs:
                user_id = kwargs['user_id']
            
            if user_id:
                # Invalidate user cache
                await cache_service.invalidate_user_cache(user_id)
                logger.debug(f"User cache invalidated for user {user_id}")
            
            return result
        
        return async_wrapper
    return decorator

def invalidate_project_cache(cache_service: CacheService):
    """Decorator to invalidate project cache after function execution."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Execute function
            result = await func(*args, **kwargs)
            
            # Extract project_id from arguments
            project_id = None
            if len(args) > 1:
                project_id = args[1]
            elif 'project_id' in kwargs:
                project_id = kwargs['project_id']
            
            if project_id:
                # Invalidate project cache
                await cache_service.invalidate_project_cache(project_id)
                logger.debug(f"Project cache invalidated for project {project_id}")
            
            return result
        
        return async_wrapper
    return decorator

def invalidate_portfolio_cache(cache_service: CacheService):
    """Decorator to invalidate portfolio cache after function execution."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Execute function
            result = await func(*args, **kwargs)
            
            # Extract portfolio_id from arguments
            portfolio_id = None
            if len(args) > 1:
                portfolio_id = args[1]
            elif 'portfolio_id' in kwargs:
                portfolio_id = kwargs['portfolio_id']
            
            if portfolio_id:
                # Invalidate portfolio cache
                await cache_service.invalidate_portfolio_cache(portfolio_id)
                logger.debug(f"Portfolio cache invalidated for portfolio {portfolio_id}")
            
            return result
        
        return async_wrapper
    return decorator
