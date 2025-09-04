"""
Team member model for managing project team members.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.session import Base

class TeamRole(enum.Enum):
    """Team member roles."""
    PROJECT_MANAGER = "project_manager"
    DEVELOPER = "developer"
    DESIGNER = "designer"
    ANALYST = "analyst"
    TESTER = "tester"
    CLIENT = "client"
    STAKEHOLDER = "stakeholder"
    CONSULTANT = "consultant"

class TeamMember(Base):
    """Team member model for project team management."""
    
    __tablename__ = "team_members"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Member information
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    position = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)
    
    # Role and responsibilities
    role = Column(Enum(TeamRole), nullable=False, default=TeamRole.STAKEHOLDER)
    responsibilities = Column(Text, nullable=True)
    
    # Project association
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    
    # Access and permissions
    is_active = Column(Boolean, default=True, nullable=False)
    can_edit = Column(Boolean, default=False, nullable=False)
    can_view_financials = Column(Boolean, default=False, nullable=False)
    
    # Communication preferences
    preferred_communication = Column(String(50), default="email", nullable=False)  # email, phone, slack, etc.
    communication_frequency = Column(String(50), default="weekly", nullable=False)  # daily, weekly, monthly
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="team_members")
    
    def __repr__(self):
        return f"<TeamMember(id={self.id}, name='{self.name}', role='{self.role.value}', project_id={self.project_id})>"
    
    @property
    def is_project_manager(self) -> bool:
        """Check if member is a project manager."""
        return self.role == TeamRole.PROJECT_MANAGER
    
    @property
    def is_client(self) -> bool:
        """Check if member is a client."""
        return self.role == TeamRole.CLIENT
    
    @property
    def is_developer(self) -> bool:
        """Check if member is a developer."""
        return self.role == TeamRole.DEVELOPER
    
    @property
    def full_contact_info(self) -> str:
        """Get full contact information."""
        contact_parts = [self.name]
        if self.email:
            contact_parts.append(f"Email: {self.email}")
        if self.phone:
            contact_parts.append(f"Phone: {self.phone}")
        if self.company:
            contact_parts.append(f"Company: {self.company}")
        return " | ".join(contact_parts)
