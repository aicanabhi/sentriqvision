"""
Standard API Response Models

Used throughout the SentriqVision platform.
"""

from datetime import datetime, timezone
from typing import Any, Generic, TypeVar

from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

T = TypeVar("T")


# ==========================================================
# Meta
# ==========================================================

class ResponseMeta(BaseModel):
    page: int | None = None
    page_size: int | None = None
    total_records: int | None = None
    total_pages: int | None = None


# ==========================================================
# Standard Response
# ==========================================================

class ApiResponse(BaseModel, Generic[T]):

    success: bool = True

    message: str = "Success"

    data: T | None = None

    errors: Any | None = None

    meta: ResponseMeta | None = None

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# ==========================================================
# Success Response
# ==========================================================

def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = 200,
):

    return JSONResponse(
        status_code=status_code,
        content=ApiResponse(
            success=True,
            message=message,
            data=data,
        ).model_dump(mode="json"),
    )


# ==========================================================
# Error Response
# ==========================================================

def error_response(
    message: str,
    errors: Any = None,
    status_code: int = 400,
):

    return JSONResponse(
        status_code=status_code,
        content=ApiResponse(
            success=False,
            message=message,
            errors=errors,
        ).model_dump(mode="json"),
    )


# ==========================================================
# Created Response
# ==========================================================

def created_response(
    data: Any,
    message: str = "Created successfully",
):

    return success_response(
        data=data,
        message=message,
        status_code=201,
    )


# ==========================================================
# Paginated Response
# ==========================================================

def paginated_response(
    *,
    data: list[Any],
    page: int,
    page_size: int,
    total_records: int,
    message: str = "Success",
):

    total_pages = (
        (total_records + page_size - 1) // page_size
        if page_size > 0
        else 1
    )

    return JSONResponse(
        status_code=200,
        content=ApiResponse(
            success=True,
            message=message,
            data=data,
            meta=ResponseMeta(
                page=page,
                page_size=page_size,
                total_records=total_records,
                total_pages=total_pages,
            ),
        ).model_dump(mode="json"),
    )


# ==========================================================
# No Content Response
# ==========================================================

def deleted_response(
    message: str = "Deleted successfully",
):

    return success_response(
        data=None,
        message=message,
        status_code=200,
    )


# ==========================================================
# Accepted Response
# ==========================================================

def accepted_response(
    data: Any = None,
    message: str = "Request accepted",
):

    return success_response(
        data=data,
        message=message,
        status_code=202,
    )


# ==========================================================
# Utility
# ==========================================================

def bool_response(
    status: bool,
    message: str,
):

    return success_response(
        data={"status": status},
        message=message,
    )