"""
User Model
"""

from datetime import datetime

from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base import (
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
)


class User(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
):
    """
    System User Model
    """

    __tablename__ = "users"



    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )


    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )


    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )


    full_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )


    

    is_super_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )


    organization_id: Mapped[str | None] = mapped_column(
        ForeignKey(
            "organizations.id"
        ),
        nullable=True
    )


    role_id: Mapped[str | None] = mapped_column(
        ForeignKey(
            "roles.id"
        ),
        nullable=True
    )

    team_id: Mapped[str | None] = mapped_column(
        ForeignKey(
            "teams.id"
        ),
        nullable=True
    )

    # Relationship

    organization = relationship(
        "Organization",
        back_populates="users"
    )


    role = relationship(
        "Role",
        back_populates="users"
    )

    team = relationship(
        "Team",
        foreign_keys=[team_id],
        back_populates="users"
    )


    sessions = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete"
    )

    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete"
    )

    audit_logs = relationship(
    "Audit",
    back_populates="user",
    cascade="all, delete-orphan",
    )  