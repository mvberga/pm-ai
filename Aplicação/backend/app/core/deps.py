from typing import Annotated, AsyncGenerator
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.models.user import User
from app.utils.auth import decode_access_token, security, verify_token

# Database session dependency
Session = Annotated[AsyncSession, Depends(get_session)]

# User authentication dependency
async def get_current_user(
    session: Session,
    token: str = Depends(decode_access_token)
) -> User:
    """Get current authenticated user from JWT token"""
    user = await session.get(User, token.get("sub"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    # Alguns modelos podem não ter o atributo is_active no MVP.
    # Tratar como ativo por padrão, e apenas bloquear se o atributo existir e for False.
    if getattr(user, "is_active", True) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return user

# Current user dependency
CurrentUser = Annotated[User, Depends(get_current_user)]

# Optional user dependency (for endpoints that can work with or without auth)
async def get_optional_user(
    session: Session,
    credentials: HTTPAuthorizationCredentials | None = Security(security)
) -> User | None:
    """Get current user if authenticated, None otherwise.

    - Sem header Authorization: retorna None (público).
    - Com header inválido: propaga 401.
    """
    if credentials is None or not credentials.credentials:
        return None
    payload = verify_token(credentials.credentials)  # pode levantar 401 se inválido
    user = await session.get(User, payload.get("sub"))
    return user

OptionalUser = Annotated[User | None, Depends(get_optional_user)]