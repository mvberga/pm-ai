"""
Custom exceptions for the application.
"""

class PMAIException(Exception):
    """Base exception for PM AI MVP application."""
    pass

class NotFoundError(PMAIException):
    """Raised when a resource is not found."""
    pass

class ValidationError(PMAIException):
    """Raised when validation fails."""
    pass

class AuthenticationError(PMAIException):
    """Raised when authentication fails."""
    pass

class AuthorizationError(PMAIException):
    """Raised when authorization fails."""
    pass

class DatabaseError(PMAIException):
    """Raised when database operations fail."""
    pass

class ExternalServiceError(PMAIException):
    """Raised when external service calls fail."""
    pass
