from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import AsyncSessionLocal
from app.db.tenant import set_tenant_schema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as db:
        yield db


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        tenant_slug: str = payload.get("tenant")
        user_type: str = payload.get("type")
        role: str = payload.get("role")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    if tenant_slug:
        await set_tenant_schema(db, f"tenant_{tenant_slug}")

    return {
        "id": user_id,
        "tenant": tenant_slug,
        "type": user_type,
        "role": role,
    }


def require_role(*roles: str):
    def checker(user: dict = Depends(get_current_user)):
        if user.get("role") not in roles and user.get("type") not in roles:
            raise HTTPException(status_code=403, detail="Permiso insuficiente")
        return user

    return checker


def require_superadmin(user: dict = Depends(get_current_user)):
    if user.get("type") != "superadmin":
        raise HTTPException(status_code=403, detail="Acceso exclusivo para superadmin")
    return user
