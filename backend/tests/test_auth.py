"""
==================================================
CommuteShare Authentication Tests

Backend Internship Project
Bermer Software Private Limited

Tests:
- Health Check
- User Registration
- Duplicate Registration
- Invalid Login
==================================================
"""

from __future__ import annotations


# ==========================================================
# Health Check
# ==========================================================

def test_health_endpoint(client):
    """
    Verify the application is running.
    """

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# ==========================================================
# User Registration
# ==========================================================

def test_register_user(client):
    """
    Register a new user.
    """

    response = client.post(
        "/auth/register",
        json={
            "full_name": "John Doe",
            "email": "john@example.com",
            "password": "Password123",
            "phone_number": "9876543210",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "john@example.com"
    assert data["full_name"] == "John Doe"


# ==========================================================
# Duplicate Registration
# ==========================================================

def test_duplicate_registration(client):
    """
    Registering the same email twice should fail.
    """

    payload = {
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "password": "Password123",
        "phone_number": "9876543211",
    }

    client.post(
        "/auth/register",
        json=payload,
    )

    response = client.post(
        "/auth/register",
        json=payload,
    )

    assert response.status_code == 400


# ==========================================================
# Invalid Login
# ==========================================================

def test_invalid_login(client):
    """
    Login with invalid credentials.
    """

    response = client.post(
        "/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "WrongPassword",
        },
    )

    assert response.status_code in (
        400,
        401,
    )