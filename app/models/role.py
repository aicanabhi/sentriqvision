"""
Role Model

Defines RBAC roles for each Organization.
"""

from __future__ import annotations

import enum

from sqlalchemy import (
    Boolean,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
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


# ==========================================================
# Role Type
# ==========================================================

class RoleType(str, enum.Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ORGANIZATION_ADMIN = "ORGANIZATION_ADMIN"
    MANAGER = "MANAGER"
    SUPERVISOR = "SUPERVISOR"
    OPERATOR = "OPERATOR"
    SECURITY = "SECURITY"
    VIEWER = "VIEWER"
    CUSTOM = "CUSTOM"


# ==========================================================
# Role Model
# ==========================================================

class Role(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
    SoftDeleteMixin,
    AuditMixin,
):
    """
    Organization Role
    """

    __tablename__ = "roles"

    # ======================================================
    # Organization
    # ======================================================

    organization_id: Mapped[str | None] = mapped_column(
        String,
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE",
        ),
        nullable=True,
        index=True,
    )

    # Null only for Super Admin role.

    # ======================================================
    # Basic Information
    # ======================================================

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    display_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    role_type: Mapped[RoleType] = mapped_column(
        Enum(RoleType),
        default=RoleType.CUSTOM,
        nullable=False,
    )

    priority: Mapped[int] = mapped_column(
        Integer,
        default=100,
    )

    # Lower value = Higher Priority

    is_system_role: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    editable: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    deletable: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    # ======================================================
    # Relationships
    # ======================================================

    organization = relationship(
        "Organization",
        back_populates="roles",
    )

    users = relationship(
        "User",
        back_populates="role",
    )

    permissions = relationship(
        "RolePermission",
        back_populates="role",
        cascade="all, delete-orphan",
    )

    # ======================================================

    def __repr__(self) -> str:
        return (
            f"<Role("
            f"name='{self.name}', "
            f"type='{self.role_type}')>"
        )