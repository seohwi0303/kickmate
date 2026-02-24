from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class UserCreate(BaseModel):
    handle: str = Field(min_length=2, max_length=30)
    display_name: str = Field(min_length=1, max_length=50)


class UserOut(BaseModel):
    id: UUID
    handle: str
    display_name: str
    elo: int
    level: str
    trust_tier: int
    created_at: datetime

    class Config:
        from_attributes = True
    
from pydantic import BaseModel
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    limit: int
    offset: int
    next_offset: Optional[int] = None
    prev_offset: Optional[int] = None
    has_more: bool

class PaginatedUsersOut(Page[UserOut]):
    pass