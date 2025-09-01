from pydantic import BaseModel
from typing import Optional, List

class ChecklistGroupIn(BaseModel):
    name: str
    project_id: int  # Adicionado campo obrigatório

class ChecklistGroupOut(ChecklistGroupIn):
    id: int
    class Config:
        from_attributes = True

class ChecklistItemIn(BaseModel):
    title: str
    type: str  # 'Ação' or 'Documentação'
    notes: Optional[str] = None
    is_done: Optional[bool] = False

class ChecklistItemOut(ChecklistItemIn):
    id: int
    group_id: int
    class Config:
        from_attributes = True
