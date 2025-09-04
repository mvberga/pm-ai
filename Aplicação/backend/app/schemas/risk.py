from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class RiskBase(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: int
    risk_level: str = "medium"
    status: str = "open"
    mitigation_plan: Optional[str] = None

class RiskCreate(RiskBase):
    pass

class RiskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    project_id: Optional[int] = None
    risk_level: Optional[str] = None
    status: Optional[str] = None
    mitigation_plan: Optional[str] = None

class RiskInDB(RiskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class Risk(RiskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class RiskWithProject(Risk):
    project: dict = {}

class RiskSummary(BaseModel):
    id: int
    title: str
    risk_level: str
    status: str
    project_name: str

class RiskAnalysis(BaseModel):
    total_risks: int
    high_risks: int
    medium_risks: int
    low_risks: int
    open_risks: int
    closed_risks: int

class RiskBulkCreate(BaseModel):
    risks: List[RiskCreate]

class RiskBulkUpdate(BaseModel):
    risks: List[RiskUpdate]

class RiskResponse(Risk):
    pass