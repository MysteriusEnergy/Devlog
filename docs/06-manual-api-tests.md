# 06 - Pruebas Manuales de API

Esta guia sirve para probar manualmente la API con Postman o Insomnia.

Base local esperada:

```text
http://127.0.0.1:8000
```

## 1. Variables

Crea estas variables en Postman o Insomnia:

```text
base_url = http://127.0.0.1:8000/api/v1
access_token =
refresh_token =
project_id =
other_access_token =
other_project_id =
```

---

## 2. Auth - Register

```http
POST {{base_url}}/auth/register/
```

Body JSON:

```json
{
  "email": "test@example.com",
  "password": "testpass123"
}
```

Resultado esperado:

```http
201 Created
```

Respuesta esperada:

```json
{
  "id": "uuid",
  "email": "test@example.com",
  "created_at": "timestamp"
}
```

Validaciones:

- Debe crear el usuario.
- No debe devolver `password`.

Postman Tests opcional:

```javascript
pm.test("Status 201", () => {
  pm.response.to.have.status(201);
});

pm.test("No devuelve password", () => {
  const json = pm.response.json();
  pm.expect(json).to.not.have.property("password");
});
```

---

## 3. Auth - Register Sin Email

```http
POST {{base_url}}/auth/register/
```

Body JSON:

```json
{
  "password": "testpass123"
}
```

Resultado esperado:

```http
400 Bad Request
```

Validacion:

- Debe devolver error en `email`.

---

## 4. Auth - Register Email Duplicado

Ejecuta nuevamente el registro con el mismo email:

```http
POST {{base_url}}/auth/register/
```

Body JSON:

```json
{
  "email": "test@example.com",
  "password": "testpass123"
}
```

Resultado esperado:

```http
400 Bad Request
```

Validacion:

- No debe permitir dos usuarios con el mismo email.

---

## 5. Auth - Login Correcto

```http
POST {{base_url}}/auth/login/
```

Body JSON:

```json
{
  "email": "test@example.com",
  "password": "testpass123"
}
```

Resultado esperado:

```http
200 OK
```

Respuesta esperada:

```json
{
  "access_token": "jwt",
  "refresh_token": "jwt",
  "expires_in": 3600
}
```

Postman Tests para guardar tokens:

```javascript
const json = pm.response.json();

pm.environment.set("access_token", json.access_token);
pm.environment.set("refresh_token", json.refresh_token);

pm.test("Status 200", () => {
  pm.response.to.have.status(200);
});

pm.test("Devuelve tokens", () => {
  pm.expect(json).to.have.property("access_token");
  pm.expect(json).to.have.property("refresh_token");
  pm.expect(json).to.have.property("expires_in");
});
```

---

## 6. Auth - Login Con Password Incorrecto

```http
POST {{base_url}}/auth/login/
```

Body JSON:

```json
{
  "email": "test@example.com",
  "password": "wrongpass"
}
```

Resultado esperado:

```http
401 Unauthorized
```

Respuesta esperada:

```json
{
  "status": 401,
  "error": "Unauthorized",
  "message": "Credenciales invalidas"
}
```

---

## 7. Auth - Login Sin Password

```http
POST {{base_url}}/auth/login/
```

Body JSON:

```json
{
  "email": "test@example.com"
}
```

Resultado esperado:

```http
400 Bad Request
```

Respuesta esperada:

```json
{
  "status": 400,
  "error": "Bad Request",
  "message": "Email y password son obligatorios"
}
```

---

## 8. Auth - Refresh Token

```http
POST {{base_url}}/auth/refresh/
```

Body JSON:

```json
{
  "refresh_token": "{{refresh_token}}"
}
```

Resultado esperado:

```http
200 OK
```

Respuesta esperada:

```json
{
  "access_token": "jwt",
  "expires_in": 3600
}
```

Postman Tests opcional:

```javascript
const json = pm.response.json();

pm.environment.set("access_token", json.access_token);

pm.test("Status 200", () => {
  pm.response.to.have.status(200);
});

pm.test("Devuelve nuevo access token", () => {
  pm.expect(json).to.have.property("access_token");
  pm.expect(json).to.have.property("expires_in");
});
```

