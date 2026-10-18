import pytest

from app.core.config import Settings


@pytest.mark.parametrize("environment_value", ["release", "production", "prod"])
def test_release_environment_never_enables_debug(environment_value):
    config = Settings(
        _env_file=None,
        DATABASE_URL="sqlite:///./settings-test.db",
        SECRET_KEY="settings-test-only",
        DEBUG=environment_value,
    )
    assert config.DEBUG is False


def test_development_environment_enables_debug():
    config = Settings(
        _env_file=None,
        DATABASE_URL="sqlite:///./settings-test.db",
        SECRET_KEY="settings-test-only",
        DEBUG="development",
    )
    assert config.DEBUG is True
