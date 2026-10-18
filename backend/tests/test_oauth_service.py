import pytest

from app.services import oauth_service


def test_google_identity_requires_verified_email(monkeypatch):
    monkeypatch.setattr(oauth_service, "_post_form", lambda *_args, **_kwargs: {"access_token": "provider-token"})
    monkeypatch.setattr(
        oauth_service,
        "_get_json",
        lambda *_args, **_kwargs: {
            "sub": "google-user-1",
            "email": "person@example.com",
            "email_verified": False,
        },
    )

    with pytest.raises(oauth_service.OAuthProviderError):
        oauth_service.fetch_google_identity("code", "http://localhost/callback")


def test_github_identity_uses_verified_primary_email(monkeypatch):
    monkeypatch.setattr(oauth_service, "_post_form", lambda *_args, **_kwargs: {"access_token": "provider-token"})

    def provider_response(url, *, headers):
        if url.endswith("/user"):
            return {"id": 123, "login": "rider", "name": None}
        return [
            {"email": "unverified@example.com", "primary": True, "verified": False},
            {"email": "verified@example.com", "primary": True, "verified": True},
        ]

    monkeypatch.setattr(oauth_service, "_get_json", provider_response)
    identity = oauth_service.fetch_github_identity("code", "http://localhost/callback")

    assert identity["subject"] == "123"
    assert identity["email"] == "verified@example.com"
    assert identity["full_name"] == "rider"
