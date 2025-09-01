from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.deps import Session
from app.models.checklist import ChecklistGroup, ChecklistItem
from app.schemas.checklist import ChecklistGroupIn, ChecklistGroupOut, ChecklistItemIn, ChecklistItemOut

router = APIRouter()

@router.get("/checklists", response_model=list[ChecklistGroupOut])
async def list_checklists(db: Session):
    res = await db.execute(select(ChecklistGroup))
    return res.scalars().all()

@router.post("/checklists", response_model=ChecklistGroupOut, status_code=201)
async def create_checklist(payload: ChecklistGroupIn, db: Session, request: Request):
    checklist = ChecklistGroup(**payload.model_dump())
    lock = getattr(request.app.state, "db_write_lock", None)
    if lock is None:
        import asyncio
        lock = asyncio.Lock()
        request.app.state.db_write_lock = lock
    async with lock:
        db.add(checklist)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        await db.refresh(checklist)
        return checklist

@router.get("/checklists/{checklist_id}", response_model=ChecklistGroupOut)
async def get_checklist(checklist_id: int, db: Session):
    res = await db.execute(select(ChecklistGroup).where(ChecklistGroup.id == checklist_id))
    checklist = res.scalar_one_or_none()
    if not checklist:
        raise HTTPException(status_code=404, detail="Checklist not found")
    return checklist