from enum import Enum

class AccountRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    OPERATOR = "OPERATOR"
    AUTHORIZED_VIEWER = "AUTHORIZED_VIEWER"

    """
    Roles:
    SUPER_ADMIN:
        Platform-level administrator with access to all organizations.

    ADMIN:
        Organization-level administrator with full access to the
        organization's resources and configuration.

    OPERATOR:
        Organization-level operational role with access to
        authorized cameras, events, and operational data.

    AUTHORIZED_VIEWER:
        Organization-level read-only role with access only to
        explicitly authorized resources.

    """