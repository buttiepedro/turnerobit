import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.tenant import create_tenant_schema, drop_tenant_schema
from app.models.public.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantUpdate


class TenantService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_tenants(self) -> list[Tenant]:
        result = await self.db.execute(select(Tenant).order_by(Tenant.created_at.desc()))
        return result.scalars().all()

    async def get_tenant(self, tenant_id: str) -> Tenant:
        tenant = await self.db.get(Tenant, uuid.UUID(tenant_id))
        if not tenant:
            raise HTTPException(404, "Tenant no encontrado")
        return tenant

    async def create_tenant(self, data: TenantCreate) -> Tenant:
        existing = await self.db.execute(select(Tenant).where(Tenant.slug == data.slug))
        if existing.scalar_one_or_none():
            raise HTTPException(409, f"Ya existe un tenant con slug '{data.slug}'")

        schema_name = f"tenant_{data.slug}"
        tenant = Tenant(
            id=uuid.uuid4(),
            slug=data.slug,
            name=data.name,
            schema_name=schema_name,
            max_agendas=data.max_agendas,
            plan=data.plan,
        )
        self.db.add(tenant)
        await self.db.flush()

        await create_tenant_schema(self.db, schema_name)
        await self.db.refresh(tenant)
        return tenant

    async def update_tenant(self, tenant_id: str, data: TenantUpdate) -> Tenant:
        tenant = await self.get_tenant(tenant_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(tenant, field, value)
        await self.db.commit()
        await self.db.refresh(tenant)
        return tenant

    async def deactivate_tenant(self, tenant_id: str) -> Tenant:
        tenant = await self.get_tenant(tenant_id)
        tenant.is_active = False
        await self.db.commit()
        await self.db.refresh(tenant)
        return tenant
