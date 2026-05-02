from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, require_superadmin
from app.schemas.tenant import TenantCreate, TenantOut, TenantUpdate
from app.services.tenant_service import TenantService

router = APIRouter()


@router.get("/tenants", response_model=list[TenantOut])
async def list_tenants(
    _=Depends(require_superadmin),
    db: AsyncSession = Depends(get_db),
):
    svc = TenantService(db)
    return await svc.list_tenants()


@router.post("/tenants", response_model=TenantOut, status_code=201)
async def create_tenant(
    data: TenantCreate,
    _=Depends(require_superadmin),
    db: AsyncSession = Depends(get_db),
):
    svc = TenantService(db)
    return await svc.create_tenant(data)


@router.get("/tenants/{tenant_id}", response_model=TenantOut)
async def get_tenant(
    tenant_id: str,
    _=Depends(require_superadmin),
    db: AsyncSession = Depends(get_db),
):
    svc = TenantService(db)
    return await svc.get_tenant(tenant_id)


@router.patch("/tenants/{tenant_id}", response_model=TenantOut)
async def update_tenant(
    tenant_id: str,
    data: TenantUpdate,
    _=Depends(require_superadmin),
    db: AsyncSession = Depends(get_db),
):
    svc = TenantService(db)
    return await svc.update_tenant(tenant_id, data)


@router.delete("/tenants/{tenant_id}", response_model=TenantOut)
async def deactivate_tenant(
    tenant_id: str,
    _=Depends(require_superadmin),
    db: AsyncSession = Depends(get_db),
):
    svc = TenantService(db)
    return await svc.deactivate_tenant(tenant_id)
