from app.core.config import settings
from app.services import email_service


def test_smtp_sender_uses_starttls_and_sends_reset_message(monkeypatch):
    calls = []

    class FakeSMTP:
        def __init__(self, host, port, timeout):
            calls.append(("connect", host, port, timeout))

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def starttls(self, *, context):
            calls.append(("starttls", context))

        def login(self, username, password):
            calls.append(("login", username, password))

        def send_message(self, message):
            calls.append(("send", message["To"], message["Subject"], message.get_content()))

    monkeypatch.setattr(settings, "SMTP_HOST", "smtp.example.test")
    monkeypatch.setattr(settings, "SMTP_PORT", 587)
    monkeypatch.setattr(settings, "SMTP_USERNAME", "account@example.test")
    monkeypatch.setattr(settings, "SMTP_PASSWORD", "test-only-password")
    monkeypatch.setattr(settings, "SMTP_FROM_EMAIL", "CommuteShare <account@example.test>")
    monkeypatch.setattr(settings, "SMTP_USE_SSL", False)
    monkeypatch.setattr(settings, "SMTP_STARTTLS", True)
    monkeypatch.setattr(email_service.smtplib, "SMTP", FakeSMTP)

    email_service.send_password_reset_email(
        "rider@example.test",
        "http://localhost:5173/reset-password#token=single-use-token",
    )

    assert calls[0] == ("connect", "smtp.example.test", 587, 10)
    assert calls[1][0] == "starttls"
    assert calls[2] == ("login", "account@example.test", "test-only-password")
    assert calls[3][1:3] == ("rider@example.test", "Reset your CommuteShare password")
    assert "single-use-token" in calls[3][3]


def test_smtp_sender_rejects_missing_configuration(monkeypatch):
    monkeypatch.setattr(settings, "SMTP_HOST", None)

    assert not email_service.is_smtp_configured()
