from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


async def set_tenant_schema(db: AsyncSession, schema_name: str):
    """Switch the search_path to the active tenant schema."""
    await db.execute(text(f"SET search_path TO {schema_name}, public"))


async def create_tenant_schema(db: AsyncSession, schema_name: str):
    """Create the schema and all tables for a new tenant."""
    await db.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
    await db.execute(text(f"SET search_path TO {schema_name}"))
    await _create_tenant_tables(db)
    await db.commit()


async def drop_tenant_schema(db: AsyncSession, schema_name: str):
    """Drop the schema and all its tables (hard delete)."""
    await db.execute(text(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE"))
    await db.commit()


async def _create_tenant_tables(db: AsyncSession):
    stmts = [
        """CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            email VARCHAR(255) UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            full_name VARCHAR(200) NOT NULL,
            role VARCHAR(50) NOT NULL DEFAULT 'usuario_agenda',
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS agendas (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            owner_id UUID REFERENCES users(id) ON DELETE SET NULL,
            name VARCHAR(200) NOT NULL,
            description TEXT,
            slot_duration_minutes INTEGER NOT NULL DEFAULT 30,
            max_future_days INTEGER NOT NULL DEFAULT 30,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            color VARCHAR(7) NOT NULL DEFAULT '#3B82F6',
            created_at TIMESTAMPTZ DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS schedules (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            agenda_id UUID NOT NULL REFERENCES agendas(id) ON DELETE CASCADE,
            day_of_week SMALLINT NOT NULL CHECK (day_of_week BETWEEN 0 AND 6),
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            valid_from DATE,
            valid_until DATE
        )""",
        """CREATE TABLE IF NOT EXISTS schedule_exceptions (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            agenda_id UUID NOT NULL REFERENCES agendas(id) ON DELETE CASCADE,
            exception_date DATE NOT NULL,
            is_closed BOOLEAN NOT NULL DEFAULT TRUE,
            open_time TIME,
            close_time TIME,
            reason TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS appointments (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            agenda_id UUID NOT NULL REFERENCES agendas(id) ON DELETE CASCADE,
            appointment_date DATE NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'confirmed',
            client_name VARCHAR(200) NOT NULL,
            client_email VARCHAR(255),
            client_phone VARCHAR(50),
            notes TEXT,
            client_notes TEXT,
            created_by UUID REFERENCES users(id) ON DELETE SET NULL,
            cancelled_at TIMESTAMPTZ,
            cancelled_by UUID REFERENCES users(id) ON DELETE SET NULL,
            cancel_reason TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        )""",
        """CREATE INDEX IF NOT EXISTS idx_appointments_agenda_date
            ON appointments(agenda_id, appointment_date)""",
        """CREATE INDEX IF NOT EXISTS idx_schedules_agenda_day
            ON schedules(agenda_id, day_of_week)""",
    ]
    for stmt in stmts:
        await db.execute(text(stmt))
