import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, String, Text
from sqlalchemy.dialects.postgresql import TIMESTAMPTZ, UUID

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(Text, nullable=False)
    full_name = Column(String(200), nullable=False)
    role = Column(String(50), nullable=False, default="usuario_agenda")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMPTZ, default=datetime.utcnow)
