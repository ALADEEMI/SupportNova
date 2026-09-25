"""Settings come from the environment; a missing secret stops start-up clearly (P01-S2)."""

import pytest

from src.core.errors import ConfigurationError
from src.core.settings import load_settings

pytestmark = pytest.mark.unit

REQUIRED = {
    "OPENAI_API_KEY": "fixture-key-value",
    "OPENAI_BASE_URL": "https://gateway.example.test/v1",
    "DATABASE_URL": "sqlite:///:memory:",
    "APP_SECRET_KEY": "fixture-secret-value",
}


@pytest.fixture
def full_env(monkeypatch: pytest.MonkeyPatch) -> pytest.MonkeyPatch:
    for key, value in REQUIRED.items():
        monkeypatch.setenv(key, value)
    return monkeypatch


def test_settings_load_from_environment(full_env: pytest.MonkeyPatch) -> None:
    settings = load_settings(env_file=None)
    assert settings.openai_base_url == REQUIRED["OPENAI_BASE_URL"]
    assert settings.database_url == REQUIRED["DATABASE_URL"]
    assert settings.openai_api_key.get_secret_value() == REQUIRED["OPENAI_API_KEY"]


@pytest.mark.parametrize("missing", sorted(REQUIRED))
def test_missing_secret_raises_clear_startup_error(
    full_env: pytest.MonkeyPatch, missing: str
) -> None:
    full_env.delenv(missing)
    with pytest.raises(ConfigurationError) as caught:
        load_settings(env_file=None)
    assert missing in str(caught.value)
    assert ".env.example" in str(caught.value)


def test_empty_secret_counts_as_missing(full_env: pytest.MonkeyPatch) -> None:
    full_env.setenv("APP_SECRET_KEY", "")
    with pytest.raises(ConfigurationError, match="APP_SECRET_KEY"):
        load_settings(env_file=None)


def test_startup_error_never_echoes_secret_values(full_env: pytest.MonkeyPatch) -> None:
    full_env.delenv("DATABASE_URL")
    with pytest.raises(ConfigurationError) as caught:
        load_settings(env_file=None)
    for value in REQUIRED.values():
        assert value not in str(caught.value)


def test_secrets_are_hidden_in_repr(full_env: pytest.MonkeyPatch) -> None:
    rendered = repr(load_settings(env_file=None))
    assert REQUIRED["OPENAI_API_KEY"] not in rendered
    assert REQUIRED["APP_SECRET_KEY"] not in rendered
