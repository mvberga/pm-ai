"""
Risk router for risk management endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import Session, CurrentUser
from app.schemas.risk import RiskCreate, RiskUpdate, RiskResponse
from app.services.risk_service import RiskService

router = APIRouter()

@router.post("/", response_model=RiskResponse, status_code=status.HTTP_201_CREATED)
async def create_risk(
    risk_data: RiskCreate,
    session: Session,
    current_user: CurrentUser
):
    """Create a new risk."""
    try:
        service = RiskService(session)
        risk = await service.create_risk(risk_data, current_user.id)
        return risk
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/", response_model=List[RiskResponse])
async def get_risks(
    session: Session,
    current_user: CurrentUser,
    project_id: int = Query(..., description="Project ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    status_filter: Optional[str] = Query(None, description="Filter by status"),
    priority_filter: Optional[str] = Query(None, description="Filter by priority"),
    category_filter: Optional[str] = Query(None, description="Filter by category")
):
    """Get all risks for a project."""
    try:
        service = RiskService(session)
        risks = await service.get_project_risks(
            project_id, 
            current_user.id, 
            skip=skip, 
            limit=limit,
            status_filter=status_filter,
            priority_filter=priority_filter,
            category_filter=category_filter
        )
        return risks
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/{risk_id}", response_model=RiskResponse)
async def get_risk(
    risk_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Get a specific risk by ID."""
    try:
        service = RiskService(session)
        risk = await service.get_risk_by_id(risk_id, current_user.id)
        if not risk:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Risk not found")
        return risk
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.put("/{risk_id}", response_model=RiskResponse)
async def update_risk(
    risk_id: int,
    risk_data: RiskUpdate,
    session: Session,
    current_user: CurrentUser
):
    """Update a risk."""
    try:
        service = RiskService(session)
        risk = await service.update_risk(risk_id, current_user.id, risk_data)
        if not risk:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Risk not found")
        return risk
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/{risk_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_risk(
    risk_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Delete a risk."""
    try:
        service = RiskService(session)
        success = await service.delete_risk(risk_id, current_user.id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Risk not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/project/{project_id}/statistics")
async def get_risk_statistics(
    project_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Get risk statistics for a project."""
    try:
        service = RiskService(session)
        stats = await service.get_risk_statistics(project_id, current_user.id)
        if not stats:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return stats
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/project/{project_id}/high-priority")
async def get_high_priority_risks(
    project_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Get high priority risks for a project."""
    try:
        service = RiskService(session)
        risks = await service.get_high_priority_risks(project_id, current_user.id)
        return risks
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/project/{project_id}/overdue-reviews")
async def get_overdue_reviews(
    project_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Get risks with overdue reviews."""
    try:
        service = RiskService(session)
        risks = await service.get_overdue_reviews(project_id, current_user.id)
        return risks
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/{risk_id}/update-status")
async def update_risk_status(
    risk_id: int,
    session: Session,
    current_user: CurrentUser,
    status: str = Query(..., description="New risk status")
):
    """Update risk status."""
    try:
        service = RiskService(session)
        success = await service.update_risk_status(risk_id, current_user.id, status)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Risk not found")
        return {"message": "Risk status updated successfully"}
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/{risk_id}/ai-analysis")
async def generate_ai_analysis(
    risk_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Generate AI analysis for a risk."""
    try:
        service = RiskService(session)
        analysis = await service.generate_ai_analysis(risk_id, current_user.id)
        if not analysis:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Risk not found")
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/{risk_id}/schedule-review")
async def schedule_risk_review(
    risk_id: int,
    session: Session,
    current_user: CurrentUser,
    next_review_date: str = Query(..., description="Next review date (YYYY-MM-DD)")
):
    """Schedule next risk review."""
    try:
        from datetime import datetime
        review_date = datetime.fromisoformat(next_review_date)
        
        service = RiskService(session)
        success = await service.schedule_next_review(risk_id, current_user.id, review_date)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Risk not found")
        return {"message": "Next review scheduled successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
