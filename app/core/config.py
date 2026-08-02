"""
Application configuration compatibility layer.

Loads values from app.core.settings and exposes
uppercase constants for the rest of the application.
"""

from app.core.settings import settings

# ==========================================================
# Application
# ==========================================================

APP_NAME = settings.app_name
APP_ENV = settings.app_env
DEBUG = settings.debug

API_V1_PREFIX = settings.api_v1_prefix

HOST = settings.host
PORT = settings.port

# ==========================================================
# Database
# ==========================================================

DATABASE_URL = settings.database_url
DATABASE_ECHO = settings.database_echo

# ==========================================================
# Redis
# ==========================================================

REDIS_URL = settings.redis_url

# ==========================================================
# Authentication
# ==========================================================

SECRET_KEY = settings.secret_key

JWT_SECRET_KEY = settings.secret_key
JWT_ALGORITHM = settings.jwt_algorithm

ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = settings.refresh_token_expire_days

# ==========================================================
# Security
# ==========================================================

ALLOWED_HOSTS = settings.allowed_hosts_list
CORS_ORIGINS = settings.cors_origins_list

# ==========================================================
# Logging
# ==========================================================

LOG_LEVEL = settings.log_level
LOG_DIR = settings.log_dir

# ==========================================================
# Storage
# ==========================================================

STORAGE_DIR = settings.storage_dir
SNAPSHOT_DIR = settings.snapshot_dir
VIDEO_DIR = settings.video_dir
REPORT_DIR = settings.report_dir
# ==========================================================
# AI
# ==========================================================

MODEL_DIR = settings.model_dir
DEVICE = settings.device
CPU_THREADS = settings.cpu_threads
GPU_MEMORY_LIMIT = settings.gpu_memory_limit
AI_CONFIDENCE_THRESHOLD = settings.ai_confidence_threshold
AI_FRAME_SKIP = settings.ai_frame_skip
MAX_CONCURRENT_STREAMS = settings.max_concurrent_streams

# ==========================================================
# Camera
# ==========================================================

RTSP_TIMEOUT_SECONDS = settings.rtsp_timeout_seconds
CAMERA_RECONNECT_INTERVAL = settings.camera_reconnect_interval
FRAME_BUFFER_SIZE = settings.frame_buffer_size

# ==========================================================
# Super Admin
# ==========================================================

SUPER_ADMIN_NAME = settings.super_admin_name
SUPER_ADMIN_EMAIL = settings.super_admin_email
SUPER_ADMIN_PASSWORD = settings.super_admin_password
