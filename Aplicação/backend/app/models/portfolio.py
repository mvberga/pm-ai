"""
Portfolio model for managing project portfolios.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base

class Portfolio(Base):
    """Portfolio model for grouping related projects."""
    
    __tablename__ = "portfolios"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Portfolio metadata
    status = Column(String(50), default="active", nullable=False)  # active, archived, planning
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    
    # Ownership and access
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    owner = relationship("User", foreign_keys=[owner_id], back_populates="owned_portfolios")
    creator = relationship("User", foreign_keys=[created_by])
    projects = relationship("Project", back_populates="portfolio", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Portfolio(id={self.id}, name='{self.name}', status='{self.status}')>"
    
    @property
    def is_active(self) -> bool:
        """Check if portfolio is active."""
        return self.status == "active"
    
    @property
    def is_archived(self) -> bool:
        """Check if portfolio is archived."""
        return self.status == "archived"
    
    @property
    def project_count(self) -> int:
        """Get number of projects in portfolio."""
        return len(self.projects) if self.projects else 0
    
    @property
    def completion_rate(self) -> float:
        """Calculate portfolio completion rate based on projects."""
        if not self.projects:
            return 0.0
        
        completed_projects = len([p for p in self.projects if p.status == "completed"])
        return (completed_projects / len(self.projects)) * 100
