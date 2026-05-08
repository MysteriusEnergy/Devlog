# DevLog – Visión del Proyecto

## 1. Propósito

DevLog es una aplicación web diseñada para permitir a desarrolladores y freelancers registrar, organizar y analizar su tiempo de trabajo en proyectos personales o profesionales.

El objetivo principal es construir una aplicación moderna con arquitectura desacoplada que sirva como base sólida para crecimiento técnico y futura escalabilidad.

Este proyecto no nace con enfoque comercial inmediato, sino como ejercicio de arquitectura profesional, buenas prácticas y disciplina de desarrollo.

---

## 2. Problema que Resuelve

Muchos desarrolladores trabajan en múltiples proyectos y no tienen:

- Registro estructurado de sesiones de trabajo
- Métricas claras de productividad
- Visualización consolidada de horas invertidas
- Organización por proyecto

DevLog busca resolver ese problema mediante un sistema simple pero bien diseñado.

---

## 3. Objetivos del Proyecto

### Objetivos Técnicos

- Construir una arquitectura desacoplada (Frontend + Backend separados).
- Implementar API REST versionada.
- Centralizar lógica de negocio en el backend.
- Aplicar estructura modular por dominio.
- Documentar decisiones técnicas desde el inicio.
- Preparar base escalable para futuro crecimiento.

### Objetivos Personales

- Mejorar criterio arquitectónico.
- Practicar desarrollo SPA moderno. (Single Page Application)
- Construir disciplina de finalizar proyectos.
- Mantener repositorio profesional en GitHub.

---

## 4. Alcance del MVP (Producto Mínimo Viable)

El MVP incluirá únicamente:

- Registro y autenticación de usuario.
- CRUD de proyectos.
- Registro de sesiones de trabajo.
- Cálculo automático de duración.
- Dashboard con métricas
- Total de horas por proyecto.
- Total de horas semanales.
- Visualización básica de métricas.

El MVP no incluirá funcionalidades avanzadas como exportaciones, facturación, planes premium o integraciones externas.

---

## 5. No Alcance (Fuera del MVP)

Para evitar sobreingeniería, el proyecto NO incluirá en su primera versión:

- Sistema de pagos.
- Roles avanzados de usuario.
- Integraciones con terceros.
- Exportación a PDF o Excel.
- Notificaciones.
- Aplicación móvil.

Estas funcionalidades podrán evaluarse en futuras versiones.

---

## 6. Principios Técnicos

1. El backend es la fuente de verdad.
2. Toda lógica de negocio vive en el backend.
3. El frontend es responsable únicamente de UI y consumo de API.
4. Arquitectura modular por dominio.
5. Versionado de API desde el inicio (`/api/v1/`).
6. Uso de variables de entorno para configuración.
7. Código claro antes que código complejo.
8. Escalabilidad estructural sin sobreingeniería.

---

## 7. Arquitectura General

El sistema estará compuesto por:

### Backend
- Django
- Django REST Framework
- Autenticación JWT
- PostgreSQL
- Monolito modular por dominio (código base unificado)

### Frontend
- SvelteKit
- TypeScript
- Arquitectura SPA moderna
- Comunicación vía API REST

Ambos sistemas estarán desacoplados y podrán evolucionar de manera independiente.

---

## 8. Filosofía del Desarrollo

- 1 feature completa antes de empezar otra.
- Priorizar funcionalidad sobre perfección estética.
- Documentar decisiones importantes.
- Mantener commits claros y descriptivos.
- Evitar agregar nuevas tecnologías sin justificación real.