from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select, func, and_
from app.core.deps import Session, CurrentUser, OptionalUser
from app.models.project import Project, ProjectStatus, ProjectTask, ProjectImplantador, ProjectMigrador
from app.schemas.project import (
    ProjectIn, ProjectOut, ProjectMetrics, ProjectFilter, ProjectUpdate,
    ProjectTaskIn, ProjectTaskOut,
    ProjectImplantadorIn, ProjectImplantadorOut,
    ProjectMigradorIn, ProjectMigradorOut
)
from typing import Optional
import asyncio

router = APIRouter()

@router.get("/", response_model=list[ProjectOut])
async def list_projects(
    db: Session,
    current_user: CurrentUser,
    municipio: Optional[str] = Query(None),
    portfolio: Optional[str] = Query(None),
    vertical: Optional[str] = Query(None),
    status: Optional[ProjectStatus] = Query(None),
    gerente_projeto_id: Optional[int] = Query(None)
):
    """Lista projetos com filtros opcionais"""
    query = select(Project)
    
    filters = []
    if municipio:
        filters.append(Project.municipio.ilike(f"%{municipio}%"))
    if portfolio:
        filters.append(Project.portfolio == portfolio)
    if vertical:
        filters.append(Project.vertical == vertical)
    if status:
        filters.append(Project.status == status)
    if gerente_projeto_id:
        filters.append(Project.gerente_projeto_id == gerente_projeto_id)
    
    if filters:
        query = query.where(and_(*filters))
    
    res = await db.execute(query)
    return res.scalars().all()

@router.get("/metrics", response_model=ProjectMetrics)
async def get_project_metrics(db: Session, current_user: CurrentUser):
    """Retorna métricas agregadas do portfólio"""
    # Total de projetos
    total_projects = await db.scalar(select(func.count(Project.id)))
    
    # Valores totais
    total_implantation = await db.scalar(select(func.sum(Project.valor_implantacao)))
    total_recurring = await db.scalar(select(func.sum(Project.valor_recorrente)))
    total_resources = await db.scalar(select(func.sum(Project.recursos)))
    
    # Projetos por status
    status_counts = await db.execute(
        select(Project.status, func.count(Project.id))
        .group_by(Project.status)
    )
    projects_by_status = {status.value: count for status, count in status_counts}
    
    # Projetos por município
    municipio_counts = await db.execute(
        select(Project.municipio, func.count(Project.id))
        .group_by(Project.municipio)
    )
    projects_by_municipio = {municipio: count for municipio, count in municipio_counts}
    
    # Projetos por portfólio
    portfolio_counts = await db.execute(
        select(Project.portfolio_name, func.count(Project.id))
        .where(Project.portfolio_name.isnot(None))
        .group_by(Project.portfolio_name)
    )
    projects_by_portfolio = {portfolio: count for portfolio, count in portfolio_counts}
    
    return ProjectMetrics(
        total_projects=total_projects or 0,
        total_implantation=total_implantation or 0.0,
        total_recurring=total_recurring or 0.0,
        total_resources=total_resources or 0,
        projects_by_status=projects_by_status,
        projects_by_municipio=projects_by_municipio,
        projects_by_portfolio=projects_by_portfolio
    )

@router.post("/", response_model=ProjectOut, status_code=201)
async def create_project(payload: ProjectIn, db: Session, current_user: CurrentUser, request: Request):
    """Cria um novo projeto"""
    project = Project(**payload.model_dump(), owner_id=1)  # TODO: take from auth context
    # Lock específico do app, criado no loop atual
    # Lock global de escrita
    write_lock = getattr(request.app.state, "db_write_lock", None)
    if write_lock is None:
        write_lock = asyncio.Lock()
        request.app.state.db_write_lock = write_lock
    lock = getattr(request.app.state, "create_project_lock", None)
    if lock is None:
        lock = asyncio.Lock()
        request.app.state.create_project_lock = lock
    async with write_lock:
        db.add(project)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        await db.refresh(project)
        return project

@router.get("/{project_id}", response_model=ProjectOut)
async def get_project(project_id: int, db: Session, current_user: CurrentUser):
    """Retorna um projeto específico"""
    res = await db.execute(select(Project).where(Project.id == project_id))
    project = res.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: int, db: Session, current_user: CurrentUser, request: Request):
    """Remove um projeto e seus relacionamentos em cascata"""
    write_lock = getattr(request.app.state, "db_write_lock", None)
    if write_lock is None:
        write_lock = asyncio.Lock()
        request.app.state.db_write_lock = write_lock
    async with write_lock:
        res = await db.execute(select(Project).where(Project.id == project_id))
        project = res.scalar_one_or_none()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        await db.delete(project)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return None

@router.put("/{project_id}", response_model=ProjectOut)
async def update_project(project_id: int, payload: ProjectUpdate, db: Session, current_user: CurrentUser, request: Request):
    """Atualiza um projeto existente"""
    write_lock = getattr(request.app.state, "db_write_lock", None)
    if write_lock is None:
        write_lock = asyncio.Lock()
        request.app.state.db_write_lock = write_lock
    lock = getattr(request.app.state, "update_project_lock", None)
    if lock is None:
        lock = asyncio.Lock()
        request.app.state.update_project_lock = lock
    async with write_lock:
        res = await db.execute(select(Project).where(Project.id == project_id))
        project = res.scalar_one_or_none()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(project, field, value)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        await db.refresh(project)
        return project

# Endpoints para Tarefas
@router.get("/{project_id}/tasks", response_model=list[ProjectTaskOut])
async def list_project_tasks(project_id: int, db: Session):
    """Lista tarefas de um projeto"""
    res = await db.execute(select(ProjectTask).where(ProjectTask.project_id == project_id))
    return res.scalars().all()

@router.post("/{project_id}/tasks", response_model=ProjectTaskOut)
async def create_project_task(project_id: int, payload: ProjectTaskIn, db: Session):
    """Cria uma nova tarefa para um projeto"""
    task = ProjectTask(**payload.model_dump(), project_id=project_id)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

# Endpoints para Implantadores
@router.get("/{project_id}/implantadores", response_model=list[ProjectImplantadorOut])
async def list_project_implantadores(project_id: int, db: Session):
    """Lista implantadores de um projeto"""
    res = await db.execute(select(ProjectImplantador).where(ProjectImplantador.project_id == project_id))
    return res.scalars().all()

@router.post("/{project_id}/implantadores", response_model=ProjectImplantadorOut)
async def add_project_implantador(project_id: int, payload: ProjectImplantadorIn, db: Session):
    """Adiciona um implantador a um projeto"""
    implantador = ProjectImplantador(**payload.model_dump(), project_id=project_id)
    db.add(implantador)
    await db.commit()
    await db.refresh(implantador)
    return implantador

# Endpoints para Migradores
@router.get("/{project_id}/migradores", response_model=list[ProjectMigradorOut])
async def list_project_migradores(project_id: int, db: Session):
    """Lista migradores de um projeto"""
    res = await db.execute(select(ProjectMigrador).where(ProjectMigrador.project_id == project_id))
    return res.scalars().all()

@router.post("/{project_id}/migradores", response_model=ProjectMigradorOut)
async def add_project_migrador(project_id: int, payload: ProjectMigradorIn, db: Session):
    """Adiciona um migrador a um projeto"""
    migrador = ProjectMigrador(**payload.model_dump(), project_id=project_id)
    db.add(migrador)
    await db.commit()
    await db.refresh(migrador)
    return migrador