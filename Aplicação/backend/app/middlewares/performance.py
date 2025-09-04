"""
Performance monitoring middleware.
"""

import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.monitoring.performance_monitor import PerformanceMonitor

logger = logging.getLogger(__name__)

class PerformanceMiddleware(BaseHTTPMiddleware):
    """Middleware for monitoring request performance."""
    
    def __init__(self, app: ASGIApp, monitor: PerformanceMonitor):
        super().__init__(app)
        self.monitor = monitor
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and monitor performance."""
        start_time = time.time()
        
        # Extract request information
        method = request.method
        path = request.url.path
        user_id = getattr(request.state, 'user_id', None)
        ip_address = request.client.host if request.client else None
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Record request metric
            self.monitor.record_request(
                method=method,
                path=path,
                status_code=response.status_code,
                duration=duration,
                user_id=user_id,
                ip_address=ip_address
            )
            
            # Add performance headers
            response.headers["X-Response-Time"] = f"{duration:.3f}s"
            response.headers["X-Request-ID"] = getattr(request.state, 'request_id', 'unknown')
            
            return response
            
        except Exception as e:
            # Calculate duration even for errors
            duration = time.time() - start_time
            
            # Record error request
            self.monitor.record_request(
                method=method,
                path=path,
                status_code=500,
                duration=duration,
                user_id=user_id,
                ip_address=ip_address
            )
            
            # Record error metric
            self.monitor.record_metric(
                "request_errors",
                1,
                "count",
                {"method": method, "path": path, "error_type": type(e).__name__}
            )
            
            logger.error(f"Request error: {method} {path} - {str(e)}")
            raise

class DatabasePerformanceMiddleware:
    """Middleware for monitoring database query performance."""
    
    def __init__(self, monitor: PerformanceMonitor):
        self.monitor = monitor
        self.query_count = 0
        self.total_query_time = 0.0
    
    def record_query(self, query_type: str, duration: float, success: bool = True):
        """Record database query performance."""
        self.query_count += 1
        self.total_query_time += duration
        
        # Record query metric
        self.monitor.record_metric(
            "database_query_duration",
            duration,
            "duration",
            {"query_type": query_type, "success": str(success)}
        )
        
        # Record query count
        self.monitor.record_metric(
            "database_query_count",
            1,
            "count",
            {"query_type": query_type, "success": str(success)}
        )
        
        # Check for slow queries
        if duration > 1.0:  # 1 second threshold
            self.monitor.record_metric(
                "slow_database_queries",
                1,
                "count",
                {"query_type": query_type, "duration": duration}
            )
            logger.warning(f"Slow database query detected: {query_type} took {duration:.3f}s")
    
    def get_query_stats(self) -> dict:
        """Get database query statistics."""
        avg_query_time = self.total_query_time / self.query_count if self.query_count > 0 else 0
        
        return {
            "total_queries": self.query_count,
            "total_query_time": self.total_query_time,
            "avg_query_time": avg_query_time
        }

class CachePerformanceMiddleware:
    """Middleware for monitoring cache performance."""
    
    def __init__(self, monitor: PerformanceMonitor):
        self.monitor = monitor
        self.cache_hits = 0
        self.cache_misses = 0
        self.cache_operations = 0
    
    def record_cache_operation(
        self, 
        operation: str, 
        cache_type: str, 
        hit: bool, 
        duration: float = 0.0
    ):
        """Record cache operation performance."""
        self.cache_operations += 1
        
        if hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        
        # Record cache metric
        self.monitor.record_metric(
            "cache_operation",
            1,
            "count",
            {
                "operation": operation,
                "cache_type": cache_type,
                "hit": str(hit)
            }
        )
        
        # Record cache duration if provided
        if duration > 0:
            self.monitor.record_metric(
                "cache_operation_duration",
                duration,
                "duration",
                {
                    "operation": operation,
                    "cache_type": cache_type,
                    "hit": str(hit)
                }
            )
    
    def get_cache_stats(self) -> dict:
        """Get cache performance statistics."""
        total_operations = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_operations * 100) if total_operations > 0 else 0
        
        return {
            "total_operations": total_operations,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "hit_rate": hit_rate
        }

class APIPerformanceMiddleware:
    """Middleware for monitoring API endpoint performance."""
    
    def __init__(self, monitor: PerformanceMonitor):
        self.monitor = monitor
        self.endpoint_stats = {}
    
    def record_endpoint_call(
        self, 
        endpoint: str, 
        method: str, 
        duration: float, 
        status_code: int,
        user_id: int = None
    ):
        """Record API endpoint performance."""
        key = f"{method}:{endpoint}"
        
        if key not in self.endpoint_stats:
            self.endpoint_stats[key] = {
                "call_count": 0,
                "total_duration": 0.0,
                "min_duration": float('inf'),
                "max_duration": 0.0,
                "error_count": 0,
                "user_calls": set()
            }
        
        stats = self.endpoint_stats[key]
        stats["call_count"] += 1
        stats["total_duration"] += duration
        stats["min_duration"] = min(stats["min_duration"], duration)
        stats["max_duration"] = max(stats["max_duration"], duration)
        
        if status_code >= 400:
            stats["error_count"] += 1
        
        if user_id:
            stats["user_calls"].add(user_id)
        
        # Record endpoint metric
        self.monitor.record_metric(
            "endpoint_call",
            1,
            "count",
            {
                "endpoint": endpoint,
                "method": method,
                "status_code": str(status_code)
            }
        )
        
        # Record endpoint duration
        self.monitor.record_metric(
            "endpoint_duration",
            duration,
            "duration",
            {
                "endpoint": endpoint,
                "method": method
            }
        )
    
    def get_endpoint_stats(self) -> dict:
        """Get API endpoint statistics."""
        result = {}
        
        for key, stats in self.endpoint_stats.items():
            method, endpoint = key.split(":", 1)
            
            avg_duration = stats["total_duration"] / stats["call_count"] if stats["call_count"] > 0 else 0
            error_rate = (stats["error_count"] / stats["call_count"] * 100) if stats["call_count"] > 0 else 0
            unique_users = len(stats["user_calls"])
            
            result[key] = {
                "endpoint": endpoint,
                "method": method,
                "call_count": stats["call_count"],
                "avg_duration": avg_duration,
                "min_duration": stats["min_duration"] if stats["min_duration"] != float('inf') else 0,
                "max_duration": stats["max_duration"],
                "error_count": stats["error_count"],
                "error_rate": error_rate,
                "unique_users": unique_users
            }
        
        return result
    
    def get_top_endpoints(self, limit: int = 10, sort_by: str = "call_count") -> list:
        """Get top endpoints by specified metric."""
        endpoint_stats = self.get_endpoint_stats()
        
        # Sort by specified metric
        sorted_endpoints = sorted(
            endpoint_stats.items(),
            key=lambda x: x[1][sort_by],
            reverse=True
        )
        
        return [
            {
                "endpoint": key,
                "stats": stats
            }
            for key, stats in sorted_endpoints[:limit]
        ]

class PerformanceCollector:
    """Collector for all performance monitoring components."""
    
    def __init__(self):
        self.monitor = PerformanceMonitor()
        self.db_middleware = DatabasePerformanceMiddleware(self.monitor)
        self.cache_middleware = CachePerformanceMiddleware(self.monitor)
        self.api_middleware = APIPerformanceMiddleware(self.monitor)
    
    def get_comprehensive_stats(self) -> dict:
        """Get comprehensive performance statistics."""
        return {
            "system_health": self.monitor._calculate_system_health(),
            "request_stats": self.monitor._calculate_request_stats(list(self.monitor.request_metrics)),
            "database_stats": self.db_middleware.get_query_stats(),
            "cache_stats": self.cache_middleware.get_cache_stats(),
            "endpoint_stats": self.api_middleware.get_endpoint_stats(),
            "top_slow_endpoints": self.monitor.get_top_slow_endpoints(),
            "recent_alerts": self.monitor._get_recent_alerts(3600),
            "performance_trends": self.monitor.get_performance_trends(24)
        }
    
    async def collect_system_metrics(self):
        """Collect system performance metrics."""
        await self.monitor.collect_system_metrics()
    
    def cleanup_old_data(self, hours: int = 24):
        """Clean up old performance data."""
        self.monitor.clear_old_data(hours)
