# Backend development

The backend is a FastAPI application using SQLAlchemy, PostgreSQL, Pydantic, and Alembic. The root [README](../README.md) is the primary setup guide.

## Local setup

From this directory, create a virtual environment, activate it, and install dependencies:

```sh
python -m venv .venv
python -m pip install -r requirements.txt
```

Create `.env` from `.env.example`. For a backend process running on the host with the Compose database, set the database host to `localhost`; the Compose service hostname `postgres` is only resolvable from containers. Set a generated local `SECRET_KEY` and use a dedicated development database.

```sh
python -m alembic upgrade head
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Interactive API docs are available at `/docs`; the basic process health endpoint is `/health` and does not check the database.

## Google and GitHub sign-in

Social sign-in is optional and disabled until credentials are set in `backend/.env`. Create web OAuth clients with these exact callback URLs:

- Google: `http://127.0.0.1:8000/auth/oauth/google/callback`
- GitHub: `http://127.0.0.1:8000/auth/oauth/github/callback`

Set `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, `GITHUB_OAUTH_CLIENT_ID`, and `GITHUB_OAUTH_CLIENT_SECRET`. Keep both secrets only in the ignored local `.env`; never put them in Vite variables. Set `BACKEND_PUBLIC_URL` and `FRONTEND_URL` to the correct URLs for the environment, and use HTTPS outside local development. A first social sign-in creates a passenger account from the provider's verified email and available profile details; existing accounts are linked only by matching verified email. Phone numbers are not reliably provided by either provider, so social sign-up leaves the phone blank for the user to add later. Google requests basic OpenID/email/profile claims. GitHub requests only `read:user` and `user:email` so it can find a verified primary email. No provider identity service or SMS verification is included.

After configuring a provider, apply the additive OAuth identity migration with `python -m alembic upgrade head` against the intended development database before starting the app.

## Password reset email

Password reset uses ordinary SMTP through an account you already have; the code adds no email provider or paid service. Add `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, and `SMTP_FROM_EMAIL` to the ignored `backend/.env` file. `SMTP_STARTTLS=True` is the default for STARTTLS submission; set `SMTP_USE_SSL=True` only if your provider requires implicit TLS (commonly port 465). Use the TLS mode and credentials specified by your existing provider; never commit credentials. The included Compose configuration loads `backend/.env.example` first and then overrides it with `backend/.env` when present. The API does not send SMS and does not claim to verify mobile-number ownership.

Reset tokens are random, stored only as SHA-256 digests, expire after the configured interval, are accepted once, and are rate-limited to one email per account per minute. The reset request response does not disclose whether an email has a CommuteShare account. Apply the password-reset Alembic migration with `python -m alembic upgrade head` before enabling the flow.

## Checks

```sh
python -m pytest -q
python -m ruff check app tests
python -m alembic heads
```

The PostgreSQL concurrency test requires `COMMUTESHARE_TEST_POSTGRES_URL` to point to an isolated test database. The test creates and drops tables; never use an application or production database for it.

See [Architecture](../docs/ARCHITECTURE.md), [Database schema](../docs/DATABASE_SCHEMA.md), [API reference](../docs/API_REFERENCE.md), and [Security](../docs/SECURITY.md).
