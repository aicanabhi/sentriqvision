"""
User Session Model

Stores active login sessions for users.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
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


class UserSession(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
    SoftDeleteMixin,
    AuditMixin,
):
    """
    User Login Session
    """

    __tablename__ = "user_sessions"

    # ==========================================================
    # User
    # ==========================================================

    user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ==========================================================
    # Tokens
    # ==========================================================

    access_token_jti: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    refresh_token_jti: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    # ==========================================================
    # Device Information
    # ==========================================================

    device_name: Mapped[str | None] = mapped_column(
        String(200),
    )

    device_type: Mapped[str | None] = mapped_column(
        String(50),
    )  # Desktop / Mobile / Tablet

    operating_system: Mapped[str | None] = mapped_column(
        String(100),
    )

    browser: Mapped[str | None] = mapped_column(
        String(100),
    )

    browser_version: Mapped[str | None] = mapped_column(
        String(50),
    )

    # ==========================================================
    # Network
    # ==========================================================

    ip_address: Mapped[str | None] = mapped_column(
        String(50),
    )

    user_agent: Mapped[str | None] = mapped_column(
        Text,
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
    )

    # ==========================================================
    # Session Status
    # ==========================================================

    login_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    last_activity: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    logout_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    # ==========================================================
    # Flags
    # ==========================================================

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    remember_me: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # ==========================================================
    # Relationships
    # ==========================================================

    user = relationship(
        "User",
        back_populates="sessions",
    )

    # ==========================================================

    @property
    def is_expired(self) -> bool:
        return datetime.utcnow() >= self.expires_at

    @property
    def is_valid(self) -> bool:
        return (
            self.is_active
            and not self.is_revoked
            and not self.is_expired
        )

    def __repr__(self) -> str:
        return (
            f"<UserSession("
            f"user='{self.user_id}', "
            f"active={self.is_active})>"
        )