"""
Risk model for managing project risks and mitigation strategies.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.session import Base

class RiskCategory(enum.Enum):
    """Risk categories."""
    TECHNICAL = "technical"
    BUSINESS = "business"
    FINANCIAL = "financial"
    OPERATIONAL = "operational"
    EXTERNAL = "external"
    REGULATORY = "regulatory"
    SECURITY = "security"
    RESOURCE = "resource"

class RiskStatus(enum.Enum):
    """Risk status."""
    IDENTIFIED = "identified"
    ANALYZED = "analyzed"
    MITIGATED = "mitigated"
    MONITORED = "monitored"
    CLOSED = "closed"
    ACCEPTED = "accepted"

class RiskPriority(enum.Enum):
    """Risk priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Risk(Base):
    """Risk model for managing project risks and mitigation strategies."""
    
    __tablename__ = "risks"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Risk identification
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(Enum(RiskCategory), nullable=False, default=RiskCategory.TECHNICAL)
    
    # Risk assessment
    probability = Column(Float, nullable=False, default=0.5)  # 0.0 to 1.0
    impact = Column(Float, nullable=False, default=0.5)  # 0.0 to 1.0
    priority = Column(Enum(RiskPriority), nullable=False, default=RiskPriority.MEDIUM)
    status = Column(Enum(RiskStatus), nullable=False, default=RiskStatus.IDENTIFIED)
    
    # Risk details
    root_cause = Column(Text, nullable=True)
    potential_impact = Column(Text, nullable=True)
    warning_signs = Column(Text, nullable=True)
    
    # Mitigation strategy
    mitigation_strategy = Column(Text, nullable=True)
    contingency_plan = Column(Text, nullable=True)
    mitigation_owner = Column(String(255), nullable=True)
    mitigation_deadline = Column(DateTime, nullable=True)
    
    # Monitoring
    monitoring_frequency = Column(String(50), default="weekly", nullable=False)
    last_review_date = Column(DateTime, nullable=True)
    next_review_date = Column(DateTime, nullable=True)
    
    # Project association
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    
    # AI integration
    ai_analysis = Column(Text, nullable=True)  # AI-generated analysis
    ai_recommendations = Column(Text, nullable=True)  # AI-generated recommendations
    ai_confidence_score = Column(Float, nullable=True)  # AI confidence in analysis
    
    # Timestamps
    identified_date = Column(DateTime, nullable=False, default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="risks")
    
    def __repr__(self):
        return f"<Risk(id={self.id}, title='{self.title}', priority='{self.priority.value}', status='{self.status.value}')>"
    
    @property
    def risk_score(self) -> float:
        """Calculate risk score (probability * impact)."""
        return self.probability * self.impact
    
    @property
    def is_high_risk(self) -> bool:
        """Check if risk is high priority or high score."""
        return self.priority == RiskPriority.HIGH or self.priority == RiskPriority.CRITICAL or self.risk_score >= 0.7
    
    @property
    def is_critical(self) -> bool:
        """Check if risk is critical."""
        return self.priority == RiskPriority.CRITICAL or self.risk_score >= 0.8
    
    @property
    def is_mitigated(self) -> bool:
        """Check if risk is mitigated."""
        return self.status == RiskStatus.MITIGATED or self.status == RiskStatus.CLOSED
    
    @property
    def is_overdue_review(self) -> bool:
        """Check if risk review is overdue."""
        if not self.next_review_date:
            return False
        return datetime.now() > self.next_review_date
    
    @property
    def risk_level_description(self) -> str:
        """Get human-readable risk level description."""
        if self.risk_score >= 0.8:
            return "Very High Risk"
        elif self.risk_score >= 0.6:
            return "High Risk"
        elif self.risk_score >= 0.4:
            return "Medium Risk"
        elif self.risk_score >= 0.2:
            return "Low Risk"
        else:
            return "Very Low Risk"
    
    @property
    def mitigation_status(self) -> str:
        """Get mitigation status description."""
        if self.status == RiskStatus.CLOSED:
            return "Risk Closed"
        elif self.status == RiskStatus.MITIGATED:
            return "Mitigated"
        elif self.status == RiskStatus.MONITORED:
            return "Under Monitoring"
        elif self.status == RiskStatus.ANALYZED:
            return "Analysis Complete"
        else:
            return "Under Analysis"
