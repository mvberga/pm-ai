from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.is_production,  # Only echo in production for debugging
    future=True,
    pool_pre_ping=True,  # Validate connections before use
    pool_recycle=3600,   # Recycle connections every hour
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models"""
    pass

async def get_session() -> AsyncSession:
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_models():
    """Initialize database models and create tables"""
    try:
        # Import models so metadata is populated
        from app.models import user, project, checklist, action_item  # noqa
        
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database models initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database models: {e}")
        raise

async def close_engine():
    """Close database engine on shutdown"""
    await engine.dispose()
    logger.info("Database engine closed")
