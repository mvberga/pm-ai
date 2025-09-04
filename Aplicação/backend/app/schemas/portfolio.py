from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class PortfolioBase(BaseModel):
    name: str
    description: Optional[str] = None
    owner_id: int

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[int] = None

class PortfolioInDB(PortfolioBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class Portfolio(PortfolioBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class PortfolioWithProjects(Portfolio):
    projects: List[dict] = []

class PortfolioWithOwner(Portfolio):
    owner: dict = {}

class PortfolioSummary(BaseModel):
    id: int
    name: str
    project_count: int = 0
    total_value: float = 0.0