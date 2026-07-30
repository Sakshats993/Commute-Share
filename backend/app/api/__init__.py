"""
==================================================
CommuteShare API Package

Backend Internship Project
Bermer Software Private Limited

This package contains all API route modules
for the CommuteShare backend.
==================================================
"""

from app.api.routes import (
    admin_router,
    auth_router,
    bookings_router,
    notifications_router,
    ratings_router,
    rides_router,
    sos_router,
    users_router,
    vehicles_router,
)

__all__ = [
    "admin_router",
    "auth_router",
    "bookings_router",
    "notifications_router",
    "ratings_router",
    "rides_router",
    "sos_router",
    "users_router",
    "vehicles_router",
]