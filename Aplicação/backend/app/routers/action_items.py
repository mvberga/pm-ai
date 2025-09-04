from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.deps import Session
from app.models.action_item import ActionItem
from app.schemas.action_item import ActionItemIn, ActionItemOut

router = APIRouter()

@router.get("/action-items", response_model=list[ActionItemOut])
async def list_action_items(db: Session):
    res = await db.execute(select(ActionItem))
    return res.scalars().all()

@router.post("/action-items", response_model=ActionItemOut, status_code=201)
async def create_action_item(payload: ActionItemIn, db: Session, request: Request):
    action_item = ActionItem(**payload.model_dump())
    lock = getattr(request.app.state, "db_write_lock", None)
    if lock is None:
        import asyncio
        lock = asyncio.Lock()
        request.app.state.db_write_lock = lock
    async with lock:
        db.add(action_item)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        await db.refresh(action_item)
        return action_item

@router.get("/action-items/{action_item_id}", response_model=ActionItemOut)
async def get_action_item(action_item_id: int, db: Session):
    res = await db.execute(select(ActionItem).where(ActionItem.id == action_item_id))
    action_item = res.scalar_one_or_none()
    if not action_item:
        raise HTTPException(status_code=404, detail="Action item not found")
    return action_item