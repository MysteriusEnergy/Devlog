# 04 – API Especificaciones

## 1. Principios de la API

- La API será RESTful.
- Todas las respuestas serán en formato JSON.
- Todas las rutas protegidas requerirán autenticación JWT.
- Los recursos siempre estarán asociados al usuario autenticado.
- Los UUID serán utilizados como identificadores públicos.
- Los errores tendrán mensajes claros. Los errores de validación pueden devolverse por campo siguiendo el formato estándar de Django REST Framework.

Base URL (local):
/api/v1

---

## 2. Autenticación

### 2.1 Registro de Usuario

POST /api/v1/auth/register/

Body:

{
  "email": "[user@email.com](mailto:user@email.com)",
  "password": "string"
}

Response 201:

{
  "id": "uuid",
  "email": "[user@email.com](mailto:user@email.com)",
  "created_at": "timestamp"
}

---

### 2.2 Login

POST /api/v1/auth/login/

Body:

{
  "email": "[user@email.com](mailto:user@email.com)",
  "password": "string"
}

Response 200:

{
  "access_token": "jwt_token",
  "refresh_token": "jwt_refresh_token",
  "expires_in": 3600
}

---

### 2.3 Refresh Token

POST /api/v1/auth/refresh/

Body:

{
  "refresh_token": "jwt_refresh_token"
}

Response 200:

{
  "access_token": "jwt_token",
  "expires_in": 3600
}

Errores:

- 401 si el refresh_token es inválido o ha expirado.

---

### 2.4 Logout

POST /api/v1/auth/logout/

Body:

{
  "refresh_token": "jwt_refresh_token"
}

Response 204:
Sin contenido.

Comportamiento:

- No requiere Authorization header. Solo el refresh_token en el body.
- El refresh_token es añadido a la blacklist en backend.
- El access_token expira naturalmente (no se invalida en servidor).
- Después del logout, intentar usar el refresh_token devuelve 401.

Errores:

- 400 si no se envía el refresh_token en el body.
- 401 si el refresh_token es inválido o ya fue invalidado.

---

## 3. Projects

### 3.1 Crear Proyecto

POST /api/v1/projects/

Headers:
Authorization: Bearer <access_token>

Body:

{
  "name": "Proyecto A",
  "description": "Opcional",
  "color": "#FF5733"
}

Response 201:

{
  "id": "uuid",
  "name": "Proyecto A",
  "description": "Opcional",
  "color": "#FF5733",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}

---

### 3.2 Obtener Proyectos del Usuario

GET /api/v1/projects/

Nota: sin paginación en el MVP. Considerar agregar page/per_page en versión futura
si el volumen de proyectos por usuario lo justifica.

Response 200:

[
  {
    "id": "uuid",
    "name": "Proyecto A",
    "description": "Opcional",
    "color": "#FF5733",
    "created_at": "timestamp",
    "updated_at": "timestamp"
  }
]

---

### 3.3 Actualizar Proyecto

PATCH /api/v1/projects/{project_id}/

Body (parcial):

{
  "name": "Nuevo nombre"
}

Response 200:
Proyecto actualizado.

---

### 3.4 Eliminar Proyecto

DELETE /api/v1/projects/{project_id}/

Response 204:
Sin contenido.

(Borrado físico)

---

## 4. WorkSessions

### 4.1 Crear Sesión

POST /api/v1/work-sessions/

Body:

{
  "project_id": "uuid",
  "date": "YYYY-MM-DD",
  "start_time": "HH:MM",
  "end_time": "HH:MM",
  "notes": "Opcional"
}

Response 201:

{
  "id": "uuid",
  "project_id": "uuid",
  "date": "YYYY-MM-DD",
  "start_time": "HH:MM",
  "end_time": "HH:MM",
  "duration_minutes": 120,
  "notes": "Opcional",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}

---

### 4.2 Obtener Sesiones

GET /api/v1/work-sessions/

Query params opcionales:

- project_id
- date
- from
- to
- page     (entero, default: 1)
- per_page (entero, default: 20, máximo: 100)

Validaciones de paginación:

- 400 si page < 1.
- 400 si per_page < 1 o per_page > 100.

Response 200:

{
  "data": [
    {
      "id": "uuid",
      "project_id": "uuid",
      "date": "YYYY-MM-DD",
      "start_time": "HH:MM",
      "end_time": "HH:MM",
      "duration_minutes": 120,
      "notes": "Opcional",
      "created_at": "timestamp",
      "updated_at": "timestamp"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 54,
    "total_pages": 3
  }
}

---

### 4.3 Actualizar Sesión

PATCH /api/v1/work-sessions/{session_id}/

Campos editables:

- notes (string, opcional)
- start_time (HH:MM)
- end_time (HH:MM)

Restricciones:

- duration_minutes no es editable. Se recalcula automáticamente en backend si start_time o end_time cambian.
- project_id y date no son editables después de la creación.

Body (parcial):

{
  "start_time": "09:00",
  "end_time": "11:30",
  "notes": "Nota actualizada"
}

Response 200:

{
  "id": "uuid",
  "project_id": "uuid",
  "date": "YYYY-MM-DD",
  "start_time": "09:00",
  "end_time": "11:30",
  "duration_minutes": 150,
  "notes": "Nota actualizada",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}

Errores:

- 400 si start_time >= end_time.
- 400 si el nuevo horario genera traslape con otra sesión del usuario.

---

### 4.4 Eliminar Sesión

DELETE /api/v1/work-sessions/{session_id}/

Response 204:
Sin contenido.

(Borrado físico)

---

## 5. Analytics

### 5.1 Resumen General

GET /api/v1/analytics/summary/

Query params opcionales:

- from (YYYY-MM-DD) — fecha de inicio del rango
- to   (YYYY-MM-DD) — fecha de fin del rango

Si no se envían parámetros, se devuelven métricas globales de todo el historial del usuario.

Ejemplos de uso:

- /api/v1/analytics/summary/                          → historial completo
- /api/v1/analytics/summary/?from=2025-04-07&to=2025-04-13 → rango filtrado

Response 200:

{
  "total_minutes": 1234,
  "total_hours": 20.56,
  "weekly_minutes": 300,
  "project_breakdown": [
    {
      "project_id": "uuid",
      "total_minutes": 500
    }
  ]
}

Nota: weekly_minutes refleja siempre la semana en curso (lunes a domingo),
independientemente del rango from/to.

---

## 6. Estructura de Errores

Los errores generales manejados explícitamente por la API seguirán este formato:

{
  "status": 400,
  "error": "Bad Request",
  "message": "Descripción clara del error"
}

Los errores de validación pueden devolverse asociados a campos o a `message`, por ejemplo:

{
  "project_id": "El proyecto no existe"
}

{
  "message": "La sesión se traslapa con otra sesión existente"
}
