"""Logs are JSON and never contain emails, phone numbers or card-like numbers (spec 17, P01-S2)."""

import io
import json
import logging
from collections.abc import Iterator

import pytest

from security.pii import CARD_MASK, EMAIL_MASK, PHONE_MASK, mask_pii
from src.core.logging import JsonFormatter, PiiMaskingFilter, configure_logging

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    "text",
    ["jane.doe@example.com", "Contact: j_doe+tag@mail.co.uk please"],
)
def test_emails_are_masked(text: str) -> None:
    masked = mask_pii(text)
    assert EMAIL_MASK in masked
    assert "@" not in masked


@pytest.mark.parametrize(
    "text",
    ["+1 (555) 123-4567", "call 0300-1234567 now", "+92 300 1234567", "555.123.4567"],
)
def test_phone_numbers_are_masked(text: str) -> None:
    masked = mask_pii(text)
    assert PHONE_MASK in masked
    assert sum(ch.isdigit() for ch in masked) < 5


@pytest.mark.parametrize(
    "text",
    ["4111 1111 1111 1111", "card 4111-1111-1111-1111 declined", "5500000000000004"],
)
def test_card_like_numbers_are_masked(text: str) -> None:
    masked = mask_pii(text)
    assert CARD_MASK in masked
    assert "1111" not in masked
    assert "0000" not in masked


@pytest.mark.parametrize(
    "text",
    [
        "Order placed on 2026-09-25",
        "Logged at 2026-09-25 12:30",
        "Order ORD-12345678 shipped",
        "Complaint CMP-2026-000123 received",
        "Warranty is 24 months",
    ],
)
def test_dates_and_business_references_are_not_masked(text: str) -> None:
    assert mask_pii(text) == text


@pytest.fixture
def captured() -> Iterator[tuple[logging.Logger, io.StringIO]]:
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonFormatter())
    handler.addFilter(PiiMaskingFilter())
    logger = logging.getLogger("tests.masking")
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    yield logger, stream
    logger.removeHandler(handler)


def test_log_lines_are_json_with_masked_message_and_args(
    captured: tuple[logging.Logger, io.StringIO],
) -> None:
    logger, stream = captured
    logger.info("Customer %s called from %s", "ali@example.com", "+1 555 123 4567")
    line = json.loads(stream.getvalue())
    assert line["level"] == "INFO"
    assert "ali@example.com" not in line["message"]
    assert "555" not in line["message"]
    assert EMAIL_MASK in line["message"]
    assert PHONE_MASK in line["message"]


def test_stack_traces_are_masked(captured: tuple[logging.Logger, io.StringIO]) -> None:
    logger, stream = captured
    try:
        raise RuntimeError("payment 4111 1111 1111 1111 failed for bob@example.com")
    except RuntimeError:
        logger.exception("Payment step failed")
    line = json.loads(stream.getvalue())
    assert "Traceback" in line["stack_trace"]
    assert "4111" not in line["stack_trace"]
    assert "bob@example.com" not in line["stack_trace"]


def test_configure_logging_installs_one_masked_json_handler() -> None:
    root = logging.getLogger()
    saved_handlers, saved_level = root.handlers[:], root.level
    try:
        configure_logging("warning")
        configure_logging("warning")
        assert len(root.handlers) == 1
        handler = root.handlers[0]
        assert isinstance(handler.formatter, JsonFormatter)
        assert any(isinstance(f, PiiMaskingFilter) for f in handler.filters)
        assert root.level == logging.WARNING
    finally:
        root.handlers, root.level = saved_handlers, saved_level
