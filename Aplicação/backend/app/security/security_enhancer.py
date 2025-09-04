"""
Security enhancement system for the application.
"""

import re
import hashlib
import secrets
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from fastapi import HTTPException, status
from pydantic import BaseModel, validator
from sqlalchemy import text

logger = logging.getLogger(__name__)

class SecurityLevel(Enum):
    """Security levels for different operations."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatType(Enum):
    """Types of security threats."""
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    CSRF = "csrf"
    BRUTE_FORCE = "brute_force"
    RATE_LIMIT = "rate_limit"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    DATA_LEAK = "data_leak"
    MALICIOUS_INPUT = "malicious_input"

@dataclass
class SecurityEvent:
    """Security event data structure."""
    timestamp: datetime
    event_type: ThreatType
    severity: SecurityLevel
    user_id: Optional[int]
    ip_address: Optional[str]
    endpoint: str
    details: Dict[str, Any]
    blocked: bool = False

class SecurityEnhancer:
    """Security enhancement system."""
    
    def __init__(self):
        self.security_events = []
        self.blocked_ips = set()
        self.suspicious_patterns = {
            'sql_injection': [
                r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)",
                r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
                r"(\b(OR|AND)\s+'.*'\s*=\s*'.*')",
                r"(;\s*(DROP|DELETE|INSERT|UPDATE))",
                r"(\b(UNION|SELECT)\s+.*\bFROM\b)",
                r"(\b(SCRIPT|JAVASCRIPT|VBSCRIPT)\b)",
                r"(\b(EXEC|EXECUTE|SP_)\b)",
                r"(\b(WAITFOR|DELAY)\b)",
                r"(\b(CHAR|ASCII|SUBSTRING)\b)",
                r"(\b(CAST|CONVERT)\b)"
            ],
            'xss': [
                r"<script[^>]*>.*?</script>",
                r"javascript:",
                r"on\w+\s*=",
                r"<iframe[^>]*>",
                r"<object[^>]*>",
                r"<embed[^>]*>",
                r"<link[^>]*>",
                r"<meta[^>]*>",
                r"<style[^>]*>",
                r"expression\s*\(",
                r"url\s*\(",
                r"@import"
            ],
            'path_traversal': [
                r"\.\./",
                r"\.\.\\",
                r"%2e%2e%2f",
                r"%2e%2e%5c",
                r"\.\.%2f",
                r"\.\.%5c",
                r"\.\.%252f",
                r"\.\.%255c"
            ],
            'command_injection': [
                r"[;&|`$]",
                r"\b(cat|ls|pwd|whoami|id|uname|ps|netstat|ifconfig)\b",
                r"\b(ping|nslookup|traceroute|telnet|ssh|ftp)\b",
                r"\b(wget|curl|nc|netcat)\b",
                r"\b(rm|mv|cp|chmod|chown)\b"
            ]
        }
        
        # Rate limiting configuration
        self.rate_limits = {
            'login': {'requests': 5, 'window': 300},  # 5 requests per 5 minutes
            'api': {'requests': 100, 'window': 60},   # 100 requests per minute
            'upload': {'requests': 10, 'window': 60}, # 10 uploads per minute
            'password_reset': {'requests': 3, 'window': 3600}  # 3 resets per hour
        }
        
        self.rate_limit_tracker = {}
    
    def validate_input(self, input_data: str, input_type: str = "general") -> Dict[str, Any]:
        """
        Validate input data for security threats.
        
        Args:
            input_data: Input string to validate
            input_type: Type of input (sql, html, path, etc.)
            
        Returns:
            Validation result with security assessment
        """
        validation_result = {
            'is_safe': True,
            'threats_detected': [],
            'sanitized_input': input_data,
            'risk_level': SecurityLevel.LOW
        }
        
        if not input_data or not isinstance(input_data, str):
            return validation_result
        
        # Check for SQL injection patterns
        if input_type in ['sql', 'general']:
            for pattern in self.suspicious_patterns['sql_injection']:
                if re.search(pattern, input_data, re.IGNORECASE):
                    validation_result['threats_detected'].append({
                        'type': ThreatType.SQL_INJECTION,
                        'pattern': pattern,
                        'severity': SecurityLevel.HIGH
                    })
                    validation_result['is_safe'] = False
                    validation_result['risk_level'] = SecurityLevel.HIGH
        
        # Check for XSS patterns
        if input_type in ['html', 'general']:
            for pattern in self.suspicious_patterns['xss']:
                if re.search(pattern, input_data, re.IGNORECASE):
                    validation_result['threats_detected'].append({
                        'type': ThreatType.XSS,
                        'pattern': pattern,
                        'severity': SecurityLevel.MEDIUM
                    })
                    validation_result['is_safe'] = False
                    if validation_result['risk_level'] == SecurityLevel.LOW:
                        validation_result['risk_level'] = SecurityLevel.MEDIUM
        
        # Check for path traversal
        if input_type in ['path', 'general']:
            for pattern in self.suspicious_patterns['path_traversal']:
                if re.search(pattern, input_data, re.IGNORECASE):
                    validation_result['threats_detected'].append({
                        'type': ThreatType.MALICIOUS_INPUT,
                        'pattern': pattern,
                        'severity': SecurityLevel.HIGH
                    })
                    validation_result['is_safe'] = False
                    validation_result['risk_level'] = SecurityLevel.HIGH
        
        # Check for command injection
        if input_type in ['command', 'general']:
            for pattern in self.suspicious_patterns['command_injection']:
                if re.search(pattern, input_data, re.IGNORECASE):
                    validation_result['threats_detected'].append({
                        'type': ThreatType.MALICIOUS_INPUT,
                        'pattern': pattern,
                        'severity': SecurityLevel.CRITICAL
                    })
                    validation_result['is_safe'] = False
                    validation_result['risk_level'] = SecurityLevel.CRITICAL
        
        # Sanitize input if threats detected
        if not validation_result['is_safe']:
            validation_result['sanitized_input'] = self._sanitize_input(input_data, input_type)
        
        return validation_result
    
    def _sanitize_input(self, input_data: str, input_type: str) -> str:
        """Sanitize input data by removing or escaping dangerous patterns."""
        sanitized = input_data
        
        if input_type in ['sql', 'general']:
            # Remove SQL injection patterns
            for pattern in self.suspicious_patterns['sql_injection']:
                sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        if input_type in ['html', 'general']:
            # Remove XSS patterns
            for pattern in self.suspicious_patterns['xss']:
                sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        if input_type in ['path', 'general']:
            # Remove path traversal patterns
            for pattern in self.suspicious_patterns['path_traversal']:
                sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        if input_type in ['command', 'general']:
            # Remove command injection patterns
            for pattern in self.suspicious_patterns['command_injection']:
                sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        # Additional sanitization
        sanitized = sanitized.strip()
        sanitized = re.sub(r'\s+', ' ', sanitized)  # Normalize whitespace
        
        return sanitized
    
    def check_rate_limit(
        self, 
        identifier: str, 
        endpoint_type: str, 
        ip_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Check if request exceeds rate limits.
        
        Args:
            identifier: User ID or IP address
            endpoint_type: Type of endpoint (login, api, upload, etc.)
            ip_address: IP address for additional tracking
            
        Returns:
            Rate limit check result
        """
        current_time = datetime.now()
        rate_limit_config = self.rate_limits.get(endpoint_type, self.rate_limits['api'])
        
        # Create unique key for tracking
        tracking_key = f"{endpoint_type}:{identifier}"
        if ip_address:
            ip_key = f"{endpoint_type}:ip:{ip_address}"
        else:
            ip_key = None
        
        # Check user rate limit
        user_allowed = self._check_rate_limit_for_key(tracking_key, rate_limit_config, current_time)
        
        # Check IP rate limit if provided
        ip_allowed = True
        if ip_key:
            ip_allowed = self._check_rate_limit_for_key(ip_key, rate_limit_config, current_time)
        
        is_allowed = user_allowed and ip_allowed
        
        # Record security event if rate limit exceeded
        if not is_allowed:
            self._record_security_event(
                ThreatType.RATE_LIMIT,
                SecurityLevel.MEDIUM,
                int(identifier) if identifier.isdigit() else None,
                ip_address,
                endpoint_type,
                {
                    'rate_limit_type': endpoint_type,
                    'identifier': identifier,
                    'user_allowed': user_allowed,
                    'ip_allowed': ip_allowed
                }
            )
        
        return {
            'allowed': is_allowed,
            'user_allowed': user_allowed,
            'ip_allowed': ip_allowed,
            'rate_limit_config': rate_limit_config,
            'reset_time': self._get_reset_time(tracking_key, rate_limit_config, current_time)
        }
    
    def _check_rate_limit_for_key(
        self, 
        key: str, 
        config: Dict[str, int], 
        current_time: datetime
    ) -> bool:
        """Check rate limit for a specific key."""
        if key not in self.rate_limit_tracker:
            self.rate_limit_tracker[key] = []
        
        # Clean old entries
        window_start = current_time - timedelta(seconds=config['window'])
        self.rate_limit_tracker[key] = [
            timestamp for timestamp in self.rate_limit_tracker[key]
            if timestamp > window_start
        ]
        
        # Check if under limit
        if len(self.rate_limit_tracker[key]) >= config['requests']:
            return False
        
        # Add current request
        self.rate_limit_tracker[key].append(current_time)
        return True
    
    def _get_reset_time(
        self, 
        key: str, 
        config: Dict[str, int], 
        current_time: datetime
    ) -> datetime:
        """Get the time when rate limit resets."""
        if key not in self.rate_limit_tracker or not self.rate_limit_tracker[key]:
            return current_time
        
        oldest_request = min(self.rate_limit_tracker[key])
        return oldest_request + timedelta(seconds=config['window'])
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """
        Validate password strength.
        
        Args:
            password: Password to validate
            
        Returns:
            Password strength validation result
        """
        result = {
            'is_strong': True,
            'score': 0,
            'issues': [],
            'recommendations': []
        }
        
        if not password:
            result['is_strong'] = False
            result['issues'].append('Password is required')
            return result
        
        # Length check
        if len(password) < 8:
            result['is_strong'] = False
            result['issues'].append('Password must be at least 8 characters long')
            result['score'] -= 2
        elif len(password) >= 12:
            result['score'] += 2
        
        # Character variety checks
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        
        if not has_lower:
            result['is_strong'] = False
            result['issues'].append('Password must contain lowercase letters')
            result['score'] -= 1
        else:
            result['score'] += 1
        
        if not has_upper:
            result['is_strong'] = False
            result['issues'].append('Password must contain uppercase letters')
            result['score'] -= 1
        else:
            result['score'] += 1
        
        if not has_digit:
            result['is_strong'] = False
            result['issues'].append('Password must contain numbers')
            result['score'] -= 1
        else:
            result['score'] += 1
        
        if not has_special:
            result['issues'].append('Password should contain special characters')
            result['score'] -= 1
        else:
            result['score'] += 2
        
        # Common password check
        common_passwords = [
            'password', '123456', '123456789', 'qwerty', 'abc123',
            'password123', 'admin', 'letmein', 'welcome', 'monkey'
        ]
        
        if password.lower() in common_passwords:
            result['is_strong'] = False
            result['issues'].append('Password is too common')
            result['score'] -= 3
        
        # Sequential characters check
        if re.search(r'(.)\1{2,}', password):
            result['issues'].append('Password contains repeated characters')
            result['score'] -= 1
        
        # Sequential patterns check
        if re.search(r'(012|123|234|345|456|567|678|789|890)', password):
            result['issues'].append('Password contains sequential numbers')
            result['score'] -= 1
        
        # Generate recommendations
        if not has_lower:
            result['recommendations'].append('Add lowercase letters')
        if not has_upper:
            result['recommendations'].append('Add uppercase letters')
        if not has_digit:
            result['recommendations'].append('Add numbers')
        if not has_special:
            result['recommendations'].append('Add special characters')
        if len(password) < 12:
            result['recommendations'].append('Make password longer (12+ characters)')
        
        return result
    
    def generate_secure_token(self, length: int = 32) -> str:
        """Generate a cryptographically secure random token."""
        return secrets.token_urlsafe(length)
    
    def hash_sensitive_data(self, data: str, salt: Optional[str] = None) -> Dict[str, str]:
        """
        Hash sensitive data with salt.
        
        Args:
            data: Data to hash
            salt: Optional salt (generated if not provided)
            
        Returns:
            Dictionary with hash and salt
        """
        if salt is None:
            salt = secrets.token_hex(16)
        
        # Combine data with salt
        salted_data = f"{data}{salt}"
        
        # Generate hash
        hash_value = hashlib.sha256(salted_data.encode()).hexdigest()
        
        return {
            'hash': hash_value,
            'salt': salt
        }
    
    def verify_hash(self, data: str, hash_value: str, salt: str) -> bool:
        """
        Verify hashed data.
        
        Args:
            data: Original data
            hash_value: Stored hash
            salt: Salt used for hashing
            
        Returns:
            True if hash matches
        """
        salted_data = f"{data}{salt}"
        computed_hash = hashlib.sha256(salted_data.encode()).hexdigest()
        return computed_hash == hash_value
    
    def _record_security_event(
        self,
        event_type: ThreatType,
        severity: SecurityLevel,
        user_id: Optional[int],
        ip_address: Optional[str],
        endpoint: str,
        details: Dict[str, Any]
    ):
        """Record a security event."""
        event = SecurityEvent(
            timestamp=datetime.now(),
            event_type=event_type,
            severity=severity,
            user_id=user_id,
            ip_address=ip_address,
            endpoint=endpoint,
            details=details
        )
        
        self.security_events.append(event)
        
        # Log security event
        logger.warning(
            f"Security event: {event_type.value} - {severity.value} - "
            f"User: {user_id} - IP: {ip_address} - Endpoint: {endpoint}"
        )
        
        # Block IP if critical threat
        if severity == SecurityLevel.CRITICAL and ip_address:
            self.blocked_ips.add(ip_address)
            logger.critical(f"IP {ip_address} blocked due to critical security threat")
    
    def is_ip_blocked(self, ip_address: str) -> bool:
        """Check if IP address is blocked."""
        return ip_address in self.blocked_ips
    
    def get_security_events(
        self, 
        hours: int = 24, 
        severity: Optional[SecurityLevel] = None
    ) -> List[SecurityEvent]:
        """Get security events within specified time window."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        events = [
            event for event in self.security_events
            if event.timestamp >= cutoff_time
        ]
        
        if severity:
            events = [event for event in events if event.severity == severity]
        
        return sorted(events, key=lambda x: x.timestamp, reverse=True)
    
    def get_security_summary(self) -> Dict[str, Any]:
        """Get security summary statistics."""
        current_time = datetime.now()
        last_24h = current_time - timedelta(hours=24)
        last_7d = current_time - timedelta(days=7)
        
        # Count events by type and severity
        events_24h = [e for e in self.security_events if e.timestamp >= last_24h]
        events_7d = [e for e in self.security_events if e.timestamp >= last_7d]
        
        threat_counts_24h = {}
        threat_counts_7d = {}
        severity_counts_24h = {}
        severity_counts_7d = {}
        
        for event in events_24h:
            threat_counts_24h[event.event_type.value] = threat_counts_24h.get(event.event_type.value, 0) + 1
            severity_counts_24h[event.severity.value] = severity_counts_24h.get(event.severity.value, 0) + 1
        
        for event in events_7d:
            threat_counts_7d[event.event_type.value] = threat_counts_7d.get(event.event_type.value, 0) + 1
            severity_counts_7d[event.severity.value] = severity_counts_7d.get(event.severity.value, 0) + 1
        
        return {
            'total_events_24h': len(events_24h),
            'total_events_7d': len(events_7d),
            'threat_counts_24h': threat_counts_24h,
            'threat_counts_7d': threat_counts_7d,
            'severity_counts_24h': severity_counts_24h,
            'severity_counts_7d': severity_counts_7d,
            'blocked_ips_count': len(self.blocked_ips),
            'blocked_ips': list(self.blocked_ips),
            'rate_limit_configs': self.rate_limits,
            'active_rate_limits': len(self.rate_limit_tracker)
        }
    
    def cleanup_old_events(self, days: int = 30):
        """Clean up old security events."""
        cutoff_time = datetime.now() - timedelta(days=days)
        self.security_events = [
            event for event in self.security_events
            if event.timestamp >= cutoff_time
        ]
        
        logger.info(f"Cleaned up security events older than {days} days")
    
    def cleanup_old_rate_limits(self, hours: int = 24):
        """Clean up old rate limit data."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        for key in list(self.rate_limit_tracker.keys()):
            self.rate_limit_tracker[key] = [
                timestamp for timestamp in self.rate_limit_tracker[key]
                if timestamp > cutoff_time
            ]
            
            # Remove empty entries
            if not self.rate_limit_tracker[key]:
                del self.rate_limit_tracker[key]
        
        logger.info(f"Cleaned up rate limit data older than {hours} hours")
