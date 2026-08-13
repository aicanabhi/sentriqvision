"""
Alembic migration environment.

This file connects Alembic to our application configuration
and SQLAlchemy models so that migrations can be generated
and applied against PostgreSQL.
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.config import settings
from app.models import Base


# Alembic Config object.
config = context.config


# ---------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# ---------------------------------------------------------
# Database configuration
# ---------------------------------------------------------

# Get the database URL from our application settings.
#
# Example:
# postgresql+asyncpg://user:password@localhost:5432/database
#
# Alembic will use this URL to connect to PostgreSQL.
config.set_main_option(
    "sqlalchemy.url",
    settings.database_url.replace("%", "%%"),
)


# ---------------------------------------------------------
# SQLAlchemy model metadata
# ---------------------------------------------------------

# Alembic uses this metadata to compare our Python models
# against the actual PostgreSQL database schema.
#
# Example models:
#
# Organization
# Site
# Zone
# Camera
# Module
# CameraModule
# ModuleConfig
#
target_metadata = Base.metadata


# ---------------------------------------------------------
# Offline migration
# ---------------------------------------------------------

def run_migrations_offline() -> None:
    """
    Run migrations without creating a database connection.

    This is useful for generating SQL scripts instead of
    directly executing changes against PostgreSQL.
    """

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,

        # Include non-public PostgreSQL schemas.
        include_schemas=True,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named",
        },
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------
# Online migration
# ---------------------------------------------------------

def do_run_migrations(connection: Connection) -> None:
    """
    Configure Alembic using an active database connection.
    """

    context.configure(
        connection=connection,
        target_metadata=target_metadata,

        # IMPORTANT:
        # Our SQLAlchemy models use the PostgreSQL "platform"
        # schema instead of the default "public" schema.
        include_schemas=True,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Create an async SQLAlchemy engine and run migrations.
    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Run migrations against the live PostgreSQL database.
    """

    import asyncio

    asyncio.run(run_async_migrations())


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()