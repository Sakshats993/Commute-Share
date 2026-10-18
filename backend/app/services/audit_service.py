"""
==================================================
CommuteShare Audit Service

Backend Internship Project
Bermer Software Private Limited

Handles creation of audit logs for important
system events.

Examples:
- User Login
- User Registration
- Ride Creation
- Ride Booking
- Booking Cancellation
- SOS Trigger
- Admin Actions
==================================================
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    *,
    action: str,
    resource: str,
    user_id: Optional[int] = None,
    description: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    commit: bool = True,
) -> AuditLog:
    """
    Create and persist an audit log entry.

    Args:
        db: Database session.
        action: Action performed (LOGIN, CREATE, DELETE, etc.).
        resource: Resource affected (Ride, Booking, User, etc.).
        user_id: ID of the user performing the action.
        description: Additional details.
        ip_address: Client IP address.
        user_agent: Browser/device information.

    Returns:
        The created AuditLog object.
    """

    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        resource=resource,
        description=description,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    try:
        db.add(audit_log)
        if commit:
            db.commit()
            db.refresh(audit_log)
        else:
            db.flush()

    except Exception:
        db.rollback()
        raise

    return audit_log


def log_login(
    db: Session,
    *,
    user_id: int,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> AuditLog:
    """
    Log a successful user login.
    """

    return create_audit_log(
        db=db,
        action="LOGIN",
        resource="Authentication",
        user_id=user_id,
        description="User logged in successfully.",
        ip_address=ip_address,
        user_agent=user_agent,
    )


def log_registration(
    db: Session,
    *,
    user_id: int,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> AuditLog:
    """
    Log a new user registration.
    """

    return create_audit_log(
        db=db,
        action="REGISTER",
        resource="User",
        user_id=user_id,
        description="New user registered.",
        ip_address=ip_address,
        user_agent=user_agent,
    )


def log_admin_action(
    db: Session,
    *,
    user_id: int,
    action: str,
    resource: str,
    description: str,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> AuditLog:
    """
    Log an administrative action.
    """

    return create_audit_log(
        db=db,
        action=action,
        resource=resource,
        user_id=user_id,
        description=description,
        ip_address=ip_address,
        user_agent=user_agent,
    )
