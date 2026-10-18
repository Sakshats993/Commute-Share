# Architecture

## Runtime request flow

```text
React pages and components
        │
        ├── hooks and AuthContext manage client state
        └── Axios API modules add the bearer access token
                    │ HTTP/JSON
                    ▼
             FastAPI route modules
        schemas validate input and output
        dependencies load DB sessions and enforce roles
                    │
                    ▼
              service modules
        business rules and transactions
                    │ SQLAlchemy
                    ▼
            PostgreSQL database
        schema changes are applied by Alembic
```

The frontend code is in `frontend/src`. HTTP endpoints are registered from `backend/app/api/routes`; request and response schemas are in `backend/app/schemas`; authorization dependencies and settings are in `backend/app/core`; persistence models live in `backend/app/models`; service logic is in `backend/app/services`.

The FastAPI application is created in `backend/main.py`. It registers the route groups, CORS middleware, a static `/uploads` mount for profile images, `/health`, and the root route. FastAPI's generated OpenAPI interfaces are available at `/docs` and `/redoc` when the API is running.

Database sessions are created per request by `app.core.deps.get_db`. Alembic reads the same `DATABASE_URL` setting used by the application. Application startup does not automatically run migrations.

## Local services

`docker-compose.yml` defines PostgreSQL 16, the FastAPI backend, and the Vite development server. Its host ports bind to loopback. Compose waits for PostgreSQL health before starting the backend, but schema migration still requires `alembic upgrade head`.

## Important boundaries

- Authorization is enforced by backend dependencies and service ownership checks; frontend guards are not security boundaries.
- Payment records represent internal tracking, not payment processing.
- SOS records and admin notifications remain inside the application; they do not dispatch emergency services.
- The frontend map uses Leaflet and a tile server. It draws a straight line between supplied coordinates; there is no routing or geocoding service.
- No production AWS topology or deployment automation is defined in the repository.
