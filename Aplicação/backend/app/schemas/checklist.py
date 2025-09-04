from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class ChecklistGroupBase(BaseModel):
    name: str
    project_id: int

class ChecklistGroupCreate(ChecklistGroupBase):
    pass

class ChecklistGroupUpdate(BaseModel):
    name: Optional[str] = None
    project_id: Optional[int] = None

class ChecklistGroupInDB(ChecklistGroupBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ChecklistGroup(ChecklistGroupBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ChecklistGroupOut(ChecklistGroup):
    pass

class ChecklistGroupIn(ChecklistGroupBase):
    pass

class ChecklistItemBase(BaseModel):
    title: str
    type: str  # 'Ação' or 'Documentação'
    notes: Optional[str] = None
    is_done: Optional[bool] = False

class ChecklistItemCreate(ChecklistItemBase):
    group_id: int

class ChecklistItemUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[str] = None
    notes: Optional[str] = None
    is_done: Optional[bool] = None

class ChecklistItemInDB(ChecklistItemBase):
    id: int
    group_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ChecklistItem(ChecklistItemBase):
    id: int
    group_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ChecklistItemOut(ChecklistItem):
    pass

class ChecklistItemIn(ChecklistItemBase):
    group_id: int
