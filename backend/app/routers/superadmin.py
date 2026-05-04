from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, require_superadmin
from app.db.tenant import set_tenant_schema
from app.schemas.tenant import TenantCreate, TenantOut, TenantUpdate
from app.schemas.user import PasswordResetBySuperadmin, UserCreate, UserOut, UserUpdate
from app.services.tenant_service import TenantService
from app.services.user_service import UserService

router = APIRouter()


@router.get("/tenants", response_model=list[TenantOut])
async def list_tenants(
    _=Depends(require_superadmin),
    db: AsyncSession = Depends(get_db),
):
    return await TenantService(db).list_tenants()


@router.post("/tenants", response_model=TenantOut, status_code=201)
async def create_tenant(
    data: TenantCreate,
    _=Depends(require_superadmin),
    db: AsyncSession = Depends(get_db),
):
    return await TenantService(db).create_tenant(data)


@router.get("/tenants/{tenant_id}", response_model=TenantOut)
async def get_tenant(
    tenant_id: str,
    _=Depends(require_superadmin),
    db: AsyncSession = Depends(get_db),
):
    return await TenantService(db).get_tenant(tenant_id)


@router.patch("/tenants/{tenant_id}", response_model=TenantOut)
async def update_tenant(
    tenant_id: str,
    data: TenantUpdate,
    _=Depends(require_superadmin),
    db: AsyncSession = Depends(get_db),
):
    return await TenantService(db).update_tenant(tenant_id, data)


@router.delete("/tenants/{tenant_id}", response_model=TenantOut)
async def deactivate_tenant(
    tenant_id: str,
    _=Depends(require_superadmin),
    db: AsyncSession = Depends(get_db),
):
    return await TenantService(db).deactivate_tenant(tenant_id)


# ── Tenant user management (superadmin) ────────────────────────────────────

async def _switch_to_tenant(tenant_id: str, db: AsyncSession):
    """Resolve tenant → switch DB search_path to its schema."""
    tenant = await TenantService(db).get_tenant(tenant_id)
    await set_tenant_schema(db, tenant.schema_name)


@router.get("/tenants/{tenant_id}/users", response_model=list[UserOut])
async def list_tenant_users(
    tenant_id: str,
    _=Depends(require_superadmin),
    db: AsyncSession = Depends(get_db),
):
    await _switch_to_tenant(tenant_id, db)
    return await UserService(db).list_users()


@router.post("/tenants/{tenant_id}/users", response_model=UserOut, status_code=201)
async def create_tenant_user(
    tenant_id: str,
    data: UserCreate,
    _=Depends(require_superadmin),
    db: AsyncSession = Depends(get_db),
):
    await _switch_to_tenant(tenant_id, db)
    return await UserService(db).create_user(data)


@router.patch("/tenants/{tenant_id}/users/{user_id}", response_model=UserOut)
async def update_tenant_user(
    tenant_id: str,
    user_id: str,
    data: UserUpdate,
    _=Depends(require_superadmin),
    db: AsyncSession = Depends(get_db),
):
    await _switch_to_tenant(tenant_id, db)
    return await UserService(db).update_user(user_id, data)


@router.post("/tenants/{tenant_id}/users/{user_id}/reset-password", response_model=UserOut)
async def reset_tenant_user_password(
    tenant_id: str,
    user_id: str,
    data: PasswordResetBySuperadmin,
    _=Depends(require_superadmin),
    db: AsyncSession = Depends(get_db),
):
    await _switch_to_tenant(tenant_id, db)
    return await UserService(db).reset_password(user_id, data.new_password)
