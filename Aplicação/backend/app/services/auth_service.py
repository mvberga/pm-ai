"""
Authentication service for user management and JWT operations.
"""

from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.utils.auth import create_access_token, verify_password

class AuthService:
    """Service for authentication and user management operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password.
        
        Args:
            email: User email
            password: Plain text password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        try:
            # Get user by email
            stmt = select(User).where(User.email == email)
            result = await self.session.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                return None
                
            # Verify password
            if not verify_password(password, user.hashed_password):
                return None
                
            return user
            
        except Exception as e:
            # Log error in production
            print(f"Authentication error: {e}")
            return None
    
    async def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new user.
        
        Args:
            user_data: User creation data
            
        Returns:
            Created user object
            
        Raises:
            ValueError: If user already exists
        """
        try:
            # Check if user already exists
            stmt = select(User).where(User.email == user_data.email)
            result = await self.session.execute(stmt)
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                raise ValueError("User with this email already exists")
            
            # Create new user
            hashed_password = self.pwd_context.hash(user_data.password)
            user = User(
                email=user_data.email,
                hashed_password=hashed_password,
                full_name=user_data.full_name,
                is_active=True
            )
            
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            
            return user
            
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User object if found, None otherwise
        """
        try:
            stmt = select(User).where(User.id == user_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception:
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            email: User email
            
        Returns:
            User object if found, None otherwise
        """
        try:
            stmt = select(User).where(User.email == email)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception:
            return None
    
    async def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        """
        Update user information.
        
        Args:
            user_id: User ID
            **kwargs: Fields to update
            
        Returns:
            Updated user object if successful, None otherwise
        """
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return None
            
            # Update fields
            for field, value in kwargs.items():
                if hasattr(user, field):
                    setattr(user, field, value)
            
            await self.session.commit()
            await self.session.refresh(user)
            
            return user
            
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def deactivate_user(self, user_id: int) -> bool:
        """
        Deactivate user account.
        
        Args:
            user_id: User ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return False
            
            user.is_active = False
            await self.session.commit()
            
            return True
            
        except Exception as e:
            await self.session.rollback()
            raise e
    
    def create_access_token(self, user: User) -> str:
        """
        Create JWT access token for user.
        
        Args:
            user: User object
            
        Returns:
            JWT access token
        """
        return create_access_token(data={"sub": str(user.id)})
    
    def verify_token(self, token: str) -> Optional[dict]:
        """
        Verify JWT token and return payload.
        
        Args:
            token: JWT token
            
        Returns:
            Token payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM]
            )
            return payload
        except JWTError:
            return None
