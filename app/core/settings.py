"""
Central application settings.
"""

from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True,
    )

    # ==================================================
    # Application
    # ==================================================

    app_name: str = Field(
        default="SentriqVision AI Platform",
        alias="APP_NAME",
    )

    app_version: str = Field(
        default="1.0.0",
        alias="APP_VERSION",
    )

    app_env: str = Field(
        default="development",
        alias="APP_ENV",
    )

    debug: bool = Field(
        default=True,
        alias="DEBUG",
    )

    api_v1_prefix: str = Field(
        default="/api/v1",
        alias="API_V1_PREFIX",
    )

    host: str = Field(
        default="0.0.0.0",
        alias="HOST",
    )

    port: int = Field(
        default=8000,
        alias="PORT",
    )

    # ==================================================
    # Database
    # ==================================================

    database_url: str = Field(alias="DATABASE_URL")

    database_echo: bool = Field(
        default=False,
        alias="DATABASE_ECHO",
    )

    # ==================================================
    # Redis
    # ==================================================

    redis_url: str = Field(
        default="redis://localhost:6379/0",
        alias="REDIS_URL",
    )

    # ==================================================
    # Security
    # ==================================================

    secret_key: str = Field(alias="SECRET_KEY")

    jwt_algorithm: str = Field(
        default="HS256",
        alias="JWT_ALGORITHM",
    )

    access_token_expire_minutes: int = Field(
        default=30,
        alias="ACCESS_TOKEN_EXPIRE_MINUTES",
    )

    refresh_token_expire_days: int = Field(
        default=7,
        alias="REFRESH_TOKEN_EXPIRE_DAYS",
    )

    # ==================================================
    # Network
    # ==================================================

    allowed_hosts: str = Field(
        default="localhost,127.0.0.1",
        alias="ALLOWED_HOSTS",
    )

    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173",
        alias="CORS_ORIGINS",
    )

    # ==================================================
    # Logging
    # ==================================================

    log_level: str = Field(
        default="INFO",
        alias="LOG_LEVEL",
    )

    log_dir: str = Field(
        default="logs",
        alias="LOG_DIR",
    )

    # ==================================================
    # Storage
    # ==================================================

    storage_dir: str = Field(
        default="storage",
        alias="STORAGE_DIR",
    )

    snapshot_dir: str = Field(
        default="storage/snapshots",
        alias="SNAPSHOT_DIR",
    )

    video_dir: str = Field(
        default="storage/videos",
        alias="VIDEO_DIR",
    )

    report_dir: str = Field(
        default="storage/reports",
        alias="REPORT_DIR",
    )

    model_dir: str = Field(
        default="models",
        alias="MODEL_DIR",
    )

    # ==================================================
    # AI
    # ==================================================

    device: str = Field(
        default="auto",
        alias="DEVICE",
    )

    cpu_threads: int = Field(
        default=4,
        alias="CPU_THREADS",
    )

    gpu_memory_limit: int = Field(
        default=4096,
        alias="GPU_MEMORY_LIMIT",
    )

    ai_confidence_threshold: float = Field(
        default=0.50,
        alias="AI_CONFIDENCE_THRESHOLD",
    )

    ai_frame_skip: int = Field(
        default=2,
        alias="AI_FRAME_SKIP",
    )

    max_concurrent_streams: int = Field(
        default=10,
        alias="MAX_CONCURRENT_STREAMS",
    )

    worker_count: int = Field(
        default=2,
        alias="WORKER_COUNT",
    )

    queue_size: int = Field(
        default=500,
        alias="QUEUE_SIZE",
    )

    # ==================================================
    # Camera
    # ==================================================

    rtsp_timeout_seconds: int = Field(default=10, alias="RTSP_TIMEOUT_SECONDS")
    camera_reconnect_interval: int = Field(default=5, alias="CAMERA_RECONNECT_INTERVAL")
    frame_buffer_size: int = Field(default=30, alias="FRAME_BUFFER_SIZE")
    stream_width: int = Field(default=1280, alias="STREAM_WIDTH")
    stream_height: int = Field(default=720, alias="STREAM_HEIGHT")
    stream_fps: int = Field(default=15, alias="STREAM_FPS")

    # ==================================================
    # Super Admin
    # ==================================================

    super_admin_name: str = Field(default="Super Admin", alias="SUPER_ADMIN_NAME")
    super_admin_email: str = Field(default="admin@sentriqvision.com", alias="SUPER_ADMIN_EMAIL")
    super_admin_password: str = Field(default="Admin@123456", alias="SUPER_ADMIN_PASSWORD")

    @property
    def allowed_hosts_list(self) -> List[str]:
        return [x.strip() for x in self.allowed_hosts.split(",") if x.strip()]

    @property
    def cors_origins_list(self) -> List[str]:
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()