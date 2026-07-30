"""
==================================================
CommuteShare User Routes

Backend Internship Project
Bermer Software Private Limited

Handles:
- Current User Profile
- Update Profile
- Get User by ID
- Deactivate Account
==================================================
"""

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.deps import (
    get_current_active_user,
    get_db,
)

from app.models.user import User

from app.schemas.user import (
    UserResponse,
    UserUpdate,
)

from app.services.user_service import (
    deactivate_user,
    get_user_by_id,
    update_user_profile,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# ==========================================================
# Current User
# ==========================================================

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_current_user(
    current_user: User = Depends(get_current_active_user),
):
    """
    Return the currently authenticated user.
    """

    return current_user


# ==========================================================
# Get User By ID
# ==========================================================

@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Return a user by ID.
    """

    return get_user_by_id(
        db=db,
        user_id=user_id,
    )


# ==========================================================
# Update Profile
# ==========================================================

@router.put(
    "/me",
    response_model=UserResponse,
)
def update_profile(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update current user's profile.
    """

    return update_user_profile(
        db=db,
        current_user=current_user,
        user_data=user_data,
    )


# ==========================================================
# Deactivate Account
# ==========================================================

@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Deactivate the current user's account.
    """

    deactivate_user(
        db=db,
        current_user=current_user,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )