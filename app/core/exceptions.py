"""
Application Custom Exceptions

Centralized exception classes for the entire platform.
"""

from fastapi import HTTPException, status


# ==========================================================
# Base Exception
# ==========================================================

class AppException(HTTPException):
    """
    Base application exception.
    """

    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: str | None = None,
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "success": False,
                "message": message,
                "error_code": error_code,
            },
        )


# ==========================================================
# Authentication
# ==========================================================

class UnauthorizedException(AppException):
    def __init__(self, message="Authentication required"):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            message,
            "AUTH_401",
        )


class InvalidCredentialsException(AppException):
    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid email or password.",
            "AUTH_402",
        )


class InvalidTokenException(AppException):
    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid or expired token.",
            "AUTH_403",
        )


class ForbiddenException(AppException):
    def __init__(self, message="Permission denied"):
        super().__init__(
            status.HTTP_403_FORBIDDEN,
            message,
            "AUTH_403",
        )


# ==========================================================
# Resource
# ==========================================================

class NotFoundException(AppException):
    def __init__(self, resource="Resource"):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            f"{resource} not found.",
            "NOT_FOUND",
        )


class ConflictException(AppException):
    def __init__(self, message="Resource already exists"):
        super().__init__(
            status.HTTP_409_CONFLICT,
            message,
            "CONFLICT",
        )


class ValidationException(AppException):
    def __init__(self, message="Validation failed"):
        super().__init__(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            message,
            "VALIDATION_ERROR",
        )


class BadRequestException(AppException):
    def __init__(self, message="Bad request"):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            message,
            "BAD_REQUEST",
        )


# ==========================================================
# Organization
# ==========================================================

class OrganizationInactiveException(AppException):
    def __init__(self):
        super().__init__(
            status.HTTP_403_FORBIDDEN,
            "Organization is inactive.",
            "ORG_INACTIVE",
        )


class OrganizationSuspendedException(AppException):
    def __init__(self):
        super().__init__(
            status.HTTP_403_FORBIDDEN,
            "Organization is suspended.",
            "ORG_SUSPENDED",
        )


# ==========================================================
# Camera
# ==========================================================

class CameraOfflineException(AppException):
    def __init__(self):
        super().__init__(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "Camera is offline.",
            "CAMERA_OFFLINE",
        )


class CameraConnectionException(AppException):
    def __init__(self):
        super().__init__(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Unable to connect camera.",
            "CAMERA_CONNECTION_FAILED",
        )


# ==========================================================
# AI Engine
# ==========================================================

class AIModelException(AppException):
    def __init__(self, message="AI model error"):
        super().__init__(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            message,
            "AI_MODEL_ERROR",
        )


class DetectionException(AppException):
    def __init__(self, message="Detection failed"):
        super().__init__(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            message,
            "DETECTION_ERROR",
        )


# ==========================================================
# Database
# ==========================================================

class DatabaseException(AppException):
    def __init__(self):
        super().__init__(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Database error occurred.",
            "DATABASE_ERROR",
        )


# ==========================================================
# Service
# ==========================================================

class ServiceDisabledException(AppException):
    def __init__(self, service_name: str):
        super().__init__(
            status.HTTP_403_FORBIDDEN,
            f"{service_name} service is disabled.",
            "SERVICE_DISABLED",
        )


# ==========================================================
# File
# ==========================================================

class FileUploadException(AppException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            "File upload failed.",
            "FILE_UPLOAD_ERROR",
        )


class UnsupportedFileException(AppException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            "Unsupported file type.",
            "UNSUPPORTED_FILE",
        )