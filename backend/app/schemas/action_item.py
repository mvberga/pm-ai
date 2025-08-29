from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Optional
from datetime import datetime

class ActionItemIn(BaseModel):
    title: str
    type: str
    project_id: int  # Adicionado campo obrigatório
    priority: Optional[str] = None
    assignee_id: Optional[int] = None
    status: Optional[str] = "open"
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    # Aceitar campos extras (ex.: priority) sem falhar
    model_config = ConfigDict(extra="ignore")

class ActionItemOut(ActionItemIn):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True
