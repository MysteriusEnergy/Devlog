# 03 – Modelo de Datos

## 1. Principios del Modelo

- Cada dato pertenece a un usuario.
- No existen entidades globales sin propietario.
- Las relaciones son explícitas.
- Las reglas críticas se validan en backend.
- El modelo debe permitir futura monetización sin rediseño.
- Se utilizarán UUID como identificadores primarios para permitir futura escalabilidad, seguridad en exposición de API y consistencia en sistemas distribuidos.
- Todas las entidades persistidas incluirán:
  - id (UUID)
  - created_at
  - updated_at
- El sistema utilizará borrado físico (hard delete).
- No se implementará soft delete en esta versión.

---

## 2. Entidades Principales

### 2.1 User

Representa al usuario del sistema.

Campos:

- id (UUID)
- email (único)
- password (hash)
- created_at
- updated_at

Consideraciones:

- Se utilizará autenticación JWT.
- El email será el identificador principal.
- En el futuro podría agregarse el campo `plan`.

---

### 2.2 Project

Representa un proyecto creado por un usuario.

Campos:

- id (UUID)
- user_id (UUID, FK → User)
- name
- description (opcional)
- color (string corta)
- created_at
- updated_at

Reglas:

- Un proyecto pertenece a un único usuario.
- Un usuario puede tener múltiples proyectos.
- No puede existir un proyecto sin usuario.

Relación:

User (1) → (N) Project

---

### 2.3 WorkSession

Representa una sesión de trabajo registrada.

Campos:

- id (UUID)
- user_id (UUID, FK → User)
- project_id (UUID, FK → Project)
- date
- start_time
- end_time
- duration_minutes (calculado y definido exclusivamente en backend)
- notes (opcional)
- created_at
- updated_at

Reglas de negocio:

- La sesión debe pertenecer al mismo usuario dueño del proyecto.
- start_time < end_time.
- No puede existir traslape de sesiones para el mismo usuario.
- duration_minutes es calculado únicamente en backend.
- duration_minutes no es editable después de su creación.

Relaciones:

User (1) → (N) WorkSession  
Project (1) → (N) WorkSession

---

## 3. Entidad Derivada (No Persistida)

### 3.1 Analytics

No será una tabla.  
Se calculará dinámicamente en backend mediante consultas agregadas.

Ejemplos de métricas:

- Total horas por proyecto.
- Total horas por semana.
- Total horas globales.
- Promedio de horas por día.

---

## 4. Índices Recomendados

Para optimización futura:

- Índice en user_id (Project)
- Índice compuesto en (user_id, date) para WorkSession
- Índice en project_id (WorkSession)

Esto permitirá escalar consultas de dashboard sin rediseñar el modelo.

---

## 5. Preparación para Escalabilidad Futura

El modelo permite:

- Agregar planes de usuario.
- Agregar límites por plan.
- Agregar facturación.
- Agregar roles.
- Agregar equipos (team_id futuro).

Sin rediseñar las tablas principales.