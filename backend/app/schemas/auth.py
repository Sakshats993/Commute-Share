"""
==================================================
CommuteShare Authentication Schemas

Backend Internship Project
Bermer Software Private Limited

Pydantic schemas related to authentication.

Includes:
- Login Request
- JWT Token
- Token Payload
- Login Response
==================================================
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field



# ======================================================
# Login Request
# ======================================================

class LoginRequest(BaseModel):
    """
    Schema used when a user logs in.
    """

    email: EmailStr = Field(
        ...,
        description="Registered email address.",
        examples=["user@example.com"],
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password.",
    )

# ======================================================
# Change Password Request
# ======================================================

class ChangePasswordRequest(BaseModel):
    """
    Request schema for changing the user's password.
    """

    current_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Current account password.",
    )

    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="New account password.",
    )


class PasswordResetRequest(BaseModel):
    """Request a password reset link for an email address."""

    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Set a new password using a one-time reset token."""

    token: str = Field(..., min_length=40, max_length=128)
    new_password: str = Field(..., min_length=8, max_length=128)

# ======================================================
# JWT Token
# ======================================================

class Token(BaseModel):
    """
    JWT access token response.
    """

    access_token: str

    token_type: str = "bearer"


# ======================================================
# Token Payload
# ======================================================

class TokenPayload(BaseModel):
    """
    Data stored inside the JWT.
    """

    sub: str
    exp: int


# ======================================================
# Login Response
# ======================================================

class LoginResponse(BaseModel):
    """
    Response returned after successful login.
    """

    message: str

    access_token: str

    token_type: str = "bearer"


# ======================================================
# Pydantic Configuration
# ======================================================

class AuthSchemaConfig(BaseModel):
    """
    Shared configuration for authentication schemas.
    """

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        str_strip_whitespace=True,
    )
