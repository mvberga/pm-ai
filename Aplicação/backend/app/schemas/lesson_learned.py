from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class LessonLearnedBase(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: int
    category: str = "general"
    impact: str = "medium"
    status: str = "draft"

class LessonLearnedCreate(LessonLearnedBase):
    pass

class LessonLearnedUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    project_id: Optional[int] = None
    category: Optional[str] = None
    impact: Optional[str] = None
    status: Optional[str] = None

class LessonLearnedInDB(LessonLearnedBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class LessonLearned(LessonLearnedBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class LessonLearnedWithProject(LessonLearned):
    project: dict = {}

class LessonLearnedSummary(BaseModel):
    id: int
    title: str
    category: str
    impact: str
    project_name: str

class LessonLearnedAnalysis(BaseModel):
    total_lessons: int
    by_category: dict = {}
    by_impact: dict = {}
    by_status: dict = {}

class LessonLearnedBulkCreate(BaseModel):
    lessons: List[LessonLearnedCreate]

class LessonLearnedBulkUpdate(BaseModel):
    lessons: List[LessonLearnedUpdate]