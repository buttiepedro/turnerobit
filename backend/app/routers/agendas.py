from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user, require_role
from app.schemas.agenda import AgendaCreate, AgendaOut, AgendaUpdate
from app.schemas.appointment import SlotOut
from app.services.agenda_service import AgendaService
from app.services.appointment_service import AppointmentService

router = APIRouter()


@router.get("", response_model=list[AgendaOut])
async def list_agendas(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = AgendaService(db)
    return await svc.list_agendas()


@router.post("", response_model=AgendaOut, status_code=201)
async def create_agenda(
    data: AgendaCreate,
    current_user: dict = Depends(require_role("admin_empresa")),
    db: AsyncSession = Depends(get_db),
):
    svc = AgendaService(db)
    return await svc.create_agenda(data, current_user["tenant"])


@router.get("/{agenda_id}", response_model=AgendaOut)
async def get_agenda(
    agenda_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = AgendaService(db)
    return await svc.get_agenda(agenda_id)


@router.put("/{agenda_id}", response_model=AgendaOut)
async def update_agenda(
    agenda_id: str,
    data: AgendaUpdate,
    current_user: dict = Depends(require_role("admin_empresa")),
    db: AsyncSession = Depends(get_db),
):
    svc = AgendaService(db)
    return await svc.update_agenda(agenda_id, data)


@router.delete("/{agenda_id}", response_model=AgendaOut)
async def deactivate_agenda(
    agenda_id: str,
    current_user: dict = Depends(require_role("admin_empresa")),
    db: AsyncSession = Depends(get_db),
):
    svc = AgendaService(db)
    return await svc.deactivate_agenda(agenda_id)


@router.get("/{agenda_id}/slots", response_model=list[SlotOut])
async def get_slots(
    agenda_id: str,
    date: date = Query(..., description="Fecha objetivo YYYY-MM-DD"),
    db: AsyncSession = Depends(get_db),
):
    svc = AppointmentService(db)
    return await svc.get_slots(agenda_id, date)
