from sqlalchemy import String, ForeignKey, DateTime, func, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class ChecklistGroup(Base):
    __tablename__ = "checklist_groups"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

class ChecklistItem(Base):
    __tablename__ = "checklist_items"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("checklist_groups.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(20))  # 'Ação' | 'Documentação'
    notes: Mapped[str | None] = mapped_column(Text(), nullable=True)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())
