from sqlalchemy.ext.asyncio import (AsyncSession, create_async_engine, async_scoped_session)
from app.config import settings

# --------------------------------------------------------------
# Database Engine
# --------------------------------------------------------------
# The engine manages connections to PostgreSQL.
#
# echo=False means SQL queries aren't printed in production.
# During development you can temporarily change this to True.
# --------------------------------------------------------------

engine = create_async_engine(settings.database_url, echo=False,)

# --------------------------------------------------------------
# Session Factory
# --------------------------------------------------------------
# Every API request that needs a database will obtain an
# AsyncSession from this factory.
# --------------------------------------------------------------

AsyncSessionLocal = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
async def get_db():
    """
    FastAPI dependency that provides a database session.
    Usage later:
    async def endpoint(db: AsyncSession = Depends(get_db)):
    ...
    The 'async with' guarantees that the session is closed after the request finishes.
    """
    async with AsyncSessionLocal() as session:
        yield session