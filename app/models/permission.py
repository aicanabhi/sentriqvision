"""
Permission Model

Defines all platform permissions for RBAC.
"""

from __future__ import annotations

import enum

from sqlalchemy import (
    Boolean,
    Enum,
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
# Permission Category
# ==========================================================

class PermissionCategory(str, enum.Enum):
    AUTH = "AUTH"

    ORGANIZATION = "ORGANIZATION"
    USER = "USER"
    ROLE = "ROLE"
    PERMISSION = "PERMISSION"

    SERVICE = "SERVICE"

    CAMERA = "CAMERA"
    CAMERA_GROUP = "CAMERA_GROUP"

    TEAM = "TEAM"

    PARKING = "PARKING"

    VEHICLE = "VEHICLE"

    AI = "AI"

    DETECTION = "DETECTION"

    EVENT = "EVENT"

    ALERT = "ALERT"

    REPORT = "REPORT"

    ANALYTICS = "ANALYTICS"

    DASHBOARD = "DASHBOARD"

    SETTINGS = "SETTINGS"

    AUDIT = "AUDIT"


# ==========================================================
# Permission Model
# ==========================================================

class Permission(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
    SoftDeleteMixin,
    AuditMixin,
):
    """
    Master Permission Table.
    """

    __tablename__ = "permissions"

    # ======================================================
    # Basic Information
    # ======================================================

    name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True,
    )

    display_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    category: Mapped[PermissionCategory] = mapped_column(
        Enum(PermissionCategory),
        nullable=False,
    )

    module: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    is_system_permission: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    # ======================================================
    # Relationships
    # ======================================================

    roles = relationship(
        "RolePermission",
        back_populates="permission",
        cascade="all, delete-orphan",
    )

    # ======================================================

    def __repr__(self) -> str:
        return (
            f"<Permission("
            f"name='{self.name}', "
            f"category='{self.category}')>"
        )