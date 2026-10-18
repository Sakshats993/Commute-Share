# Database schema

SQLAlchemy models are in `backend/app/models`; Alembic revisions are in `backend/alembic/versions`. The current Alembic head is `6f8379b0c75a`. Use migrations rather than `Base.metadata.create_all()` to evolve application databases.

## Main tables and relationships

| Table | Purpose and relationships |
| --- | --- |
| `users` | Accounts, role, profile, and reputation fields. A user may own vehicles, drive rides, make bookings, and receive notifications. |
| `vehicles` | Vehicles belong to an owner/user and may be attached to rides. Registration number is unique. |
| `rides` | Driver, vehicle, route coordinates, schedule, seats, fare, and lifecycle status. A ride has bookings, waitlist entries, ratings, SOS records, and payment records. |
| `bookings` | Connects a passenger to a ride and stores booking/boarding state. A passenger can have at most one booking row per ride; cancellation and waitlist promotion can reuse that row. |
| `waitlists` | Ordered passenger queue for a ride. Database constraints prevent duplicate passenger/ride entries. |
| `ratings` | Ride-related reviewer and recipient feedback. |
| `notifications` | In-app messages associated with users. |
| `sos_events` | Safety records associated with a user and optionally a ride. |
| `payments` | Internal payment status records associated with a booking and ride; one payment record per booking. No payment processor is connected. |
| `audit_logs` | Records selected actions and the associated actor/resource description. |

Foreign keys and uniqueness constraints are defined by the ORM models and migrations. Consult those files for exact column types, nullability, indexes, and cascade behavior; this overview is not a generated ER diagram.

## Migration workflow

Run from `backend/` with `DATABASE_URL` configured:

```sh
python -m alembic current
python -m alembic heads
python -m alembic upgrade head
```

Generate and review a candidate revision after a model change:

```sh
python -m alembic revision --autogenerate -m "describe the change"
```

Do not apply a migration to a database with valuable data until its upgrade/downgrade behavior and backup plan have been reviewed.
