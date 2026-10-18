<<<<<<< HEAD
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
=======
# 🚗 CommuteShare — Backend

The backend API for **CommuteShare**, a community-driven ride-sharing platform for daily commuters.

The backend is built using FastAPI and follows a structured architecture with API routes, services, database models, schemas, authentication, authorization, logging, testing, and database migrations.

---

## ✨ Features

* 🔐 JWT Authentication
* 👤 User Management
* 🚗 Ride Management
* 📅 Ride Booking System
* ⏳ Waitlist Management
* 🚙 Vehicle Management
* ⭐ Rating System
* 🔔 Notifications
* 🆘 SOS Emergency Events
* 💳 Payment Management
* 👨‍💼 Admin Management
* 📝 Audit Logging
* 🔒 Role-Based Access Control
* 🗄️ PostgreSQL Database
* 🔄 Database Migrations with Alembic
* 📍 Geolocation Support
* 🧪 Automated Testing
* 🐳 Docker Support
* 📖 Interactive API Documentation

---

## 🛠️ Tech Stack

| Technology       | Purpose              |
| ---------------- | -------------------- |
| Python           | Programming Language |
| FastAPI          | REST API Framework   |
| PostgreSQL       | Relational Database  |
| SQLAlchemy       | ORM                  |
| Alembic          | Database Migrations  |
| Pydantic         | Data Validation      |
| Python-JOSE      | JWT Authentication   |
| Passlib + Bcrypt | Password Hashing     |
| Geopy            | Geolocation          |
| Loguru           | Logging              |
| Pytest           | Testing              |
| Docker           | Containerization     |

---

## 🏗️ Architecture

The backend follows a layered architecture:

```text
Client
   │
   ▼
API Routes
   │
   ▼
Services
   │
   ▼
Database Models
   │
   ▼
PostgreSQL
```

### Layers

#### API Routes

Responsible for:

* Handling HTTP requests
* Validating incoming data
* Returning HTTP responses
* Connecting API endpoints to services

#### Services

Responsible for:

* Business logic
* Application workflows
* Database operations
* Validation logic

#### Models

Responsible for:

* Database structure
* Relationships
* SQLAlchemy ORM mappings

#### Schemas

Responsible for:

* Request validation
* Response serialization
* Pydantic data models

---

## 📁 Project Structure

```text
backend/
│
├── alembic/
│   ├── versions/
│   │   ├── initial_migration.py
│   │   ├── add_driver_statistics.py
│   │   ├── create_payments_table.py
│   │   └── ride_lifecycle_fields.py
│   │
│   ├── env.py
│   └── script.py.mako
│
├── app/
│   │
│   ├── api/
│   │   └── routes/
│   │       ├── admin.py
│   │       ├── auth.py
│   │       ├── bookings.py
│   │       ├── notifications.py
│   │       ├── payments.py
│   │       ├── ratings.py
│   │       ├── rides.py
│   │       ├── sos.py
│   │       ├── users.py
│   │       └── vehicles.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── deps.py
│   │   ├── exceptions.py
│   │   └── security.py
│   │
│   ├── database/
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── ride.py
│   │   ├── booking.py
│   │   ├── vehicle.py
│   │   ├── rating.py
│   │   ├── notification.py
│   │   ├── payment.py
│   │   ├── sos_event.py
│   │   ├── waitlist.py
│   │   └── audit_log.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── booking.py
│   │   ├── payment.py
│   │   ├── ride.py
│   │   ├── ride_details.py
│   │   ├── user.py
│   │   └── vehicle.py
│   │
│   ├── services/
│   │   ├── admin_service.py
│   │   ├── audit_service.py
│   │   ├── auth_service.py
│   │   ├── booking_service.py
│   │   ├── matching_service.py
│   │   └── ...
│   │
│   └── utils/
│       └── logger.py
│
├── logs/
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_bookings.py
│   └── test_rides.py
│
├── .env.example
├── alembic.ini
├── Dockerfile
├── main.py
├── requirements.txt
└── README.md
```

---

# 🚀 Getting Started

## Prerequisites

Make sure you have installed:

* Python 3.12+
* PostgreSQL
* pip
* Git

---

## 1. Navigate to the Backend

```bash
cd backend
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Environment Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Configure the environment variables:

```env
APP_NAME=CommuteShare
APP_VERSION=1.0.0
DEBUG=True

DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/commuteshare

SECRET_KEY=CHANGE_THIS_TO_A_LONG_RANDOM_SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

