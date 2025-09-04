"""
Tests for repositories layer.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from app.repositories.user_repository import UserRepository
from app.repositories.project_repository import ProjectRepository
from app.models.user import User
from app.models.project import Project

@pytest.fixture
def mock_session():
    """Mock database session."""
    return AsyncMock()

@pytest.fixture
def user_repository(mock_session):
    """User repository instance."""
    return UserRepository(mock_session)

@pytest.fixture
def project_repository(mock_session):
    """Project repository instance."""
    return ProjectRepository(mock_session)

class TestUserRepository:
    """Test cases for UserRepository."""
    
    @pytest.mark.asyncio
    async def test_get_by_email_success(self, user_repository, mock_session):
        """Test getting user by email."""
        email = "test@example.com"
        mock_user = MagicMock()
        mock_user.email = email
        
        mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user
        
        result = await user_repository.get_by_email(email)
        
        assert result == mock_user
        mock_session.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_by_email_not_found(self, user_repository, mock_session):
        """Test getting user by email when not found."""
        email = "nonexistent@example.com"
        
        mock_session.execute.return_value.scalar_one_or_none.return_value = None
        
        result = await user_repository.get_by_email(email)
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_active_users(self, user_repository, mock_session):
        """Test getting active users."""
        mock_users = [MagicMock(), MagicMock()]
        mock_session.execute.return_value.scalars.return_value.all.return_value = mock_users
        
        result = await user_repository.get_active_users()
        
        assert len(result) == 2
        mock_session.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_user_statistics(self, user_repository, mock_session):
        """Test getting user statistics."""
        # Mock count results
        mock_session.execute.return_value.scalar.return_value = 10
        
        result = await user_repository.get_user_statistics()
        
        assert 'total_users' in result
        assert 'active_users' in result
        assert 'inactive_users' in result
        assert 'activation_rate' in result

class TestProjectRepository:
    """Test cases for ProjectRepository."""
    
    @pytest.mark.asyncio
    async def test_get_by_owner(self, project_repository, mock_session):
        """Test getting projects by owner."""
        owner_id = 1
        mock_projects = [MagicMock(), MagicMock()]
        
        mock_session.execute.return_value.scalars.return_value.all.return_value = mock_projects
        
        result = await project_repository.get_by_owner(owner_id)
        
        assert len(result) == 2
        mock_session.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_by_status(self, project_repository, mock_session):
        """Test getting projects by status."""
        status = "active"
        owner_id = 1
        mock_projects = [MagicMock()]
        
        mock_session.execute.return_value.scalars.return_value.all.return_value = mock_projects
        
        result = await project_repository.get_by_status(status, owner_id)
        
        assert len(result) == 1
        mock_session.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_search_projects(self, project_repository, mock_session):
        """Test searching projects."""
        query = "test"
        owner_id = 1
        mock_projects = [MagicMock()]
        
        mock_session.execute.return_value.scalars.return_value.all.return_value = mock_projects
        
        result = await project_repository.search_projects(query, owner_id)
        
        assert len(result) == 1
        mock_session.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_project_statistics(self, project_repository, mock_session):
        """Test getting project statistics."""
        owner_id = 1
        
        # Mock count results
        mock_session.execute.return_value.scalar.return_value = 5
        
        result = await project_repository.get_project_statistics(owner_id)
        
        assert 'total_projects' in result
        assert 'active_projects' in result
        assert 'completed_projects' in result
        assert 'on_hold_projects' in result
        assert 'completion_rate' in result
