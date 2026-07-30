"""
==================================================
CommuteShare Authentication Routes

Backend Internship Project
Bermer Software Private Limited

Handles:
- User Registration
- User Login
- Current User
- Password Change
==================================================
"""

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm

from app.core.deps import (
    get_current_active_user,
    get_db,
)

from app.models.user import User

from app.schemas.auth import (
    ChangePasswordRequest,
    LoginResponse,
)

from app.schemas.user import (
    UserCreate,
    UserResponse,
)

from app.services.auth_service import (
    change_password,
    login_user,
    register_user,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

# ==========================================================
# Register
# ==========================================================
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new user.
    """

    return register_user(
        db=db,
        user_data=user_data,
    )

# ==========================================================
# Login
# ==========================================================

@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return login_user(
        db=db,
        email=form_data.username,
        password=form_data.password,
    )

# ==========================================================
# Current User
# ==========================================================

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(
        get_current_active_user,
    ),
):
    """
    Return current authenticated user.
    """

    return current_user

# ==========================================================
# Change Password
# ==========================================================

@router.put(
    "/change-password",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_password(
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_active_user,
    ),
):
    """
    Change current user's password.
    """

    change_password(
        db=db,
        current_user=current_user,
        password_data=password_data,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )   