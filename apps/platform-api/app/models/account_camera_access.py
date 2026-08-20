"""
Represents explicit access granted from an organization account
to an individual camera.

Camera-level access is useful when an account needs access
to a specific camera without receiving access to the entire site.
"""

import uuid
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, UniqueConstraint
from .base import Base

class AccountCameraAccess(Base):
    __tablename__ = "account_camera_access"
    __table_args__ = (
        UniqueConstraint(
            "account_id",
            "camera_id",
            name="uq_account_camera_access_account_camera"
        ),
        {"schema": "platform"}
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("platform.accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    camera_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("platform.cameras.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    account = relationship("Account")
    camera = relationship("Camera")