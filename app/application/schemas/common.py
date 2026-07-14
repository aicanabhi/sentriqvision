
from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar
from datetime import datetime

T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    message: Optional[str] = None
    data: Optional[T] = None


class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    message: Optional[str] = None
    data: Optional[T] = None
    total: int
    page: int
    page_size: int


class MongoDBRef(BaseModel):
    id: str


class TimestampsMixin(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
