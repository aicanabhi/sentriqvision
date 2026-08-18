import uuid
from pydantic import BaseModel, ConfigDict

class CameraModuleCreate(BaseModel):
    camera_id: uuid.UUID
    module_id: uuid.UUID
    enabled: bool = True

class CameraModuleResponse(BaseModel):
    id: uuid.UUID
    camera_id: uuid.UUID
    module_id: uuid.UUID
    enabled: bool

    model_config = ConfigDict(from_attributes=True)