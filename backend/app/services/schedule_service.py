import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tenant.schedule import Schedule, ScheduleException
from app.schemas.schedule import (
    ScheduleCreate,
    ScheduleExceptionCreate,
    ScheduleUpdate,
)


class ScheduleService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_schedules(self, agenda_id: str) -> list[Schedule]:
        result = await self.db.execute(
            select(Schedule)
            .where(Schedule.agenda_id == uuid.UUID(agenda_id))
            .order_by(Schedule.day_of_week, Schedule.start_time)
        )
        return result.scalars().all()

    async def create_schedule(self, data: ScheduleCreate) -> Schedule:
        schedule = Schedule(
            id=uuid.uuid4(),
            agenda_id=data.agenda_id,
            day_of_week=data.day_of_week,
            start_time=data.start_time,
            end_time=data.end_time,
            valid_from=data.valid_from,
            valid_until=data.valid_until,
        )
        self.db.add(schedule)
        await self.db.commit()
        await self.db.refresh(schedule)
        return schedule

    async def update_schedule(self, schedule_id: str, data: ScheduleUpdate) -> Schedule:
        schedule = await self.db.get(Schedule, uuid.UUID(schedule_id))
        if not schedule:
            raise HTTPException(404, "Horario no encontrado")
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(schedule, field, value)
        await self.db.commit()
        await self.db.refresh(schedule)
        return schedule

    async def delete_schedule(self, schedule_id: str) -> None:
        schedule = await self.db.get(Schedule, uuid.UUID(schedule_id))
        if not schedule:
            raise HTTPException(404, "Horario no encontrado")
        await self.db.delete(schedule)
        await self.db.commit()

    async def list_exceptions(self, agenda_id: str) -> list[ScheduleException]:
        result = await self.db.execute(
            select(ScheduleException)
            .where(ScheduleException.agenda_id == uuid.UUID(agenda_id))
            .order_by(ScheduleException.exception_date)
        )
        return result.scalars().all()

    async def create_exception(self, data: ScheduleExceptionCreate) -> ScheduleException:
        exc = ScheduleException(
            id=uuid.uuid4(),
            agenda_id=data.agenda_id,
            exception_date=data.exception_date,
            is_closed=data.is_closed,
            open_time=data.open_time,
            close_time=data.close_time,
            reason=data.reason,
        )
        self.db.add(exc)
        await self.db.commit()
        await self.db.refresh(exc)
        return exc
