import uuid
from typing import Any
from pydantic import BaseModel, Field, ConfigDict

class ModuleConfigCreate(BaseModel):
    camera_module_id: uuid.UUID
    configuration: Any = Field(default_factory=dict)

class ModuleConfigUpdate(BaseModel):
    configuration: Any = Field(default_factory=dict)

class ModuleConfigResponse(BaseModel):
    id: uuid.UUID
    camera_module_id: uuid.UUID
    configuration: Any

    model_config = ConfigDict(from_attributes=True)
