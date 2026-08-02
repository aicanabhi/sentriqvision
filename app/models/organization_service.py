"""
Organization Service Model

Mapping between organizations and subscribed services.
"""

from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base


class OrganizationService(Base):
    """
    Organization-Service mapping table.
    """

    __tablename__ = "organization_services"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    organization_id = Column(
        Integer,
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )


    service_id = Column(
        Integer,
        ForeignKey(
            "services.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )


    is_active = Column(
        Boolean,
        default=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )


    # Relationships

    organization = relationship(
        "Organization",
        back_populates="services"
    )


    service = relationship(
        "Service",
        back_populates="organizations"
    )

    configuration = relationship(
        "ServiceConfiguration",
        back_populates="organization_service",
        uselist=False,
        cascade="all, delete-orphan"
    )


    def __repr__(self):
        return (
            f"<OrganizationService "
            f"org={self.organization_id} "
            f"service={self.service_id}>"
        )