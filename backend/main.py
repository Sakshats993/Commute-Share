"""
==================================================
CommuteShare Backend

Backend Internship Project
Bermer Software Private Limited

Application Entry Point

Features:
- FastAPI App
- Router Registration
- CORS
- Startup Events
- Health Check
==================================================
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import (
    admin_router,
    auth_router,
    bookings_router,
    notifications_router,
    payments_router,
    ratings_router,
    rides_router,
    sos_router,
    users_router,
    vehicles_router,
)

from app.core.config import settings
from app.utils.logger import logger


# ==========================================================
# Application Lifespan
# ==========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events.
    """

    logger.info("Starting CommuteShare Backend...")

    yield

    logger.info("Shutting down CommuteShare Backend...")


# ==========================================================
# FastAPI Application
# ==========================================================

app = FastAPI(
    title="CommuteShare API",
    description=(
        "Community ride-sharing platform "
        "for daily commuters."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# Health Check
# ==========================================================

@app.get(
    "/health",
    tags=["Health"],
)
def health_check():
    """
    Health check endpoint.
    """

    return {
        "status": "healthy",
        "service": "CommuteShare Backend",
    }


# ==========================================================
# API Routers
# ==========================================================

app.include_router(auth_router)

app.include_router(users_router)

app.include_router(vehicles_router)

app.include_router(rides_router)

app.include_router(bookings_router)

app.include_router(ratings_router)

app.include_router(notifications_router)

app.include_router(sos_router)

app.include_router(admin_router)

app.include_router(payments_router)


# ==========================================================
# Root Endpoint
# ==========================================================

@app.get(
    "/",
    tags=["Root"],
)
def root():
    """
    Root endpoint.
    """

    return {
        "message": "Welcome to CommuteShare API",
        "version": "1.0.0",
        "docs": "/docs",
    }