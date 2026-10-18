<<<<<<< HEAD
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
=======
# 🏗️ CommuteShare Architecture

This document describes the high-level architecture, component structure, data flow, and design approach used in **CommuteShare**.

CommuteShare is designed as a full-stack web application with a clear separation between the frontend, backend, database, and supporting infrastructure.

---

## 📋 Table of Contents

* [Architecture Overview](#-architecture-overview)
* [System Components](#-system-components)
* [High-Level Architecture](#-high-level-architecture)
* [Frontend Architecture](#-frontend-architecture)
* [Backend Architecture](#-backend-architecture)
* [Database Architecture](#-database-architecture)
* [Authentication & Authorization Flow](#-authentication--authorization-flow)
* [Ride Booking Workflow](#-ride-booking-workflow)
* [Notification Flow](#-notification-flow)
* [Application Data Flow](#-application-data-flow)
* [Docker Architecture](#-docker-architecture)
* [Design Principles](#-design-principles)
* [Security Architecture](#-security-architecture)
* [Future Architecture Improvements](#-future-architecture-improvements)

---

# 🎯 Architecture Overview

CommuteShare follows a modern **client-server architecture**.

The application is divided into three primary layers:

1. **Frontend Layer** — React-based user interface.
2. **Backend Layer** — FastAPI REST API containing business logic.
3. **Database Layer** — PostgreSQL database for persistent storage.

```text
┌─────────────────────┐
│                     │
│   React Frontend    │
│                     │
│  Vite + Tailwind    │
└──────────┬──────────┘
           │
           │ HTTP / REST API
           │
           ▼
┌─────────────────────┐
│                     │
│   FastAPI Backend   │
│                     │
│ Authentication      │
│ Business Logic      │
│ RBAC                │
│ Services            │
│                     │
└──────────┬──────────┘
           │
           │ SQLAlchemy ORM
           │
           ▼
┌─────────────────────┐
│                     │
│ PostgreSQL Database │
│                     │
└─────────────────────┘
```

---

# 🧩 System Components

## Frontend

The frontend is responsible for:

* Rendering the user interface
* Managing client-side navigation
* Handling forms and user input
* Communicating with the backend API
* Managing authentication state
* Displaying notifications and application data
* Protecting routes based on authentication and user roles

### Primary Technologies

* React
* Vite
* Tailwind CSS
* React Router
* Axios
* React Hook Form
* React Leaflet
* Recharts

---

## Backend

The backend provides the REST API and handles application logic.

Responsibilities include:

* User authentication
* Authorization
* Role-based access control
* Ride management
* Booking workflows
* Vehicle management
* Rating management
* Notification management
* SOS event handling
* Payment workflows
* Administrative operations
* Database communication

### Primary Technologies

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* Pydantic

---

## Database

PostgreSQL is used as the primary relational database.

The database stores information related to:

* Users
* Vehicles
* Rides
* Bookings
* Ratings
* Notifications
* Payments
* SOS Events
* Waitlists
* Audit Logs

---

# 🌐 High-Level Architecture

```text
                        ┌──────────────────────┐
                        │       Users          │
                        │                      │
                        │ Passenger / Driver   │
                        │ Administrator        │
                        └──────────┬───────────┘
                                   │
                                   │ Browser
                                   ▼
                    ┌─────────────────────────────┐
                    │                             │
                    │      React Frontend         │
                    │                             │
                    │ ┌─────────────────────────┐ │
                    │ │ Pages                  │ │
                    │ │ Components             │ │
                    │ │ Context                │ │
                    │ │ Hooks                  │ │
                    │ │ API Services           │ │
                    │ └─────────────────────────┘ │
                    │                             │
                    └──────────────┬──────────────┘
                                   │
                                   │ HTTPS / REST
                                   ▼
                    ┌─────────────────────────────┐
                    │                             │
                    │      FastAPI Backend        │
                    │                             │
                    │ ┌─────────────────────────┐ │
                    │ │ API Routes              │ │
                    │ ├─────────────────────────┤ │
                    │ │ Dependencies            │ │
                    │ ├─────────────────────────┤ │
                    │ │ Authentication          │ │
                    │ │ Authorization           │ │
                    │ ├─────────────────────────┤ │
                    │ │ Services                │ │
                    │ │ Business Logic          │ │
                    │ ├─────────────────────────┤ │
                    │ │ SQLAlchemy Models       │ │
                    │ └─────────────────────────┘ │
                    │                             │
                    └──────────────┬──────────────┘
                                   │
                                   │ SQL
                                   ▼
                    ┌─────────────────────────────┐
                    │                             │
                    │     PostgreSQL Database     │
                    │                             │
                    │ Users • Rides • Bookings    │
                    │ Vehicles • Ratings          │
                    │ Notifications • Payments    │
                    │ SOS • Waitlists             │
                    │ Audit Logs                  │
                    │                             │
                    └─────────────────────────────┘
```

---

# 💻 Frontend Architecture

The frontend follows a modular React architecture.

```text
src/
│
├── api/
│   └── API communication layer
│
├── components/
│   └── Reusable UI components
│
├── constants/
│   ├── roles.js
│   └── routes.js
│
├── context/
│   └── Global application context
│
├── hooks/
│   └── Custom React hooks
│
├── pages/
│   └── Application pages
│
├── routes/
│   └── Route configuration
│
├── store/
│   └── Application state
│
├── utils/
│   └── Helper functions
│
├── App.jsx
└── main.jsx
```

---

## Frontend Layers

### Pages

Pages represent complete application screens.

Examples include:

* Login Page
* Registration Page
* Dashboard
* Rides Page
* Ride Details
* Bookings
* Vehicles
* Ratings
* Notifications
* SOS
* Admin Dashboard

Pages coordinate components, hooks, and API calls.

---

### Components

Components contain reusable user interface elements.

Examples may include:

* Navigation
* Forms
* Buttons
* Cards
* Modals
* Tables
* Loading states
* Error messages

This improves UI consistency and code reuse.

---

### API Layer

The API layer centralizes communication with the backend.

```text
src/api/
│
├── axios.js
├── auth.js
├── users.js
├── rides.js
├── bookings.js
├── vehicles.js
├── ratings.js
├── notifications.js
├── sos.js
└── admin.js
```

Each module is responsible for a specific application domain.

Example:

```text
Frontend
    │
    ▼
rides.js
    │
    ▼
Axios
    │
    ▼
FastAPI Endpoint
    │
    ▼
JSON Response
    │
    ▼
React Component
```

---

### Context and State

Authentication state is managed centrally.

```text
User Logs In
      │
      ▼
Receive JWT Token
      │
      ▼
Store Authentication State
      │
      ▼
Auth Context
      │
      ├──────────────► Navbar
      │
      ├──────────────► Protected Routes
      │
      ├──────────────► Dashboard
      │
      └──────────────► User Features
```

This prevents authentication data from being unnecessarily passed through multiple component levels.

---

# ⚙️ Backend Architecture

The backend follows a layered structure.

```text
Request
   │
   ▼
API Route
   │
   ▼
Dependencies
   │
   ├── Authentication
   ├── Authorization
   └── Database Session
   │
   ▼
Service Layer
   │
   ├── Business Logic
   ├── Validation
   └── Application Workflows
   │
   ▼
Models / ORM
   │
   ▼
PostgreSQL
```

---

## API Routes

API routes define HTTP endpoints.

Example domains:

```text
/api/routes/
│
├── auth.py
├── users.py
├── rides.py
├── bookings.py
├── vehicles.py
├── ratings.py
├── notifications.py
├── sos.py
├── payments.py
└── admin.py
```

Routes are responsible for:

* Receiving requests
* Validating input
* Applying dependencies
* Calling services
* Returning responses

Routes should remain focused on HTTP handling rather than containing large amounts of business logic.

---

## Service Layer

The service layer contains application business logic.

Example services include:

```text
services/
│
├── auth_service.py
├── booking_service.py
├── admin_service.py
├── audit_service.py
└── matching_service.py
```

The service layer handles workflows such as:

* User authentication
* Password verification
* Ride booking validation
* Seat availability checks
* Booking state transitions
* Administrative operations
* Audit logging

---

## Core Layer

The core layer contains application-wide functionality.

```text
core/
│
├── config.py
├── deps.py
├── exceptions.py
└── security.py
```

### Responsibilities

| File            | Responsibility                                      |
| --------------- | --------------------------------------------------- |
| `config.py`     | Application configuration and environment variables |
| `deps.py`       | FastAPI dependencies                                |
| `exceptions.py` | Custom application exceptions                       |
| `security.py`   | Password hashing and JWT functionality              |

---

## Database Layer

The database layer manages database connectivity and ORM configuration.

```text
database/
│
├── base.py
└── session.py
```

### Responsibilities

* Database engine configuration
* SQLAlchemy session management
* Model registration
* Database connection lifecycle

---

## Models

SQLAlchemy models define the relational structure of the application.

```text
models/
│
├── user.py
├── vehicle.py
├── ride.py
├── booking.py
├── rating.py
├── notification.py
├── payment.py
├── sos_event.py
├── waitlist.py
└── audit_log.py
```

Models define:

* Database tables
* Columns
* Primary keys
* Foreign keys
* Relationships

---

## Schemas

Pydantic schemas define API request and response formats.

```text
schemas/
│
├── auth.py
├── user.py
├── vehicle.py
├── ride.py
├── ride_details.py
├── booking.py
└── payment.py
```

Schemas provide:

* Input validation
* Type validation
* Request serialization
* Response serialization

---

# 🗄️ Database Architecture

CommuteShare uses a relational database design.

```text
                    ┌─────────────┐
                    │    Users    │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
         Vehicles        Rides      Notifications
              │            │
              │            │
              └──────┬─────┘
                     │
                     ▼
                 Bookings
                     │
           ┌─────────┼─────────┐
           │         │         │
           ▼         ▼         ▼
        Payments   Ratings  Waitlist
```

Detailed entity relationships are documented in:

```text
docs/DATABASE_SCHEMA.md
```

The visual database relationship diagram is available in:

```text
docs/ER_Diagram.png
```

---

# 🔐 Authentication & Authorization Flow

CommuteShare uses JWT-based authentication.

```text
┌───────────────┐
│     User      │
└───────┬───────┘
        │
        │ Login Credentials
        ▼
┌─────────────────────┐
│   /auth/login       │
└─────────┬───────────┘
          │
          │ Validate User
          ▼
┌─────────────────────┐
│ Password Verification│
└─────────┬───────────┘
          │
          │ Valid
          ▼
┌─────────────────────┐
│ Generate JWT Token  │
└─────────┬───────────┘
          │
          │ Access Token
          ▼
┌─────────────────────┐
│     Frontend        │
└─────────┬───────────┘
          │
          │ Authorization Header
          ▼
┌─────────────────────────────┐
│ Protected API Endpoint      │
└──────────────┬──────────────┘
               │
               ▼
        Verify JWT Token
               │
               ▼
        Check User Role
               │
               ▼
         Allow / Deny
```

---

# 👥 Role-Based Access Control

CommuteShare uses role-based authorization.

```text
                    ┌─────────────┐
                    │    User     │
                    └──────┬──────┘
                           │
                           ▼
                    Authentication
                           │
                           ▼
                    Identify Role
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
         Passenger       Driver        Admin
              │            │            │
              ▼            ▼            ▼
        Passenger     Driver       Platform
        Features      Features     Management
```

Authorization checks are performed before protected operations.

Examples:

| Action              | Required Access    |
| ------------------- | ------------------ |
| Create Ride         | Driver             |
| Register Vehicle    | Driver             |
| Book Ride           | Authenticated User |
| Manage Own Booking  | Booking Owner      |
| View Earnings       | Driver             |
| Platform Statistics | Admin              |
| Manage Users        | Admin              |

---

# 🚗 Ride Booking Workflow

The ride booking system follows a controlled workflow.

```text
Driver
   │
   ▼
Create Vehicle
   │
   ▼
Create Ride
   │
   ▼
Ride Available
   │
   │
Passenger
   │
   ▼
Search Ride
   │
   ▼
Select Ride
   │
   ▼
Create Booking
   │
   ▼
Check Seat Availability
   │
   ├──────────────► Available
   │                    │
   │                    ▼
   │               Booking Created
   │                    │
   │                    ▼
   │               Confirm Booking
   │
   └──────────────► Full
                        │
                        ▼
                    Waitlist
```

This workflow ensures that:

* Seat availability is checked
* Invalid bookings are prevented
* Drivers maintain control over ride operations
* Passengers can track their bookings

---

# 🔔 Notification Flow

Notifications are used to inform users about important events.

```text
Application Event
       │
       ▼
Business Logic
       │
       ▼
Create Notification
       │
       ▼
Store in Database
       │
       ▼
User Requests Notifications
       │
       ▼
Frontend Displays Notification
```

Possible notification events include:

* Booking confirmation
* Booking cancellation
* Ride updates
* Ride lifecycle changes
* Administrative actions

---

# 🆘 SOS Event Flow

The SOS system allows users to report emergency events.

```text
User
 │
 │ Trigger SOS
 ▼
SOS API Endpoint
 │
 ▼
Validate Request
 │
 ▼
Create SOS Event
 │
 ▼
Store Event
 │
 ▼
Authorized Access / Review
```

The system records relevant emergency information such as:

* User
* Ride
* Emergency type
* Description
* Location data
* Timestamp

---

# 📊 Application Data Flow

A typical application request follows this path:

```text
User Interaction
      │
      ▼
React Component
      │
      ▼
Custom Hook
      │
      ▼
API Module
      │
      ▼
Axios HTTP Request
      │
      ▼
FastAPI Route
      │
      ▼
Authentication / Dependencies
      │
      ▼
Service Layer
      │
      ▼
SQLAlchemy Model
      │
      ▼
PostgreSQL
      │
      ▼
JSON Response
      │
      ▼
Frontend State Update
      │
      ▼
Updated User Interface
```

---

# 🐳 Docker Architecture

The application can run using Docker containers.

```text
                    Docker Compose
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
   ┌────────────┐   ┌────────────┐   ┌────────────┐
   │  Frontend  │   │  Backend   │   │ PostgreSQL │
   │            │   │            │   │            │
   │ React/Vite │──►│  FastAPI   │──►│ PostgreSQL │
   │            │   │            │   │            │
   └────────────┘   └────────────┘   └────────────┘
```

### Container Responsibilities

| Container | Responsibility                     |
| --------- | ---------------------------------- |
| Frontend  | Serves the React application       |
| Backend   | Runs the FastAPI API               |
| Database  | Stores persistent application data |

---

# 🧱 Design Principles

CommuteShare follows several important software engineering principles.

## Separation of Concerns

Each layer has a defined responsibility.

```text
Frontend     → User Interface
Routes       → HTTP Handling
Services     → Business Logic
Models       → Database Structure
Schemas      → Data Validation
Database     → Persistent Storage
```

---

## Modularity

Application functionality is divided into independent domains.

Examples:

* Authentication
* Users
* Vehicles
* Rides
* Bookings
* Ratings
* Payments
* Notifications
* SOS
* Administration

This improves maintainability and makes future expansion easier.

---

## Reusability

Reusable components are used throughout the frontend and backend.

Examples:

* API clients
* Authentication dependencies
* Database sessions
* Custom hooks
* Utility functions
* Shared schemas

---

## Scalability

The architecture allows individual components to evolve independently.

Potential future improvements include:

```text
React Frontend
      │
      ▼
Load Balancer
      │
      ▼
Multiple Backend Instances
      │
      ▼
Redis Cache
      │
      ▼
PostgreSQL
```

---

# 🛡️ Security Architecture

Security is implemented across multiple layers.

```text
┌──────────────────────────────┐
│         Frontend             │
│                              │
│ Protected Routes             │
│ Input Validation             │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         Backend              │
│                              │
│ JWT Authentication           │
│ RBAC                         │
│ Ownership Validation         │
│ Pydantic Validation          │
│ Password Hashing             │
│ Exception Handling           │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         Database             │
│                              │
│ Foreign Keys                 │
│ Relationships                │
│ Data Integrity               │
└──────────────────────────────┘
```

Detailed security information is documented in:

```text
docs/SECURITY.md
```

---

# 📈 Future Architecture Improvements

Potential architectural improvements include:

## Infrastructure

* Reverse proxy with Nginx
* HTTPS/TLS configuration
* Cloud deployment
* CI/CD pipeline
* Container orchestration

## Backend

* Redis caching
* Background workers
* Task queues
* Rate limiting
* API versioning
* Refresh tokens

## Frontend

* Progressive Web App support
* Offline functionality
* Improved caching
* Enhanced accessibility

## Monitoring

* Centralized logging
* Application metrics
* Error tracking
* Health monitoring
* Performance monitoring

---

# 📚 Related Documentation

| Document             | Description                          |
| -------------------- | ------------------------------------ |
| `API_REFERENCE.md`   | Complete API endpoint documentation  |
| `DATABASE_SCHEMA.md` | Database structure and relationships |
| `SECURITY.md`        | Security design and practices        |
| `DEPLOYMENT.md`      | Application deployment guide         |
| `ROADMAP.md`         | Planned future improvements          |
| `architecture.png`   | Visual system architecture diagram   |
| `ER_Diagram.png`     | Database entity relationship diagram |

---

<div align="center">

### 🏗️ Designed for Learning. Structured for Growth. Built for Real-World Workflows.

**CommuteShare Architecture**

</div>
>>>>>>> origin/main
