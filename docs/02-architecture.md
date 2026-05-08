# 02 – Arquitectura del Sistema

## 1. Visión General

DevLog estará compuesto por dos sistemas independientes:

- Backend (API REST)
- Frontend (SPA)

Ambos se comunican exclusivamente mediante HTTP usando JSON.

El backend será la única fuente de verdad.
El frontend será un consumidor de la API.

---

## 2. Arquitectura General

[ Usuario ]
      ↓
[ Frontend – SvelteKit ]
      ↓ HTTP (JSON)
[ Backend – Django REST ]
      ↓
[ PostgreSQL ]

---

## 3. Backend

### 3.1 Tipo de Arquitectura

- Monolito modular
- Separado por dominios (apps)
- API versionada (`/api/v1/`)

### 3.2 Estructura Interna

backend/
    config/
    apps/
        users/
        projects/
        sessions/
        analytics/

Cada dominio tendrá:
- models.py
- serializers.py
- views.py
- urls.py
- services/ (si requiere lógica de negocio)

### 3.3 Responsabilidades del Backend

- Autenticación y autorización
- Validaciones de datos
- Lógica de negocio
- Cálculos (duración de sesiones, métricas)
- Persistencia
- Seguridad

El backend nunca renderiza HTML.

---

## 4. Frontend

### 4.1 Tipo de Arquitectura

- SPA moderna
- SvelteKit
- TypeScript
- Consumo de API REST

### 4.2 Estructura Interna

frontend/
    src/
        routes/
        lib/
            components/
            stores/
            services/
            types/

### 4.3 Responsabilidades del Frontend

- Interfaz de usuario
- Manejo de estado
- Protección de rutas
- Consumo de API
- Manejo de errores visuales

El frontend no contiene lógica de negocio crítica.

---

## 5. Comunicación Frontend ↔ Backend

- Formato: JSON
- Autenticación: JWT
- Header:
  Authorization: Bearer <token>

Flujo general:

1. Usuario inicia sesión.
2. Backend devuelve access_token y refresh_token.
3. Frontend guarda token (estrategia segura).
4. Cada request incluye token en headers.
5. Backend valida y responde.

---

## 6. Flujo Principal: Registro de Sesión

1. Usuario envía:
   - project_id
   - start_time
   - end_time
   - notes

2. Backend:
   - Valida que el proyecto pertenezca al usuario.
   - Calcula duración.
   - Verifica que no haya traslape.
   - Guarda sesión.
   - Devuelve resultado.

El frontend solo muestra el resultado.

---

## 7. Escalabilidad Futura

La arquitectura permite:

- Agregar plan premium.
- Agregar facturación.
- Crear aplicación móvil.
- Separar microservicios si fuera necesario.
- Exponer API pública.

Sin reescribir la base del sistema.