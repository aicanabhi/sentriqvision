"""
Team Model

Organization Teams / Departments
"""

from __future__ import annotations

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base import (
    ActiveMixin,
    AuditMixin,
    Base,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDMixin,
)


class Team(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
    SoftDeleteMixin,
    AuditMixin,
):
    """
    Organization Team
    """

    __tablename__ = "teams"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "name",
            name="uq_team_name_per_organization",
        ),
    )

    # ==========================================================
    # Organization
    # ==========================================================

    organization_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ==========================================================
    # Team Information
    # ==========================================================

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    display_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    code: Mapped[str | None] = mapped_column(
        String(50),
    )

    department: Mapped[str | None] = mapped_column(
        String(100),
    )

    shift: Mapped[str | None] = mapped_column(
        String(100),
    )

    location: Mapped[str | None] = mapped_column(
        String(150),
    )

    floor: Mapped[str | None] = mapped_column(
        String(100),
    )

    building: Mapped[str | None] = mapped_column(
        String(100),
    )

    # ==========================================================
    # Team Manager
    # ==========================================================

    manager_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
    )

    # ==========================================================
    # Settings
    # ==========================================================

    color: Mapped[str | None] = mapped_column(
        String(20),
    )

    icon: Mapped[str | None] = mapped_column(
        String(100),
    )

    allow_camera_access: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    allow_reports: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    allow_alerts: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    # ==========================================================
    # Relationships
    # ==========================================================

    organization = relationship(
        "Organization",
        back_populates="teams",
    )

    users = relationship(
        "User",
        foreign_keys="User.team_id",
        back_populates="team",
    )

    manager = relationship(
        "User",
        foreign_keys=[manager_id],
    )

    # ==========================================================

    def __repr__(self) -> str:
        return (
            f"<Team("
            f"name='{self.name}', "
            f"organization='{self.organization_id}')>"
        )