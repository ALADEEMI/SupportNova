"""Failures reach users as a friendly message plus reference; stack traces go to logs (P01-S2)."""

import logging
import re
from collections.abc import Iterator
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from src.core import errors
from src.core.errors import (
    ConfigurationError,
    ExternalServiceError,
    NotFoundError,
    PermissionDeniedError,
    ValidationError,
    capture_exception,
    new_error_ref,
    set_error_sink,
)

pytestmark = pytest.mark.unit

ERROR_REF_PATTERN = re.compile(r"^ERR-[0-9A-F]{6}$")


class RecordingSink:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str, int | None]] = []

    def record(self, error_ref: str, where: str, message: str, user_id: int | None) -> None:
        self.rows.append((error_ref, where, message, user_id))


class BrokenSink:
    def record(self, error_ref: str, where: str, message: str, user_id: int | None) -> None:
        raise OSError("database unavailable")


@pytest.fixture
def sink() -> Iterator[RecordingSink]:
    recording = RecordingSink()
    set_error_sink(recording)
    yield recording
    set_error_sink(errors._NoopSink())


def _failing_service() -> None:
    raise KeyError("internal_column_name")


def test_error_ref_has_quotable_format_and_is_random() -> None:
    refs = {new_error_ref() for _ in range(200)}
    assert all(ERROR_REF_PATTERN.match(ref) for ref in refs)
    assert len(refs) > 190


def test_unhandled_exception_gives_friendly_message_and_ref(sink: RecordingSink) -> None:
    try:
        _failing_service()
    except KeyError as exc:
        shown = capture_exception(exc, where="TestService.run", user_id=7)
    assert ERROR_REF_PATTERN.match(shown.error_ref)
    assert "internal_column_name" not in shown.message + shown.action
    assert "KeyError" not in shown.message + shown.action
    assert sink.rows == [(shown.error_ref, "TestService.run", sink.rows[0][2], 7)]


def test_unhandled_exception_logs_stack_trace_with_same_ref(
    sink: RecordingSink, caplog: pytest.LogCaptureFixture
) -> None:
    try:
        _failing_service()
    except KeyError as exc:
        with caplog.at_level(logging.ERROR, logger=errors.__name__):
            shown = capture_exception(exc, where="TestService.run")
    record = caplog.records[-1]
    assert record.exc_info is not None
    assert getattr(record, "error_ref") == shown.error_ref  # noqa: B009
    assert "_failing_service" in caplog.text


@pytest.mark.parametrize("error_cls", [ValidationError, NotFoundError, PermissionDeniedError])
def test_expected_user_errors_are_warnings_and_not_persisted(
    sink: RecordingSink, caplog: pytest.LogCaptureFixture, error_cls: type[errors.SupportNovaError]
) -> None:
    with caplog.at_level(logging.WARNING, logger=errors.__name__):
        shown = capture_exception(error_cls("internal detail"), where="TestService.run")
    assert shown.message == error_cls.default_message
    assert "internal detail" not in shown.message
    assert caplog.records[-1].levelno == logging.WARNING
    assert caplog.records[-1].exc_info is None
    assert sink.rows == []


@pytest.mark.parametrize("error_cls", [ExternalServiceError, ConfigurationError])
def test_serious_domain_errors_are_persisted(
    sink: RecordingSink, error_cls: type[errors.SupportNovaError]
) -> None:
    shown = capture_exception(error_cls("gateway timeout"), where="TestService.run")
    assert shown.message == error_cls.default_message
    assert [row[0] for row in sink.rows] == [shown.error_ref]


def test_specific_user_message_overrides_default() -> None:
    error = ValidationError("len=3", user_message="The description must be at least 30 characters.")
    assert capture_exception(error, where="t").message.startswith("The description")


def test_persisted_message_is_pii_masked(sink: RecordingSink) -> None:
    capture_exception(RuntimeError("failed for ali@example.com"), where="t")
    assert "ali@example.com" not in sink.rows[0][2]


def test_broken_sink_does_not_hide_original_error() -> None:
    set_error_sink(BrokenSink())
    try:
        shown = capture_exception(RuntimeError("boom"), where="t")
    finally:
        set_error_sink(errors._NoopSink())
    assert ERROR_REF_PATTERN.match(shown.error_ref)


def test_page_shows_error_box_with_ref_instead_of_crashing() -> None:
    app = AppTest.from_file(str(Path(__file__).parent / "streamlit_apps" / "failing_page.py"))
    app.run()
    assert not app.exception
    assert len(app.error) == 1
    shown = app.error[0].value
    assert re.search(r"Reference: `ERR-[0-9A-F]{6}`", shown)
    assert "Traceback" not in shown
    assert "ZeroDivisionError" not in shown
