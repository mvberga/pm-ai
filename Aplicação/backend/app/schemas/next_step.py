from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class NextStepBase(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: int
    priority: str = "medium"
    status: str = "pending"
    due_date: Optional[datetime] = None

class NextStepCreate(NextStepBase):
    pass

class NextStepUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    project_id: Optional[int] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None

class NextStepInDB(NextStepBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class NextStep(NextStepBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class NextStepWithProject(NextStep):
    project: dict = {}

class NextStepSummary(BaseModel):
    id: int
    title: str
    priority: str
    status: str
    project_name: str

class NextStepAnalysis(BaseModel):
    total_steps: int
    by_priority: dict = {}
    by_status: dict = {}
    overdue_steps: int = 0

class NextStepBulkCreate(BaseModel):
    steps: List[NextStepCreate]

class NextStepBulkUpdate(BaseModel):
    steps: List[NextStepUpdate]