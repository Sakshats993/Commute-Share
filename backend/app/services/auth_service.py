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

from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User

from app.schemas.auth import (
    ChangePasswordRequest,
    LoginResponse,
)

from app.schemas.user import UserCreate

from app.services.audit_service import (
    log_login,
    log_registration,
)


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
        role=user_data.role,
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