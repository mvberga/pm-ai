from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import Session
from app.models.user import User
from app.core.config import settings
from app.utils.auth import create_access_token

router = APIRouter()

class GoogleLoginIn(BaseModel):
    id_token: str
    email: str
    name: str

@router.post("/google/login")
async def google_login(payload: GoogleLoginIn, db: Session):
    # TODO: validate payload.id_token with Google Identity before production use.
    # For MVP/stub: trust the provided email/name
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if not user:
        user = User(email=payload.email, name=payload.name)
        db.add(user)
        await db.commit()
        await db.refresh(user)

    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": token, "token_type": "bearer", "user": {"id": user.id, "email": user.email, "name": user.name}}