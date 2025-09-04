from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import Session
from app.models.user import User
from app.core.config import settings
from app.utils.auth import create_access_token, verify_password
from app.schemas.user import UserLogin

router = APIRouter()

class GoogleLoginIn(BaseModel):
    id_token: str
    email: str
    name: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

@router.post("/google/login")
async def google_login(payload: GoogleLoginIn, db: Session):
    # TODO: validate payload.id_token with Google Identity before production use.
    # For MVP/stub: trust the provided email/name
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if not user:
        user = User(
            email=payload.email, 
            name=payload.name,
            hashed_password="google_oauth_user"  # Valor padrão para usuários OAuth
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": token, "token_type": "bearer", "user": {"id": user.id, "email": user.email, "name": user.name}}

@router.get("/test")
async def test_auth():
    """Endpoint de teste para verificar se o router está funcionando"""
    return {"message": "Auth router funcionando", "status": "ok"}

@router.get("/test-db")
async def test_db(db: Session):
    """Endpoint de teste para verificar se a sessão do banco está funcionando"""
    try:
        # Teste simples de conexão com o banco
        result = await db.execute(select(User).limit(1))
        user = result.scalar_one_or_none()
        return {"message": "Database connection working", "user_count": 1 if user else 0}
    except Exception as e:
        return {"error": str(e), "message": "Database connection failed"}

@router.post("/login", response_model=LoginResponse)
async def login(login_data: UserLogin, db: Session):
    """
    Authenticate user with email and password.
    
    Args:
        login_data: User login credentials (email and password)
        db: Database session
        
    Returns:
        Access token and user information
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        # Get user by email
        result = await db.execute(select(User).where(User.email == login_data.email))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Credenciais inválidas"
            )
        
        # Verify password
        if not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Credenciais inválidas"
            )
        
        # Create access token
        token = create_access_token({"sub": str(user.id), "email": user.email})
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Erro interno do servidor"
        )