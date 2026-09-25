"""Domain exceptions, error references and the single place where failures become friendly messages.

Every user-facing error shows a friendly message, what to do next and an error reference such as
`ERR-7F3A21`. The stack trace goes to the log only (CLAUDE.md rule 11, spec 13 "Errors",
spec 17 "Error handling", FR lxxiv).
"""

import logging
import secrets
from typing import ClassVar, Protocol

from pydantic import BaseModel, ConfigDict

from security.pii import mask_pii

logger = logging.getLogger(__name__)

ERROR_REF_PREFIX = "ERR-"
_ERROR_REF_BYTES = 3

UNEXPECTED_MESSAGE = "Something went wrong while processing your request."
UNEXPECTED_ACTION = (
    "Please try again. If the problem continues, contact support and quote the reference."
)


class SupportNovaError(Exception):
    """Base class for expected failures raised by services.

    Subclasses define a default friendly message and next action; callers may pass a more specific,
    user-safe message. `detail` is for logs only and is never shown to users.
    """

    default_message: ClassVar[str] = UNEXPECTED_MESSAGE
    default_action: ClassVar[str] = UNEXPECTED_ACTION
    log_level: ClassVar[int] = logging.ERROR

    def __init__(self, detail: str = "", *, user_message: str | None = None) -> None:
        super().__init__(detail or self.default_message)
        self.detail = detail
        self.user_message = user_message or self.default_message
        self.user_action = self.default_action


class ValidationError(SupportNovaError):
    """Input that breaks a rule the user can fix."""

    default_message = "Some of the information provided is not valid."
    default_action = "Check the highlighted fields and try again."
    log_level = logging.WARNING


class NotFoundError(SupportNovaError):
    """A referenced record does not exist or is not visible to the actor."""

    default_message = "The requested item could not be found."
    default_action = "Check the reference and try again."
    log_level = logging.WARNING


class PermissionDeniedError(SupportNovaError):
    """The actor's role does not grant the requested permission (ADR-014)."""

    default_message = "You are not authorized to perform this action."
    default_action = "Contact an administrator if you need access."
    log_level = logging.WARNING


class ExternalServiceError(SupportNovaError):
    """A dependency such as the GenAI gateway failed or timed out."""

    default_message = "An external service is temporarily unavailable."
    default_action = (
        "Please try again in a few minutes. If it continues, contact support with the reference."
    )


class ConfigurationError(SupportNovaError):
    """Missing or invalid configuration (environment or database)."""

    default_message = "The application is not configured correctly."
    default_action = "Ask an administrator to check the configuration on the System Health page."


class UserFacingError(BaseModel):
    """What the UI shows for a failure: never a stack trace, SQL or secret."""

    model_config = ConfigDict(frozen=True)

    message: str
    action: str
    error_ref: str


class ErrorSink(Protocol):
    """Destination for serious errors (the `app_errors` table, shown on System Health)."""

    def record(self, error_ref: str, where: str, message: str, user_id: int | None) -> None: ...


class _NoopSink:
    """Default until the database sink is registered; the log line already carries the reference."""

    def record(self, error_ref: str, where: str, message: str, user_id: int | None) -> None:
        return None


_sink: ErrorSink = _NoopSink()


def set_error_sink(sink: ErrorSink) -> None:
    """Register where serious errors are persisted (called once at application start-up)."""
    global _sink
    _sink = sink


def new_error_ref() -> str:
    """Short, random, human-quotable reference, e.g. `ERR-7F3A21`."""
    return ERROR_REF_PREFIX + secrets.token_hex(_ERROR_REF_BYTES).upper()


def _describe(exc: BaseException) -> tuple[str, str, int]:
    if isinstance(exc, SupportNovaError):
        return exc.user_message, exc.user_action, exc.log_level
    return UNEXPECTED_MESSAGE, UNEXPECTED_ACTION, logging.ERROR


def _record_safely(error_ref: str, where: str, exc: BaseException, user_id: int | None) -> None:
    """Persist without ever hiding the original failure behind a sink failure."""
    message = mask_pii(f"{type(exc).__name__}: {exc}")
    try:
        _sink.record(error_ref, where, message, user_id)
    except Exception:
        logger.exception("Could not persist error %s", error_ref, extra={"error_ref": error_ref})


def capture_exception(
    exc: BaseException, *, where: str, user_id: int | None = None
) -> UserFacingError:
    """Log a failure with a new reference and return the friendly view of it.

    Serious failures (unexpected exceptions, external service and configuration errors) are
    logged with their stack trace and persisted through the error sink; expected user errors are
    logged as warnings.
    """
    error_ref = new_error_ref()
    message, action, level = _describe(exc)
    is_serious = level >= logging.ERROR
    logger.log(
        level,
        "Error %s in %s: %s",
        error_ref,
        where,
        exc,
        exc_info=exc if is_serious else None,
        extra={"error_ref": error_ref, "where": where},
    )
    if is_serious:
        _record_safely(error_ref, where, exc, user_id)
    return UserFacingError(message=message, action=action, error_ref=error_ref)
