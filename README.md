# DevLog

DevLog es una aplicacion web para registrar proyectos, sesiones de trabajo y metricas de tiempo. El proyecto usa backend y frontend desacoplados.

## Stack

- Backend: Django, Django REST Framework, Simple JWT, PostgreSQL
- Frontend: SvelteKit, Svelte 5, TypeScript
- API base local: `http://127.0.0.1:8000/api/v1`
- Frontend local: `http://localhost:5173`

## Estado Del MVP

MVP funcional y presentable.

Incluye:

- Registro, login, refresh y logout con JWT.
- CRUD de proyectos.
- CRUD de sesiones de trabajo.
- Calculo automatico de duracion de sesiones.
- Validacion de traslapes de sesiones.
- Dashboard con metricas generales.
- Horas por proyecto.
- Horas de la semana actual.
- UI responsive basica con SvelteKit.

## Estructura

```text
DevLog/
  backend/
  frontend/
  docs/
```

## Requisitos

- Python 3.12+
- Node.js LTS
- pnpm
- PostgreSQL

Si no tienes `pnpm`:

```bash
npm install -g pnpm
```

## Configurar Backend

Entra al backend:

```bash
cd backend
```

Crea entorno virtual:

```bash
python -m venv venv
```

Activa el entorno:

```bash
source venv/bin/activate
```

En Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

En Windows CMD:

```cmd
.\venv\Scripts\activate.bat
```

Instala dependencias:

```bash
pip install -r requirements.txt
```

Crea el archivo `.env` desde el ejemplo:

```bash
cp env.example .env
```

Edita `.env` con tus credenciales locales de PostgreSQL:

```env
DEBUG=True
SECRET_KEY=tu-secret-key-temporal-cambiar-luego
DATABASE_NAME=devlog_db
DATABASE_USER=devlog_user
DATABASE_PASSWORD=tu_password_aqui
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

Crea la base de datos y usuario en PostgreSQL segun esos valores. Ejemplo usando `psql`:

```sql
CREATE DATABASE devlog_db;
CREATE USER devlog_user WITH PASSWORD 'tu_password_aqui';
GRANT ALL PRIVILEGES ON DATABASE devlog_db TO devlog_user;
```

Ejecuta migraciones:

```bash
python manage.py migrate
```

Levanta el backend:

```bash
python manage.py runserver
```

Backend disponible en:

```text
http://127.0.0.1:8000
```

## Configurar Frontend

En otra terminal, desde la raiz del proyecto:

```bash
cd frontend
```

Instala dependencias:

```bash
pnpm install
```

Crea el archivo `.env` desde el ejemplo:

```bash
cp .env.example .env
```

Contenido esperado:

```env
VITE_API_URL=http://127.0.0.1:8000/api/v1
```

Levanta el frontend:

```bash
pnpm dev
```

Frontend disponible en:

```text
http://localhost:5173
```

## CORS

El backend ya permite el frontend local:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
```

Si cambias el puerto del frontend, actualiza `backend/config/settings.py`.

## Ejecutar Tests Backend

Desde `backend` con el entorno virtual activo:

```bash
python manage.py test apps.users apps.projects apps.sessions apps.analytics
```

## Verificar Frontend

Desde `frontend`:

```bash
pnpm check
```

Opcionalmente:

```bash
pnpm lint
```

## Checklist Manual MVP

1. Crear cuenta.
2. Iniciar sesion.
3. Crear proyecto.
4. Editar proyecto.
5. Crear sesion de trabajo.
6. Ver metricas en dashboard.
7. Filtrar sesiones.
8. Editar sesion.
9. Eliminar sesion.
10. Cerrar sesion.

## Flujo Para Continuar En Otra Maquina

1. Clona el repositorio.
2. Configura PostgreSQL.
3. Crea `backend/.env` usando `backend/env.example`.
4. Instala dependencias del backend.
5. Ejecuta migraciones.
6. Levanta backend con `python manage.py runserver`.
7. Crea `frontend/.env` usando `frontend/.env.example`.
8. Instala dependencias del frontend con `pnpm install`.
9. Levanta frontend con `pnpm dev`.
10. Abre `http://localhost:5173`.

## Endpoints Principales

- `POST /api/v1/auth/register/`
- `POST /api/v1/auth/login/`
- `POST /api/v1/auth/refresh/`
- `POST /api/v1/auth/logout/`
- `GET|POST /api/v1/projects/`
- `GET|POST /api/v1/work-sessions/`
- `GET /api/v1/analytics/summary/`

La especificacion completa esta en:

```text
docs/04-api-spec.md
```

Las pruebas manuales de API estan en:

```text
docs/06-manual-api-tests.md
```

## Archivos Locales No Versionados

No se deben subir al repositorio:

- `backend/.env`
- `frontend/.env`
- `backend/venv/`
- `.venv/`
- `frontend/node_modules/`
- colecciones locales con tokens reales
