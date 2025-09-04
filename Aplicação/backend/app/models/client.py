"""
Client model for managing client information and communication.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.session import Base

class ClientType(enum.Enum):
    """Client types."""
    CORPORATE = "corporate"
    GOVERNMENT = "government"
    NON_PROFIT = "non_profit"
    STARTUP = "startup"
    INDIVIDUAL = "individual"

class CommunicationLevel(enum.Enum):
    """Communication levels."""
    EXECUTIVE = "executive"
    MANAGERIAL = "managerial"
    OPERATIONAL = "operational"
    TECHNICAL = "technical"

class Client(Base):
    """Client model for managing client information and communication."""
    
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Client information
    name = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=True, index=True)
    client_type = Column(Enum(ClientType), nullable=False, default=ClientType.CORPORATE)
    
    # Contact information
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    website = Column(String(255), nullable=True)
    
    # Communication details
    primary_contact = Column(String(255), nullable=True)
    communication_level = Column(Enum(CommunicationLevel), nullable=False, default=CommunicationLevel.MANAGERIAL)
    preferred_communication = Column(String(50), default="email", nullable=False)
    communication_frequency = Column(String(50), default="weekly", nullable=False)
    
    # Project association
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    
    # Business information
    industry = Column(String(255), nullable=True)
    company_size = Column(String(50), nullable=True)  # small, medium, large, enterprise
    annual_revenue = Column(String(100), nullable=True)
    
    # Relationship management
    satisfaction_score = Column(Integer, nullable=True)  # 1-10 scale
    last_contact_date = Column(DateTime, nullable=True)
    next_contact_date = Column(DateTime, nullable=True)
    
    # Status and notes
    is_active = Column(Boolean, default=True, nullable=False)
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="clients")
    
    def __repr__(self):
        return f"<Client(id={self.id}, name='{self.name}', company='{self.company}', project_id={self.project_id})>"
    
    @property
    def is_corporate(self) -> bool:
        """Check if client is corporate."""
        return self.client_type == ClientType.CORPORATE
    
    @property
    def is_government(self) -> bool:
        """Check if client is government."""
        return self.client_type == ClientType.GOVERNMENT
    
    @property
    def is_startup(self) -> bool:
        """Check if client is a startup."""
        return self.client_type == ClientType.STARTUP
    
    @property
    def full_contact_info(self) -> str:
        """Get full contact information."""
        contact_parts = [self.name]
        if self.company:
            contact_parts.append(f"Company: {self.company}")
        if self.email:
            contact_parts.append(f"Email: {self.email}")
        if self.phone:
            contact_parts.append(f"Phone: {self.phone}")
        return " | ".join(contact_parts)
    
    @property
    def communication_summary(self) -> str:
        """Get communication summary."""
        return f"{self.communication_level.value.title()} level, {self.communication_frequency} via {self.preferred_communication}"
    
    @property
    def is_satisfied(self) -> bool:
        """Check if client satisfaction is good (score >= 7)."""
        return self.satisfaction_score is not None and self.satisfaction_score >= 7
