import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.tenant.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_users(self) -> list[User]:
        result = await self.db.execute(select(User).order_by(User.created_at.desc()))
        return result.scalars().all()

    async def get_user(self, user_id: str) -> User:
        user = await self.db.get(User, uuid.UUID(user_id))
        if not user:
            raise HTTPException(404, "Usuario no encontrado")
        return user

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create_user(self, data: UserCreate) -> User:
        existing = await self.get_by_email(data.email)
        if existing:
            raise HTTPException(409, "Ya existe un usuario con ese email")
        user = User(
            id=uuid.uuid4(),
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
            role=data.role,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user(self, user_id: str, data: UserUpdate) -> User:
        user = await self.get_user(user_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def reset_password(self, user_id: str, new_password: str) -> User:
        user = await self.get_user(user_id)
        user.hashed_password = hash_password(new_password)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def authenticate(self, email: str, password: str) -> User:
        user = await self.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(401, "Credenciales inválidas")
        if not user.is_active:
            raise HTTPException(403, "Usuario inactivo")
        return user
