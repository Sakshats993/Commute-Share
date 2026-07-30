"""
==================================================
CommuteShare Services Package

Backend Internship Project
Bermer Software Private Limited

Exports all business logic services used
throughout the CommuteShare backend.
==================================================
"""

# Authentication
from app.services.auth_service import (
    authenticate_user,
    change_password,
    get_user_by_email,
    get_user_by_id,
    login_user,
    register_user,
)

# Audit
from app.services.audit_service import (
    create_audit_log,
    log_admin_action,
    log_login,
    log_registration,
)

# Notifications
from app.services.notification_service import (
    create_notification,
    delete_notification,
    get_notifications,
    get_unread_notifications,
    mark_all_as_read,
    mark_as_read,
)

# Ride Management
from app.services.ride_service import (
    create_ride,
    delete_ride,
    get_available_rides,
    get_ride_by_id,
    search_rides,
    update_ride,
)

# Ride Matching
from app.services.matching_service import (
    calculate_distance,
    filter_available_rides,
    find_nearby_rides,
    sort_by_departure,
    sort_by_distance,
)

# Reputation
from app.services.reputation_service import (
    calculate_average_rating,
    calculate_cancellation_rate,
    calculate_completion_rate,
    calculate_trust_score,
    refresh_user_reputation,
)

__all__ = [

    # Authentication
    "authenticate_user",
    "change_password",
    "get_user_by_email",
    "get_user_by_id",
    "login_user",
    "register_user",

    # Audit
    "create_audit_log",
    "log_admin_action",
    "log_login",
    "log_registration",

    # Notifications
    "create_notification",
    "delete_notification",
    "get_notifications",
    "get_unread_notifications",
    "mark_all_as_read",
    "mark_as_read",

    # Ride Management
    "create_ride",
    "delete_ride",
    "get_available_rides",
    "get_ride_by_id",
    "search_rides",
    "update_ride",

    # Matching
    "calculate_distance",
    "filter_available_rides",
    "find_nearby_rides",
    "sort_by_departure",
    "sort_by_distance",

    # Reputation
    "calculate_average_rating",
    "calculate_cancellation_rate",
    "calculate_completion_rate",
    "calculate_trust_score",
    "refresh_user_reputation",
]