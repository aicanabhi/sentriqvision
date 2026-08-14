import uuid
from pydantic import BaseModel, Field, ConfigDict

class CameraCreate(BaseModel):
    site_id: uuid.UUID
    zone_id: uuid.UUID | None=None
    camera_code: str = Field(min_length=1, max_length=20)
    name: str = Field(min_length=1, max_length=255)
    rtsp_url: str = Field(min_length=1, max_length=1000)
    resolution: str = Field(default="1080p", max_length=20)
    fps: int = Field(default=5, gt=0)
    status: str = Field(default="OFFLINE", max_length=50)

class CameraResponse(BaseModel):
    id: uuid.UUID
    site_id: uuid.UUID
    zone_id: uuid.UUID | None
    camera_code: str
    name: str
    rtsp_url: str
    resolution: str
    fps: int
    status: str

    model_config = ConfigDict(from_attributes=True)