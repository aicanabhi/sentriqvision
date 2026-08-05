"""
AI Model Schemas
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field

from app.schemas.base import BaseResponseSchema, BaseSchema


# ==========================================================
# Base
# ==========================================================

class AIModelBase(BaseSchema):
    """
    Base AI model schema.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    slug: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    version: str = Field(
        default="1.0.0",
        max_length=50,
    )

    framework: str = Field(
        default="ONNX",
        max_length=50,
    )

    model_type: str = Field(
        ...,
        max_length=100,
    )

    description: Optional[str] = None


# ==========================================================
# Create
# ==========================================================

class AIModelCreate(AIModelBase):
    """
    Create AI model.
    """

    file_path: str

    file_size_mb: Optional[float] = None

    input_width: int = Field(
        default=640,
        ge=1,
    )

    input_height: int = Field(
        default=640,
        ge=1,
    )

    supported_devices: list[str] = [
        "CPU",
        "GPU",
    ]

    confidence_threshold: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
    )


# ==========================================================
# Update
# ==========================================================

class AIModelUpdate(BaseSchema):
    """
    Update AI model.
    """

    name: Optional[str] = None

    description: Optional[str] = None

    version: Optional[str] = None

    confidence_threshold: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )

    is_active: Optional[bool] = None


# ==========================================================
# Assign Model To Organization
# ==========================================================

class AssignAIModelRequest(BaseSchema):
    """
    Assign AI model to organization.
    """

    organization_id: UUID

    model_id: UUID

    enabled: bool = True


# ==========================================================
# Response
# ==========================================================

class AIModelResponse(BaseResponseSchema):
    """
    AI model response.
    """

    name: str

    slug: str

    version: str

    framework: str

    model_type: str

    description: Optional[str]

    file_path: str

    file_size_mb: Optional[float]

    input_width: int

    input_height: int

    supported_devices: list[str]

    confidence_threshold: float

    is_active: bool


# ==========================================================
# Detail Response
# ==========================================================

class AIModelDetailResponse(AIModelResponse):
    """
    Detailed AI model information.
    """

    organizations_count: int = 0

    total_predictions: int = 0

    last_used_at: Optional[datetime] = None


# ==========================================================
# List Response
# ==========================================================

class AIModelListResponse(BaseSchema):
    """
    Paginated AI model list.
    """

    models: list[AIModelResponse]

    total: int

    page: int

    page_size: int


# ==========================================================
# Filter
# ==========================================================

class AIModelFilter(BaseSchema):
    """
    AI model filters.
    """

    search: Optional[str] = None

    model_type: Optional[str] = None

    framework: Optional[str] = None

    device: Optional[str] = None

    is_active: Optional[bool] = None

    page: int = 1

    page_size: int = 20


# ==========================================================
# Load Model Request
# ==========================================================

class LoadAIModelRequest(BaseSchema):
    """
    Request AI Engine to load model.
    """

    model_id: UUID

    device: str = "AUTO"


# ==========================================================
# Delete Response
# ==========================================================

class AIModelDeleteResponse(BaseSchema):

    success: bool = True

    message: str = "AI Model deleted successfully."