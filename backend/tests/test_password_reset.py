from datetime import datetime, timedelta, timezone
from hashlib import sha256
from urllib.parse import parse_qs, urlparse

from sqlalchemy import select

from app.api.routes import auth
from app.models.user import User
from app.services import auth_service
from app.core.security import verify_password


def _register(client, email="reset-user@example.com"):
    return client.post("/auth/register", json={
        "full_name": "Reset User",
        "email": email,
        "phone_number": "9876501240",
        "password": "Password123",
    })


def test_reset_request_is_generic_for_known_and_unknown_email(client, monkeypatch):
    _register(client)
    sent = []
    monkeypatch.setattr(auth, "is_smtp_configured", lambda: True)
    monkeypatch.setattr(auth_service, "send_password_reset_email", lambda email, link: sent.append((email, link)))

    known = client.post("/auth/password-reset/request", json={"email": "reset-user@example.com"})
    unknown = client.post("/auth/password-reset/request", json={"email": "missing@example.com"})

    assert known.status_code == unknown.status_code == 202
    assert known.json() == unknown.json()
    assert len(sent) == 1


def test_reset_link_is_hashed_expires_and_can_only_be_used_once(client, db, monkeypatch):
    _register(client)
    captured = {}
    monkeypatch.setattr(auth, "is_smtp_configured", lambda: True)

    def capture_email(recipient, link):
        captured.update(recipient=recipient, link=link)

    monkeypatch.setattr(auth_service, "send_password_reset_email", capture_email)
    response = client.post("/auth/password-reset/request", json={"email": "reset-user@example.com"})
    assert response.status_code == 202

    token = parse_qs(urlparse(captured["link"]).fragment)["token"][0]
    user = db.scalar(select(User).where(User.email == "reset-user@example.com"))
    assert captured["recipient"] == user.email
    assert user.password_reset_token_hash == sha256(token.encode()).hexdigest()
    assert user.password_reset_token_hash != token
    assert user.password_reset_expires_at is not None

    reset = client.post("/auth/password-reset/confirm", json={
        "token": token,
        "new_password": "NewPassword123",
    })
    replay = client.post("/auth/password-reset/confirm", json={
        "token": token,
        "new_password": "AnotherPassword123",
    })

    assert reset.status_code == 204
    assert replay.status_code == 400
    db.refresh(user)
    assert verify_password("NewPassword123", user.password_hash)
    assert user.password_reset_token_hash is None


def test_expired_reset_token_cannot_change_password(client, db, monkeypatch):
    _register(client)
    captured = {}
    monkeypatch.setattr(auth, "is_smtp_configured", lambda: True)
    monkeypatch.setattr(auth_service, "send_password_reset_email", lambda _email, link: captured.update(link=link))
    client.post("/auth/password-reset/request", json={"email": "reset-user@example.com"})
    token = parse_qs(urlparse(captured["link"]).fragment)["token"][0]
    user = db.scalar(select(User).where(User.email == "reset-user@example.com"))
    user.password_reset_expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
    db.commit()

    response = client.post("/auth/password-reset/confirm", json={
        "token": token,
        "new_password": "NewPassword123",
    })

    assert response.status_code == 400
    db.refresh(user)
    assert verify_password("Password123", user.password_hash)


def test_reset_request_cooldown_prevents_repeat_email(client, monkeypatch):
    _register(client)
    sent = []
    monkeypatch.setattr(auth, "is_smtp_configured", lambda: True)
    monkeypatch.setattr(auth_service, "send_password_reset_email", lambda *_args: sent.append(True))

    first = client.post("/auth/password-reset/request", json={"email": "reset-user@example.com"})
    second = client.post("/auth/password-reset/request", json={"email": "reset-user@example.com"})

    assert first.status_code == second.status_code == 202
    assert first.json() == second.json()
    assert len(sent) == 1


def test_reset_request_reports_missing_smtp_configuration(client, monkeypatch):
    monkeypatch.setattr(auth, "is_smtp_configured", lambda: False)

    response = client.post("/auth/password-reset/request", json={"email": "nobody@example.com"})

    assert response.status_code == 503
    assert response.json()["detail"] == "Password reset email is not configured on this server."
