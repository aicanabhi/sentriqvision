"""
Camera Group Model
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import (
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
)

if TYPE_CHECKING:
    from app.models.camera import Camera


class CameraGroup(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
):
    __tablename__ = "camera_groups"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    cameras: Mapped[list["Camera"]] = relationship(
        "Camera",
        back_populates="group",
    )