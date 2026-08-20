from typing import Any, Optional
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    message: str
    request_id: Optional[str] = None
    details: Optional[Any] = None


class StandardErrorResponse(BaseModel):
    success: bool = False
    data: Optional[Any] = None
    error: ErrorDetail


class PlatformException(HTTPException):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[Any] = None,
    ):
        super().__init__(status_code=status_code, detail=message)
        self.code = code
        self.message = message
        self.details = details


def create_error_response(
    code: str,
    message: str,
    status_code: int = 400,
    request_id: Optional[str] = None,
    details: Optional[Any] = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": code,
                "message": message,
                "request_id": request_id,
                "details": details,
            },
        },
    )
