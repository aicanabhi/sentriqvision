import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class CameraCreate(BaseModel):
    name: str
    location: Optional[str] = None
    rtsp_url: Optional[str] = "webcam://0"
    substream_url: Optional[str] = None
    camera_type: str = "WEBCAM" # WEBCAM, IP_CAMERA, CCTV, RTSP
    device_index: Optional[int] = 0
    fps_sampling: int = 5
    roi_polygons: Optional[dict] = None


class CameraUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    rtsp_url: Optional[str] = None
    substream_url: Optional[str] = None
    camera_type: Optional[str] = None
    device_index: Optional[int] = None
    fps_sampling: Optional[int] = None
    status: Optional[str] = None
    roi_polygons: Optional[dict] = None


class CameraResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    location: Optional[str] = None
    rtsp_url: str
    substream_url: Optional[str] = None
    camera_type: str = "RTSP"
    device_index: Optional[int] = None
    is_running: bool = False
    fps_sampling: int = 5
    status: str = "OFFLINE"
    roi_polygons: Optional[dict] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WebcamDevice(BaseModel):
    index: int
    name: str
    available: bool
    path: Optional[str] = None
