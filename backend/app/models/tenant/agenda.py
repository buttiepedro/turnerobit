import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import TIMESTAMPTZ, UUID

from app.db.base import Base


class Agenda(Base):
    __tablename__ = "agendas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    slot_duration_minutes = Column(Integer, nullable=False, default=30)
    max_future_days = Column(Integer, nullable=False, default=30)
    is_active = Column(Boolean, nullable=False, default=True)
    color = Column(String(7), nullable=False, default="#3B82F6")
    created_at = Column(TIMESTAMPTZ, default=datetime.utcnow)
