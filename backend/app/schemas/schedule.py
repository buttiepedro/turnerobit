from datetime import date, time
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class ScheduleCreate(BaseModel):
    agenda_id: UUID
    day_of_week: int = Field(..., ge=0, le=6)
    start_time: time
    end_time: time
    valid_from: date | None = None
    valid_until: date | None = None

    @model_validator(mode="after")
    def validate_times(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class ScheduleUpdate(BaseModel):
    start_time: time | None = None
    end_time: time | None = None
    is_active: bool | None = None
    valid_from: date | None = None
    valid_until: date | None = None


class ScheduleOut(BaseModel):
    id: UUID
    agenda_id: UUID
    day_of_week: int
    start_time: time
    end_time: time
    is_active: bool
    valid_from: date | None
    valid_until: date | None

    model_config = {"from_attributes": True}


class ScheduleExceptionCreate(BaseModel):
    agenda_id: UUID
    exception_date: date
    is_closed: bool = True
    open_time: time | None = None
    close_time: time | None = None
    reason: str | None = None


class ScheduleExceptionOut(BaseModel):
    id: UUID
    agenda_id: UUID
    exception_date: date
    is_closed: bool
    open_time: time | None
    close_time: time | None
    reason: str | None

    model_config = {"from_attributes": True}
