from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class TenantCreate(BaseModel):
    slug: str = Field(..., min_length=2, max_length=50, pattern=r"^[a-z0-9_-]+$")
    name: str = Field(..., min_length=2, max_length=200)
    max_agendas: int = Field(default=1, ge=1)
    plan: str = Field(default="basic")


class TenantUpdate(BaseModel):
    name: str | None = None
    max_agendas: int | None = Field(default=None, ge=1)
    plan: str | None = None
    is_active: bool | None = None
    settings: dict[str, Any] | None = None


class TenantOut(BaseModel):
    id: UUID
    slug: str
    name: str
    schema_name: str
    max_agendas: int
    is_active: bool
    plan: str
    settings: dict[str, Any]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
