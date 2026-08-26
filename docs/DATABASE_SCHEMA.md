# 🗄️ CommuteShare Database Schema

This document describes the database structure used by **CommuteShare**.

CommuteShare uses **PostgreSQL** as its primary relational database and **SQLAlchemy ORM** for database modelling and interaction. Database schema changes are managed using **Alembic migrations**.

The database is designed around the core workflows of the platform:

* User authentication and profiles
* Vehicle registration
* Ride creation and lifecycle management
* Passenger bookings
* Waitlist management
* Payments
* Ratings and reviews
* Notifications
* SOS emergency events
* Security and audit logging

---

## 📋 Table of Contents

* [Database Overview](#-database-overview)
* [Common Model Fields](#-common-model-fields)
* [Entity Overview](#-entity-overview)
* [Users](#-users)
* [Vehicles](#-vehicles)
* [Rides](#-rides)
* [Bookings](#-bookings)
* [Waitlists](#-waitlists)
* [Payments](#-payments)
* [Ratings](#-ratings)
* [Notifications](#-notifications)
* [SOS Events](#-sos-events)
* [Audit Logs](#-audit-logs)
* [Entity Relationships](#-entity-relationships)
* [Enumerations](#-enumerations)
* [Constraints and Data Integrity](#-constraints-and-data-integrity)
* [Cascade Behaviour](#-cascade-behaviour)
* [Indexes](#-indexes)

---

# 🎯 Database Overview

The CommuteShare database contains the following primary tables:

| Table           | Purpose                                                    |
| --------------- | ---------------------------------------------------------- |
| `users`         | Stores user accounts, profiles, roles, and reputation data |
| `vehicles`      | Stores vehicles registered by users                        |
| `rides`         | Stores rides created by drivers                            |
| `bookings`      | Stores passenger ride bookings                             |
| `waitlists`     | Stores passengers waiting for a seat                       |
| `payments`      | Stores payment information for bookings                    |
| `ratings`       | Stores ratings and reviews between users                   |
| `notifications` | Stores user notifications                                  |
| `sos_events`    | Stores emergency SOS events                                |
| `audit_logs`    | Stores important security and system events                |

---

# 🧱 Common Model Fields

Most database models inherit from the shared `BaseModel`.

Every model using `BaseModel` contains the following fields:

| Column       | Type     | Description               |
| ------------ | -------- | ------------------------- |
| `id`         | Integer  | Primary key               |
| `created_at` | DateTime | Record creation timestamp |
| `updated_at` | DateTime | Last update timestamp     |

Example:

```text
BaseModel
│
├── id
├── created_at
└── updated_at
```

The `id` field is:

* Primary key
* Auto-incremented
* Indexed

---

# 🧩 Entity Overview

```text
                         USERS
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
       VEHICLES         BOOKINGS       NOTIFICATIONS
          │                │
          ▼                ▼
        RIDES ◄──────── PAYMENTS
          │
    ┌─────┼──────────┬──────────┐
    │     │          │          │
    ▼     ▼          ▼          ▼
 BOOKINGS WAITLISTS RATINGS  SOS EVENTS

USERS
 ├── RATINGS GIVEN
 ├── RATINGS RECEIVED
 ├── AUDIT LOGS
 └── SOS EVENTS
```

A detailed visual representation is available in:

```text
docs/ER_Diagram.png
```

---

# 👤 Users

## Table

```text
users
```

The `users` table stores authentication details, profile information, roles, account status, and reputation-related data.

---

## Columns

| Column            | Type        | Nullable | Description                 |
| ----------------- | ----------- | -------: | --------------------------- |
| `id`              | Integer     |       No | Primary key                 |
| `full_name`       | String(100) |       No | User's full name            |
| `email`           | String(255) |       No | Unique email address        |
| `password_hash`   | String(255) |       No | Hashed password             |
| `phone_number`    | String(20)  |      Yes | User phone number           |
| `profile_image`   | String(500) |      Yes | Profile image URL/path      |
| `bio`             | String(500) |      Yes | User biography              |
| `role`            | Enum        |       No | User role                   |
| `is_active`       | Boolean     |       No | Account activation status   |
| `is_verified`     | Boolean     |       No | Verification status         |
| `average_rating`  | Float       |       No | Average rating received     |
| `trust_score`     | Float       |       No | Calculated user trust score |
| `completed_rides` | Integer     |       No | Number of completed rides   |
| `review_count`    | Integer     |       No | Number of reviews           |
| `created_at`      | DateTime    |       No | Creation timestamp          |
| `updated_at`      | DateTime    |       No | Update timestamp            |

---

## Relationships

A user can have:

```text
User
 ├── Many Vehicles
 ├── Many Rides as Driver
 ├── Many Bookings as Passenger
 ├── Many Ratings Given
 ├── Many Ratings Received
 ├── Many Notifications
 ├── Many Audit Logs
 ├── Many SOS Events
 └── Many Waitlist Entries
```

---

## User Roles

The `role` column uses the `UserRole` enumeration.

```text
admin
driver
passenger
```

Default role:

```text
passenger
```

---

# 🚙 Vehicles

## Table

```text
vehicles
```

The `vehicles` table stores vehicles registered by users.

A vehicle belongs to one user and can be associated with multiple rides.

---

## Columns

| Column                | Type       | Nullable | Description                 |
| --------------------- | ---------- | -------: | --------------------------- |
| `id`                  | Integer    |       No | Primary key                 |
| `owner_id`            | Integer    |       No | References `users.id`       |
| `make`                | String(50) |       No | Vehicle manufacturer        |
| `model`               | String(50) |       No | Vehicle model               |
| `color`               | String(30) |       No | Vehicle colour              |
| `registration_number` | String(20) |       No | Unique registration number  |
| `seating_capacity`    | Integer    |       No | Maximum seating capacity    |
| `is_active`           | Boolean    |       No | Vehicle availability status |
| `created_at`          | DateTime   |       No | Creation timestamp          |
| `updated_at`          | DateTime   |       No | Update timestamp            |

---

## Relationships

```text
User
  │
  │ 1
  │
  └──────────< Vehicle
                 │
                 │ 1
                 │
                 └──────────< Ride
```

### Relationship Details

* One user can own multiple vehicles.
* One vehicle belongs to one user.
* One vehicle can be used for multiple rides.

---

# 🚗 Rides

## Table

```text
rides
```

The `rides` table represents rides created by drivers.

It stores route information, geographic coordinates, schedule information, capacity, pricing, and ride lifecycle status.

---

## Driver and Vehicle Columns

| Column       | Type    | Description              |
| ------------ | ------- | ------------------------ |
| `driver_id`  | Integer | References `users.id`    |
| `vehicle_id` | Integer | References `vehicles.id` |

---

## Route Columns

| Column                  | Type        | Description           |
| ----------------------- | ----------- | --------------------- |
| `pickup_location`       | String(255) | Pickup location       |
| `pickup_latitude`       | Float       | Pickup latitude       |
| `pickup_longitude`      | Float       | Pickup longitude      |
| `destination_location`  | String(255) | Destination           |
| `destination_latitude`  | Float       | Destination latitude  |
| `destination_longitude` | Float       | Destination longitude |

---

## Schedule Columns

| Column                   | Type     | Nullable | Description            |
| ------------------------ | -------- | -------: | ---------------------- |
| `departure_time`         | DateTime |       No | Planned departure time |
| `estimated_arrival_time` | DateTime |      Yes | Estimated arrival time |

---

## Ride Lifecycle Columns

| Column                   | Type     | Nullable | Description                     |
| ------------------------ | -------- | -------: | ------------------------------- |
| `boarding_verified_at`   | DateTime |      Yes | Boarding verification timestamp |
| `driver_completed_at`    | DateTime |      Yes | Driver completion timestamp     |
| `passenger_completed_at` | DateTime |      Yes | Passenger completion timestamp  |
| `completed_at`           | DateTime |      Yes | Final ride completion timestamp |

---

## Capacity Columns

| Column            | Type    | Description               |
| ----------------- | ------- | ------------------------- |
| `total_seats`     | Integer | Total seats offered       |
| `available_seats` | Integer | Remaining available seats |

---

## Pricing

| Column           | Type          | Description              |
| ---------------- | ------------- | ------------------------ |
| `price_per_seat` | Numeric(10,2) | Price per passenger seat |

---

## Additional Information

| Column   | Type | Nullable | Description             |
| -------- | ---- | -------: | ----------------------- |
| `notes`  | Text |      Yes | Additional driver notes |
| `status` | Enum |       No | Current ride status     |

---

## Ride Status

The `status` column uses the `RideStatus` enumeration.

```text
scheduled
waiting_for_boarding
in_progress
awaiting_passenger_confirmation
completed
cancelled
```

Default status:

```text
scheduled
```

---

## Relationships

A ride can have:

```text
Ride
 ├── One Driver
 ├── One Vehicle
 ├── Many Bookings
 ├── Many Waitlist Entries
 ├── Many Ratings
 ├── Many SOS Events
 └── Many Payments
```

---

# 📅 Bookings

## Table

```text
bookings
```

The `bookings` table represents a passenger booking a seat on a ride.

Each booking connects:

```text
Passenger
    │
    ▼
 Booking
    │
    ▼
  Ride
```

---

## Columns

| Column                  | Type     | Nullable | Description                     |
| ----------------------- | -------- | -------: | ------------------------------- |
| `id`                    | Integer  |       No | Primary key                     |
| `passenger_id`          | Integer  |       No | References `users.id`           |
| `ride_id`               | Integer  |       No | References `rides.id`           |
| `status`                | Enum     |       No | Booking status                  |
| `cancelled_at`          | DateTime |      Yes | Cancellation timestamp          |
| `has_boarded`           | Boolean  |       No | Passenger boarding status       |
| `has_confirmed_dropoff` | Boolean  |       No | Passenger drop-off confirmation |
| `created_at`            | DateTime |       No | Creation timestamp              |
| `updated_at`            | DateTime |       No | Update timestamp                |

---

## Booking Status

```text
pending
confirmed
cancelled
waitlisted
```

Default:

```text
confirmed
```

---

## Relationships

```text
User (Passenger)
        │
        │ 1
        │
        └──────────< Booking >──────────1 Ride
                         │
                         │ 1
                         │
                         └──────────1 Payment
```

---

## Unique Constraint

A passenger cannot create multiple bookings for the same ride.

```text
(passenger_id, ride_id)
```

Constraint name:

```text
uq_booking_passenger_ride
```

This ensures:

```text
One Passenger + One Ride = Maximum One Booking
```

---

# ⏳ Waitlists

## Table

```text
waitlists
```

The waitlist stores passengers waiting for seats when a ride reaches capacity.

---

## Columns

| Column           | Type     | Nullable | Description              |
| ---------------- | -------- | -------: | ------------------------ |
| `id`             | Integer  |       No | Primary key              |
| `ride_id`        | Integer  |       No | References `rides.id`    |
| `passenger_id`   | Integer  |       No | References `users.id`    |
| `queue_position` | Integer  |       No | Passenger queue position |
| `created_at`     | DateTime |       No | Creation timestamp       |
| `updated_at`     | DateTime |       No | Update timestamp         |

---

## Relationships

```text
Ride
 │
 └──────────< Waitlist >────────── User
```

A ride can have multiple waitlist entries.

A passenger can appear in multiple waitlists for different rides.

---

## Unique Constraint

A passenger can only appear once in the waitlist for a specific ride.

```text
(ride_id, passenger_id)
```

Constraint:

```text
uq_waitlist_passenger_ride
```

---

# 💳 Payments

## Table

```text
payments
```

The payments table stores payment information associated with ride bookings.

A payment is associated with:

* One booking
* One ride

---

## Columns

| Column       | Type          | Nullable | Description              |
| ------------ | ------------- | -------: | ------------------------ |
| `id`         | Integer       |       No | Primary key              |
| `ride_id`    | Integer       |       No | References `rides.id`    |
| `booking_id` | Integer       |       No | References `bookings.id` |
| `amount`     | Numeric(10,2) |       No | Payment amount           |
| `status`     | Enum          |       No | Payment status           |
| `method`     | String(50)    |      Yes | Payment method           |
| `paid_at`    | DateTime      |      Yes | Payment timestamp        |
| `created_at` | DateTime      |       No | Creation timestamp       |
| `updated_at` | DateTime      |       No | Update timestamp         |

---

## Payment Status

```text
unpaid
paid
failed
refunded
```

Default:

```text
unpaid
```

---

## Relationships

```text
Ride
 │
 └──────────< Payment >────────── Booking
```

Each booking can have only one payment.

---

## Unique Constraint

```text
booking_id
```

Constraint name:

```text
uq_payment_booking
```

This ensures:

```text
One Booking = Maximum One Payment
```

---

# ⭐ Ratings

## Table

```text
ratings
```

The ratings table stores ratings and reviews exchanged between users after a ride.

Each rating connects:

```text
Reviewer
    │
    ▼
  Rating
    │
    ▼
 Reviewee

    │
    ▼
   Ride
```

---

## Columns

| Column        | Type     | Nullable | Description           |
| ------------- | -------- | -------: | --------------------- |
| `id`          | Integer  |       No | Primary key           |
| `ride_id`     | Integer  |       No | References `rides.id` |
| `reviewer_id` | Integer  |       No | References `users.id` |
| `reviewee_id` | Integer  |       No | References `users.id` |
| `rating`      | Integer  |       No | Rating from 1 to 5    |
| `review`      | Text     |      Yes | Written review        |
| `created_at`  | DateTime |       No | Creation timestamp    |
| `updated_at`  | DateTime |       No | Update timestamp      |

---

## Rating Relationships

```text
User
 │
 ├── Gives ───────────► Rating
 │                         │
 │                         ▼
 │                       User
 │                    (Reviewee)
 │
 └── Rating is linked to Ride
```

---

## Rating Range Constraint

The rating value must be between:

```text
1 and 5
```

Database constraint:

```sql
rating >= 1 AND rating <= 5
```

Constraint name:

```text
ck_rating_range
```

---

## Unique Constraint

A duplicate rating relationship for the same ride is prevented using:

```text
(ride_id, reviewer_id, reviewee_id)
```

Constraint name:

```text
uq_rating_per_ride
```

---

# 🔔 Notifications

## Table

```text
notifications
```

Notifications store messages sent to users when important application events occur.

Examples:

* Ride booked
* Booking confirmed
* Waitlist promoted
* Ride cancelled
* Rating received
* SOS triggered

---

## Columns

| Column       | Type        | Nullable | Description           |
| ------------ | ----------- | -------: | --------------------- |
| `id`         | Integer     |       No | Primary key           |
| `user_id`    | Integer     |       No | References `users.id` |
| `title`      | String(100) |       No | Notification title    |
| `message`    | Text        |       No | Notification content  |
| `type`       | Enum        |       No | Notification category |
| `is_read`    | Boolean     |       No | Read status           |
| `created_at` | DateTime    |       No | Creation timestamp    |
| `updated_at` | DateTime    |       No | Update timestamp      |

---

## Notification Types

```text
ride_booked
booking_confirmed
waitlist_promoted
ride_cancelled
rating_received
sos_triggered
```

---

## Relationship

```text
User
 │
 │ 1
 │
 └──────────< Notification
```

A user can receive multiple notifications.

---

# 🆘 SOS Events

## Table

```text
sos_events
```

The SOS events table stores emergency alerts triggered by users.

An SOS event can optionally be linked to a ride.

---

## Columns

| Column           | Type        | Nullable | Description            |
| ---------------- | ----------- | -------: | ---------------------- |
| `id`             | Integer     |       No | Primary key            |
| `user_id`        | Integer     |       No | User who triggered SOS |
| `ride_id`        | Integer     |      Yes | Related ride           |
| `emergency_type` | String(100) |       No | Emergency category     |
| `description`    | Text        |      Yes | Additional information |
| `latitude`       | Float       |      Yes | User latitude          |
| `longitude`      | Float       |      Yes | User longitude         |
| `status`         | Enum        |       No | SOS status             |
| `created_at`     | DateTime    |       No | Creation timestamp     |
| `updated_at`     | DateTime    |       No | Update timestamp       |

---

## SOS Status

```text
active
acknowledged
resolved
```

Default:

```text
active
```

---

## Relationships

```text
User
 │
 └──────────< SOS Event >────────── Ride
```

A user can trigger multiple SOS events.

An SOS event may optionally be connected to a ride.

---

# 📝 Audit Logs

## Table

```text
audit_logs
```

Audit logs store important security and system events.

Examples include:

* User registration
* User login
* Ride creation
* Ride updates
* Booking creation
* Booking cancellation
* SOS events
* Administrative actions

---

## Columns

| Column        | Type        | Nullable | Description                |
| ------------- | ----------- | -------: | -------------------------- |
| `id`          | Integer     |       No | Primary key                |
| `user_id`     | Integer     |      Yes | User associated with event |
| `action`      | String(100) |       No | Action performed           |
| `resource`    | String(100) |       No | Resource affected          |
| `description` | Text        |      Yes | Event details              |
| `ip_address`  | String(45)  |      Yes | Client IP address          |
| `user_agent`  | Text        |      Yes | Client user agent          |
| `created_at`  | DateTime    |       No | Event timestamp            |
| `updated_at`  | DateTime    |       No | Update timestamp           |

---

## Relationship

```text
User
 │
 │ 1
 │
 └──────────< Audit Log
```

The `user_id` field is optional because some system events may not have an associated authenticated user.

---

# 🔗 Entity Relationships

The core relationships in CommuteShare are:

```text
USER
 ├── 1:N VEHICLES
 ├── 1:N RIDES
 ├── 1:N BOOKINGS
 ├── 1:N NOTIFICATIONS
 ├── 1:N SOS EVENTS
 ├── 1:N AUDIT LOGS
 ├── 1:N WAITLIST ENTRIES
 ├── 1:N RATINGS GIVEN
 └── 1:N RATINGS RECEIVED

VEHICLE
 └── 1:N RIDES

RIDE
 ├── 1:N BOOKINGS
 ├── 1:N WAITLIST ENTRIES
 ├── 1:N RATINGS
 ├── 1:N SOS EVENTS
 └── 1:N PAYMENTS

BOOKING
 └── 1:1 PAYMENT
```

---

# 🧬 Complete Relationship Map

```text
                           ┌──────────────┐
                           │    USERS     │
                           └──────┬───────┘
                                  │
          ┌───────────────┬───────┼───────────────┬───────────────┐
          │               │       │               │               │
          ▼               ▼       ▼               ▼               ▼
      VEHICLES         BOOKINGS  RATINGS    NOTIFICATIONS     AUDIT LOGS
          │               │       │
          │               │       │
          ▼               ▼       ▼
        RIDES ◄──────── PAYMENTS  USERS
          │
    ┌─────┼──────────────┐
    │     │              │
    ▼     ▼              ▼
WAITLISTS RATINGS     SOS EVENTS
```

---

# 📚 Enumerations

CommuteShare uses centralized Python enumerations for controlled values.

---

## UserRole

```text
admin
driver
passenger
```

---

## RideStatus

```text
scheduled
waiting_for_boarding
in_progress
awaiting_passenger_confirmation
completed
cancelled
```

---

## BookingStatus

```text
pending
confirmed
cancelled
waitlisted
```

---

## NotificationType

```text
ride_booked
booking_confirmed
waitlist_promoted
ride_cancelled
rating_received
sos_triggered
```

---

## SOSStatus

```text
active
acknowledged
resolved
```

---

## PaymentStatus

```text
unpaid
paid
failed
refunded
```

---

# 🛡️ Constraints and Data Integrity

The database uses multiple constraints to protect data consistency.

## Unique Email

```text
users.email
```

Each email address must be unique.

---

## Unique Vehicle Registration

```text
vehicles.registration_number
```

Each vehicle registration number must be unique.

---

## Unique Booking

```text
(passenger_id, ride_id)
```

A passenger cannot book the same ride multiple times.

---

## Unique Waitlist Entry

```text
(ride_id, passenger_id)
```

A passenger cannot join the same ride's waitlist multiple times.

---

## One Payment per Booking

```text
payments.booking_id
```

Only one payment can exist for each booking.

---

## Rating Range

```text
1 ≤ rating ≤ 5
```

---

## Unique Rating Relationship

```text
(ride_id, reviewer_id, reviewee_id)
```

Duplicate ratings for the same reviewer-reviewee relationship on the same ride are prevented.

---

# 🔥 Cascade Behaviour

Several relationships use cascade deletion.

## User Deletion

Related records may be removed depending on the relationship:

```text
User
 ├── Vehicles
 ├── Rides
 ├── Bookings
 ├── Notifications
 ├── SOS Events
 └── Waitlist Entries
```

---

## Ride Deletion

Related ride data can also be removed:

```text
Ride
 ├── Bookings
 ├── Waitlist Entries
 ├── Ratings
 ├── SOS Events
 └── Payments
```

---

## Audit Log Behaviour

Audit logs use:

```text
ON DELETE SET NULL
```

This means an audit record can remain even when its associated user reference is removed.

```text
User Deleted
     │
     ▼
Audit Log Remains
     │
     ▼
user_id = NULL
```

---

# ⚡ Indexes

Indexes are used on commonly queried fields.

Examples include:

| Table           | Indexed Field         |
| --------------- | --------------------- |
| `users`         | `id`                  |
| `users`         | `email`               |
| `vehicles`      | `owner_id`            |
| `vehicles`      | `registration_number` |
| `rides`         | `driver_id`           |
| `rides`         | `vehicle_id`          |
| `bookings`      | `passenger_id`        |
| `bookings`      | `ride_id`             |
| `payments`      | `ride_id`             |
| `payments`      | `booking_id`          |
| `ratings`       | `ride_id`             |
| `ratings`       | `reviewer_id`         |
| `ratings`       | `reviewee_id`         |
| `notifications` | `user_id`             |
| `sos_events`    | `user_id`             |
| `sos_events`    | `ride_id`             |
| `waitlists`     | `ride_id`             |
| `waitlists`     | `passenger_id`        |
| `audit_logs`    | `user_id`             |

Indexes help improve query performance for frequently accessed relationships.

---

# 🔄 Database Migration Management

Database schema changes are managed using **Alembic**.

Common commands:

### Apply Latest Migrations

```bash
alembic upgrade head
```

### Create a New Migration

```bash
alembic revision --autogenerate -m "describe changes"
```

### Roll Back One Migration

```bash
alembic downgrade -1
```

The migration history is stored in:

```text
backend/alembic/versions/
```

---

# 🗺️ Database Design Principles

The CommuteShare database follows these principles:

### Normalization

Data is separated into related tables to reduce duplication.

### Referential Integrity

Foreign keys maintain valid relationships between entities.

### Controlled States

Enums are used for statuses such as:

* User roles
* Ride lifecycle
* Booking status
* Payment status
* SOS status

### Unique Constraints

Business rules are reinforced at the database level.

### Auditability

Important actions can be recorded using the `audit_logs` table.

### Extensibility

The schema supports future additions such as:

* Payment gateways
* Advanced analytics
* Additional user verification
* Real-time ride tracking
* Rewards and reputation systems

---

# 📊 Related Documentation

| Document           | Description                        |
| ------------------ | ---------------------------------- |
| `API_REFERENCE.md` | API endpoint documentation         |
| `ARCHITECTURE.md`  | System architecture                |
| `SECURITY.md`      | Security practices                 |
| `DEPLOYMENT.md`    | Deployment guide                   |
| `ER_Diagram.png`   | Visual entity relationship diagram |

---

<div align="center">

### 🗄️ Structured Data. Reliable Relationships. Built for Real-World Commutes.

**CommuteShare Database Schema**

</div>
