# Deploy en Railway

## Servicios a crear

| Servicio | Directorio raíz | Dockerfile |
|---|---|---|
| `turnos-db` | — | Plugin PostgreSQL de Railway |
| `turnos-backend` | `backend/` | `Dockerfile` |
| `turnos-frontend` | `frontend/` | `Dockerfile.railway` |

---

## Pasos

### 1. Crear el proyecto en Railway

1. Nuevo proyecto → **Deploy from GitHub repo**
2. Seleccionar el repositorio `turnerobit`

### 2. Agregar PostgreSQL

En el proyecto: **+ New** → **Database** → **PostgreSQL**

Railway inyecta `DATABASE_URL` automáticamente en el servicio que lo referencie.

### 3. Configurar el servicio Backend

- **Root Directory**: `backend`
- **Dockerfile Path**: `Dockerfile` *(Railway lo detecta solo)*

**Variables de entorno** (Settings → Variables):

| Variable | Valor |
|---|---|
| `DATABASE_URL` | *(referencia al plugin PG: `${{Postgres.DATABASE_URL}}`)* |
| `SECRET_KEY` | `<clave-aleatoria-segura>` |

> `start.sh` convierte automáticamente `postgresql://` → `postgresql+asyncpg://` y corre las migraciones antes de iniciar.

### 4. Configurar el servicio Frontend

- **Root Directory**: `frontend`
- **Dockerfile Path**: `Dockerfile.railway`

**Variables de entorno** (Settings → Variables):

| Variable | Valor |
|---|---|
| `BACKEND_URL` | URL pública del backend, ej: `https://turnos-backend.up.railway.app` |

> Nginx proxea `/api/` → `$BACKEND_URL/api/` en runtime, sin rebuild.

### 5. Seed inicial (una sola vez)

Una vez que el backend esté corriendo, ejecutar desde la terminal de Railway:

```sh
python scripts/seed.py
```

Esto crea el superadmin `admin@sistema.com` / `changeme123` y el tenant demo.

---

## Variables de entorno completas por servicio

### Backend
```
DATABASE_URL=${{Postgres.DATABASE_URL}}
SECRET_KEY=<genera-con: openssl rand -hex 32>
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Frontend
```
BACKEND_URL=https://<tu-backend>.up.railway.app
```
