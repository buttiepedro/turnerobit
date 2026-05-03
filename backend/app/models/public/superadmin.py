import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, String, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


def utcnow():
    return datetime.now(timezone.utc)


class SuperAdmin(Base):
    __tablename__ = "superadmins"
    __table_args__ = {"schema": "public"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(Text, nullable=False)
    full_name = Column(String(200), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP(timezone=True), default=utcnow)
