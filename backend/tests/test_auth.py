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


def test_registration_requires_valid_mobile_number(client):
    payload = {
        "full_name": "Mobile Required",
        "email": "mobile-required@example.com",
        "password": "Password123",
    }

    missing = client.post("/auth/register", json=payload)
    invalid = client.post("/auth/register", json={**payload, "phone_number": "12345"})

    assert missing.status_code == 422
    assert invalid.status_code == 422


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
        data={
            "username": "unknown@example.com",
            "password": "WrongPassword",
        },
    )

    assert response.status_code in (
        400,
        401,
    )


def test_registration_cannot_assign_admin_role(client):
    response = client.post(
        "/auth/register",
        json={
            "full_name": "Unexpected Admin",
            "email": "unexpected-admin@example.com",
            "password": "Password123",
            "role": "admin",
        },
    )

    assert response.status_code == 422


def test_oauth_provider_status_does_not_expose_credentials(client):
    response = client.get("/auth/providers")

    assert response.status_code == 200
    assert set(response.json()) == {"google", "github"}
    assert "client_secret" not in response.text


def test_oauth_start_sets_state_cookie_and_minimal_provider_scopes(client, monkeypatch):
    from urllib.parse import parse_qs, urlparse

    from app.api.routes import auth

    monkeypatch.setitem(auth.OAUTH_PROVIDERS, "google", {
        "client_id": "test-client-id",
        "client_secret": "test-client-secret",
    })
    response = client.get("/auth/oauth/google/start", follow_redirects=False)

    assert response.status_code == 302
    authorization = urlparse(response.headers["location"])
    query = parse_qs(authorization.query)
    cookie = response.headers["set-cookie"]
    assert authorization.netloc == "accounts.google.com"
    assert query["scope"] == ["openid email profile"]
    assert query["state"][0]
    assert query["state"][0] in cookie
    assert "httponly" in cookie.lower()
    assert "samesite=lax" in cookie.lower()


def test_oauth_callback_requires_matching_state(client, monkeypatch):
    from app.api.routes import auth

    def unexpected_provider_call(*_args, **_kwargs):
        raise AssertionError("Provider call must not happen when OAuth state is invalid")

    monkeypatch.setattr(auth, "fetch_google_identity", unexpected_provider_call)
    client.cookies.set("commuteshare_oauth_state_google", "different-cookie-state")
    response = client.get(
        "/auth/oauth/google/callback?code=code&state=query-state",
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "oauth_error=invalid_state" in response.headers["location"]


def test_google_oauth_links_only_existing_verified_email_account(client, db, monkeypatch):
    from app.api.routes import auth
    from app.models.user import User
    from sqlalchemy import select

    registration = client.post("/auth/register", json={
        "full_name": "OAuth User",
        "email": "oauth-user@example.com",
        "phone_number": "9876501236",
        "password": "Password123",
    })
    assert registration.status_code == 201

    monkeypatch.setattr(
        auth,
        "fetch_google_identity",
        lambda *_args, **_kwargs: {
            "subject": "google-subject-123",
            "email": "oauth-user@example.com",
            "full_name": "OAuth User",
            "profile_image": None,
        },
    )
    client.cookies.set("commuteshare_oauth_state_google", "valid-state")
    response = client.get(
        "/auth/oauth/google/callback?code=mock-code&state=valid-state",
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/oauth/callback#access_token=" in response.headers["location"]
    user = db.scalar(select(User).where(User.email == "oauth-user@example.com"))
    assert user.google_subject == "google-subject-123"


def test_google_oauth_creates_passenger_account_without_phone(client, db, monkeypatch):
    from app.api.routes import auth
    from app.models.enums import UserRole
    from app.models.user import User
    from sqlalchemy import select

    monkeypatch.setattr(
        auth,
        "fetch_google_identity",
        lambda *_args, **_kwargs: {
            "subject": "new-google-subject",
            "email": "new-user@example.com",
            "full_name": "New User",
            "profile_image": None,
        },
    )
    client.cookies.set("commuteshare_oauth_state_google", "valid-state")
    response = client.get(
        "/auth/oauth/google/callback?code=mock-code&state=valid-state",
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/oauth/callback#access_token=" in response.headers["location"]
    user = db.scalar(select(User).where(User.email == "new-user@example.com"))
    assert user is not None
    assert user.full_name == "New User"
    assert user.phone_number is None
    assert user.role == UserRole.PASSENGER
    assert user.google_subject == "new-google-subject"


def test_github_oauth_creates_account_from_provider_profile(client, db, monkeypatch):
    from app.api.routes import auth
    from app.models.enums import UserRole
    from app.models.user import User
    from sqlalchemy import select

    monkeypatch.setattr(
        auth,
        "fetch_github_identity",
        lambda *_args, **_kwargs: {
            "subject": "github-subject-456",
            "email": "github-user@example.com",
            "full_name": "GitHub User",
            "profile_image": "https://avatars.example.com/user.png",
        },
    )
    client.cookies.set("commuteshare_oauth_state_github", "valid-state")
    response = client.get(
        "/auth/oauth/github/callback?code=mock-code&state=valid-state",
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/oauth/callback#access_token=" in response.headers["location"]
    user = db.scalar(select(User).where(User.email == "github-user@example.com"))
    assert user is not None
    assert user.profile_image == "https://avatars.example.com/user.png"
    assert user.phone_number is None
    assert user.role == UserRole.PASSENGER
    assert user.github_subject == "github-subject-456"
