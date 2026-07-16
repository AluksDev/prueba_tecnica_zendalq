# Mini Gestor de Incidencias

Aplicación mínima de gestión de incidencias (tickets) construida con Django REST Framework (backend) y Nuxt 4 (frontend), contenerizada con Docker.

## Stack

- **Backend:** Django 6 + Django REST Framework, Poetry, SQLite
- **Frontend:** Nuxt 4, Vue 3, pnpm
- **Infra:** Docker Compose

## Arranque rápido

```bash
docker compose up
```

Esto levanta ambos servicios. No debería hacer falta ningún paso adicional.

| Servicio  | URL                                |
|-----------|------------------------------------|
| Frontend  | http://localhost:3000               |
| Backend   | http://localhost:8000/api/tickets/  |

## Estructura del proyecto

```
.
├── backend/
│   ├── config/           # Settings, URLs, WSGI/ASGI
│   ├── tickets/          # App principal: models, views, serializer, tests
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/
│   ├── app/
│   │   ├── components/   # TicketList, TicketItem, TicketForm, TicketFilters, TicketStats, ToastContainer
│   │   ├── composables/  # useApi, useTickets, useToast
│   │   ├── helpers/      # statusLabels, statusColors, priorityLabels
│   │   ├── models/       # Interfaces TypeScript (Ticket, TicketCreate, TicketStats)
│   │   └── pages/        # index.vue (única vista)
│   ├── pnpm-lock.yaml
│   └── Dockerfile
└── docker-compose.yml
```

## Endpoints de la API

| Método | Endpoint                | Descripción |
|--------|-------------------------|-------------|
| GET    | `/api/tickets/`         | Listado de tickets. Admite filtros `?status=` y `?priority=`. Ordenado por `created_at` descendente. |
| POST   | `/api/tickets/`         | Creación de ticket. No puede crearse directamente con `status=closed`. |
| PATCH  | `/api/tickets/<id>/`    | Actualización parcial. La transición `closed → open` se rechaza; debe pasar por `in_progress`. |
| GET    | `/api/tickets/stats/`   | Recuento de tickets agrupado por status. |

## Decisiones técnicas

**Backend:**

- **`TextChoices` para choice fields.** Garantiza valores válidos y permite referenciarlos como constantes (`Ticket.Status.OPEN`) en lugar de strings mágicos, mejorando legibilidad y mantenibilidad.
- **Campos explícitos en el serializer** en vez de `__all__`. Control total sobre qué expone la API; `id` y `created_at` marcados como `read_only`.
- **Separación `validate_status()` / `validate()`.** El primero valida el valor del campo individual; el segundo valida reglas que dependen del estado actual del objeto (transiciones de status).
- **`GenericViewSet` con mixins mínimos** en vez de `ModelViewSet`. Solo se exponen los métodos que el contrato de la API necesita (GET, POST, PATCH), evitando endpoints innecesarios.
- **Autenticación deshabilitada** intencionalmente para esta prueba. En producción sería imprescindible implementar auth y permisos.

**Frontend:**

- **Composable `useApi`** centraliza todas las llamadas a la API, manejo de errores y permite añadir interceptores en el futuro sin tocar cada componente.
- **Interfaces TypeScript en `models/`.** Tipado fuerte, reutilizable entre composables, componentes y páginas.
- **Proxy de Vite** para redirigir `/api` al backend. Evita CORS en desarrollo y refleja la arquitectura real (reverse proxy en producción). Configurable via `NUXT_API_PROXY_TARGET` para funcionar en local y en Docker.
- **Mapa de transiciones en el frontend** que refleja las reglas de negocio del backend. Reduce llamadas innecesarias a la API, aunque el backend siempre valida.
- **Helpers compartidos** (`helpers/ticket.ts`) para labels y colores, evitando duplicación entre componentes.

**Docker:**

- **`ALLOWED_HOSTS = ["*"]`** para permitir conexiones desde el contenedor. Suficiente para esta prueba; en producción se acotaría al dominio real.
- **Variable de entorno `NUXT_API_PROXY_TARGET`** en el docker-compose permite que el proxy apunte a `backend:8000` (red Docker) en contenedor, y a `localhost:8000` en desarrollo local, sin duplicar configuración.

## Cómo ejecutar los tests

```bash
docker compose exec backend python manage.py test tickets
```

**Qué se cubre y por qué:**

- `TicketCreateValidationTest` — verifica que no se pueda crear un ticket con `status=closed`. Cubre la regla de negocio que impide estados iniciales inválidos.
- `TicketTransitionValidationTest` — verifica que un ticket `closed` no pueda volver a `open` directamente, y que sí pueda pasar a `in_progress`. Cubre la transición de estados permitida.
- `TicketStatsTest` — verifica que el endpoint `/api/tickets/stats/` devuelve los conteos correctos por status. Cubre la funcionalidad de consulta.

## Qué dejaría para una segunda iteración

- Autenticación y permisos (ahora deshabilitados intencionalmente)
- Paginación en el listado de tickets
- PostgreSQL como base de datos en Docker (SQLite es suficiente para el alcance de esta prueba)
- Tests e2e (Playwright o similar)
- Pipeline de CI con linting y tests automáticos

## Notas

- La autenticación y CSRF están deshabilitadas en la API para simplificar el desarrollo y testing de esta prueba. En producción sería imprescindible implementarlas.
- Se usa `docker compose up` como único comando de arranque, incluyendo `migrate` automático al iniciar el contenedor del backend.
- El frontend usa un proxy de Vite para redirigir `/api` al backend, configurado via variable de entorno `NUXT_API_PROXY_TARGET` para que funcione tanto en local como en Docker.
