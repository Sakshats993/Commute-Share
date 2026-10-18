# Local run and deployment status

## Supported local development setup

The repository provides Docker Compose for local development. From the repository root:

```sh
docker compose up --build
docker compose exec backend alembic upgrade head
```

The stack includes PostgreSQL 16, FastAPI, and Vite. It binds host ports 5432, 8000, and 5173 to loopback. The PostgreSQL named volume persists data after `docker compose down`. Do not remove that volume unless you intend to delete the local database.

The Compose backend uses `backend/.env.example`, which contains development-only credentials and a placeholder JWT key. Migrations are not automatically applied at startup. Review [the root setup guide](../README.md) before running components separately.

## Production status

No AWS infrastructure definitions, deployment workflow, or production topology are present in the repository. The local Compose stack is not a production deployment recipe. Before a deployment is planned, determine and review the operating costs and configure, at minimum, production secrets, TLS, database network access, migrations, persistent avatar storage, backups/restore, health monitoring, logging, and recovery procedures. No cloud resources have been created by this project documentation.

Do not use the sample credentials or run migrations against a production database without a separately reviewed and approved deployment plan.
