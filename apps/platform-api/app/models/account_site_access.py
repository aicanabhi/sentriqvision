"""
Represents explicit access granted from an organization account to a site.

Site-level access allows an OPERATOR or AUTHORIZED_VIEWER to
access the cameras and related resources belonging to that site.
"""

import uuid
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, UniqueConstraint
from .base import Base

class AccountSiteAccess(Base):
    __tablename__ = 'account_site_access'
    __table_args__ = (
        UniqueConstraint(
            "account_id",
            "site_id",
            name="uq_account_site_access_account_site",
        ),
        {"schema": "platform"},
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

    site_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("platform.sites.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    account = relationship("Account")
    site = relationship("Site")