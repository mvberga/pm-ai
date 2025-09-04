"""
Schemas Pydantic para validação de dados
"""

# Schemas existentes
from .user import User, UserCreate, UserUpdate, UserInDB
from .project import Project, ProjectCreate, ProjectUpdate, ProjectInDB
from .checklist import ChecklistGroup, ChecklistGroupCreate, ChecklistGroupUpdate, ChecklistItem, ChecklistItemCreate, ChecklistItemUpdate
from .action_item import ActionItem, ActionItemCreate, ActionItemUpdate, ActionItemInDB

# Novos schemas
from .portfolio import (
    Portfolio, PortfolioCreate, PortfolioUpdate, PortfolioInDB,
    PortfolioWithProjects, PortfolioWithOwner, PortfolioSummary
)
from .team_member import (
    TeamMember, TeamMemberCreate, TeamMemberUpdate, TeamMemberInDB,
    TeamMemberWithProject, TeamMemberSummary, TeamMemberBulkCreate, TeamMemberBulkUpdate
)
from .client import (
    Client, ClientCreate, ClientUpdate, ClientInDB,
    ClientWithProject, ClientSummary, ClientBulkCreate, ClientBulkUpdate
)
from .risk import (
    Risk, RiskCreate, RiskUpdate, RiskInDB,
    RiskWithProject, RiskSummary, RiskAnalysis, RiskBulkCreate, RiskBulkUpdate
)
from .lesson_learned import (
    LessonLearned, LessonLearnedCreate, LessonLearnedUpdate, LessonLearnedInDB,
    LessonLearnedWithProject, LessonLearnedSummary, LessonLearnedAnalysis,
    LessonLearnedBulkCreate, LessonLearnedBulkUpdate
)
from .next_step import (
    NextStep, NextStepCreate, NextStepUpdate, NextStepInDB,
    NextStepWithProject, NextStepSummary, NextStepAnalysis,
    NextStepBulkCreate, NextStepBulkUpdate
)

__all__ = [
    # Schemas existentes
    "User", "UserCreate", "UserUpdate", "UserInDB",
    "Project", "ProjectCreate", "ProjectUpdate", "ProjectInDB",
    "ChecklistGroup", "ChecklistGroupCreate", "ChecklistGroupUpdate",
    "ChecklistItem", "ChecklistItemCreate", "ChecklistItemUpdate",
    "ActionItem", "ActionItemCreate", "ActionItemUpdate", "ActionItemInDB",
    
    # Novos schemas
    "Portfolio", "PortfolioCreate", "PortfolioUpdate", "PortfolioInDB",
    "PortfolioWithProjects", "PortfolioWithOwner", "PortfolioSummary",
    "TeamMember", "TeamMemberCreate", "TeamMemberUpdate", "TeamMemberInDB",
    "TeamMemberWithProject", "TeamMemberSummary", "TeamMemberBulkCreate", "TeamMemberBulkUpdate",
    "Client", "ClientCreate", "ClientUpdate", "ClientInDB",
    "ClientWithProject", "ClientSummary", "ClientBulkCreate", "ClientBulkUpdate",
    "Risk", "RiskCreate", "RiskUpdate", "RiskInDB",
    "RiskWithProject", "RiskSummary", "RiskAnalysis", "RiskBulkCreate", "RiskBulkUpdate",
    "LessonLearned", "LessonLearnedCreate", "LessonLearnedUpdate", "LessonLearnedInDB",
    "LessonLearnedWithProject", "LessonLearnedSummary", "LessonLearnedAnalysis",
    "LessonLearnedBulkCreate", "LessonLearnedBulkUpdate",
    "NextStep", "NextStepCreate", "NextStepUpdate", "NextStepInDB",
    "NextStepWithProject", "NextStepSummary", "NextStepAnalysis",
    "NextStepBulkCreate", "NextStepBulkUpdate"
]
