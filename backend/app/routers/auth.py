from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.core.security import create_access_token, verify_password
from app.models.public.superadmin import SuperAdmin
from app.schemas.user import TokenOut, UserOut
from app.services.user_service import UserService
from sqlalchemy import select

router = APIRouter()


@router.post("/login", response_model=TokenOut)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Login for tenant users. Requires X-Tenant-Slug header or pass tenant in username as tenant:email."""
    parts = form_data.username.split(":", 1)
    if len(parts) == 2:
        tenant_slug, email = parts
        from app.db.tenant import set_tenant_schema
        await set_tenant_schema(db, f"tenant_{tenant_slug}")
        svc = UserService(db)
        user = await svc.authenticate(email, form_data.password)
        token = create_access_token({
            "sub": str(user.id),
            "tenant": tenant_slug,
            "type": "tenant_user",
            "role": user.role,
        })
    else:
        result = await db.execute(
            select(SuperAdmin).where(SuperAdmin.email == form_data.username)
        )
        superadmin = result.scalar_one_or_none()
        if not superadmin or not verify_password(form_data.password, superadmin.hashed_password):
            from fastapi import HTTPException
            raise HTTPException(401, "Credenciales inválidas")
        token = create_access_token({
            "sub": str(superadmin.id),
            "type": "superadmin",
            "role": "superadmin",
        })

    return TokenOut(access_token=token)


@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    return current_user
