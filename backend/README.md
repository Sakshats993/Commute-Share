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
