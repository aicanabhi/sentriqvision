"""
Application Constants

This module contains reusable constants used across the platform.
Never hardcode these values inside business logic.
"""

from enum import Enum

# API
API_VERSION = "v1"

API_PREFIX = f"/api/{API_VERSION}"

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Token Types


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    RESET_PASSWORD = "reset_password"
    VERIFY_EMAIL = "verify_email"
    OTP = "otp"


# User Roles


class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    ORGANIZATION_ADMIN = "organization_admin"
    ADMIN = "admin"
    SUPERVISOR = "supervisor"
    OPERATOR = "operator"
    VIEWER = "viewer"


# Organization Status


class OrganizationStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


# User Status


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    LOCKED = "locked"
    DELETED = "deleted"


# Camera Status


class CameraStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    ERROR = "error"
    CONNECTING = "connecting"


# Detection Status


class DetectionStatus(str, Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    PAUSED = "paused"


# AI Service Status


class ServiceStatus(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"


# Event Types


class EventType(str, Enum):
    FACE = "face"
    PPE = "ppe"
    HELMET = "helmet"
    FIRE = "fire"
    SMOKE = "smoke"
    WEAPON = "weapon"
    FALL = "fall"
    VIOLENCE = "violence"
    INTRUSION = "intrusion"
    LOITERING = "loitering"
    PARKING = "parking"
    ANPR = "anpr"
    PEOPLE_COUNT = "people_count"
    CROWD = "crowd"
    OCR = "ocr"
    QR = "qr"
    BARCODE = "barcode"

# Notification Channels

class NotificationType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"
    WEBHOOK = "webhook"
    ALARM = "alarm"


# Redis Prefix

REDIS_TOKEN_BLACKLIST_PREFIX = "token:blacklist:"
REDIS_REFRESH_TOKEN_PREFIX = "token:refresh:"
REDIS_OTP_PREFIX = "otp:"
REDIS_SESSION_PREFIX = "session:"
REDIS_RATE_LIMIT_PREFIX = "rate_limit:"

# 
# Permissions

ACTION_CREATE = "create"
ACTION_READ = "read"
ACTION_UPDATE = "update"
ACTION_DELETE = "delete"
ACTION_MANAGE = "manage"
ACTION_EXPORT = "export"

# AI Services

DEFAULT_AI_SERVICES = [
    {
        "slug": "face_recognition",
        "name": "Face Recognition",
        "category": "Security",
        "supports_cpu": True,
        "supports_gpu": True,
        "enabled_by_default": True,
    },
    {
        "slug": "ppe",
        "name": "PPE Detection",
        "category": "Safety",
        "supports_cpu": True,
        "supports_gpu": True,
        "enabled_by_default": True,
    },
    {
        "slug": "helmet",
        "name": "Helmet Detection",
        "category": "Safety",
        "supports_cpu": True,
        "supports_gpu": True,
        "enabled_by_default": True,
    },
    {
        "slug": "fire",
        "name": "Fire Detection",
        "category": "Safety",
        "supports_cpu": True,
        "supports_gpu": True,
        "enabled_by_default": True,
    },
    {
        "slug": "smoke",
        "name": "Smoke Detection",
        "category": "Safety",
        "supports_cpu": True,
        "supports_gpu": True,
        "enabled_by_default": True,
    },
    {
        "slug": "anpr",
        "name": "Automatic Number Plate Recognition",
        "category": "Vehicle",
        "supports_cpu": True,
        "supports_gpu": True,
        "enabled_by_default": True,
    },
    {
        "slug": "parking",
        "name": "Parking Management",
        "category": "Vehicle",
        "supports_cpu": True,
        "supports_gpu": True,
        "enabled_by_default": True,
    },
    {
        "slug": "attendance",
        "name": "Face Attendance",
        "category": "Attendance",
        "supports_cpu": True,
        "supports_gpu": True,
        "enabled_by_default": False,
    },
    {
        "slug": "people_count",
        "name": "People Counting",
        "category": "Analytics",
        "supports_cpu": True,
        "supports_gpu": True,
        "enabled_by_default": False,
    },
    {
        "slug": "intrusion",
        "name": "Intrusion Detection",
        "category": "Security",
        "supports_cpu": True,
        "supports_gpu": True,
        "enabled_by_default": False,
    },
    {
        "slug": "ocr",
        "name": "OCR",
        "category": "OCR",
        "supports_cpu": True,
        "supports_gpu": True,
        "enabled_by_default": False,
    },
    {
        "slug": "qr",
        "name": "QR Detection",
        "category": "OCR",
        "supports_cpu": True,
        "supports_gpu": True,
        "enabled_by_default": False,
    },
    {
        "slug": "barcode",
        "name": "Barcode Detection",
        "category": "OCR",
        "supports_cpu": True,
        "supports_gpu": True,
        "enabled_by_default": False,
    },
]

# 
# File Extensions
# 

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}

# 
# Health Check
# 

APP_HEALTHY = "healthy"
APP_UNHEALTHY = "unhealthy"