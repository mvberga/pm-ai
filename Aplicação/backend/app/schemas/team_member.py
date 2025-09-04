from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class TeamMemberBase(BaseModel):
    user_id: int
    project_id: int
    role: str
    is_active: bool = True

class TeamMemberCreate(TeamMemberBase):
    pass

class TeamMemberUpdate(BaseModel):
    user_id: Optional[int] = None
    project_id: Optional[int] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class TeamMemberInDB(TeamMemberBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class TeamMember(TeamMemberBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class TeamMemberWithProject(TeamMember):
    project: dict = {}

class TeamMemberSummary(BaseModel):
    id: int
    user_id: int
    role: str
    project_name: str

class TeamMemberBulkCreate(BaseModel):
    members: List[TeamMemberCreate]

class TeamMemberBulkUpdate(BaseModel):
    members: List[TeamMemberUpdate]

class TeamMemberResponse(TeamMember):
    pass