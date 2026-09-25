"""Application settings read from environment variables (spec 17 "Secrets", Deliverables 12, 14).

Only deployment secrets and infrastructure values live here. Business configuration (categories,
SLA, thresholds, model id, ...) lives in the database and is read through the configuration
service (ADR-004).
"""

from functools import lru_cache

from pydantic import Field, SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.errors import ConfigurationError

DEFAULT_ENV_FILE = ".env"


class Settings(BaseSettings):
    """Environment-backed settings; empty values count as missing so a bare `.env.example` fails."""

    model_config = SettingsConfigDict(
        env_file=DEFAULT_ENV_FILE, env_file_encoding="utf-8", extra="ignore", case_sensitive=False
    )

    openai_api_key: SecretStr = Field(min_length=1)
    openai_base_url: str = Field(min_length=1)
    database_url: str = Field(min_length=1)
    app_secret_key: SecretStr = Field(min_length=1)
    log_level: str = "INFO"


def _missing_variables(error: ValidationError) -> list[str]:
    names = {str(item["loc"][0]).upper() for item in error.errors() if item["loc"]}
    return sorted(names)


def load_settings(env_file: str | None = DEFAULT_ENV_FILE) -> Settings:
    """Build settings, turning validation failures into one clear startup error.

    The error names the variables only; values are never echoed because they may be secrets.
    `env_file=None` reads the process environment only (used by tests).
    """
    try:
        return Settings(_env_file=env_file)  # type: ignore[call-arg]  # values come from env
    except ValidationError as error:
        names = ", ".join(_missing_variables(error))
        raise ConfigurationError(
            f"Missing or empty environment variables: {names}. "
            "Copy .env.example to .env and set a value for each of them."
        ) from None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Process-wide settings, loaded once."""
    return load_settings()
