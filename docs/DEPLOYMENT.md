# 🚀 CommuteShare Deployment Guide

This document explains how to run and deploy **CommuteShare** using local development tools and Docker.

CommuteShare consists of three main services:

* 🌐 React Frontend
* ⚙️ FastAPI Backend
* 🗄️ PostgreSQL Database

The application can be run locally for development or containerized using Docker and Docker Compose.

---

## 📋 Table of Contents

* [Deployment Overview](#-deployment-overview)
* [Prerequisites](#-prerequisites)
* [Environment Configuration](#-environment-configuration)
* [Local Development Setup](#-local-development-setup)
* [Database Setup](#-database-setup)
* [Running the Backend](#-running-the-backend)
* [Running the Frontend](#-running-the-frontend)
* [Docker Deployment](#-docker-deployment)
* [Docker Compose Deployment](#-docker-compose-deployment)
* [Database Migrations](#-database-migrations)
* [Production Considerations](#-production-considerations)
* [Troubleshooting](#-troubleshooting)
* [Useful Commands](#-useful-commands)

---

# 🎯 Deployment Overview

CommuteShare follows a multi-service architecture.

```text
                    User Browser
                         │
                         ▼
                  ┌──────────────┐
                  │   Frontend   │
                  │ React + Vite │
                  └──────┬───────┘
                         │
                         │ HTTP / REST
                         ▼
                  ┌──────────────┐
                  │   Backend    │
                  │   FastAPI    │
                  └──────┬───────┘
                         │
                         │ SQL
                         ▼
                  ┌──────────────┐
                  │  PostgreSQL  │
                  └──────────────┘
```

---

# 📦 Prerequisites

Before running CommuteShare, install the following.

## Required

* Git
* Python 3.11 or newer
* Node.js 18 or newer
* npm
* PostgreSQL 15 or newer

## Optional

* Docker
* Docker Compose

Check your installations:

```bash
git --version
```

```bash
python --version
```

```bash
node --version
```

```bash
npm --version
```

```bash
docker --version
```

---

# ⚙️ Environment Configuration

CommuteShare uses environment variables for configuration.

Never commit production secrets or passwords to Git.

---

## Backend Environment

Navigate to the backend:

```bash
cd backend
```

Create your environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Configure your `.env` file.

Example:

```env
APP_NAME=CommuteShare
APP_VERSION=1.0.0
DEBUG=True

DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/commuteshare

SECRET_KEY=CHANGE_THIS_TO_A_LONG_RANDOM_SECRET
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

BACKEND_CORS_ORIGINS=["http://localhost:5173"]

LOG_LEVEL=INFO
```

> ⚠️ Use a strong and unique `SECRET_KEY` in production.

---

## Frontend Environment

Navigate to the frontend:

```bash
cd frontend
```

Create a `.env` file:

```env
VITE_API_BASE_URL=http://localhost:8000
```

For production, replace the local backend URL with your deployed backend URL.

Example:

```env
VITE_API_BASE_URL=https://api.example.com
```

---

# 💻 Local Development Setup

Clone the repository:

```bash
git clone https://github.com/Sakshats993/Commute-Share.git
```

Navigate to the project:

```bash
cd Commute-Share
```

The project structure is:

```text
Commute-Share/
│
├── backend/
│   ├── app/
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   └── main.py
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
├── docs/
├── docker-compose.yml
└── README.md
```

---

# 🗄️ Database Setup

## 1. Start PostgreSQL

Make sure PostgreSQL is running.

On Linux:

```bash
sudo systemctl start postgresql
```

On Windows, start PostgreSQL using:

* Services
* pgAdmin
* PostgreSQL installer tools

---

## 2. Create the Database

Connect to PostgreSQL:

```bash
psql -U postgres
```

Create the database:

```sql
CREATE DATABASE commuteshare;
```

Exit PostgreSQL:

```sql
\q
```

---

## 3. Configure Database Connection

Update your backend `.env` file:

```env
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/commuteshare
```

---

# ⚙️ Running the Backend

Navigate to the backend:

```bash
cd backend
```

---

## 1. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```powershell
venv\Scripts\Activate.ps1
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

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Run Database Migrations

```bash
alembic upgrade head
```

---

## 4. Start the Backend

```bash
uvicorn main:app --reload
```

The backend should be available at:

```text
http://localhost:8000
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

---

# 🌐 Running the Frontend

Open another terminal.

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend should be available at:

```text
http://localhost:5173
```

---

# 🔄 Local Development Architecture

When running locally:

```text
┌──────────────────────────────┐
│        Web Browser           │
│                              │
│ http://localhost:5173        │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│        React + Vite          │
│                              │
│        Frontend              │
└───────────────┬──────────────┘
                │
                │ API Requests
                ▼
┌──────────────────────────────┐
│        FastAPI Backend       │
│                              │
│ http://localhost:8000        │
└───────────────┬──────────────┘
                │
                │ SQLAlchemy
                ▼
┌──────────────────────────────┐
│        PostgreSQL            │
│                              │
│ localhost:5432               │
└──────────────────────────────┘
```

---

# 🐳 Docker Deployment

Docker allows the application to run inside containers.

CommuteShare can containerize:

* Frontend
* Backend
* Database

---

## Build Backend Image

From the backend directory:

```bash
docker build -t commuteshare-backend .
```

Run the backend:

```bash
docker run -p 8000:8000 commuteshare-backend
```

The backend will be available at:

```text
http://localhost:8000
```

---

## Build Frontend Image

From the frontend directory:

```bash
docker build -t commuteshare-frontend .
```

Run the frontend:

```bash
docker run -p 5173:5173 commuteshare-frontend
```

---

# 🐳 Docker Compose Deployment

Docker Compose is the recommended way to run the complete application.

From the project root:

```bash
docker compose up --build
```

This starts all services.

```text
Docker Compose
      │
      ├──────────────► PostgreSQL
      │
      ├──────────────► FastAPI Backend
      │
      └──────────────► React Frontend
```

---

## Run in Detached Mode

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs
```

Follow logs:

```bash
docker compose logs -f
```

---

# 🌐 Application URLs

After successful deployment:

| Service    | URL                           |
| ---------- | ----------------------------- |
| Frontend   | `http://localhost:5173`       |
| Backend    | `http://localhost:8000`       |
| Swagger UI | `http://localhost:8000/docs`  |
| ReDoc      | `http://localhost:8000/redoc` |
| PostgreSQL | `localhost:5432`              |

---

# 🗄️ Database Migrations

CommuteShare uses Alembic for database migrations.

---

## Apply Latest Migration

```bash
alembic upgrade head
```

---

## Check Current Revision

```bash
alembic current
```

---

## View Migration History

```bash
alembic history
```

---

## Create New Migration

After changing a database model:

```bash
alembic revision --autogenerate -m "describe your changes"
```

Example:

```bash
alembic revision --autogenerate -m "add user verification fields"
```

Apply the migration:

```bash
alembic upgrade head
```

---

## Roll Back One Migration

```bash
alembic downgrade -1
```

> ⚠️ Always back up production databases before running destructive migrations.

---

# 🏭 Production Deployment

For production environments, additional configuration is recommended.

```text
                        Internet
                           │
                           ▼
                    ┌─────────────┐
                    │    HTTPS    │
                    │ Reverse Proxy│
                    └──────┬──────┘
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
         Frontend Server        Backend Server
                │                     │
                └──────────┬──────────┘
                           │
                           ▼
                     PostgreSQL
```

Recommended production components:

* Reverse proxy
* HTTPS certificates
* Environment secrets
* Managed PostgreSQL database
* Automated backups
* Centralized logging
* Health monitoring
* CI/CD pipeline

---

# 🔒 Production Environment Variables

Production values should differ from local development.

Example:

```env
DEBUG=False

DATABASE_URL=postgresql+psycopg://production_user:strong_password@database-host:5432/commuteshare

SECRET_KEY=VERY_LONG_RANDOM_PRODUCTION_SECRET

ACCESS_TOKEN_EXPIRE_MINUTES=30

BACKEND_CORS_ORIGINS=["https://yourdomain.com"]
```

Never expose:

* Database passwords
* JWT secrets
* API keys
* Production credentials

---

# 🔐 Production Security Checklist

Before deploying publicly:

* [ ] Set `DEBUG=False`
* [ ] Use a strong random `SECRET_KEY`
* [ ] Use HTTPS
* [ ] Configure production CORS origins
* [ ] Use strong PostgreSQL credentials
* [ ] Remove development credentials
* [ ] Run database migrations
* [ ] Enable database backups
* [ ] Review application logs
* [ ] Configure monitoring
* [ ] Test authentication
* [ ] Test authorization rules
* [ ] Verify environment variables are not committed
* [ ] Review Docker image security

---

# 🧪 Deployment Verification

After deployment, verify the following.

## Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

---

## API Documentation

Open:

```text
http://localhost:8000/docs
```

Verify that:

* API documentation loads
* Authentication endpoints work
* Protected routes require authentication

---

## Frontend

Open:

```text
http://localhost:5173
```

Verify:

* Application loads
* Login works
* Registration works
* API communication works
* Protected routes work

---

# 🔧 Troubleshooting

## Backend Cannot Connect to Database

Check:

```text
DATABASE_URL
```

Verify:

* PostgreSQL is running
* Database exists
* Username is correct
* Password is correct
* Port is correct

Test manually:

```bash
psql -U postgres -d commuteshare
```

---

## Port Already in Use

### Backend

If port `8000` is busy:

```bash
uvicorn main:app --reload --port 8001
```

### Frontend

Vite may automatically select another available port.

---

## Frontend Cannot Reach Backend

Check the frontend environment variable:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Also verify backend CORS settings:

```env
BACKEND_CORS_ORIGINS=["http://localhost:5173"]
```

Restart both applications after changing environment variables.

---

## Docker Containers Fail

Check logs:

```bash
docker compose logs
```

Check running containers:

```bash
docker compose ps
```

Rebuild containers:

```bash
docker compose down
```

```bash
docker compose up --build
```

---

## Database Migration Errors

Check the current migration:

```bash
alembic current
```

Check migration history:

```bash
alembic history
```

Verify:

* Database connection
* Migration files
* SQLAlchemy models
* Alembic configuration

---

# ⚡ Useful Commands

## Backend

```bash
# Activate environment
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn main:app --reload

# Run tests
pytest

# Run migrations
alembic upgrade head
```

---

## Frontend

```bash
# Install dependencies
npm install

# Development server
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

---

## Docker

```bash
# Start application
docker compose up --build

# Start in background
docker compose up -d --build

# View containers
docker compose ps

# View logs
docker compose logs

# Follow logs
docker compose logs -f

# Stop containers
docker compose down

# Stop and remove volumes
docker compose down -v
```

---

# 📚 Related Documentation

| Document             | Description                         |
| -------------------- | ----------------------------------- |
| `API_REFERENCE.md`   | Complete REST API documentation     |
| `ARCHITECTURE.md`    | Application architecture            |
| `DATABASE_SCHEMA.md` | Database design and relationships   |
| `SECURITY.md`        | Security architecture and practices |
| `ROADMAP.md`         | Future development plans            |

---

<div align="center">

### 🚀 From Local Development to Deployment.

**CommuteShare Deployment Guide**

</div>
