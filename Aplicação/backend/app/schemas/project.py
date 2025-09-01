from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ProjectStatus(str, Enum):
    NOT_STARTED = "not_started"
    ON_TRACK = "on_track"
    WARNING = "warning"
    DELAYED = "delayed"
    COMPLETED = "completed"

class ProjectType(str, Enum):
    IMPLANTACAO = "implantacao"
    MIGRACAO = "migracao"
    CONFIGURACAO = "configuracao"
    TREINAMENTO = "treinamento"
    SUPORTE = "suporte"

class ProjectIn(BaseModel):
    name: str = Field(..., description="Nome do projeto")
    description: Optional[str] = None
    municipio: str = Field(..., description="Cidade/município")
    entidade: Optional[str] = None
    chamado_jira: Optional[str] = None
    portfolio: Optional[str] = None
    vertical: Optional[str] = None
    product: Optional[str] = None
    tipo: ProjectType = ProjectType.IMPLANTACAO
    data_inicio: datetime
    data_fim: datetime
    etapa_atual: Optional[str] = None
    valor_implantacao: float = Field(default=0.0, ge=0)
    valor_recorrente: float = Field(default=0.0, ge=0)
    recursos: int = Field(default=0, ge=0)
    gerente_projeto_id: int
    gerente_portfolio_id: int

class ProjectOut(ProjectIn):
    id: int
    status: ProjectStatus
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    municipio: Optional[str] = None
    entidade: Optional[str] = None
    chamado_jira: Optional[str] = None
    portfolio: Optional[str] = None
    vertical: Optional[str] = None
    product: Optional[str] = None
    tipo: Optional[ProjectType] = None
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    etapa_atual: Optional[str] = None
    valor_implantacao: Optional[float] = Field(default=None, ge=0)
    valor_recorrente: Optional[float] = Field(default=None, ge=0)
    recursos: Optional[int] = Field(default=None, ge=0)
    gerente_projeto_id: Optional[int] = None
    gerente_portfolio_id: Optional[int] = None

class ProjectMetrics(BaseModel):
    total_projects: int
    total_implantation: float
    total_recurring: float
    total_resources: int
    projects_by_status: dict[str, int]
    projects_by_municipio: dict[str, int]
    projects_by_portfolio: dict[str, int]

class ProjectFilter(BaseModel):
    municipio: Optional[str] = None
    portfolio: Optional[str] = None
    vertical: Optional[str] = None
    status: Optional[ProjectStatus] = None
    gerente_projeto_id: Optional[int] = None
    data_inicio_min: Optional[datetime] = None
    data_fim_max: Optional[datetime] = None

class ProjectTaskIn(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    status: str = "not_started"
    assignee_id: Optional[int] = None

class ProjectTaskOut(ProjectTaskIn):
    id: int
    project_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProjectImplantadorIn(BaseModel):
    user_id: int
    role: Optional[str] = None

class ProjectImplantadorOut(ProjectImplantadorIn):
    id: int
    project_id: int
    
    class Config:
        from_attributes = True

class ProjectMigradorIn(BaseModel):
    user_id: int
    role: Optional[str] = None

class ProjectMigradorOut(ProjectMigradorIn):
    id: int
    project_id: int
    
    class Config:
        from_attributes = True
