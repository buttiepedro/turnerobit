import uuid
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tenant.agenda import Agenda
from app.models.tenant.appointment import Appointment
from app.models.tenant.schedule import Schedule, ScheduleException
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate
from app.utils.slot_generator import generate_slots


class AppointmentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_appointments(
        self,
        agenda_id: str | None = None,
        appointment_date=None,
        status: str | None = None,
    ) -> list[Appointment]:
        query = select(Appointment).order_by(
            Appointment.appointment_date, Appointment.start_time
        )
        if agenda_id:
            query = query.where(Appointment.agenda_id == uuid.UUID(agenda_id))
        if appointment_date:
            query = query.where(Appointment.appointment_date == appointment_date)
        if status:
            query = query.where(Appointment.status == status)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_appointment(self, appt_id: str) -> Appointment:
        appt = await self.db.get(Appointment, uuid.UUID(appt_id))
        if not appt:
            raise HTTPException(404, "Turno no encontrado")
        return appt

    async def create_appointment(self, data: AppointmentCreate, created_by: str) -> Appointment:
        agenda = await self.db.get(Agenda, data.agenda_id)
        if not agenda or not agenda.is_active:
            raise HTTPException(404, "Agenda no encontrada o inactiva")

        day_of_week = data.appointment_date.weekday()
        schedules = await self._get_schedules(data.agenda_id, day_of_week)
        if not schedules:
            raise HTTPException(409, "No hay atención configurada para ese día")

        exceptions = await self._get_exceptions(data.agenda_id, data.appointment_date)
        booked = await self._get_booked(data.agenda_id, data.appointment_date)
        slots = generate_slots(data.appointment_date, schedules, agenda.slot_duration_minutes, booked, exceptions)

        start_str = data.start_time.strftime("%H:%M:%S")
        if not any(s["start_time"] == start_str and s["available"] for s in slots):
            raise HTTPException(409, "El slot solicitado no está disponible")

        dt_start = datetime.combine(data.appointment_date, data.start_time)
        dt_end = dt_start + timedelta(minutes=agenda.slot_duration_minutes)

        appointment = Appointment(
            id=uuid.uuid4(),
            agenda_id=data.agenda_id,
            appointment_date=data.appointment_date,
            start_time=data.start_time,
            end_time=dt_end.time(),
            status="confirmed",
            client_name=data.client_name,
            client_email=data.client_email,
            client_phone=data.client_phone,
            notes=data.notes,
            client_notes=data.client_notes,
            created_by=uuid.UUID(created_by),
        )
        self.db.add(appointment)
        await self.db.commit()
        await self.db.refresh(appointment)
        return appointment

    async def update_appointment(self, appt_id: str, data: AppointmentUpdate) -> Appointment:
        appt = await self.get_appointment(appt_id)
        if appt.status in ("cancelled", "completed"):
            raise HTTPException(409, "No se puede modificar un turno cancelado o completado")
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(appt, field, value)
        await self.db.commit()
        await self.db.refresh(appt)
        return appt

    async def cancel_appointment(self, appt_id: str, reason: str, cancelled_by: str) -> Appointment:
        appt = await self.get_appointment(appt_id)
        if appt.status in ("completed", "cancelled"):
            raise HTTPException(409, "No se puede cancelar en el estado actual")
        appt.status = "cancelled"
        appt.cancelled_at = datetime.now(timezone.utc)
        appt.cancelled_by = uuid.UUID(cancelled_by)
        appt.cancel_reason = reason
        await self.db.commit()
        await self.db.refresh(appt)
        return appt

    async def confirm_appointment(self, appt_id: str) -> Appointment:
        appt = await self.get_appointment(appt_id)
        if appt.status != "pending":
            raise HTTPException(409, "Solo se pueden confirmar turnos en estado pendiente")
        appt.status = "confirmed"
        await self.db.commit()
        await self.db.refresh(appt)
        return appt

    async def complete_appointment(self, appt_id: str) -> Appointment:
        appt = await self.get_appointment(appt_id)
        if appt.status not in ("pending", "confirmed"):
            raise HTTPException(409, "No se puede completar en el estado actual")
        appt.status = "completed"
        await self.db.commit()
        await self.db.refresh(appt)
        return appt

    async def get_slots(self, agenda_id: str, target_date) -> list[dict]:
        agenda = await self.db.get(Agenda, uuid.UUID(agenda_id))
        if not agenda or not agenda.is_active:
            raise HTTPException(404, "Agenda no encontrada o inactiva")

        day_of_week = target_date.weekday()
        schedules = await self._get_schedules(uuid.UUID(agenda_id), day_of_week)
        exceptions = await self._get_exceptions(uuid.UUID(agenda_id), target_date)
        booked = await self._get_booked(uuid.UUID(agenda_id), target_date)
        return generate_slots(target_date, schedules, agenda.slot_duration_minutes, booked, exceptions)

    async def _get_schedules(self, agenda_id, day_of_week: int) -> list[Schedule]:
        result = await self.db.execute(
            select(Schedule).where(
                Schedule.agenda_id == agenda_id,
                Schedule.day_of_week == day_of_week,
                Schedule.is_active == True,
            )
        )
        return result.scalars().all()

    async def _get_exceptions(self, agenda_id, target_date) -> list[ScheduleException]:
        result = await self.db.execute(
            select(ScheduleException).where(
                ScheduleException.agenda_id == agenda_id,
                ScheduleException.exception_date == target_date,
            )
        )
        return result.scalars().all()

    async def _get_booked(self, agenda_id, target_date) -> list[Appointment]:
        result = await self.db.execute(
            select(Appointment).where(
                Appointment.agenda_id == agenda_id,
                Appointment.appointment_date == target_date,
                Appointment.status.not_in(["cancelled"]),
            )
        )
        return result.scalars().all()
