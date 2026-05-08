# 05 – Estructura del Proyecto (Backend – Django)

## 1. Principios de Organización

- Monolito modular por dominio.
- Cada dominio vive en una app independiente.
- La lógica de negocio no debe estar concentrada en las views.
- El backend es la fuente de verdad.
- La arquitectura debe permitir crecimiento sin romper la base.

---

## 2. Estructura General del Backend

backend/
    manage.py
    config/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py

    apps/
        users/
        projects/
        sessions/
        analytics/

    common/
        exceptions/
        permissions/
        utils/

    requirements.txt