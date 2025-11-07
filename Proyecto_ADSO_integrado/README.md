Proyecto ADSO integrado
=======================

Contenido:
- django_project/: Proyecto Django 4.2 con DRF listo para PostgreSQL.
- laravel_project/: Estructura con migrations, controllers, services y tests (snippets).
- sql/: Triggers y procedures SQL (PostgreSQL) para integridad.

Postgres: esta integración está preparada para PostgreSQL. Ajusta variables de entorno:
POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, DJANGO_SECRET_KEY

Archivos creados: django_project, sql


---
## Cómo ejecutar (opciones)

### 1) Rápido en local con SQLite (útil para tests)
- Exportar variable para usar sqlite (opcional)
  export DJANGO_USE_SQLITE=True
- Crear virtualenv, instalar dependencias:
  pip install -r requirements.txt
- Ejecutar migrations y levantar server:
  python django_project/manage.py migrate
  python django_project/manage.py runserver

### 2) Usando Docker Compose (Postgres)
- docker compose up --build
- Las variables de Postgres están en docker-compose.yml (user: adso_user, pass: adso_pass)
- Luego ejecutar migraciones dentro del contenedor django:
  docker compose exec django python manage.py migrate

