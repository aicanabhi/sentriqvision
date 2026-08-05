"""
Role Based Access Control (RBAC)

Defines all platform permissions and role mappings.
"""

from app.core.constants import UserRole

# ==========================================================
# Permission Constants
# ==========================================================

# Organizations
ORG_CREATE = "organization:create"
ORG_READ = "organization:read"
ORG_UPDATE = "organization:update"
ORG_DELETE = "organization:delete"

# Users
USER_CREATE = "user:create"
USER_READ = "user:read"
USER_UPDATE = "user:update"
USER_DELETE = "user:delete"

# Roles
ROLE_CREATE = "role:create"
ROLE_READ = "role:read"
ROLE_UPDATE = "role:update"
ROLE_DELETE = "role:delete"

# Permissions
PERMISSION_CREATE = "permission:create"
PERMISSION_READ = "permission:read"
PERMISSION_UPDATE = "permission:update"
PERMISSION_DELETE = "permission:delete"

# Services
SERVICE_CREATE = "service:create"
SERVICE_READ = "service:read"
SERVICE_UPDATE = "service:update"
SERVICE_DELETE = "service:delete"

# Cameras
CAMERA_CREATE = "camera:create"
CAMERA_READ = "camera:read"
CAMERA_UPDATE = "camera:update"
CAMERA_DELETE = "camera:delete"
CAMERA_START = "camera:start"
CAMERA_STOP = "camera:stop"

# AI Detection
DETECTION_START = "detection:start"
DETECTION_STOP = "detection:stop"
DETECTION_VIEW = "detection:view"

# Alerts
ALERT_READ = "alert:read"
ALERT_ACKNOWLEDGE = "alert:acknowledge"
ALERT_RESOLVE = "alert:resolve"

# Reports
REPORT_VIEW = "report:view"
REPORT_EXPORT = "report:export"

# Dashboard
DASHBOARD_VIEW = "dashboard:view"

# Analytics
ANALYTICS_VIEW = "analytics:view"

# Vehicles
VEHICLE_CREATE = "vehicle:create"
VEHICLE_READ = "vehicle:read"
VEHICLE_UPDATE = "vehicle:update"
VEHICLE_DELETE = "vehicle:delete"

# Parking
PARKING_CREATE = "parking:create"
PARKING_READ = "parking:read"
PARKING_UPDATE = "parking:update"
PARKING_DELETE = "parking:delete"

# ==========================================================
# Role Permission Mapping
# ==========================================================

ROLE_PERMISSIONS = {

    UserRole.SUPER_ADMIN: {
        "*"
    },

    UserRole.ORGANIZATION_ADMIN: {

        ORG_READ,
        ORG_UPDATE,

        USER_CREATE,
        USER_READ,
        USER_UPDATE,
        USER_DELETE,

        ROLE_CREATE,
        ROLE_READ,
        ROLE_UPDATE,
        ROLE_DELETE,

        PERMISSION_READ,

        SERVICE_READ,
        SERVICE_UPDATE,

        CAMERA_CREATE,
        CAMERA_READ,
        CAMERA_UPDATE,
        CAMERA_DELETE,
        CAMERA_START,
        CAMERA_STOP,

        DETECTION_START,
        DETECTION_STOP,
        DETECTION_VIEW,

        ALERT_READ,
        ALERT_ACKNOWLEDGE,
        ALERT_RESOLVE,

        REPORT_VIEW,
        REPORT_EXPORT,

        DASHBOARD_VIEW,

        ANALYTICS_VIEW,

        VEHICLE_CREATE,
        VEHICLE_READ,
        VEHICLE_UPDATE,
        VEHICLE_DELETE,

        PARKING_CREATE,
        PARKING_READ,
        PARKING_UPDATE,
        PARKING_DELETE,
    },

    UserRole.ADMIN: {

        USER_CREATE,
        USER_READ,
        USER_UPDATE,

        CAMERA_CREATE,
        CAMERA_READ,
        CAMERA_UPDATE,

        DETECTION_START,
        DETECTION_STOP,
        DETECTION_VIEW,

        ALERT_READ,

        REPORT_VIEW,

        DASHBOARD_VIEW,

        ANALYTICS_VIEW,

        VEHICLE_CREATE,
        VEHICLE_READ,
        VEHICLE_UPDATE,

        PARKING_CREATE,
        PARKING_READ,
        PARKING_UPDATE,
    },

    UserRole.SUPERVISOR: {

        USER_READ,

        CAMERA_READ,

        DETECTION_VIEW,

        ALERT_READ,

        REPORT_VIEW,

        DASHBOARD_VIEW,

        ANALYTICS_VIEW,

        VEHICLE_READ,

        PARKING_READ,
    },

    UserRole.OPERATOR: {

        CAMERA_READ,

        DETECTION_VIEW,

        ALERT_READ,

        DASHBOARD_VIEW,

        VEHICLE_READ,

        PARKING_READ,
    },

    UserRole.VIEWER: {

        DASHBOARD_VIEW,

        CAMERA_READ,

        ALERT_READ,

        REPORT_VIEW,
    }

}

# ==========================================================
# Helper Functions
# ==========================================================

def has_permission(role: str, permission: str) -> bool:
    """
    Check if a role has a specific permission.
    """

    permissions = ROLE_PERMISSIONS.get(role, set())

    if "*" in permissions:
        return True

    return permission in permissions


def get_permissions(role: str) -> set[str]:
    """
    Return permissions assigned to a role.
    """

    return ROLE_PERMISSIONS.get(role, set())


def require_permission(role: str, permission: str) -> None:
    """
    Raise PermissionError if permission is missing.
    """

    if not has_permission(role, permission):
        raise PermissionError(
            f"Role '{role}' does not have permission '{permission}'"
        )