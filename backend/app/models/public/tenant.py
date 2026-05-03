import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.db.base import Base


def utcnow():
    return datetime.now(timezone.utc)


class Tenant(Base):
    __tablename__ = "tenants"
    __table_args__ = {"schema": "public"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug = Column(String(50), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    schema_name = Column(String(63), unique=True, nullable=False)
    max_agendas = Column(Integer, nullable=False, default=1)
    is_active = Column(Boolean, nullable=False, default=True)
    plan = Column(String(50), default="basic")
    settings = Column(JSONB, default=dict)
    created_at = Column(TIMESTAMP(timezone=True), default=utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), default=utcnow, onupdate=utcnow)
