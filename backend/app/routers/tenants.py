from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user, require_role
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.get("/users", response_model=list[UserOut])
async def list_users(
    current_user: dict = Depends(require_role("admin_empresa")),
    db: AsyncSession = Depends(get_db),
):
    svc = UserService(db)
    return await svc.list_users()


@router.post("/users", response_model=UserOut, status_code=201)
async def create_user(
    data: UserCreate,
    current_user: dict = Depends(require_role("admin_empresa")),
    db: AsyncSession = Depends(get_db),
):
    svc = UserService(db)
    return await svc.create_user(data)


@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(
    user_id: str,
    current_user: dict = Depends(require_role("admin_empresa")),
    db: AsyncSession = Depends(get_db),
):
    svc = UserService(db)
    return await svc.get_user(user_id)


@router.patch("/users/{user_id}", response_model=UserOut)
async def update_user(
    user_id: str,
    data: UserUpdate,
    current_user: dict = Depends(require_role("admin_empresa")),
    db: AsyncSession = Depends(get_db),
):
    svc = UserService(db)
    return await svc.update_user(user_id, data)
