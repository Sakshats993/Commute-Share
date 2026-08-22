"""
==================================================
CommuteShare Security

Backend Internship Project
Bermer Software Private Limited

This module provides authentication and security
utilities including:

- Password Hashing
- Password Verification
- JWT Access Tokens
- JWT Refresh Tokens
- Token Decoding
==================================================
"""

from datetime import datetime, timedelta, timezone
from uuid import uuid4
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# ---------------------------------------------------------
# Password Hashing
# ---------------------------------------------------------

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

# ---------------------------------------------------------
# Password Utilities
# ---------------------------------------------------------


def hash_password(password: str) -> str:
    """
    Hash a plain text password.
    """
    return pwd_context.hash(password)

def get_password_hash(password: str) -> str:
    """
    Backward-compatible wrapper for hash_password().
    """
    return hash_password(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    """
    return pwd_context.verify(plain_password, hashed_password)


# ---------------------------------------------------------
# JWT Token Creation
# ---------------------------------------------------------


def create_access_token(
    subject: str | Any,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a JWT Access Token.
    """

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload = {
        "sub": str(subject),
        "type": "access",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def create_refresh_token(subject: str | Any) -> str:
    """
    Create a JWT Refresh Token.
    """

    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload = {
        "sub": str(subject),
        "type": "refresh",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


# ---------------------------------------------------------
# JWT Verification
# ---------------------------------------------------------


def decode_token(token: str) -> dict:
    """
    Decode and validate a JWT token.

    Raises:
        JWTError
    """

    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )


def get_token_subject(token: str) -> str:
    """
    Extract the user id/email from the JWT token.
    """

    payload = decode_token(token)

    subject = payload.get("sub")

    if subject is None:
        raise JWTError("Token subject missing.")

    return subject


def is_refresh_token(token: str) -> bool:
    """
    Returns True if token is a refresh token.
    """

    payload = decode_token(token)

    return payload.get("type") == "refresh"


def is_access_token(token: str) -> bool:
    """
    Returns True if token is an access token.
    """

    payload = decode_token(token)

    return payload.get("type") == "access"

# ---------------------------------------------------------
# QR Boarding Token
# ---------------------------------------------------------

def create_qr_boarding_token(
    *,
    ride_id: int,
    driver_id: int,
) -> str:

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=15
    )

    payload = {
        "type": "boarding_qr",
        "ride_id": ride_id,
        "driver_id": driver_id,
        "nonce": str(uuid4()),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_qr_boarding_token(
    token: str,
) -> dict:
    """
    Decode and validate a boarding QR token.
    """

    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )

    if payload.get("type") != "boarding_qr":
        raise JWTError("Invalid boarding QR token.")

    return payload