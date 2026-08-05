"""
Super Admin Model

Stores platform level administrators.
"""

from sqlalchemy import (
    String,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.models.base import Base


class SuperAdmin(Base):
    """
    Super Admin Account
    """

    __tablename__ = "super_admins"


    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )


    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )


    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )


    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )


    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )


    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )