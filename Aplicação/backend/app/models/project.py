from sqlalchemy import String, ForeignKey, DateTime, func, Text, Integer, Float, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
import enum

class ProjectStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    ON_TRACK = "on_track"
    WARNING = "warning"
    DELAYED = "delayed"
    COMPLETED = "completed"

class ProjectType(str, enum.Enum):
    IMPLANTACAO = "implantacao"
    MIGRACAO = "migracao"
    CONFIGURACAO = "configuracao"
    TREINAMENTO = "treinamento"
    SUPORTE = "suporte"

class Project(Base):
    __tablename__ = "projects"
    
    # Identificação básica
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)
    
    # Localização e Organização
    municipio: Mapped[str] = mapped_column(String(100), index=True)  # Cidade
    entidade: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    # Rastreamento
    chamado_jira: Mapped[str | None] = mapped_column(String(50), nullable=True)
    
    # Categorização
    portfolio_id: Mapped[int | None] = mapped_column(ForeignKey("portfolios.id"), nullable=True, index=True)
    portfolio_name: Mapped[str | None] = mapped_column(String(100), nullable=True)  # Mantido para compatibilidade
    vertical: Mapped[str | None] = mapped_column(String(100), nullable=True)
    product: Mapped[str | None] = mapped_column(String(100), nullable=True)
    tipo: Mapped[ProjectType] = mapped_column(
        Enum(
            ProjectType,
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
            name="projecttype",
            native_enum=False,
        ),
        default=ProjectType.IMPLANTACAO,
    )
    
    # Cronograma
    data_inicio: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    data_fim: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    etapa_atual: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    # Financeiro
    valor_implantacao: Mapped[float] = mapped_column(Float, default=0.0)
    valor_recorrente: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Status e Recursos
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(
            ProjectStatus,
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
            name="projectstatus",
            native_enum=False,
        ),
        default=ProjectStatus.NOT_STARTED,
    )
    recursos: Mapped[int] = mapped_column(Integer, default=0)
    
    # Responsáveis
    gerente_projeto_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    gerente_portfolio_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    # Timestamps
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    portfolio = relationship("Portfolio", back_populates="projects")
    gerente_projeto = relationship("User", foreign_keys=[gerente_projeto_id])
    gerente_portfolio = relationship("User", foreign_keys=[gerente_portfolio_id])
    owner = relationship("User", foreign_keys=[owner_id])
    members = relationship("ProjectMember", back_populates="project")
    implantadores = relationship("ProjectImplantador", back_populates="project")
    migradores = relationship("ProjectMigrador", back_populates="project")
    tasks = relationship("ProjectTask", back_populates="project")
    
    # Novos relacionamentos para arquitetura expandida
    team_members = relationship("TeamMember", back_populates="project", cascade="all, delete-orphan")
    clients = relationship("Client", back_populates="project", cascade="all, delete-orphan")
    risks = relationship("Risk", back_populates="project", cascade="all, delete-orphan")
    lessons_learned = relationship("LessonLearned", back_populates="project", cascade="all, delete-orphan")
    next_steps = relationship("NextStep", back_populates="project", cascade="all, delete-orphan")

class ProjectMember(Base):
    __tablename__ = "project_members"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    role: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    project = relationship("Project", back_populates="members")
    user = relationship("User")

class ProjectImplantador(Base):
    __tablename__ = "project_implantadores"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    role: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    project = relationship("Project", back_populates="implantadores")
    user = relationship("User")

class ProjectMigrador(Base):
    __tablename__ = "project_migradores"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    role: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    project = relationship("Project", back_populates="migradores")
    user = relationship("User")

class ProjectTask(Base):
    __tablename__ = "project_tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)
    start_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(50), default="not_started")
    assignee_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User")
