"""
==================================================
CommuteShare Exception Handling

Backend Internship Project
Bermer Software Private Limited

This module defines custom exceptions and global
exception handlers used throughout the application.
==================================================
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


# ==========================================================
# Base Application Exception
# ==========================================================

class CommuteShareException(Exception):
    """Base exception for the application."""

    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


# ==========================================================
# Authentication Exceptions
# ==========================================================

class InvalidCredentialsException(CommuteShareException):
    def __init__(self):
        super().__init__(
            message="Invalid email or password.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class UnauthorizedException(CommuteShareException):
    def __init__(self):
        super().__init__(
            message="You are not authorized to perform this action.",
            status_code=status.HTTP_403_FORBIDDEN,
        )


class UserAlreadyExistsException(CommuteShareException):
    def __init__(self):
        super().__init__(
            message="A user with this email already exists.",
            status_code=status.HTTP_409_CONFLICT,
        )


# ==========================================================
# User Exceptions
# ==========================================================

class UserNotFoundException(CommuteShareException):
    def __init__(self):
        super().__init__(
            message="User not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )


# ==========================================================
# Vehicle Exceptions
# ==========================================================

class VehicleNotFoundException(CommuteShareException):
    def __init__(self):
        super().__init__(
            message="Vehicle not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )


# ==========================================================
# Ride Exceptions
# ==========================================================

class RideNotFoundException(CommuteShareException):
    def __init__(self):
        super().__init__(
            message="Ride not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class RideAlreadyStartedException(CommuteShareException):
    def __init__(self):
        super().__init__(
            message="Ride has already started.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class RideAlreadyCompletedException(CommuteShareException):
    def __init__(self):
        super().__init__(
            message="Ride has already been completed.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


# ==========================================================
# Booking Exceptions
# ==========================================================

class BookingNotFoundException(CommuteShareException):
    def __init__(self):
        super().__init__(
            message="Booking not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class RideFullException(CommuteShareException):
    def __init__(self):
        super().__init__(
            message="Ride is full.",
            status_code=status.HTTP_409_CONFLICT,
        )


class DuplicateBookingException(CommuteShareException):
    def __init__(self):
        super().__init__(
            message="You have already booked this ride.",
            status_code=status.HTTP_409_CONFLICT,
        )


# ==========================================================
# Waitlist Exceptions
# ==========================================================

class WaitlistException(CommuteShareException):
    def __init__(self):
        super().__init__(
            message="Unable to join waitlist.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


# ==========================================================
# Rating Exceptions
# ==========================================================

class RatingException(CommuteShareException):
    def __init__(self):
        super().__init__(
            message="Unable to submit rating.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


# ==========================================================
# Notification Exceptions
# ==========================================================

class NotificationException(CommuteShareException):
    def __init__(self):
        super().__init__(
            message="Notification could not be processed.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ==========================================================
# Global Exception Handler Registration
# ==========================================================

def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all custom exception handlers.
    """

    @app.exception_handler(CommuteShareException)
    async def commuteshare_exception_handler(
        request: Request,
        exc: CommuteShareException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": exc.message,
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request,
        exc: Exception,
    ):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": "An unexpected server error occurred.",
            },
        )