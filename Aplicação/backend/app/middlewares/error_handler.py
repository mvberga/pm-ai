import logging
from typing import Union
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

logger = logging.getLogger(__name__)

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle Pydantic validation errors"""
    logger.warning(
        "Validation error",
        extra={
            "request_id": getattr(request.state, "request_id", None),
            "errors": exc.errors(),
            "body": exc.body
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": "validation_error",
            "detail": "Invalid request data",
            "fields": exc.errors(),
            "type": "https://tools.ietf.org/html/rfc7231#section-6.5.1"
        }
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handle HTTP exceptions"""
    logger.info(
        "HTTP exception",
        extra={
            "request_id": getattr(request.state, "request_id", None),
            "status_code": exc.status_code,
            "detail": exc.detail
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": f"http_{exc.status_code}",
            "detail": exc.detail,
            "type": "https://tools.ietf.org/html/rfc7231#section-6.5.1"
        }
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Handle database errors"""
    logger.error(
        "Database error",
        extra={
            "request_id": getattr(request.state, "request_id", None),
            "error": str(exc),
            "error_type": type(exc).__name__
        },
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": "database_error",
            "detail": "Internal database error",
            "type": "https://tools.ietf.org/html/rfc7231#section-6.5.1"
        }
    )

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions"""
    logger.error(
        "Unexpected error",
        extra={
            "request_id": getattr(request.state, "request_id", None),
            "error": str(exc),
            "error_type": type(exc).__name__
        },
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": "internal_error",
            "detail": "Internal server error",
            "type": "https://tools.ietf.org/html/rfc7231#section-6.5.1"
        }
    )
