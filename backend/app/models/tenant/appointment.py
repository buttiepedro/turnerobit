import uuid
from datetime import datetime

from sqlalchemy import Column, Date, ForeignKey, String, Text, Time
from sqlalchemy.dialects.postgresql import TIMESTAMPTZ, UUID

from app.db.base import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agenda_id = Column(UUID(as_uuid=True), ForeignKey("agendas.id", ondelete="CASCADE"), nullable=False)
    appointment_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(String(20), nullable=False, default="confirmed")
    client_name = Column(String(200), nullable=False)
    client_email = Column(String(255), nullable=True)
    client_phone = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    client_notes = Column(Text, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    cancelled_at = Column(TIMESTAMPTZ, nullable=True)
    cancelled_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    cancel_reason = Column(Text, nullable=True)
    created_at = Column(TIMESTAMPTZ, default=datetime.utcnow)
    updated_at = Column(TIMESTAMPTZ, default=datetime.utcnow, onupdate=datetime.utcnow)
