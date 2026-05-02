from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2, max_length=200)
    role: Literal["admin_empresa", "usuario_agenda"] = "usuario_agenda"


class UserUpdate(BaseModel):
    full_name: str | None = None
    role: Literal["admin_empresa", "usuario_agenda"] | None = None
    is_active: bool | None = None


class UserOut(BaseModel):
    id: UUID
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
