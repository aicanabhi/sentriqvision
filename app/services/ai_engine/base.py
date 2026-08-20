from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class CapabilityStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    RUNNING = "RUNNING"
    DEGRADED = "DEGRADED"
    MODEL_REQUIRED = "MODEL_REQUIRED"
    DISABLED = "DISABLED"
    ERROR = "ERROR"
    OFFLINE = "OFFLINE"


class ModelDependencyInfo(BaseModel):
    capability_code: str
    capability_name: str
    model_name: str
    framework: str  # PyTorch, ONNX, OpenCV, PaddleOCR, etc.
    hardware_requirement: str  # CPU, GPU, CPU/GPU
    weights_path: Optional[str] = None
    is_installed: bool
    status: CapabilityStatus
    installation_instructions: str


class CapabilityResult(BaseModel):
    capability_code: str
    status: CapabilityStatus
    confidence: float = 0.0
    bounding_boxes: List[Dict[str, Any]] = Field(default_factory=list)
    track_ids: List[str] = Field(default_factory=list)
    events_generated: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    execution_time_ms: float = 0.0
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
