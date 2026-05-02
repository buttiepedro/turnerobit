from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.schemas.schedule import (
    ScheduleCreate,
    ScheduleExceptionCreate,
    ScheduleExceptionOut,
    ScheduleOut,
    ScheduleUpdate,
)
from app.services.schedule_service import ScheduleService

router = APIRouter()


@router.get("", response_model=list[ScheduleOut])
async def list_schedules(
    agenda_id: str = Query(...),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ScheduleService(db)
    return await svc.list_schedules(agenda_id)


@router.post("", response_model=ScheduleOut, status_code=201)
async def create_schedule(
    data: ScheduleCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ScheduleService(db)
    return await svc.create_schedule(data)


@router.put("/{schedule_id}", response_model=ScheduleOut)
async def update_schedule(
    schedule_id: str,
    data: ScheduleUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ScheduleService(db)
    return await svc.update_schedule(schedule_id, data)


@router.delete("/{schedule_id}", status_code=204)
async def delete_schedule(
    schedule_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ScheduleService(db)
    await svc.delete_schedule(schedule_id)


@router.get("/exceptions", response_model=list[ScheduleExceptionOut])
async def list_exceptions(
    agenda_id: str = Query(...),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ScheduleService(db)
    return await svc.list_exceptions(agenda_id)


@router.post("/exceptions", response_model=ScheduleExceptionOut, status_code=201)
async def create_exception(
    data: ScheduleExceptionCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ScheduleService(db)
    return await svc.create_exception(data)
