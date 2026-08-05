"""
Database Session Management
"""

from collections.abc import AsyncGenerator
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings
from app.database.base import Base
import app.models  # Ensure all models are registered

logger = logging.getLogger(__name__)


def build_engine(db_url: str):
    """Create Async SQLAlchemy engine based on database URL scheme."""
    is_sqlite = db_url.startswith("sqlite")
    if is_sqlite:
        return create_async_engine(
            db_url,
            echo=settings.database_echo,
        )
    return create_async_engine(
        db_url,
        echo=settings.database_echo,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        pool_recycle=1800,
    )


# Primary Engine Setup (with SQLite Fallback capability)
db_url = settings.database_url
try:
    engine = build_engine(db_url)
except Exception as err:
    logger.warning(f"Primary DB engine setup failed for {db_url}, using SQLite fallback: {err}")
    db_url = "sqlite+aiosqlite:///./sentriqvision.db"
    engine = build_engine(db_url)


async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

AsyncSessionLocal = async_session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Database session dependency."""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def seed_super_admin(session: AsyncSession) -> None:
    """Seed initial super admin if no user exists."""
    from app.models.user import User
    from app.core.security import hash_password

    result = await session.execute(select(User).where(User.email == settings.super_admin_email))
    admin = result.scalar_one_or_none()
    if not admin:
        new_admin = User(
            email=settings.super_admin_email,
            username="admin",
            full_name=settings.super_admin_name,
            hashed_password=hash_password(settings.super_admin_password),
            is_active=True,
            is_super_admin=True,
        )
        session.add(new_admin)
        await session.commit()
        logger.info(f"Seeded super admin: {settings.super_admin_email}")


async def create_tables() -> None:
    """Create database tables and seed initial data."""
    global engine, async_session_factory, AsyncSessionLocal
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as exc:
        logger.warning(f"PostgreSQL connection failed ({exc}). Falling back to SQLite local database.")
        sqlite_url = "sqlite+aiosqlite:///./sentriqvision.db"
        engine = build_engine(sqlite_url)
        async_session_factory = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )
        AsyncSessionLocal = async_session_factory
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # Seed super admin
    async with async_session_factory() as session:
        try:
            await seed_super_admin(session)
        except Exception as seed_err:
            logger.warning(f"Super admin seed note: {seed_err}")


async def close_database() -> None:
    """Close engine connection pool."""
    await engine.dispose()