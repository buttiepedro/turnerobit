import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, String, Text
from sqlalchemy.dialects.postgresql import TIMESTAMPTZ, UUID

from app.db.base import Base


class SuperAdmin(Base):
    __tablename__ = "superadmins"
    __table_args__ = {"schema": "public"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(Text, nullable=False)
    full_name = Column(String(200), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMPTZ, default=datetime.utcnow)
