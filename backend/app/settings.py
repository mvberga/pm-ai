from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://pmapp:pmapp@db:5432/pmdb"
    SECRET_KEY: str = "devsecret"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    CORS_ORIGINS: str = "http://localhost:5173"

settings = Settings()
