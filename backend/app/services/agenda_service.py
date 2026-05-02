import uuid

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.public.tenant import Tenant
from app.models.tenant.agenda import Agenda
from app.schemas.agenda import AgendaCreate, AgendaUpdate


class AgendaService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_agendas(self) -> list[Agenda]:
        result = await self.db.execute(select(Agenda).order_by(Agenda.created_at.desc()))
        return result.scalars().all()

    async def get_agenda(self, agenda_id: str) -> Agenda:
        agenda = await self.db.get(Agenda, uuid.UUID(agenda_id))
        if not agenda:
            raise HTTPException(404, "Agenda no encontrada")
        return agenda

    async def create_agenda(self, data: AgendaCreate, tenant_slug: str) -> Agenda:
        tenant_result = await self.db.execute(
            select(Tenant).where(Tenant.slug == tenant_slug)
        )
        tenant = tenant_result.scalar_one_or_none()
        if not tenant:
            raise HTTPException(404, "Tenant no encontrado")

        count_result = await self.db.execute(
            select(func.count()).select_from(Agenda).where(Agenda.is_active == True)
        )
        active_count = count_result.scalar_one()
        if active_count >= tenant.max_agendas:
            raise HTTPException(409, f"Se alcanzó la cuota máxima de {tenant.max_agendas} agenda(s)")

        agenda = Agenda(
            id=uuid.uuid4(),
            owner_id=data.owner_id,
            name=data.name,
            description=data.description,
            slot_duration_minutes=data.slot_duration_minutes,
            max_future_days=data.max_future_days,
            color=data.color,
        )
        self.db.add(agenda)
        await self.db.commit()
        await self.db.refresh(agenda)
        return agenda

    async def update_agenda(self, agenda_id: str, data: AgendaUpdate) -> Agenda:
        agenda = await self.get_agenda(agenda_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(agenda, field, value)
        await self.db.commit()
        await self.db.refresh(agenda)
        return agenda

    async def deactivate_agenda(self, agenda_id: str) -> Agenda:
        agenda = await self.get_agenda(agenda_id)
        agenda.is_active = False
        await self.db.commit()
        await self.db.refresh(agenda)
        return agenda
