from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.settings import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

async def init_models():
    # Import models so metadata is populated
    from app.models import user, project, checklist, action_item  # noqa
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
