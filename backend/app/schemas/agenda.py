from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AgendaCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    description: str | None = None
    slot_duration_minutes: int = Field(default=30, ge=5, le=480)
    max_future_days: int = Field(default=30, ge=1, le=365)
    color: str = Field(default="#3B82F6", pattern=r"^#[0-9A-Fa-f]{6}$")
    owner_id: UUID | None = None


class AgendaUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    slot_duration_minutes: int | None = Field(default=None, ge=5, le=480)
    max_future_days: int | None = Field(default=None, ge=1, le=365)
    color: str | None = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")
    is_active: bool | None = None
    owner_id: UUID | None = None


class AgendaOut(BaseModel):
    id: UUID
    owner_id: UUID | None
    name: str
    description: str | None
    slot_duration_minutes: int
    max_future_days: int
    is_active: bool
    color: str
    created_at: datetime

    model_config = {"from_attributes": True}
