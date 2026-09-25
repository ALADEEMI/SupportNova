"""Structured JSON logging with PII masking (CLAUDE.md section 7, spec 17 "PII")."""

import json
import logging
from datetime import UTC, datetime

from security.pii import mask_pii

_EXTRA_FIELDS = ("error_ref", "where")


class PiiMaskingFilter(logging.Filter):
    """Masks emails, phones and card-like numbers in the rendered message before handlers see it."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = mask_pii(record.getMessage())
        record.args = None
        return True


class JsonFormatter(logging.Formatter):
    """One JSON object per line; stack traces are masked too because they can contain user data."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "timestamp": datetime.fromtimestamp(record.created, UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": mask_pii(record.getMessage()),
        }
        for field in _EXTRA_FIELDS:
            if hasattr(record, field):
                payload[field] = getattr(record, field)
        if record.exc_info:
            payload["stack_trace"] = mask_pii(self.formatException(record.exc_info))
        return json.dumps(payload, ensure_ascii=False)


def build_handler() -> logging.Handler:
    """Stream handler with JSON output and PII masking."""
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    handler.addFilter(PiiMaskingFilter())
    return handler


def configure_logging(level: str = "INFO") -> None:
    """Replace root handlers with the masked JSON handler (safe to call more than once)."""
    root = logging.getLogger()
    root.handlers = [build_handler()]
    root.setLevel(level.upper())
