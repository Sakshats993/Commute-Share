"""
==================================================
CommuteShare Authentication Service

Backend Internship Project
Bermer Software Private Limited

Handles:

- User Registration
- User Authentication
- User Login
- Password Updates
==================================================
"""

from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.core.config import settings
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.enums import UserRole
from app.models.user import User

from app.schemas.auth import (
    ChangePasswordRequest,
    LoginResponse,
    PasswordResetConfirm,
)

from app.schemas.user import UserCreate

from app.services.audit_service import (
    create_audit_log,
    log_login,
    log_registration,
)
from app.services.email_service import send_password_reset_email
from app.utils.logger import logger


# ======================================================
# Get User By Email
# ======================================================

def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    """
    Returns a user by email.
    """

    stmt = select(User).where(User.email == email)

    return db.scalar(stmt)


# ======================================================
# Get User By ID
# ======================================================

def get_user_by_id(
    db: Session,
    user_id: int,
) -> User | None:
    """
    Returns a user by ID.
    """

    stmt = select(User).where(User.id == user_id)

    return db.scalar(stmt)


# ======================================================
# Register User
# ======================================================

def register_user(
    db: Session,
    user_data: UserCreate,
) -> User:
    """
    Register a new user.
    """

    existing_user = get_user_by_email(
        db,
        user_data.email,
    )

    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )

    user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        password_hash=hash_password(
            user_data.password,
        ),
        phone_number=user_data.phone_number,
        bio=user_data.bio,
        profile_image=user_data.profile_image,
        role=UserRole(user_data.role),
    )

    try:

        db.add(user)

        db.commit()

        db.refresh(user)

        log_registration(
            db=db,
            user_id=user.id,
        )

    except Exception:

        db.rollback()

        raise

    return user


# ======================================================
# Authenticate User
# ======================================================
def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User:
    """
    Verify user credentials.
    """

    user = get_user_by_email(
        db,
        email,
    )
    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not verify_password(
        password,
        user.password_hash,
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not user.is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive.",
        )

    return user


# ======================================================
# Login User
# ======================================================

def login_user(
    db: Session,
    email: str,
    password: str,
) -> LoginResponse:
    """
    Authenticate a user and return
    a JWT access token.
    """

    user = authenticate_user(
        db=db,
        email=email,
        password=password,
    )

    token = create_access_token(
        subject=user.email,
    )

    log_login(
        db=db,
        user_id=user.id,
    )

    return LoginResponse(
        message="Login successful.",
        access_token=token,
        token_type="bearer",
    )


def request_password_reset(db: Session, email: str) -> None:
    """Email a short-lived reset link without revealing whether an account exists."""
    normalized_email = email.strip().lower()
    user = db.scalar(
        select(User)
        .where(func.lower(User.email) == normalized_email, User.is_active.is_(True))
        .with_for_update()
    )
    if user is None:
        return

    now = datetime.now(timezone.utc)
    last_request = user.password_reset_requested_at
    if last_request is not None:
        if last_request.tzinfo is None:
            last_request = last_request.replace(tzinfo=timezone.utc)
        if now - last_request < timedelta(seconds=60):
            return

    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    user.password_reset_token_hash = token_hash
    user.password_reset_expires_at = now + timedelta(
        minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
    )
    user.password_reset_requested_at = now
    db.commit()

    reset_url = (
        f"{settings.FRONTEND_URL.rstrip('/')}/reset-password#token={quote(token)}"
    )
    try:
        send_password_reset_email(user.email, reset_url)
    except Exception as exc:
        db.execute(
            update(User)
            .where(User.id == user.id, User.password_reset_token_hash == token_hash)
            .values(
                password_reset_token_hash=None,
                password_reset_expires_at=None,
                password_reset_requested_at=None,
            )
        )
        db.commit()
        logger.warning("Password reset email delivery failed: {}", type(exc).__name__)


def reset_password(db: Session, reset_data: PasswordResetConfirm) -> None:
    """Atomically consume an unexpired reset token and replace its password."""
    token_hash = hashlib.sha256(reset_data.token.encode("utf-8")).hexdigest()
    statement = (
        update(User)
        .where(
            User.password_reset_token_hash == token_hash,
            User.password_reset_expires_at > func.now(),
            User.is_active.is_(True),
        )
        .values(
            password_hash=hash_password(reset_data.new_password),
            password_reset_token_hash=None,
            password_reset_expires_at=None,
            password_reset_requested_at=None,
        )
        .returning(User.id)
    )

    try:
        user_id = db.execute(statement).scalar_one_or_none()
        if user_id is None:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This password reset link is invalid or expired.",
            )
        create_audit_log(
            db=db,
            user_id=user_id,
            action="PASSWORD_RESET",
            resource="Authentication",
            description="Password reset completed.",
            commit=False,
        )
        db.commit()
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise


# ======================================================
# Change Password
# ======================================================
# ======================================================
# Change Password
# ======================================================

def change_password(
    db: Session,
    *,
    current_user: User,
    password_data: ChangePasswordRequest,
) -> User:
    """
    Change the current user's password.
    """

    if not verify_password(
        password_data.current_password,
        current_user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect.",
        )

    current_user.password_hash = hash_password(
        password_data.new_password,
    )

    try:
        db.commit()
        db.refresh(current_user)

    except Exception:
        db.rollback()
        raise

    return current_user
