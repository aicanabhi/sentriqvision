"""
Enterprise Audit Log Model
"""

from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base import (
    Base,
    TimestampMixin,
    UUIDMixin,
)


# ==========================================================
# Audit Action
# ==========================================================

class AuditAction(str, enum.Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    VIEW = "VIEW"
    EXPORT = "EXPORT"
    IMPORT = "IMPORT"
    ENABLE = "ENABLE"
    DISABLE = "DISABLE"
    ASSIGN = "ASSIGN"
    REMOVE = "REMOVE"
    RESET_PASSWORD = "RESET_PASSWORD"


# ==========================================================
# Audit Log
# ==========================================================

class Audit(
    Base,
    UUIDMixin,
    TimestampMixin,
):

    __tablename__ = "audit_logs"

    # ======================================================
    # Organization
    # ======================================================

    organization_id: Mapped[str | None] = mapped_column(
        ForeignKey("organizations.id", ondelete="SET NULL"),
        index=True,
    )

    # ======================================================
    # User
    # ======================================================

    user_id: Mapped[str | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True,
    )

    # ======================================================
    # Action
    # ======================================================

    action: Mapped[AuditAction] = mapped_column(
        Enum(AuditAction),
        nullable=False,
    )

    module: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    entity: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    entity_id: Mapped[str | None] = mapped_column(
        String(100),
    )

    # ======================================================
    # Request
    # ======================================================

    ip_address: Mapped[str | None] = mapped_column(
        String(64),
    )

    user_agent: Mapped[str | None] = mapped_column(
        Text,
    )

    request_method: Mapped[str | None] = mapped_column(
        String(20),
    )

    request_path: Mapped[str | None] = mapped_column(
        Text,
    )

    status_code: Mapped[int | None] = mapped_column(
        Integer,
    )

    # ======================================================
    # Description
    # ======================================================

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    # ======================================================
    # Changes
    # ======================================================

    old_data: Mapped[dict | None] = mapped_column(
        JSONB,
        default=dict,
    )

    new_data: Mapped[dict | None] = mapped_column(
        JSONB,
        default=dict,
    )

    metadata_json: Mapped[dict | None] = mapped_column(
        JSONB,
        default=dict,
    )

    # ======================================================
    # Time
    # ======================================================

    action_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    # ======================================================
    # Relationships
    # ======================================================

    organization = relationship(
        "Organization",
        back_populates="audit_logs",
    )

    user = relationship(
        "User",
        back_populates="audit_logs",
    )

    # ======================================================

    def __repr__(self) -> str:
        return (
            f"<Audit("
            f"{self.action.value} "
            f"{self.module})>"
        )