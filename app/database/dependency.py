"""
Database Dependencies

Provides database sessions
to FastAPI routes.
"""


from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import AsyncSessionLocal



# ==========================================================
# Database Session Dependency
# ==========================================================


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI database dependency.

    Creates new database session
    for every request.
    """

    async with AsyncSessionLocal() as session:

        try:

            yield session


        finally:

            await session.close()