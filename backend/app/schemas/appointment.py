from datetime import date, datetime, time
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class AppointmentCreate(BaseModel):
    agenda_id: UUID
    appointment_date: date
    start_time: time
    client_name: str = Field(..., min_length=2, max_length=200)
    client_email: EmailStr | None = None
    client_phone: str | None = None
    notes: str | None = None
    client_notes: str | None = None


class AppointmentUpdate(BaseModel):
    client_name: str | None = None
    client_email: EmailStr | None = None
    client_phone: str | None = None
    notes: str | None = None
    client_notes: str | None = None


class AppointmentCancel(BaseModel):
    reason: str = Field(..., min_length=1)


class AppointmentOut(BaseModel):
    id: UUID
    agenda_id: UUID
    appointment_date: date
    start_time: time
    end_time: time
    status: str
    client_name: str
    client_email: str | None
    client_phone: str | None
    notes: str | None
    client_notes: str | None
    created_by: UUID | None
    cancelled_at: datetime | None
    cancelled_by: UUID | None
    cancel_reason: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SlotOut(BaseModel):
    start_time: str
    end_time: str
    available: bool
