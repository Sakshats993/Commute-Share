"""
==================================================
CommuteShare User Schemas

Backend Internship Project
Bermer Software Private Limited

Pydantic schemas related to users.

Includes:
- User Creation
- User Update
- User Response
- Public User Profile
==================================================
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.enums import UserRole


# ======================================================
# Base Schema
# ======================================================

class UserBase(BaseModel):
    """
    Common user fields.
    """

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    phone_number: Optional[str] = Field(
        default=None,
        max_length=20,
    )

    bio: Optional[str] = Field(
        default=None,
        max_length=500,
    )

    profile_image: Optional[str] = None


# ======================================================
# Create User
# ======================================================
class UserCreate(UserBase):
    """
    Schema used during registration.
    """

    role: UserRole = Field(
        default=UserRole.PASSENGER,
        description="Role selected during registration",
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )

# ======================================================
# Update User
# ======================================================

class UserUpdate(BaseModel):
    """
    Schema used to update user profile.
    """

    full_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    phone_number: Optional[str] = Field(
        default=None,
        max_length=20,
    )

    bio: Optional[str] = Field(
        default=None,
        max_length=500,
    )

    profile_image: Optional[str] = None

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


# ======================================================
# Public User
# ======================================================

class UserPublic(UserBase):
    """
    Public information about a user.
    """

    id: int

    role: UserRole

    is_verified: bool

    model_config = ConfigDict(
        from_attributes=True,
    )


# ======================================================
# User Response
# ======================================================
class UserResponse(UserPublic):
    """
    Complete user information returned
    to the authenticated user.
    """

    is_active: bool

    average_rating: float
    trust_score: float
    completed_rides: int
    review_count: int

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )