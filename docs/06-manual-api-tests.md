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
