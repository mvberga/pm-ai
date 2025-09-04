"""
Lesson learned model for capturing and managing project lessons.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.session import Base

class LessonCategory(enum.Enum):
    """Lesson learned categories."""
    TECHNICAL = "technical"
    PROCESS = "process"
    COMMUNICATION = "communication"
    MANAGEMENT = "management"
    QUALITY = "quality"
    RESOURCE = "resource"
    CLIENT = "client"
    TEAM = "team"

class LessonType(enum.Enum):
    """Lesson types."""
    SUCCESS = "success"
    FAILURE = "failure"
    IMPROVEMENT = "improvement"
    BEST_PRACTICE = "best_practice"
    WARNING = "warning"

class LessonLearned(Base):
    """Lesson learned model for capturing and managing project lessons."""
    
    __tablename__ = "lessons_learned"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Lesson identification
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(Enum(LessonCategory), nullable=False, default=LessonCategory.PROCESS)
    lesson_type = Column(Enum(LessonType), nullable=False, default=LessonType.IMPROVEMENT)
    
    # Lesson details
    situation = Column(Text, nullable=True)  # What was the situation?
    action = Column(Text, nullable=True)  # What action was taken?
    result = Column(Text, nullable=True)  # What was the result?
    impact = Column(Text, nullable=True)  # What was the impact?
    
    # Recommendations
    recommendations = Column(Text, nullable=True)
    best_practices = Column(Text, nullable=True)
    things_to_avoid = Column(Text, nullable=True)
    
    # Project association
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    
    # Metadata
    tags = Column(String(500), nullable=True)  # Comma-separated tags
    is_public = Column(Boolean, default=True, nullable=False)  # Can be shared across projects
    is_archived = Column(Boolean, default=False, nullable=False)
    
    # Usage tracking
    view_count = Column(Integer, default=0, nullable=False)
    last_viewed = Column(DateTime, nullable=True)
    
    # Timestamps
    lesson_date = Column(DateTime, nullable=False, default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="lessons_learned")
    
    def __repr__(self):
        return f"<LessonLearned(id={self.id}, title='{self.title}', category='{self.category.value}', type='{self.lesson_type.value}')>"
    
    @property
    def is_success(self) -> bool:
        """Check if lesson is about success."""
        return self.lesson_type == LessonType.SUCCESS
    
    @property
    def is_failure(self) -> bool:
        """Check if lesson is about failure."""
        return self.lesson_type == LessonType.FAILURE
    
    @property
    def is_best_practice(self) -> bool:
        """Check if lesson is a best practice."""
        return self.lesson_type == LessonType.BEST_PRACTICE
    
    @property
    def is_warning(self) -> bool:
        """Check if lesson is a warning."""
        return self.lesson_type == LessonType.WARNING
    
    @property
    def tag_list(self) -> list:
        """Get tags as a list."""
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]
    
    @property
    def summary(self) -> str:
        """Get a summary of the lesson."""
        if len(self.description) <= 200:
            return self.description
        return self.description[:200] + "..."
    
    @property
    def is_recent(self) -> bool:
        """Check if lesson is recent (within last 30 days)."""
        thirty_days_ago = datetime.now() - timedelta(days=30)
        return self.lesson_date > thirty_days_ago
    
    @property
    def is_popular(self) -> bool:
        """Check if lesson is popular (viewed more than 10 times)."""
        return self.view_count > 10
