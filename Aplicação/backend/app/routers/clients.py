"""
Client router for client management endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import Session, CurrentUser
from app.schemas.client import ClientCreate, ClientUpdate, ClientResponse
from app.services.client_service import ClientService

router = APIRouter()

@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def create_client(
    client_data: ClientCreate,
    session: Session,
    current_user: CurrentUser
):
    """Create a new client."""
    try:
        service = ClientService(session)
        client = await service.create_client(client_data, current_user.id)
        return client
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/", response_model=List[ClientResponse])
async def get_clients(
    session: Session,
    current_user: CurrentUser,
    project_id: int = Query(..., description="Project ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    client_type_filter: Optional[str] = Query(None, description="Filter by client type")
):
    """Get all clients for a project."""
    try:
        service = ClientService(session)
        clients = await service.get_project_clients(
            project_id, 
            current_user.id, 
            skip=skip, 
            limit=limit,
            client_type_filter=client_type_filter
        )
        return clients
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Get a specific client by ID."""
    try:
        service = ClientService(session)
        client = await service.get_client_by_id(client_id, current_user.id)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
        return client
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    client_data: ClientUpdate,
    session: Session,
    current_user: CurrentUser
):
    """Update a client."""
    try:
        service = ClientService(session)
        client = await service.update_client(client_id, current_user.id, client_data)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
        return client
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: int,
    session: Session,
    current_user: CurrentUser
):
    """Delete a client."""
    try:
        service = ClientService(session)
        success = await service.delete_client(client_id, current_user.id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/project/{project_id}/statistics")
async def get_client_statistics(
    session: Session,
    current_user: CurrentUser,
    project_id: int
):
    """Get client statistics for a project."""
    try:
        service = ClientService(session)
        stats = await service.get_client_statistics(project_id, current_user.id)
        if not stats:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return stats
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/{client_id}/update-satisfaction")
async def update_client_satisfaction(
    session: Session,
    current_user: CurrentUser,
    client_id: int,
    satisfaction_score: int = Query(..., ge=1, le=10, description="Satisfaction score (1-10)")
):
    """Update client satisfaction score."""
    try:
        service = ClientService(session)
        success = await service.update_satisfaction_score(client_id, current_user.id, satisfaction_score)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
        return {"message": "Satisfaction score updated successfully"}
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/{client_id}/schedule-contact")
async def schedule_client_contact(
    session: Session,
    current_user: CurrentUser,
    client_id: int,
    next_contact_date: str = Query(..., description="Next contact date (YYYY-MM-DD)")
):
    """Schedule next client contact."""
    try:
        from datetime import datetime
        contact_date = datetime.fromisoformat(next_contact_date)
        
        service = ClientService(session)
        success = await service.schedule_next_contact(client_id, current_user.id, contact_date)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
        return {"message": "Next contact scheduled successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/project/{project_id}/communication-plan")
async def get_communication_plan(
    session: Session,
    current_user: CurrentUser,
    project_id: int
):
    """Get communication plan for project clients."""
    try:
        service = ClientService(session)
        plan = await service.get_communication_plan(project_id, current_user.id)
        return plan
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
