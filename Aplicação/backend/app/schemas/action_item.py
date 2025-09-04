from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ActionItemBase(BaseModel):
    title: str
    type: str
    project_id: int
    priority: Optional[str] = None
    assignee_id: Optional[int] = None
    status: Optional[str] = "open"
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    model_config = ConfigDict(extra="ignore")

class ActionItemCreate(ActionItemBase):
    pass

class ActionItemUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[str] = None
    project_id: Optional[int] = None
    priority: Optional[str] = None
    assignee_id: Optional[int] = None
    status: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    model_config = ConfigDict(extra="ignore")

class ActionItemInDB(ActionItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class ActionItem(ActionItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class ActionItemOut(ActionItem):
    pass

class ActionItemIn(ActionItemBase):
    pass