---

## 9. Auth - Refresh Sin Token

```http
POST {{base_url}}/auth/refresh/
```

Body JSON:

```json
{}
```

Resultado esperado:

```http
400 Bad Request
```

Respuesta esperada:

```json
{
  "status": 400,
  "error": "Bad Request",
  "message": "refresh_token es obligatorio"
}
```

---

## 10. Projects - Crear Proyecto

```http
POST {{base_url}}/projects/
```

Headers:

```http
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

Body JSON:

```json
{
  "name": "DevLog",
  "description": "Proyecto personal",
  "color": "#3B82F6"
}
```

Resultado esperado:

```http
201 Created
```

Respuesta esperada:

```json
{
  "id": "uuid",
  "name": "DevLog",
  "description": "Proyecto personal",
  "color": "#3B82F6",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

Postman Tests para guardar `project_id`:

```javascript
const json = pm.response.json();

pm.environment.set("project_id", json.id);

pm.test("Status 201", () => {
  pm.response.to.have.status(201);
});

pm.test("Proyecto creado", () => {
  pm.expect(json.name).to.eql("DevLog");
  pm.expect(json.color).to.eql("#3B82F6");
});
```

---

## 11. Projects - Crear Proyecto Sin Token

```http
POST {{base_url}}/projects/
```

Sin header `Authorization`.

Body JSON:

```json
{
  "name": "DevLog Sin Auth",
  "description": "No debe crearse",
  "color": "#3B82F6"
}
```

Resultado esperado:

```http
401 Unauthorized
```

---

## 12. Projects - Crear Proyecto Con Color Invalido

```http
POST {{base_url}}/projects/
```

Headers:

```http
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

Body JSON:

```json
{
  "name": "Proyecto Malo",
  "description": "Color invalido",
  "color": "azul"
}
```

Resultado esperado:

```http
400 Bad Request
```

Validacion:

- Debe devolver error en `color`.

Ejemplos invalidos:

```json
{
  "color": "azul"
}
```

```json
{
  "color": "#123"
}
```

```json
{
  "color": "3B82F6"
}
```

Ejemplo valido:

```json
{
  "color": "#3B82F6"
}
```

---

## 13. Projects - Listar Proyectos

```http
GET {{base_url}}/projects/
```

Headers:

```http
Authorization: Bearer {{access_token}}
```

Resultado esperado:

```http
200 OK
```

Respuesta esperada:

```json
[
  {
    "id": "uuid",
    "name": "DevLog",
    "description": "Proyecto personal",
    "color": "#3B82F6",
    "created_at": "timestamp",
    "updated_at": "timestamp"
  }
]
```

---

## 14. Projects - Obtener Detalle De Proyecto

```http
GET {{base_url}}/projects/{{project_id}}/
```

Headers:

```http
Authorization: Bearer {{access_token}}
```

Resultado esperado:

```http
200 OK
```

Respuesta esperada:

```json
{
  "id": "uuid",
  "name": "DevLog",
  "description": "Proyecto personal",
  "color": "#3B82F6",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

---

## 15. Projects - Actualizar Proyecto

```http
PATCH {{base_url}}/projects/{{project_id}}/
```

Headers:

```http
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

Body JSON:

```json
{
  "name": "DevLog Actualizado"
}
```

Resultado esperado:

```http
200 OK
```

Validacion:

- La respuesta debe devolver `name` con el valor `DevLog Actualizado`.

---

## 16. Projects - Actualizar Color Con Valor Valido

```http
PATCH {{base_url}}/projects/{{project_id}}/
```

Headers:

```http
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

Body JSON:

```json
{
  "color": "#EF4444"
}
```

Resultado esperado:

```http
200 OK
```

---

## 17. Projects - Actualizar Color Con Valor Invalido

```http
PATCH {{base_url}}/projects/{{project_id}}/
```

Headers:

```http
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

Body JSON:

```json
{
  "color": "rojo"
}
```

Resultado esperado:

```http
400 Bad Request
```

---

## 18. Seguridad - Crear Segundo Usuario

```http
POST {{base_url}}/auth/register/
```

Body JSON:

```json
{
  "email": "other@example.com",
  "password": "testpass123"
}
```

Resultado esperado:

```http
201 Created
```

---

## 19. Seguridad - Login Segundo Usuario

```http
POST {{base_url}}/auth/login/
```

Body JSON:

```json
{
  "email": "other@example.com",
  "password": "testpass123"
}
```

Resultado esperado:

```http
200 OK
```

Postman Tests para guardar `other_access_token`:

```javascript
const json = pm.response.json();

pm.environment.set("other_access_token", json.access_token);
```

---

## 20. Seguridad - Otro Usuario No Ve Tus Proyectos

```http
GET {{base_url}}/projects/
```

Headers:

```http
Authorization: Bearer {{other_access_token}}
```

Resultado esperado:

```http
200 OK
```

Respuesta esperada:

```json
[]
```

Tambien puede devolver una lista con solo proyectos del segundo usuario si ya creo alguno.

---

## 21. Seguridad - Otro Usuario No Puede Ver Tu Proyecto

```http
GET {{base_url}}/projects/{{project_id}}/
```

Headers:

```http
Authorization: Bearer {{other_access_token}}
```

Resultado esperado:

```http
404 Not Found
```

Esto es correcto porque el backend oculta recursos de otros usuarios.

---

## 22. Seguridad - Otro Usuario No Puede Editar Tu Proyecto

```http
PATCH {{base_url}}/projects/{{project_id}}/
```

Headers:

```http
Authorization: Bearer {{other_access_token}}
Content-Type: application/json
```

Body JSON:

```json
{
  "name": "Intento de hack"
}
```

Resultado esperado:

```http
404 Not Found
```

---

## 23. Seguridad - Otro Usuario No Puede Eliminar Tu Proyecto

```http
DELETE {{base_url}}/projects/{{project_id}}/
```

Headers:

```http
Authorization: Bearer {{other_access_token}}
```

Resultado esperado:

```http
404 Not Found
```

---

## 24. Projects - Eliminar Proyecto Propio

Usa nuevamente el token original:

```http
DELETE {{base_url}}/projects/{{project_id}}/
```

Headers:

```http
Authorization: Bearer {{access_token}}
```

Resultado esperado:

```http
204 No Content
```

Luego intenta obtenerlo:

```http
GET {{base_url}}/projects/{{project_id}}/
```

Headers:

```http
Authorization: Bearer {{access_token}}
```

Resultado esperado:

```http
404 Not Found
```

---

## 25. Auth - Logout

```http
POST {{base_url}}/auth/logout/
```

Body JSON:

```json
{
  "refresh_token": "{{refresh_token}}"
}
```

Resultado esperado:

```http
204 No Content
```

No necesita header `Authorization`.

---

## 26. Auth - Refresh Despues De Logout

```http
POST {{base_url}}/auth/refresh/
```

Body JSON:

```json
{
  "refresh_token": "{{refresh_token}}"
}
```

Resultado esperado:

```http
401 Unauthorized
```

Respuesta esperada:

```json
{
  "status": 401,
  "error": "Unauthorized",
  "message": "refresh_token invalido o expirado"
}
```

---

## 27. Orden Recomendado

1. Register.
2. Login.
3. Refresh.
4. Create Project.
5. List Projects.
6. Get Project Detail.
7. Update Project.
8. Invalid Color.
9. Create Second User.
10. Login Second User.
11. Confirm Second User Cannot See/Edit/Delete First User Project.
12. Delete Own Project.
13. Logout.
14. Refresh After Logout.

---

## 28. WorkSessions - Variables Adicionales

Agrega esta variable al environment:

```text
work_session_id =
```

---

## 29. WorkSessions - Crear Sesion

```http
POST {{base_url}}/work-sessions/
```

Headers:

```http
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

Body JSON:

```json
{
  "project_id": "{{project_id}}",
  "date": "2026-05-25",
  "start_time": "09:00",
  "end_time": "11:00",
  "notes": "Trabajo en backend"
}
```

Resultado esperado:

```http
201 Created
```

Validaciones:

- Debe devolver `duration_minutes` calculado en backend (`120`).
- Debe devolver `project_id`.

Postman Tests para guardar `work_session_id`:

```javascript
const json = pm.response.json();

pm.environment.set("work_session_id", json.id);

pm.test("Status 201", () => {
  pm.response.to.have.status(201);
});
```

---

## 30. WorkSessions - Crear Sesion Sin Token

```http
POST {{base_url}}/work-sessions/
```

Sin header `Authorization`.

Body JSON:

```json
{
  "project_id": "{{project_id}}",
  "date": "2026-05-25",
  "start_time": "09:00",
  "end_time": "11:00"
}
```

Resultado esperado:

```http
401 Unauthorized
```

---

## 31. WorkSessions - Crear Con Proyecto Ajeno

Usa `other_access_token` y el `project_id` del primer usuario:

```http
POST {{base_url}}/work-sessions/
```

Headers:

```http
Authorization: Bearer {{other_access_token}}
Content-Type: application/json
```

Body JSON:

```json
{
  "project_id": "{{project_id}}",
  "date": "2026-05-25",
  "start_time": "09:00",
  "end_time": "11:00"
}
```

Resultado esperado:

```http
400 Bad Request
```

Validacion:

- Debe devolver error en `project_id`.

---

## 32. WorkSessions - Crear Con Horario Invalido

```http
POST {{base_url}}/work-sessions/
```

Headers:

```http
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

Body JSON:

```json
{
  "project_id": "{{project_id}}",
  "date": "2026-05-25",
  "start_time": "12:00",
  "end_time": "10:00"
}
```

Resultado esperado:

```http
400 Bad Request
```

---

## 33. WorkSessions - Crear Sesion Traslapada

Primero crea una sesion valida de `09:00` a `11:00`.
Luego intenta crear esta:

```http
POST {{base_url}}/work-sessions/
```

Headers:

```http
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

Body JSON:

```json
{
  "project_id": "{{project_id}}",
  "date": "2026-05-25",
  "start_time": "10:00",
  "end_time": "12:00",
  "notes": "Traslape"
}
```

Resultado esperado:

```http
400 Bad Request
```

---

## 34. WorkSessions - Listar Sesiones

```http
GET {{base_url}}/work-sessions/
```

Headers:

```http
Authorization: Bearer {{access_token}}
```

Resultado esperado:

```http
200 OK
```

Validacion:

- Debe devolver solo sesiones del usuario autenticado.

---

## 35. WorkSessions - Obtener Detalle

```http
GET {{base_url}}/work-sessions/{{work_session_id}}/
```

Headers:

```http
Authorization: Bearer {{access_token}}
```

Resultado esperado:

```http
200 OK
```

---

## 36. WorkSessions - Actualizar Notes

```http
PATCH {{base_url}}/work-sessions/{{work_session_id}}/
```

Headers:

```http
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

Body JSON:

```json
{
  "notes": "Nota actualizada"
}
```

Resultado esperado:

```http
200 OK
```

---

## 37. WorkSessions - Recalcular Duracion En Update

```http
PATCH {{base_url}}/work-sessions/{{work_session_id}}/
```

Headers:

```http
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

Body JSON:

```json
{
  "start_time": "09:00",
  "end_time": "12:30"
}
```

Resultado esperado:

```http
200 OK
```

Validacion:

- Debe devolver `duration_minutes: 210`.

---

## 38. WorkSessions - Intentar Editar date

```http
PATCH {{base_url}}/work-sessions/{{work_session_id}}/
```

Headers:

```http
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

Body JSON:

```json
{
  "date": "2026-05-26"
}
```

Resultado esperado:

```http
400 Bad Request
```

---

## 39. WorkSessions - Intentar Editar project_id

```http
PATCH {{base_url}}/work-sessions/{{work_session_id}}/
```

Headers:

```http
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

Body JSON:

```json
{
  "project_id": "{{other_project_id}}"
}
```

Resultado esperado:

```http
400 Bad Request
```

---

## 40. WorkSessions - Otro Usuario No Puede Ver Sesion Ajena

```http
GET {{base_url}}/work-sessions/{{work_session_id}}/
```

Headers:

```http
Authorization: Bearer {{other_access_token}}
```

Resultado esperado:

```http
404 Not Found
```

---

## 41. WorkSessions - Otro Usuario No Puede Editar Sesion Ajena

```http
PATCH {{base_url}}/work-sessions/{{work_session_id}}/
```

Headers:

```http
Authorization: Bearer {{other_access_token}}
Content-Type: application/json
```

Body JSON:

```json
{
  "notes": "Intento de hack"
}
```

Resultado esperado:

```http
404 Not Found
```

---

## 42. WorkSessions - Eliminar Sesion Propia

```http
DELETE {{base_url}}/work-sessions/{{work_session_id}}/
```

Headers:

```http
Authorization: Bearer {{access_token}}
```

Resultado esperado:

```http
204 No Content
```

Luego valida que ya no exista:

```http
GET {{base_url}}/work-sessions/{{work_session_id}}/
```

Headers:

```http
Authorization: Bearer {{access_token}}
```

Resultado esperado:

```http
404 Not Found
```

---

## 43. WorkSessions - Listado Paginado (Formato)

```http
GET {{base_url}}/work-sessions/?page=1&per_page=2
```

Headers:

```http
Authorization: Bearer {{access_token}}
```

Resultado esperado:

```http
200 OK
```

Respuesta esperada (estructura):

```json
{
  "data": [
    {
      "id": "uuid",
      "project_id": "uuid",
      "date": "2026-05-25",
      "start_time": "09:00:00",
      "end_time": "11:00:00",
      "duration_minutes": 120,
      "notes": "Trabajo en backend",
      "created_at": "timestamp",
      "updated_at": "timestamp"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 2,
    "total": 10,
    "total_pages": 5
  }
}
```

---

## 44. WorkSessions - Filtrar Por project_id

```http
GET {{base_url}}/work-sessions/?project_id={{project_id}}
```

Headers:

```http
Authorization: Bearer {{access_token}}
```

Resultado esperado:

```http
200 OK
```

Validacion:

- Todas las sesiones devueltas deben pertenecer a ese `project_id`.

---

## 45. WorkSessions - Filtrar Por date

```http
GET {{base_url}}/work-sessions/?date=2026-05-25
```

Headers:

```http
Authorization: Bearer {{access_token}}
```

Resultado esperado:

```http
200 OK
```

Validacion:

- Todas las sesiones devueltas deben tener esa fecha.

---

## 46. WorkSessions - Filtrar Por Rango (from/to)

```http
GET {{base_url}}/work-sessions/?from=2026-05-01&to=2026-05-31
```

Headers:

```http
Authorization: Bearer {{access_token}}
```

Resultado esperado:

```http
200 OK
```

Validacion:

- Todas las sesiones deben estar dentro del rango `from` y `to`.

---

## 47. WorkSessions - Paginacion Invalida page

```http
GET {{base_url}}/work-sessions/?page=0
```

Headers:

```http
Authorization: Bearer {{access_token}}
```

Resultado esperado:

```http
400 Bad Request
```

---

## 48. WorkSessions - Paginacion Invalida per_page

```http
GET {{base_url}}/work-sessions/?per_page=0
```

Headers:

```http
Authorization: Bearer {{access_token}}
```

Resultado esperado:

```http
400 Bad Request
```

---

## 49. Analytics - Summary Sin Token

```http
GET {{base_url}}/analytics/summary/
```

Sin header `Authorization`.

Resultado esperado:

```http
401 Unauthorized
```

---

## 50. Analytics - Summary General

```http
GET {{base_url}}/analytics/summary/
```

Headers:

```http
Authorization: Bearer {{access_token}}
```

Resultado esperado:

```http
200 OK
```

Respuesta esperada (estructura):

```json
{
  "total_minutes": 330,
  "total_hours": 5.5,
  "weekly_minutes": 120,
  "project_breakdown": [
    {
      "project_id": "uuid",
      "total_minutes": 330
    }
  ]
}
```

Validaciones:

- `total_minutes` debe sumar todas las sesiones del usuario autenticado.
- `total_hours` debe ser `total_minutes / 60`.
- `weekly_minutes` debe sumar solo sesiones de la semana actual.
- `project_breakdown` debe agrupar minutos por proyecto.
- No debe incluir sesiones de otros usuarios.

Postman Tests opcional:

```javascript
const json = pm.response.json();

pm.test("Status 200", () => {
  pm.response.to.have.status(200);
});

pm.test("Tiene estructura esperada", () => {
  pm.expect(json).to.have.property("total_minutes");
  pm.expect(json).to.have.property("total_hours");
  pm.expect(json).to.have.property("weekly_minutes");
  pm.expect(json).to.have.property("project_breakdown");
});

pm.test("project_breakdown es array", () => {
  pm.expect(json.project_breakdown).to.be.an("array");
});
```

---

## 51. Analytics - Summary Con Rango

```http
GET {{base_url}}/analytics/summary/?from=2026-05-01&to=2026-05-31
```

Headers:

```http
Authorization: Bearer {{access_token}}
```

Resultado esperado:

```http
200 OK
```

Validaciones:

- `total_minutes` debe sumar solo sesiones entre `2026-05-01` y `2026-05-31`.
- `project_breakdown` debe usar el mismo rango.
- `weekly_minutes` debe ignorar ese rango y seguir calculando la semana actual.

---

## 52. Analytics - Summary Solo Desde Fecha

```http
GET {{base_url}}/analytics/summary/?from=2026-05-01
```

Headers:

```http
Authorization: Bearer {{access_token}}
```

Resultado esperado:

```http
200 OK
```

Validacion:

- Debe incluir sesiones desde `2026-05-01` en adelante.

---

## 53. Analytics - Summary Solo Hasta Fecha

```http
GET {{base_url}}/analytics/summary/?to=2026-05-31
```

Headers:

```http
Authorization: Bearer {{access_token}}
```

Resultado esperado:

```http
200 OK
```

Validacion:

- Debe incluir sesiones hasta `2026-05-31`.

---

## 54. Analytics - Usuario Sin Sesiones

Haz login con un usuario nuevo que no tenga proyectos ni sesiones.

```http
GET {{base_url}}/analytics/summary/
```

Headers:

```http
Authorization: Bearer {{access_token}}
```

Resultado esperado:

```http
200 OK
```

Respuesta esperada:

```json
{
  "total_minutes": 0,
  "total_hours": 0.0,
  "weekly_minutes": 0,
  "project_breakdown": []
}
```

---

## 55. Analytics - Aislamiento Entre Usuarios

Con el usuario A crea proyectos y sesiones.
Luego inicia sesion con usuario B y ejecuta:

```http
GET {{base_url}}/analytics/summary/
```

Headers:

```http
Authorization: Bearer {{other_access_token}}
```

Resultado esperado:

```http
200 OK
```

Validaciones:

- No debe incluir sesiones del usuario A.
- Si usuario B no tiene sesiones, debe devolver totales en `0`.

---

## 56. Analytics - Orden Recomendado

1. Crea algunas `work-sessions` con el usuario principal.
2. Ejecuta `Summary General`.
3. Ejecuta `Summary Con Rango`.
4. Ejecuta `Summary Solo Desde Fecha`.
5. Ejecuta `Summary Solo Hasta Fecha`.
6. Prueba `Summary Sin Token`.
7. Prueba un usuario sin sesiones.
8. Prueba usuario distinto para validar aislamiento.

Tambien prueba:

```http
GET {{base_url}}/work-sessions/?per_page=101
```

Resultado esperado:

```http
400 Bad Request
```
