# API reference

The running FastAPI service generates the detailed, current schemas and endpoint descriptions:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

These routes are available when running `backend/main.py`. The API uses JSON requests and responses except where an endpoint accepts an uploaded avatar file. Protected operations use a JWT access token in `Authorization: Bearer <token>`.

## Route groups

| Prefix | Functionality |
| --- | --- |
| `/auth` | Register with email/mobile, log in, use optional Google/GitHub sign-in, request/confirm password reset, read the authenticated user, and change password |
| `/users` | Profile read/update and avatar upload |
| `/vehicles` | Create, list, update, and delete vehicles |
| `/rides` | Create, list/search, update, and manage ride lifecycle; includes QR-token generation and verification endpoints |
| `/bookings` | Request a booking, list passenger/ride bookings, confirm, cancel, and waitlist operations |
| `/ratings` | Create/read/update/delete ratings and find rating candidates |
| `/notifications` | Read and update the current user's in-app notifications |
| `/sos` | Create and view the current user's safety event records |
| `/admin` | Admin-only management, reports, and SOS triage |
| `/payments` | Participant/admin reads, driver/passenger history, earnings, and admin status tracking |

The health endpoint is `GET /health`; it confirms the API process responds, not that PostgreSQL is reachable. Registration requires a valid 10-digit Indian mobile number and accepts driver and passenger roles. Administrative routes require an already provisioned admin account; public registration does not create one. Password reset requires SMTP configuration; reset requests return a generic response for unknown accounts. Social sign-in is optional and requires provider credentials and an existing account with a matching verified email.

Password reset endpoints:

- `POST /auth/password-reset/request` with `{ "email": "..." }` sends a one-time link when SMTP is configured.
- `POST /auth/password-reset/confirm` with `{ "token": "...", "new_password": "..." }` consumes the token once before it expires.

For implementation details, see `backend/app/api/routes` and the relevant service and schema modules. This summary intentionally does not duplicate the generated OpenAPI endpoint list.
