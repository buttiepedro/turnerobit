import uuid

from sqlalchemy import Boolean, Column, Date, ForeignKey, SmallInteger, Text, Time
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agenda_id = Column(UUID(as_uuid=True), ForeignKey("agendas.id", ondelete="CASCADE"), nullable=False)
    day_of_week = Column(SmallInteger, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    valid_from = Column(Date, nullable=True)
    valid_until = Column(Date, nullable=True)


class ScheduleException(Base):
    __tablename__ = "schedule_exceptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agenda_id = Column(UUID(as_uuid=True), ForeignKey("agendas.id", ondelete="CASCADE"), nullable=False)
    exception_date = Column(Date, nullable=False)
    is_closed = Column(Boolean, nullable=False, default=True)
    open_time = Column(Time, nullable=True)
    close_time = Column(Time, nullable=True)
    reason = Column(Text, nullable=True)
