from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./pmdb.db"
    
    # Security
    SECRET_KEY: str = "devsecret"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    ALGORITHM: str = "HS256"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:5173"
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "PM AI MVP API"
    VERSION: str = "1.0.0"
    
    # Performance
    MAX_PAGE_SIZE: int = 100
    DEFAULT_PAGE_SIZE: int = 20
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Environment
    ENVIRONMENT: str = "development"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
