from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.schemas.appointment import (
    AppointmentCancel,
    AppointmentCreate,
    AppointmentOut,
    AppointmentUpdate,
    SlotOut,
)
from app.services.appointment_service import AppointmentService

router = APIRouter()


@router.get("", response_model=list[AppointmentOut])
async def list_appointments(
    agenda_id: str | None = Query(default=None),
    appointment_date: date | None = Query(default=None),
    status: str | None = Query(default=None),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = AppointmentService(db)
    return await svc.list_appointments(agenda_id, appointment_date, status)


@router.post("", response_model=AppointmentOut, status_code=201)
async def create_appointment(
    data: AppointmentCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = AppointmentService(db)
    return await svc.create_appointment(data, current_user["id"])


@router.get("/availability", response_model=list[SlotOut])
async def check_availability(
    agenda_id: str = Query(...),
    date: date = Query(...),
    db: AsyncSession = Depends(get_db),
):
    svc = AppointmentService(db)
    return await svc.get_slots(agenda_id, date)


@router.get("/{appt_id}", response_model=AppointmentOut)
async def get_appointment(
    appt_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = AppointmentService(db)
    return await svc.get_appointment(appt_id)


@router.patch("/{appt_id}", response_model=AppointmentOut)
async def update_appointment(
    appt_id: str,
    data: AppointmentUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = AppointmentService(db)
    return await svc.update_appointment(appt_id, data)


@router.post("/{appt_id}/cancel", response_model=AppointmentOut)
async def cancel_appointment(
    appt_id: str,
    data: AppointmentCancel,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = AppointmentService(db)
    return await svc.cancel_appointment(appt_id, data.reason, current_user["id"])


@router.post("/{appt_id}/confirm", response_model=AppointmentOut)
async def confirm_appointment(
    appt_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = AppointmentService(db)
    return await svc.confirm_appointment(appt_id)


@router.post("/{appt_id}/complete", response_model=AppointmentOut)
async def complete_appointment(
    appt_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = AppointmentService(db)
    return await svc.complete_appointment(appt_id)
