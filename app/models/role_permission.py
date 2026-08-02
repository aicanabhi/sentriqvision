"""
Role Permission Model

Many-to-Many mapping between Roles and Permissions.
"""

from __future__ import annotations

from sqlalchemy import (
    Boolean,
    ForeignKey,
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


class RolePermission(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
    SoftDeleteMixin,
    AuditMixin,
):
    """
    Maps Roles to Permissions.
    """

    __tablename__ = "role_permissions"

    __table_args__ = (
        UniqueConstraint(
            "role_id",
            "permission_id",
            name="uq_role_permission",
        ),
    )

    # =====================================================
    # Foreign Keys
    # =====================================================

    role_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "roles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    permission_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "permissions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # =====================================================
    # Permission Status
    # =====================================================

    allowed: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # =====================================================
    # Relationships
    # =====================================================

    role = relationship(
        "Role",
        back_populates="permissions",
    )

    permission = relationship(
        "Permission",
        back_populates="roles",
    )

    # =====================================================

    def __repr__(self) -> str:
        return (
            f"<RolePermission("
            f"role={self.role_id}, "
            f"permission={self.permission_id}, "
            f"allowed={self.allowed})>"
        )