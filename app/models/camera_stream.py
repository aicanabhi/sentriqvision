"""
Enterprise Camera Stream Model
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

from sqlalchemy.dialects.postgresql import JSONB
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
# Stream Type
# ==========================================================

class StreamType(str, enum.Enum):
    MAIN = "MAIN"
    SUB = "SUB"
    MOBILE = "MOBILE"
    RECORDING = "RECORDING"
    SNAPSHOT = "SNAPSHOT"
    AI = "AI"
    WEBRTC = "WEBRTC"
    HLS = "HLS"


# ==========================================================
# Stream Protocol
# ==========================================================

class StreamProtocol(str, enum.Enum):
    RTSP = "RTSP"
    RTMP = "RTMP"
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    HLS = "HLS"
    WEBRTC = "WEBRTC"
    ONVIF = "ONVIF"


# ==========================================================
# Camera Stream
# ==========================================================

class CameraStream(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
    SoftDeleteMixin,
    AuditMixin,
):

    __tablename__ = "camera_streams"

    # ==========================================================
    # Camera
    # ==========================================================

    camera_id: Mapped[str] = mapped_column(
        ForeignKey(
            "cameras.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
        index=True,
    )

    # ==========================================================
    # Stream Details
    # ==========================================================

    stream_name: Mapped[str] = mapped_column(
        String(100),
        default="Main Stream",
    )

    stream_type: Mapped[StreamType] = mapped_column(
        Enum(StreamType),
        default=StreamType.MAIN,
    )

    protocol: Mapped[StreamProtocol] = mapped_column(
        Enum(StreamProtocol),
        default=StreamProtocol.RTSP,
    )

    stream_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    backup_stream_url: Mapped[str | None] = mapped_column(
        Text,
    )

    snapshot_url: Mapped[str | None] = mapped_column(
        Text,
    )

    # ==========================================================
    # Video Configuration
    # ==========================================================

    resolution: Mapped[str] = mapped_column(
        String(50),
        default="1920x1080",
    )

    fps: Mapped[int] = mapped_column(
        Integer,
        default=25,
    )

    bitrate: Mapped[int] = mapped_column(
        Integer,
        default=4096,
    )

    codec: Mapped[str] = mapped_column(
        String(50),
        default="H264",
    )

    audio_codec: Mapped[str | None] = mapped_column(
        String(50),
    )

    gop: Mapped[int] = mapped_column(
        Integer,
        default=50,
    )

    # ==========================================================
    # Stream Options
    # ==========================================================

    enable_audio: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    enable_recording: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    enable_ai: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    enable_snapshot: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    # ==========================================================
    # Network
    # ==========================================================

    timeout_seconds: Mapped[int] = mapped_column(
        Integer,
        default=10,
    )

    reconnect_interval: Mapped[int] = mapped_column(
        Integer,
        default=5,
    )

    max_retry: Mapped[int] = mapped_column(
        Integer,
        default=10,
    )

    # ==========================================================
    # Decoder
    # ==========================================================

    decoder: Mapped[str] = mapped_column(
        String(50),
        default="AUTO",
    )  # AUTO / CPU / CUDA / OpenVINO

    hw_acceleration: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    # ==========================================================
    # Extra Configuration
    # ==========================================================

    extra_config: Mapped[dict | None] = mapped_column(
        JSONB,
        default=dict,
    )

    # Example:
    # {
    #   "transport":"tcp",
    #   "buffer_size":4096,
    #   "ffmpeg_threads":4
    # }

    # ==========================================================
    # Relationships
    # ==========================================================

    camera = relationship(
        "Camera",
        back_populates="stream",
    )

    # ==========================================================

    def __repr__(self) -> str:
        return (
            f"<CameraStream("
            f"camera={self.camera_id}, "
            f"type={self.stream_type.value})>"
        )