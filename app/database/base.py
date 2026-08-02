"""
Database Base Configuration

Central SQLAlchemy Base class.
Used by all database models.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all database models.
    """

    pass


# Metadata reference for Alembic

metadata = Base.metadata