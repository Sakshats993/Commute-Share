"""
==================================================
CommuteShare API Routes

Backend Internship Project
Bermer Software Private Limited

Registers all API route modules.
==================================================
"""

from app.api.routes.admin import router as admin_router
from app.api.routes.auth import router as auth_router
from app.api.routes.bookings import router as bookings_router
from app.api.routes.notifications import router as notifications_router
from app.api.routes.ratings import router as ratings_router
from app.api.routes.rides import router as rides_router
from app.api.routes.sos import router as sos_router
from app.api.routes.users import router as users_router
from app.api.routes.vehicles import router as vehicles_router
from app.api.routes.payments import router as payments_router


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
    "payments_router",
]