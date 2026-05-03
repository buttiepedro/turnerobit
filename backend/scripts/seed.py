"""Seed initial superadmin and optional demo tenant."""
import asyncio
import sys
import uuid
from pathlib import Path

# Ensure /app (project root) is in sys.path when running as python scripts/seed.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.security import hash_password
from app.db.session import AsyncSessionLocal
from app.db.tenant import create_tenant_schema
from app.models.public.superadmin import SuperAdmin
from app.models.public.tenant import Tenant


async def seed():
    async with AsyncSessionLocal() as db:
        superadmin = SuperAdmin(
            id=uuid.uuid4(),
            email="admin@sistema.com",
            hashed_password=hash_password("changeme123"),
            full_name="Super Administrador",
            is_active=True,
        )
        db.add(superadmin)
        await db.commit()
        print("Superadmin creado: admin@sistema.com / changeme123")

        demo_slug = "demo"
        demo_schema = f"tenant_{demo_slug}"
        tenant = Tenant(
            id=uuid.uuid4(),
            slug=demo_slug,
            name="Empresa Demo",
            schema_name=demo_schema,
            max_agendas=3,
            plan="basic",
        )
        db.add(tenant)
        await db.flush()
        await create_tenant_schema(db, demo_schema)
        print(f"Tenant demo creado: slug='{demo_slug}', schema='{demo_schema}'")


if __name__ == "__main__":
    asyncio.run(seed())
