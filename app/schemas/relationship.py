from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Literal

RelationshipStatus = Literal["PENDING", "ACCEPTED", "REJECTED", "BLOCKED"]


class RelationshipRequestCreate(BaseModel):
    addressee_handle: str  # 친구요청 보낼 대상 handle


class RelationshipOut(BaseModel):
    id: UUID
    requester_id: UUID
    addressee_id: UUID
    status: RelationshipStatus
    created_at: datetime

    class Config:
        from_attributes = True

    class Config:
        from_attributes = True