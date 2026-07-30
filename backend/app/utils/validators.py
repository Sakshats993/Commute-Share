"""
==================================================
CommuteShare Validation Utilities

Backend Internship Project
Bermer Software Private Limited

Reusable validation functions used across
the CommuteShare backend.

Features:
- Email Validation
- Password Strength Validation
- Phone Number Validation
- Vehicle Registration Validation
==================================================
"""

from __future__ import annotations

import re

from fastapi import HTTPException, status

# ==========================================================
# Regular Expressions
# ==========================================================

EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

PHONE_PATTERN = re.compile(
    r"^[6-9]\d{9}$"
)

VEHICLE_NUMBER_PATTERN = re.compile(
    r"^[A-Z]{2}[0-9]{1,2}[A-Z]{1,2}[0-9]{4}$"
)

PASSWORD_PATTERN = re.compile(
    r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$"
)

# ==========================================================
# Email
# ==========================================================

def validate_email(
    email: str,
) -> None:
    """
    Validate email format.
    """

    if not EMAIL_PATTERN.fullmatch(email):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email address.",
        )


# ==========================================================
# Password
# ==========================================================

def validate_password(
    password: str,
) -> None:
    """
    Validate password strength.

    Requirements:
    - Minimum 8 characters
    - One uppercase letter
    - One lowercase letter
    - One number
    """

    if not PASSWORD_PATTERN.fullmatch(password):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Password must contain at least "
                "8 characters, one uppercase "
                "letter, one lowercase letter, "
                "and one number."
            ),
        )


# ==========================================================
# Phone Number
# ==========================================================

def validate_phone_number(
    phone_number: str,
) -> None:
    """
    Validate Indian mobile number.
    """

    if not PHONE_PATTERN.fullmatch(phone_number):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number.",
        )


# ==========================================================
# Vehicle Registration Number
# ==========================================================

def validate_vehicle_number(
    registration_number: str,
) -> None:
    """
    Validate Indian vehicle registration number.

    Example:
    KA20AB1234
    """

    registration_number = (
        registration_number.upper()
        .replace(" ", "")
    )

    if not VEHICLE_NUMBER_PATTERN.fullmatch(
        registration_number
    ):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid vehicle registration number.",
        )


# ==========================================================
# Rating
# ==========================================================

def validate_rating(
    rating: int,
) -> None:
    """
    Rating must be between 1 and 5.
    """

    if rating < 1 or rating > 5:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5.",
        )


# ==========================================================
# Seats
# ==========================================================

def validate_seat_count(
    seats: int,
) -> None:
    """
    Seat count must be positive.
    """

    if seats <= 0:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seat count must be greater than zero.",
        )


# ==========================================================
# Coordinates
# ==========================================================

def validate_coordinates(
    latitude: float,
    longitude: float,
) -> None:
    """
    Validate latitude and longitude.
    """

    if not (-90 <= latitude <= 90):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid latitude.",
        )

    if not (-180 <= longitude <= 180):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid longitude.",
        )


# ==========================================================
# Export
# ==========================================================

__all__ = [
    "validate_email",
    "validate_password",
    "validate_phone_number",
    "validate_vehicle_number",
    "validate_rating",
    "validate_seat_count",
    "validate_coordinates",
]