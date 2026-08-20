from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ParameterResponse(BaseModel):
    id: str
    parameter_id: str

    service_number: int
    code: str
    name: str
    domain: str
    description: str

    hardware_requirement: str
    processing_mode: str
    device_preference: str

    status: str

    enabled: bool
    entitled: bool
    configured: bool

    confidence_threshold: float
    sampling_fps: float

    alert_enabled: bool
    retention_days: int

    active_cameras: int

    configuration_json: Dict[str, Any] = Field(default_factory=dict)

    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class ParameterToggleRequest(BaseModel):
    organization_id: Optional[UUID] = None
    enabled: bool


class ParameterEntitlementRequest(BaseModel):
    organization_id: Optional[UUID] = None
    entitled: bool


class ParameterConfigRequest(BaseModel):
    organization_id: Optional[UUID] = None

    enabled: Optional[bool] = None

    confidence_threshold: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )

    sampling_fps: Optional[float] = Field(
        default=None,
        ge=1.0,
        le=60.0,
    )

    processing_mode: Optional[str] = None

    device_preference: Optional[str] = None

    alert_enabled: Optional[bool] = None

    retention_days: Optional[int] = Field(
        default=None,
        ge=1,
        le=3650,
    )

    camera_ids: Optional[List[UUID]] = None

    configuration_json: Optional[Dict[str, Any]] = None



class OrganizationCapabilityResponse(BaseModel):
    organization_id: str

    key: str
    code: str
    name: str
    domain: str

    status: str
    enabled: bool
    entitled: bool

    confidence_threshold: float
    sampling_fps: float


class CameraTestConnectionRequest(BaseModel):
    rtsp_url: str

    username: Optional[str] = None
    password: Optional[str] = None

    transport: Optional[str] = "TCP"

    timeout: Optional[int] = Field(
        default=5,
        ge=1,
        le=60,
    )


class CameraTestConnectionResponse(BaseModel):
    connected: bool

    protocol: str = "RTSP"

    resolution: Optional[str] = None
    fps: Optional[float] = None
    latency_ms: Optional[float] = None

    reason: Optional[str] = None


class SystemMetricsResponse(BaseModel):
    cpu_percent: float

    ram_used_gb: float
    ram_total_gb: float

    gpu_percent: float

    vram_used_mb: float
    vram_total_mb: float

    active_cameras: int
    online_cameras: int
    offline_cameras: int

    enabled_parameters: int

    total_events_today: int
    critical_alerts: int

    inference_latency_ms: float

    system_health: str