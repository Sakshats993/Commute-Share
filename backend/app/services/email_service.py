"""Plain SMTP email delivery using only the Python standard library."""

from __future__ import annotations

import smtplib
import ssl
from email.message import EmailMessage

from app.core.config import settings


def is_smtp_configured() -> bool:
    return all((
        settings.SMTP_HOST,
        settings.SMTP_USERNAME,
        settings.SMTP_PASSWORD,
        settings.SMTP_FROM_EMAIL,
    ))


def send_password_reset_email(recipient: str, reset_url: str) -> None:
    if not is_smtp_configured():
        raise RuntimeError("SMTP is not configured.")

    message = EmailMessage()
    message["Subject"] = "Reset your CommuteShare password"
    message["From"] = settings.SMTP_FROM_EMAIL
    message["To"] = recipient
    message.set_content(
        "We received a request to reset your CommuteShare password.\n\n"
        f"Use this single-use link within {settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES} minutes:\n"
        f"{reset_url}\n\n"
        "If you did not request this, you can ignore this message. Your password will not change."
    )

    timeout_seconds = 10
    if settings.SMTP_USE_SSL:
        with smtplib.SMTP_SSL(
            settings.SMTP_HOST,
            settings.SMTP_PORT,
            timeout=timeout_seconds,
            context=ssl.create_default_context(),
        ) as server:
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(message)
        return

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=timeout_seconds) as server:
        if settings.SMTP_STARTTLS:
            server.starttls(context=ssl.create_default_context())
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.send_message(message)