BACKEND_CORS_ORIGINS=["http://localhost:5173"]

LOG_LEVEL=INFO
```

> ⚠️ Never commit your real `.env` file or production secrets to GitHub.

---

# 🗄️ Database Setup

Create a PostgreSQL database:

```sql
CREATE DATABASE commuteshare;
```

Make sure your `DATABASE_URL` matches your PostgreSQL credentials.

Example:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres123@localhost:5432/commuteshare
```

---

# 🔄 Database Migrations

Apply existing migrations:

```bash
alembic upgrade head
```

Create a new migration:

```bash
alembic revision --autogenerate -m "describe your changes"
```

Apply the migration:

```bash
alembic upgrade head
```

Rollback the latest migration:

```bash
alembic downgrade -1
```

---

# ▶️ Running the Server

Start the FastAPI development server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

---

# 📖 API Documentation

FastAPI automatically generates interactive API documentation.

### Swagger UI

```text
http://localhost:8000/docs
```

### ReDoc

```text
http://localhost:8000/redoc
```

---

# ❤️ Health Check

The backend provides a health check endpoint:

```http
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "service": "CommuteShare Backend"
}
```

---

# 🔐 Authentication

CommuteShare uses JWT-based authentication.

```text
User
 │
 ▼
Register
 │
 ▼
Password Hashing
 │
 ▼
Login
 │
 ▼
JWT Access Token
 │
 ▼
Authenticated API Requests
```

The authentication system includes:

* Secure password hashing
* JWT access tokens
* Token expiration
* Authentication dependencies
* Role-based authorization

---

# 📡 API Modules

The API is organized into the following modules:

| Module         | Description                         |
| -------------- | ----------------------------------- |
| Authentication | Registration and Login              |
| Users          | User profile and account management |
| Vehicles       | Vehicle management                  |
| Rides          | Ride creation and management        |
| Bookings       | Ride booking workflows              |
| Ratings        | User and ride ratings               |
| Notifications  | User notifications                  |
| SOS            | Emergency event reporting           |
| Payments       | Payment-related workflows           |
| Admin          | Administrative functionality        |

---

# 🧪 Testing

The project includes automated tests for core functionality.

Run all tests:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

Example test areas:

* Authentication
* Ride Management
* Booking Workflows

---

# 🐳 Docker

The backend includes Docker support.

Build the backend container:

```bash
docker build -t commuteshare-backend .
```

Run the container:

```bash
docker run -p 8000:8000 commuteshare-backend
```

---

# 🐳 Running the Complete Application

From the project root:

```bash
docker compose up --build
```

This starts:

```text
PostgreSQL
     │
     ▼
FastAPI Backend
     │
     ▼
React Frontend
```

Services:

| Service               | URL                        |
| --------------------- | -------------------------- |
| Frontend              | http://localhost:5173      |
| Backend API           | http://localhost:8000      |
| Swagger Documentation | http://localhost:8000/docs |
| PostgreSQL            | localhost:5432             |

Stop the application:

```bash
docker compose down
```

---

# 🔒 Security Practices

The backend incorporates several security-focused practices:

* Password hashing using Bcrypt
* JWT-based authentication
* Role-based authorization
* Environment-based configuration
* Request validation with Pydantic
* Centralized exception handling
* Audit logging
* Separation of API, service, and database layers
* CORS configuration

---

# 🛣️ Future Improvements

Potential future enhancements include:

* Refresh token support
* Rate limiting
* Email verification
* Password reset functionality
* Redis caching
* Background task processing
* Real-time notifications
* Advanced ride matching
* Enhanced payment integration
* API monitoring and metrics
* CI/CD deployment pipeline

---

# 🤝 Contributing

Contributions and improvements are welcome.

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature/your-feature
```

3. Make your changes.
4. Run tests.

```bash
pytest
```

5. Commit your changes.

```bash
git commit -m "Add your feature"
```

6. Push your branch.

```bash
git push origin feature/your-feature
```

7. Open a Pull Request.

---

# 👨‍💻 Authors

* **Sakshat S**
* **Swasthi Kunder**
* **Neha S**

### 🔗 GitHub

* Sakshat: https://github.com/Sakshats993
* Swasthi: https://github.com/swasthikunder
* Neha: https://github.com/Neha-61

---

<div align="center">

### 🚗 Building Reliable APIs for Better Commutes

**If you found this project interesting, consider giving the repository a ⭐**

</div>
>>>>>>> origin/main
