"""
Next step model for managing project next steps and action items.
"""

from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.session import Base

class NextStepStatus(enum.Enum):
    """Next step status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"

class NextStepPriority(enum.Enum):
    """Next step priority."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class NextStepType(enum.Enum):
    """Next step types."""
    TASK = "task"
    DECISION = "decision"
    MEETING = "meeting"
    DELIVERABLE = "deliverable"
    REVIEW = "review"
    APPROVAL = "approval"
    COMMUNICATION = "communication"

class NextStep(Base):
    """Next step model for managing project next steps and action items."""
    
    __tablename__ = "next_steps"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Step identification
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    step_type = Column(Enum(NextStepType), nullable=False, default=NextStepType.TASK)
    
    # Step details
    status = Column(Enum(NextStepStatus), nullable=False, default=NextStepStatus.PENDING)
    priority = Column(Enum(NextStepPriority), nullable=False, default=NextStepPriority.MEDIUM)
    
    # Assignment and responsibility
    assigned_to = Column(String(255), nullable=True)  # Person or team responsible
    assigned_by = Column(String(255), nullable=True)  # Person who assigned the step
    
    # Timing
    due_date = Column(DateTime, nullable=True)
    start_date = Column(DateTime, nullable=True)
    completed_date = Column(DateTime, nullable=True)
    
    # Project association
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    
    # Dependencies
    depends_on = Column(String(500), nullable=True)  # Comma-separated IDs of dependent steps
    blocks = Column(String(500), nullable=True)  # Comma-separated IDs of steps this blocks
    
    # Progress tracking
    progress_percentage = Column(Integer, default=0, nullable=False)  # 0-100
    estimated_effort = Column(String(50), nullable=True)  # e.g., "2 hours", "1 day"
    actual_effort = Column(String(50), nullable=True)  # Actual time spent
    
    # Notes and updates
    notes = Column(Text, nullable=True)
    last_update = Column(Text, nullable=True)
    
    # Status flags
    is_milestone = Column(Boolean, default=False, nullable=False)
    is_critical_path = Column(Boolean, default=False, nullable=False)
    requires_approval = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="next_steps")
    
    def __repr__(self):
        return f"<NextStep(id={self.id}, title='{self.title}', status='{self.status.value}', priority='{self.priority.value}')>"
    
    @property
    def is_pending(self) -> bool:
        """Check if step is pending."""
        return self.status == NextStepStatus.PENDING
    
    @property
    def is_in_progress(self) -> bool:
        """Check if step is in progress."""
        return self.status == NextStepStatus.IN_PROGRESS
    
    @property
    def is_completed(self) -> bool:
        """Check if step is completed."""
        return self.status == NextStepStatus.COMPLETED
    
    @property
    def is_overdue(self) -> bool:
        """Check if step is overdue."""
        if not self.due_date or self.is_completed:
            return False
        return datetime.now() > self.due_date
    
    @property
    def is_due_soon(self) -> bool:
        """Check if step is due within 3 days."""
        if not self.due_date or self.is_completed:
            return False
        three_days_from_now = datetime.now() + timedelta(days=3)
        return self.due_date <= three_days_from_now
    
    @property
    def is_high_priority(self) -> bool:
        """Check if step is high priority."""
        return self.priority == NextStepPriority.HIGH or self.priority == NextStepPriority.URGENT
    
    @property
    def is_urgent(self) -> bool:
        """Check if step is urgent."""
        return self.priority == NextStepPriority.URGENT
    
    @property
    def is_critical(self) -> bool:
        """Check if step is critical path."""
        return self.is_critical_path
    
    @property
    def is_milestone_step(self) -> bool:
        """Check if step is a milestone."""
        return self.is_milestone
    
    @property
    def dependency_list(self) -> list:
        """Get dependencies as a list of IDs."""
        if not self.depends_on:
            return []
        return [int(dep.strip()) for dep in self.depends_on.split(",") if dep.strip().isdigit()]
    
    @property
    def blocks_list(self) -> list:
        """Get blocked steps as a list of IDs."""
        if not self.blocks:
            return []
        return [int(block.strip()) for block in self.blocks.split(",") if block.strip().isdigit()]
    
    @property
    def status_description(self) -> str:
        """Get human-readable status description."""
        status_map = {
            NextStepStatus.PENDING: "Pending",
            NextStepStatus.IN_PROGRESS: "In Progress",
            NextStepStatus.COMPLETED: "Completed",
            NextStepStatus.CANCELLED: "Cancelled",
            NextStepStatus.ON_HOLD: "On Hold"
        }
        return status_map.get(self.status, "Unknown")
    
    @property
    def priority_description(self) -> str:
        """Get human-readable priority description."""
        priority_map = {
            NextStepPriority.LOW: "Low",
            NextStepPriority.MEDIUM: "Medium",
            NextStepPriority.HIGH: "High",
            NextStepPriority.URGENT: "Urgent"
        }
        return priority_map.get(self.priority, "Unknown")
    
    @property
    def days_until_due(self) -> int:
        """Get number of days until due date."""
        if not self.due_date:
            return None
        delta = self.due_date - datetime.now()
        return delta.days
    
    @property
    def is_late(self) -> bool:
        """Check if step is late (overdue and not completed)."""
        return self.is_overdue and not self.is_completed
