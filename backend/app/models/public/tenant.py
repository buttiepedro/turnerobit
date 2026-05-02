import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMPTZ, UUID

from app.db.base import Base


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
    created_at = Column(TIMESTAMPTZ, default=datetime.utcnow)
    updated_at = Column(TIMESTAMPTZ, default=datetime.utcnow, onupdate=datetime.utcnow)
