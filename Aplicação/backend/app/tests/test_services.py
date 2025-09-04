"""
Tests for services layer.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.auth_service import AuthService
from app.services.project_service import ProjectService
from app.schemas.user import UserCreate
from app.schemas.project import ProjectCreate

@pytest.fixture
def mock_session():
    """Mock database session."""
    return AsyncMock()

@pytest.fixture
def auth_service(mock_session):
    """Auth service instance."""
    return AuthService(mock_session)

@pytest.fixture
def project_service(mock_session):
    """Project service instance."""
    return ProjectService(mock_session)

class TestAuthService:
    """Test cases for AuthService."""
    
    @pytest.mark.asyncio
    async def test_authenticate_user_success(self, auth_service, mock_session):
        """Test successful user authentication."""
        # Mock user data
        mock_user = MagicMock()
        mock_user.email = "test@example.com"
        mock_user.hashed_password = "hashed_password"
        
        # Mock database query
        mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user
        
        # Mock password verification
        with pytest.MonkeyPatch().context() as m:
            m.setattr("app.services.auth_service.verify_password", lambda pwd, hashed: True)
            
            result = await auth_service.authenticate_user("test@example.com", "password")
            
            assert result == mock_user
            mock_session.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_authenticate_user_invalid_credentials(self, auth_service, mock_session):
        """Test authentication with invalid credentials."""
        # Mock database query returning None
        mock_session.execute.return_value.scalar_one_or_none.return_value = None
        
        result = await auth_service.authenticate_user("test@example.com", "wrong_password")
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_create_user_success(self, auth_service, mock_session):
        """Test successful user creation."""
        user_data = UserCreate(
            email="test@example.com",
            password="password123",
            full_name="Test User"
        )
        
        # Mock user not existing
        mock_session.execute.return_value.scalar_one_or_none.return_value = None
        
        # Mock user creation
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = user_data.email
        mock_user.full_name = user_data.full_name
        
        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()
        
        result = await auth_service.create_user(user_data)
        
        assert result is not None
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

class TestProjectService:
    """Test cases for ProjectService."""
    
    @pytest.mark.asyncio
    async def test_create_project_success(self, project_service, mock_session):
        """Test successful project creation."""
        project_data = ProjectCreate(
            name="Test Project",
            description="Test Description",
            status="active"
        )
        user_id = 1
        
        # Mock project creation
        mock_project = MagicMock()
        mock_project.id = 1
        mock_project.name = project_data.name
        mock_project.description = project_data.description
        
        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()
        
        result = await project_service.create_project(project_data, user_id)
        
        assert result is not None
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_user_projects(self, project_service, mock_session):
        """Test getting user projects."""
        user_id = 1
        
        # Mock projects
        mock_projects = [MagicMock(), MagicMock()]
        mock_session.execute.return_value.scalars.return_value.all.return_value = mock_projects
        
        result = await project_service.get_user_projects(user_id)
        
        assert len(result) == 2
        mock_session.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_project_statistics(self, project_service, mock_session):
        """Test getting project statistics."""
        user_id = 1
        
        # Mock statistics data
        mock_session.execute.return_value.scalars.return_value.all.return_value = [MagicMock()] * 5
        
        result = await project_service.get_project_statistics(user_id)
        
        assert 'total_projects' in result
        assert 'active_projects' in result
        assert 'completed_projects' in result
        assert 'completion_rate' in result
