"""
Performance monitoring system for the application.
"""

from typing import Dict, Any, List, Optional
import asyncio
import logging
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from collections import defaultdict, deque
import psutil
import os

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetric:
    """Performance metric data structure."""
    timestamp: datetime
    metric_name: str
    value: float
    unit: str
    tags: Dict[str, str] = field(default_factory=dict)

@dataclass
class RequestMetric:
    """Request performance metric."""
    timestamp: datetime
    method: str
    path: str
    status_code: int
    duration: float
    user_id: Optional[int] = None
    ip_address: Optional[str] = None

class PerformanceMonitor:
    """Performance monitoring system."""
    
    def __init__(self, max_metrics: int = 10000, max_requests: int = 5000):
        self.max_metrics = max_metrics
        self.max_requests = max_requests
        
        # Metrics storage
        self.metrics: deque = deque(maxlen=max_metrics)
        self.request_metrics: deque = deque(maxlen=max_requests)
        
        # Performance counters
        self.counters = defaultdict(int)
        self.gauges = defaultdict(float)
        self.histograms = defaultdict(list)
        
        # System metrics
        self.system_metrics = {}
        self.last_system_check = None
        
        # Performance thresholds
        self.thresholds = {
            'request_duration': 2.0,  # seconds
            'memory_usage': 80.0,     # percentage
            'cpu_usage': 80.0,        # percentage
            'disk_usage': 90.0,       # percentage
            'error_rate': 5.0         # percentage
        }
        
        # Alerts
        self.alerts = []
        self.alert_cooldown = 300  # 5 minutes
    
    def record_metric(
        self, 
        metric_name: str, 
        value: float, 
        unit: str = "count",
        tags: Optional[Dict[str, str]] = None
    ):
        """Record a performance metric."""
        metric = PerformanceMetric(
            timestamp=datetime.now(),
            metric_name=metric_name,
            value=value,
            unit=unit,
            tags=tags or {}
        )
        
        self.metrics.append(metric)
        
        # Update counters and gauges
        if unit == "count":
            self.counters[metric_name] += int(value)
        elif unit in ["percentage", "rate", "duration"]:
            self.gauges[metric_name] = value
        
        # Update histograms for duration metrics
        if unit == "duration":
            self.histograms[metric_name].append(value)
            # Keep only last 1000 values
            if len(self.histograms[metric_name]) > 1000:
                self.histograms[metric_name] = self.histograms[metric_name][-1000:]
        
        # Check for alerts
        self._check_thresholds(metric)
    
    def record_request(
        self,
        method: str,
        path: str,
        status_code: int,
        duration: float,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None
    ):
        """Record a request metric."""
        request_metric = RequestMetric(
            timestamp=datetime.now(),
            method=method,
            path=path,
            status_code=status_code,
            duration=duration,
            user_id=user_id,
            ip_address=ip_address
        )
        
        self.request_metrics.append(request_metric)
        
        # Record related metrics
        self.record_metric("request_duration", duration, "duration", {
            "method": method,
            "path": path,
            "status_code": str(status_code)
        })
        
        self.record_metric("request_count", 1, "count", {
            "method": method,
            "status_code": str(status_code)
        })
        
        # Check for slow requests
        if duration > self.thresholds['request_duration']:
            self._create_alert(
                "slow_request",
                f"Slow request detected: {method} {path} took {duration:.2f}s",
                {"method": method, "path": path, "duration": duration}
            )
    
    async def collect_system_metrics(self):
        """Collect system performance metrics."""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            self.record_metric("cpu_usage", cpu_percent, "percentage")
            
            # Memory usage
            memory = psutil.virtual_memory()
            self.record_metric("memory_usage", memory.percent, "percentage")
            self.record_metric("memory_available", memory.available / (1024**3), "GB")
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            self.record_metric("disk_usage", disk_percent, "percentage")
            self.record_metric("disk_available", disk.free / (1024**3), "GB")
            
            # Process-specific metrics
            process = psutil.Process(os.getpid())
            process_memory = process.memory_info().rss / (1024**2)  # MB
            process_cpu = process.cpu_percent()
            
            self.record_metric("process_memory", process_memory, "MB")
            self.record_metric("process_cpu", process_cpu, "percentage")
            
            # Network I/O
            network = psutil.net_io_counters()
            self.record_metric("network_bytes_sent", network.bytes_sent, "bytes")
            self.record_metric("network_bytes_recv", network.bytes_recv, "bytes")
            
            self.last_system_check = datetime.now()
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {str(e)}")
    
    def _check_thresholds(self, metric: PerformanceMetric):
        """Check if metric exceeds thresholds and create alerts."""
        threshold_key = None
        
        if metric.metric_name == "request_duration":
            threshold_key = "request_duration"
        elif metric.metric_name == "memory_usage":
            threshold_key = "memory_usage"
        elif metric.metric_name == "cpu_usage":
            threshold_key = "cpu_usage"
        elif metric.metric_name == "disk_usage":
            threshold_key = "disk_usage"
        
        if threshold_key and metric.value > self.thresholds[threshold_key]:
            self._create_alert(
                f"high_{threshold_key}",
                f"High {threshold_key}: {metric.value:.2f}{metric.unit}",
                {"metric": metric.metric_name, "value": metric.value, "threshold": self.thresholds[threshold_key]}
            )
    
    def _create_alert(self, alert_type: str, message: str, details: Dict[str, Any]):
        """Create a performance alert."""
        # Check cooldown to avoid spam
        recent_alerts = [
            alert for alert in self.alerts
            if alert['type'] == alert_type and 
            datetime.now() - alert['timestamp'] < timedelta(seconds=self.alert_cooldown)
        ]
        
        if recent_alerts:
            return
        
        alert = {
            'type': alert_type,
            'message': message,
            'details': details,
            'timestamp': datetime.now(),
            'severity': 'warning' if alert_type.startswith('high_') else 'info'
        }
        
        self.alerts.append(alert)
        logger.warning(f"Performance Alert: {message}")
    
    def get_metrics_summary(self, time_window: int = 3600) -> Dict[str, Any]:
        """Get metrics summary for the specified time window."""
        cutoff_time = datetime.now() - timedelta(seconds=time_window)
        
        # Filter metrics by time window
        recent_metrics = [
            metric for metric in self.metrics
            if metric.timestamp >= cutoff_time
        ]
        
        recent_requests = [
            req for req in self.request_metrics
            if req.timestamp >= cutoff_time
        ]
        
        # Calculate summary statistics
        summary = {
            'time_window_seconds': time_window,
            'total_metrics': len(recent_metrics),
            'total_requests': len(recent_requests),
            'counters': dict(self.counters),
            'gauges': dict(self.gauges),
            'request_stats': self._calculate_request_stats(recent_requests),
            'system_health': self._calculate_system_health(),
            'alerts': self._get_recent_alerts(time_window)
        }
        
        return summary
    
    def _calculate_request_stats(self, requests: List[RequestMetric]) -> Dict[str, Any]:
        """Calculate request statistics."""
        if not requests:
            return {}
        
        durations = [req.duration for req in requests]
        status_codes = [req.status_code for req in requests]
        
        # Calculate percentiles
        sorted_durations = sorted(durations)
        n = len(sorted_durations)
        
        p50 = sorted_durations[int(n * 0.5)] if n > 0 else 0
        p95 = sorted_durations[int(n * 0.95)] if n > 0 else 0
        p99 = sorted_durations[int(n * 0.99)] if n > 0 else 0
        
        # Calculate error rate
        error_count = sum(1 for code in status_codes if code >= 400)
        error_rate = (error_count / len(status_codes) * 100) if status_codes else 0
        
        # Group by endpoint
        endpoint_stats = defaultdict(lambda: {'count': 0, 'total_duration': 0, 'errors': 0})
        for req in requests:
            endpoint_stats[req.path]['count'] += 1
            endpoint_stats[req.path]['total_duration'] += req.duration
            if req.status_code >= 400:
                endpoint_stats[req.path]['errors'] += 1
        
        # Calculate averages
        for endpoint in endpoint_stats:
            stats = endpoint_stats[endpoint]
            stats['avg_duration'] = stats['total_duration'] / stats['count']
            stats['error_rate'] = (stats['errors'] / stats['count'] * 100) if stats['count'] > 0 else 0
        
        return {
            'total_requests': len(requests),
            'avg_duration': sum(durations) / len(durations) if durations else 0,
            'min_duration': min(durations) if durations else 0,
            'max_duration': max(durations) if durations else 0,
            'p50_duration': p50,
            'p95_duration': p95,
            'p99_duration': p99,
            'error_rate': error_rate,
            'error_count': error_count,
            'endpoint_stats': dict(endpoint_stats)
        }
    
    def _calculate_system_health(self) -> Dict[str, Any]:
        """Calculate system health score."""
        health_score = 100.0
        issues = []
        
        # Check memory usage
        memory_usage = self.gauges.get('memory_usage', 0)
        if memory_usage > 80:
            health_score -= 20
            issues.append(f"High memory usage: {memory_usage:.1f}%")
        elif memory_usage > 60:
            health_score -= 10
            issues.append(f"Moderate memory usage: {memory_usage:.1f}%")
        
        # Check CPU usage
        cpu_usage = self.gauges.get('cpu_usage', 0)
        if cpu_usage > 80:
            health_score -= 20
            issues.append(f"High CPU usage: {cpu_usage:.1f}%")
        elif cpu_usage > 60:
            health_score -= 10
            issues.append(f"Moderate CPU usage: {cpu_usage:.1f}%")
        
        # Check disk usage
        disk_usage = self.gauges.get('disk_usage', 0)
        if disk_usage > 90:
            health_score -= 30
            issues.append(f"Critical disk usage: {disk_usage:.1f}%")
        elif disk_usage > 80:
            health_score -= 15
            issues.append(f"High disk usage: {disk_usage:.1f}%")
        
        # Check error rate
        request_stats = self._calculate_request_stats(list(self.request_metrics))
        error_rate = request_stats.get('error_rate', 0)
        if error_rate > 10:
            health_score -= 25
            issues.append(f"High error rate: {error_rate:.1f}%")
        elif error_rate > 5:
            health_score -= 10
            issues.append(f"Moderate error rate: {error_rate:.1f}%")
        
        # Determine health status
        if health_score >= 90:
            status = "excellent"
        elif health_score >= 70:
            status = "good"
        elif health_score >= 50:
            status = "warning"
        else:
            status = "critical"
        
        return {
            'score': max(0, health_score),
            'status': status,
            'issues': issues,
            'last_check': self.last_system_check.isoformat() if self.last_system_check else None
        }
    
    def _get_recent_alerts(self, time_window: int) -> List[Dict[str, Any]]:
        """Get recent alerts within the time window."""
        cutoff_time = datetime.now() - timedelta(seconds=time_window)
        
        recent_alerts = [
            {
                'type': alert['type'],
                'message': alert['message'],
                'severity': alert['severity'],
                'timestamp': alert['timestamp'].isoformat(),
                'details': alert['details']
            }
            for alert in self.alerts
            if alert['timestamp'] >= cutoff_time
        ]
        
        return recent_alerts
    
    def get_top_slow_endpoints(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top slowest endpoints."""
        endpoint_durations = defaultdict(list)
        
        for req in self.request_metrics:
            endpoint_durations[req.path].append(req.duration)
        
        # Calculate average duration for each endpoint
        endpoint_stats = []
        for endpoint, durations in endpoint_durations.items():
            avg_duration = sum(durations) / len(durations)
            endpoint_stats.append({
                'endpoint': endpoint,
                'avg_duration': avg_duration,
                'request_count': len(durations),
                'max_duration': max(durations),
                'min_duration': min(durations)
            })
        
        # Sort by average duration
        endpoint_stats.sort(key=lambda x: x['avg_duration'], reverse=True)
        
        return endpoint_stats[:limit]
    
    def get_performance_trends(self, hours: int = 24) -> Dict[str, List[Dict[str, Any]]]:
        """Get performance trends over time."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # Group metrics by hour
        hourly_metrics = defaultdict(lambda: {
            'request_count': 0,
            'avg_duration': 0,
            'error_count': 0,
            'memory_usage': 0,
            'cpu_usage': 0
        })
        
        # Process request metrics
        for req in self.request_metrics:
            if req.timestamp >= cutoff_time:
                hour_key = req.timestamp.replace(minute=0, second=0, microsecond=0)
                hourly_metrics[hour_key]['request_count'] += 1
                hourly_metrics[hour_key]['avg_duration'] += req.duration
                if req.status_code >= 400:
                    hourly_metrics[hour_key]['error_count'] += 1
        
        # Process system metrics
        for metric in self.metrics:
            if metric.timestamp >= cutoff_time:
                hour_key = metric.timestamp.replace(minute=0, second=0, microsecond=0)
                if metric.metric_name == 'memory_usage':
                    hourly_metrics[hour_key]['memory_usage'] = metric.value
                elif metric.metric_name == 'cpu_usage':
                    hourly_metrics[hour_key]['cpu_usage'] = metric.value
        
        # Calculate averages and format
        trends = {
            'requests': [],
            'performance': [],
            'system': []
        }
        
        for hour, data in sorted(hourly_metrics.items()):
            if data['request_count'] > 0:
                data['avg_duration'] = data['avg_duration'] / data['request_count']
                data['error_rate'] = (data['error_count'] / data['request_count'] * 100)
            
            trends['requests'].append({
                'timestamp': hour.isoformat(),
                'count': data['request_count'],
                'error_rate': data.get('error_rate', 0)
            })
            
            trends['performance'].append({
                'timestamp': hour.isoformat(),
                'avg_duration': data['avg_duration']
            })
            
            trends['system'].append({
                'timestamp': hour.isoformat(),
                'memory_usage': data['memory_usage'],
                'cpu_usage': data['cpu_usage']
            })
        
        return trends
    
    def clear_old_data(self, hours: int = 24):
        """Clear old metrics and requests data."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # Clear old metrics
        self.metrics = deque([
            metric for metric in self.metrics
            if metric.timestamp >= cutoff_time
        ], maxlen=self.max_metrics)
        
        # Clear old requests
        self.request_metrics = deque([
            req for req in self.request_metrics
            if req.timestamp >= cutoff_time
        ], maxlen=self.max_requests)
        
        # Clear old alerts
        self.alerts = [
            alert for alert in self.alerts
            if alert['timestamp'] >= cutoff_time
        ]
        
        logger.info(f"Cleared performance data older than {hours} hours")
    
    def get_monitoring_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive monitoring dashboard data."""
        return {
            'system_health': self._calculate_system_health(),
            'request_stats': self._calculate_request_stats(list(self.request_metrics)),
            'top_slow_endpoints': self.get_top_slow_endpoints(),
            'recent_alerts': self._get_recent_alerts(3600),  # Last hour
            'performance_trends': self.get_performance_trends(24),  # Last 24 hours
            'current_metrics': {
                'counters': dict(self.counters),
                'gauges': dict(self.gauges)
            },
            'data_retention': {
                'metrics_count': len(self.metrics),
                'requests_count': len(self.request_metrics),
                'alerts_count': len(self.alerts)
            }
        }
