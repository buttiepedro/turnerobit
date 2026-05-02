from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, superadmin, tenants, agendas, schedules, appointments

app = FastAPI(title="Sistema de Turnos", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(superadmin.router, prefix="/api/superadmin", tags=["Superadmin"])
app.include_router(tenants.router, prefix="/api/tenants", tags=["Tenants"])
app.include_router(agendas.router, prefix="/api/agendas", tags=["Agendas"])
app.include_router(schedules.router, prefix="/api/schedules", tags=["Schedules"])
app.include_router(appointments.router, prefix="/api/appointments", tags=["Appointments"])


@app.get("/health")
async def health():
    return {"status": "ok"}
