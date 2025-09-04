"""
Security middleware for request validation and protection.
"""

import time
import logging
from typing import Callable, Optional
from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.security.security_enhancer import SecurityEnhancer, ThreatType, SecurityLevel

logger = logging.getLogger(__name__)

class SecurityMiddleware(BaseHTTPMiddleware):
    """Security middleware for request validation and protection."""
    
    def __init__(self, app: ASGIApp, security_enhancer: SecurityEnhancer):
        super().__init__(app)
        self.security = security_enhancer
        self.start_time = time.time()
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with security validation."""
        # Extract request information
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "")
        method = request.method
        path = request.url.path
        user_id = getattr(request.state, 'user_id', None)
        
        # Check if IP is blocked
        if self.security.is_ip_blocked(client_ip):
            logger.warning(f"Blocked IP {client_ip} attempted to access {path}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Validate request path for path traversal
        path_validation = self.security.validate_input(path, "path")
        if not path_validation['is_safe']:
            self.security._record_security_event(
                ThreatType.MALICIOUS_INPUT,
                SecurityLevel.HIGH,
                user_id,
                client_ip,
                path,
                {
                    'threats': path_validation['threats_detected'],
                    'original_path': path,
                    'sanitized_path': path_validation['sanitized_input']
                }
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid request path"
            )
        
        # Check rate limits based on endpoint type
        endpoint_type = self._get_endpoint_type(path, method)
        rate_limit_result = self.security.check_rate_limit(
            str(user_id) if user_id else client_ip,
            endpoint_type,
            client_ip
        )
        
        if not rate_limit_result['allowed']:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
                headers={
                    "Retry-After": str(int((rate_limit_result['reset_time'] - time.time()))),
                    "X-RateLimit-Limit": str(rate_limit_result['rate_limit_config']['requests']),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(rate_limit_result['reset_time'].timestamp()))
                }
            )
        
        # Validate query parameters
        if request.query_params:
            for param_name, param_value in request.query_params.items():
                param_validation = self.security.validate_input(param_value, "general")
                if not param_validation['is_safe']:
                    self.security._record_security_event(
                        ThreatType.MALICIOUS_INPUT,
                        SecurityLevel.MEDIUM,
                        user_id,
                        client_ip,
                        path,
                        {
                            'parameter': param_name,
                            'threats': param_validation['threats_detected'],
                            'original_value': param_value,
                            'sanitized_value': param_validation['sanitized_input']
                        }
                    )
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid parameter: {param_name}"
                    )
        
        # Validate request body for POST/PUT/PATCH requests
        if method in ['POST', 'PUT', 'PATCH']:
            try:
                # Read request body
                body = await request.body()
                if body:
                    # Check content type
                    content_type = request.headers.get("content-type", "")
                    
                    # Validate JSON content
                    if "application/json" in content_type:
                        import json
                        try:
                            json_data = json.loads(body.decode())
                            self._validate_json_data(json_data, user_id, client_ip, path)
                        except json.JSONDecodeError:
                            raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid JSON format"
                            )
                    
                    # Validate form data
                    elif "application/x-www-form-urlencoded" in content_type:
                        form_data = body.decode()
                        form_validation = self.security.validate_input(form_data, "general")
                        if not form_validation['is_safe']:
                            self.security._record_security_event(
                                ThreatType.MALICIOUS_INPUT,
                                SecurityLevel.MEDIUM,
                                user_id,
                                client_ip,
                                path,
                                {
                                    'content_type': 'form',
                                    'threats': form_validation['threats_detected']
                                }
                            )
                            raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid form data"
                            )
                    
                    # Validate text content
                    elif "text/" in content_type:
                        text_validation = self.security.validate_input(body.decode(), "general")
                        if not text_validation['is_safe']:
                            self.security._record_security_event(
                                ThreatType.MALICIOUS_INPUT,
                                SecurityLevel.MEDIUM,
                                user_id,
                                client_ip,
                                path,
                                {
                                    'content_type': 'text',
                                    'threats': text_validation['threats_detected']
                                }
                            )
                            raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid text content"
                            )
                
                # Create new request with validated body
                request._body = body
                
            except Exception as e:
                if isinstance(e, HTTPException):
                    raise
                logger.error(f"Error validating request body: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Request validation failed"
                )
        
        # Add security headers
        response = await call_next(request)
        
        # Add security headers to response
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        # Add rate limit headers
        if 'X-RateLimit-Limit' not in response.headers:
            response.headers["X-RateLimit-Limit"] = str(rate_limit_result['rate_limit_config']['requests'])
            response.headers["X-RateLimit-Remaining"] = str(
                rate_limit_result['rate_limit_config']['requests'] - 
                len(self.security.rate_limit_tracker.get(
                    f"{endpoint_type}:{user_id if user_id else client_ip}", []
                ))
            )
            response.headers["X-RateLimit-Reset"] = str(int(rate_limit_result['reset_time'].timestamp()))
        
        return response
    
    def _get_endpoint_type(self, path: str, method: str) -> str:
        """Determine endpoint type for rate limiting."""
        if path.startswith("/api/v1/auth/login"):
            return "login"
        elif path.startswith("/api/v1/auth/password-reset"):
            return "password_reset"
        elif "upload" in path or method == "POST" and "file" in path:
            return "upload"
        else:
            return "api"
    
    def _validate_json_data(self, data: dict, user_id: Optional[int], client_ip: str, path: str):
        """Validate JSON data recursively."""
        if isinstance(data, dict):
            for key, value in data.items():
                # Validate key
                key_validation = self.security.validate_input(str(key), "general")
                if not key_validation['is_safe']:
                    self.security._record_security_event(
                        ThreatType.MALICIOUS_INPUT,
                        SecurityLevel.MEDIUM,
                        user_id,
                        client_ip,
                        path,
                        {
                            'field': 'key',
                            'threats': key_validation['threats_detected'],
                            'original_value': str(key)
                        }
                    )
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid field name: {key}"
                    )
                
                # Validate value
                if isinstance(value, str):
                    value_validation = self.security.validate_input(value, "general")
                    if not value_validation['is_safe']:
                        self.security._record_security_event(
                            ThreatType.MALICIOUS_INPUT,
                            SecurityLevel.MEDIUM,
                            user_id,
                            client_ip,
                            path,
                            {
                                'field': key,
                                'threats': value_validation['threats_detected'],
                                'original_value': value
                            }
                        )
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid value for field: {key}"
                        )
                elif isinstance(value, (dict, list)):
                    self._validate_json_data(value, user_id, client_ip, path)
        
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    self._validate_json_data(item, user_id, client_ip, path)
                elif isinstance(item, str):
                    item_validation = self.security.validate_input(item, "general")
                    if not item_validation['is_safe']:
                        self.security._record_security_event(
                            ThreatType.MALICIOUS_INPUT,
                            SecurityLevel.MEDIUM,
                            user_id,
                            client_ip,
                            path,
                            {
                                'field': 'array_item',
                                'threats': item_validation['threats_detected'],
                                'original_value': item
                            }
                        )
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid array item"
                        )

class AuthenticationSecurityMiddleware:
    """Security middleware for authentication endpoints."""
    
    def __init__(self, security_enhancer: SecurityEnhancer):
        self.security = security_enhancer
        self.failed_attempts = {}  # Track failed login attempts
        self.lockout_duration = 900  # 15 minutes
    
    def check_login_attempts(self, identifier: str, ip_address: str) -> bool:
        """Check if login attempts are within limits."""
        current_time = time.time()
        
        # Check user-based attempts
        user_key = f"user:{identifier}"
        if user_key in self.failed_attempts:
            attempts, lockout_time = self.failed_attempts[user_key]
            if current_time < lockout_time:
                return False
        
        # Check IP-based attempts
        ip_key = f"ip:{ip_address}"
        if ip_key in self.failed_attempts:
            attempts, lockout_time = self.failed_attempts[ip_key]
            if current_time < lockout_time:
                return False
        
        return True
    
    def record_failed_login(self, identifier: str, ip_address: str):
        """Record a failed login attempt."""
        current_time = time.time()
        max_attempts = 5
        
        # Record user-based attempt
        user_key = f"user:{identifier}"
        if user_key in self.failed_attempts:
            attempts, _ = self.failed_attempts[user_key]
            attempts += 1
        else:
            attempts = 1
        
        if attempts >= max_attempts:
            lockout_time = current_time + self.lockout_duration
            self.failed_attempts[user_key] = (attempts, lockout_time)
            
            # Record security event
            self.security._record_security_event(
                ThreatType.BRUTE_FORCE,
                SecurityLevel.HIGH,
                int(identifier) if identifier.isdigit() else None,
                ip_address,
                "/api/v1/auth/login",
                {
                    'attempts': attempts,
                    'lockout_duration': self.lockout_duration,
                    'identifier': identifier
                }
            )
        else:
            self.failed_attempts[user_key] = (attempts, current_time)
        
        # Record IP-based attempt
        ip_key = f"ip:{ip_address}"
        if ip_key in self.failed_attempts:
            attempts, _ = self.failed_attempts[ip_key]
            attempts += 1
        else:
            attempts = 1
        
        if attempts >= max_attempts:
            lockout_time = current_time + self.lockout_duration
            self.failed_attempts[ip_key] = (attempts, lockout_time)
        else:
            self.failed_attempts[ip_key] = (attempts, current_time)
    
    def record_successful_login(self, identifier: str, ip_address: str):
        """Record a successful login and clear failed attempts."""
        user_key = f"user:{identifier}"
        ip_key = f"ip:{ip_address}"
        
        if user_key in self.failed_attempts:
            del self.failed_attempts[user_key]
        
        if ip_key in self.failed_attempts:
            del self.failed_attempts[ip_key]
    
    def get_lockout_time(self, identifier: str, ip_address: str) -> Optional[float]:
        """Get remaining lockout time for identifier or IP."""
        current_time = time.time()
        
        # Check user-based lockout
        user_key = f"user:{identifier}"
        if user_key in self.failed_attempts:
            attempts, lockout_time = self.failed_attempts[user_key]
            if current_time < lockout_time:
                return lockout_time - current_time
        
        # Check IP-based lockout
        ip_key = f"ip:{ip_address}"
        if ip_key in self.failed_attempts:
            attempts, lockout_time = self.failed_attempts[ip_key]
            if current_time < lockout_time:
                return lockout_time - current_time
        
        return None
    
    def cleanup_old_attempts(self, hours: int = 24):
        """Clean up old failed login attempts."""
        current_time = time.time()
        cutoff_time = current_time - (hours * 3600)
        
        keys_to_remove = []
        for key, (attempts, lockout_time) in self.failed_attempts.items():
            if lockout_time < cutoff_time:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.failed_attempts[key]
        
        logger.info(f"Cleaned up {len(keys_to_remove)} old failed login attempts")

class CSRFProtectionMiddleware:
    """CSRF protection middleware."""
    
    def __init__(self, security_enhancer: SecurityEnhancer):
        self.security = security_enhancer
        self.csrf_tokens = {}  # Store CSRF tokens
        self.token_expiry = 3600  # 1 hour
    
    def generate_csrf_token(self, session_id: str) -> str:
        """Generate a CSRF token for a session."""
        token = self.security.generate_secure_token(32)
        self.csrf_tokens[token] = {
            'session_id': session_id,
            'created_at': time.time(),
            'expires_at': time.time() + self.token_expiry
        }
        return token
    
    def validate_csrf_token(self, token: str, session_id: str) -> bool:
        """Validate a CSRF token."""
        if token not in self.csrf_tokens:
            return False
        
        token_data = self.csrf_tokens[token]
        
        # Check if token is expired
        if time.time() > token_data['expires_at']:
            del self.csrf_tokens[token]
            return False
        
        # Check if token matches session
        if token_data['session_id'] != session_id:
            return False
        
        return True
    
    def cleanup_expired_tokens(self):
        """Clean up expired CSRF tokens."""
        current_time = time.time()
        expired_tokens = [
            token for token, data in self.csrf_tokens.items()
            if current_time > data['expires_at']
        ]
        
        for token in expired_tokens:
            del self.csrf_tokens[token]
        
        if expired_tokens:
            logger.info(f"Cleaned up {len(expired_tokens)} expired CSRF tokens")
