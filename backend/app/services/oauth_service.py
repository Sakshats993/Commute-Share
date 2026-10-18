"""Small, server-side OAuth client for Google and GitHub identity login."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from app.core.config import settings


class OAuthProviderError(Exception):
    """Raised when a provider cannot return a verified identity."""


def _request_json(url: str, *, data: bytes | None = None, headers: dict | None = None) -> dict | list:
    request = Request(url, data=data, headers=headers or {})
    try:
        with urlopen(request, timeout=8) as response:
            return json.loads(response.read())
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise OAuthProviderError("The identity provider could not be reached.") from exc


def _post_form(url: str, values: dict, *, headers: dict | None = None) -> dict:
    request_headers = {"Content-Type": "application/x-www-form-urlencoded", **(headers or {})}
    result = _request_json(url, data=urlencode(values).encode(), headers=request_headers)
    if not isinstance(result, dict):
        raise OAuthProviderError("The identity provider returned an invalid response.")
    return result


def _get_json(url: str, *, headers: dict) -> dict | list:
    return _request_json(url, headers=headers)


def fetch_google_identity(code: str, callback_url: str) -> dict:
    token_data = _post_form(
        "https://oauth2.googleapis.com/token",
        {
            "code": code,
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "redirect_uri": callback_url,
            "grant_type": "authorization_code",
        },
    )
    access_token = token_data.get("access_token")
    if not access_token:
        raise OAuthProviderError("Google did not authorize this sign-in.")

    profile = _get_json(
        "https://openidconnect.googleapis.com/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if not isinstance(profile, dict) or profile.get("email_verified") is not True:
        raise OAuthProviderError("Google did not provide a verified email address.")
    subject, email = profile.get("sub"), profile.get("email")
    if not subject or not email:
        raise OAuthProviderError("Google did not provide a usable identity.")
    return {
        "subject": str(subject),
        "email": email.strip().lower(),
        "full_name": profile.get("name") or email.split("@", 1)[0],
        "profile_image": profile.get("picture"),
    }


def fetch_github_identity(code: str, callback_url: str) -> dict:
    token_data = _post_form(
        "https://github.com/login/oauth/access_token",
        {
            "code": code,
            "client_id": settings.GITHUB_OAUTH_CLIENT_ID,
            "client_secret": settings.GITHUB_OAUTH_CLIENT_SECRET,
            "redirect_uri": callback_url,
        },
        headers={"Accept": "application/json"},
    )
    access_token = token_data.get("access_token")
    if not access_token:
        raise OAuthProviderError("GitHub did not authorize this sign-in.")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "CommuteShare",
    }
    profile = _get_json("https://api.github.com/user", headers=headers)
    emails = _get_json("https://api.github.com/user/emails", headers=headers)
    if not isinstance(profile, dict) or not isinstance(emails, list):
        raise OAuthProviderError("GitHub returned an invalid identity response.")

    verified_email = next(
        (
            item.get("email")
            for item in emails
            if isinstance(item, dict)
            and item.get("primary") is True
            and item.get("verified") is True
            and isinstance(item.get("email"), str)
        ),
        None,
    )
    subject = profile.get("id")
    if subject is None or not verified_email:
        raise OAuthProviderError("GitHub did not provide a verified primary email address.")
    return {
        "subject": str(subject),
        "email": verified_email.strip().lower(),
        "full_name": profile.get("name") or profile.get("login") or verified_email.split("@", 1)[0],
        "profile_image": profile.get("avatar_url"),
    }
