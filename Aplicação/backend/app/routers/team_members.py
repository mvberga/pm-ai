"""
Team member router for team management endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import Session, CurrentUser
from app.schemas.team_member import TeamMemberCreate, TeamMemberUpdate, TeamMemberResponse
from app.services.team_member_service import TeamMemberService

router = APIRouter()

@router.post("/", response_model=TeamMemberResponse, status_code=status.HTTP_201_CREATED)
async def create_team_member(
    team_member_data: TeamMemberCreate,
    session: Session,
    current_user: CurrentUser
):
    """Create a new team member."""
    try:
        service = TeamMemberService(session)
        team_member = await service.create_team_member(team_member_data, current_user.id)
        return team_member
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/", response_model=List[TeamMemberResponse])
async def get_team_members(
    session: Session,
    current_user: CurrentUser,
    project_id: int = Query(..., description="Project ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    role_filter: Optional[str] = Query(None, description="Filter by role")
):
    """Get all team members for a project."""
    try:
        service = TeamMemberService(session)
        team_members = await service.get_project_team_members(
            project_id, 
            current_user.id, 
            skip=skip, 
            limit=limit,
            role_filter=role_filter
        )
        return team_members
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/{team_member_id}", response_model=TeamMemberResponse)
async def get_team_member(
    team_member_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Get a specific team member by ID."""
    try:
        service = TeamMemberService(session)
        team_member = await service.get_team_member_by_id(team_member_id, current_user.id)
        if not team_member:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found")
        return team_member
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.put("/{team_member_id}", response_model=TeamMemberResponse)
async def update_team_member(
    team_member_id: int,
    team_member_data: TeamMemberUpdate,
    session: Session,
    current_user: CurrentUser
):
    """Update a team member."""
    try:
        service = TeamMemberService(session)
        team_member = await service.update_team_member(team_member_id, current_user.id, team_member_data)
        if not team_member:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found")
        return team_member
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/{team_member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team_member(
    team_member_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Delete a team member."""
    try:
        service = TeamMemberService(session)
        success = await service.delete_team_member(team_member_id, current_user.id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/project/{project_id}/statistics")
async def get_team_statistics(
    session: Session,
    current_user: CurrentUser,
    project_id: int
):
    """Get team statistics for a project."""
    try:
        service = TeamMemberService(session)
        stats = await service.get_team_statistics(project_id, current_user.id)
        if not stats:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return stats
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/project/{project_id}/by-role")
async def get_team_members_by_role(
    session: Session,
    current_user: CurrentUser,
    project_id: int
):
    """Get team members grouped by role."""
    try:
        service = TeamMemberService(session)
        team_by_role = await service.get_team_members_by_role(project_id, current_user.id)
        return team_by_role
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/{team_member_id}/activate")
async def activate_team_member(
    team_member_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Activate a team member."""
    try:
        service = TeamMemberService(session)
        success = await service.activate_team_member(team_member_id, current_user.id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found")
        return {"message": "Team member activated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/{team_member_id}/deactivate")
async def deactivate_team_member(
    team_member_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Deactivate a team member."""
    try:
        service = TeamMemberService(session)
        success = await service.deactivate_team_member(team_member_id, current_user.id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found")
        return {"message": "Team member deactivated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
