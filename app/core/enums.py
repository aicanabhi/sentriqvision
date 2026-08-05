"""Application-wide enumerations."""

from enum import Enum


class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    ORG_ADMIN = "org_admin"
    MANAGER = "manager"
    SECURITY_GUARD = "security_guard"
    EMPLOYEE = "employee"
    VIEWER = "viewer"


class OrganizationStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"
    PENDING = "pending"


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    TRIAL = "trial"


class CameraStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class CameraType(str, Enum):
    RTSP = "rtsp"
    ONVIF = "onvif"
    USB = "usb"
    WEBCAM = "webcam"
    IP = "ip"
    UPLOAD = "upload"


class AlertPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AlertStatus(str, Enum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


class IncidentStatus(str, Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    CLOSED = "closed"


class DetectionType(str, Enum):
    FACE = "face"
    VEHICLE = "vehicle"
    PERSON = "person"
    FIRE = "fire"
    SMOKE = "smoke"
    PPE = "ppe"
    INTRUSION = "intrusion"
    LOITERING = "loitering"
    CROWD = "crowd"
    ANPR = "anpr"
    PARKING = "parking"
    WEAPON = "weapon"
    FALL = "fall"
    VIOLENCE = "violence"
    ABANDONED_OBJECT = "abandoned_object"
    OCR = "ocr"
    QR = "qr"
    BARCODE = "barcode"
    OTHER = "other"


class ServiceCategory(str, Enum):
    SECURITY = "security"
    SAFETY = "safety"
    VEHICLE = "vehicle"
    RETAIL = "retail"
    INDUSTRIAL = "industrial"
    SMART_CITY = "smart_city"
    OCR = "ocr"
    INTELLIGENCE = "intelligence"


class ParkingSlotStatus(str, Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"
    DISABLED = "disabled"


class AttendanceStatus(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    HALF_DAY = "half_day"
    LEAVE = "leave"


class NotificationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"
    WEBHOOK = "webhook"
    PUSH = "push"
    WEBSOCKET = "websocket"
    POPUP = "popup"
    ALARM = "alarm"


class ReportType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    CUSTOM = "custom"


class ReportFormat(str, Enum):
    PDF = "pdf"
    EXCEL = "excel"
    CSV = "csv"
