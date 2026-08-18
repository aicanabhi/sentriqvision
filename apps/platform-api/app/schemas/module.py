import uuid
from pydantic import BaseModel, Field, ConfigDict

class ModuleCreate(BaseModel):
    code: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    enabled: bool = True

class ModuleResponse(BaseModel):
    id: uuid.UUID
    code: str
    name: str
    description: str | None
    enabled: bool

    model_config = ConfigDict(from_attributes=True)