"""Error box component: friendly message, next action and error reference (spec 13 "Errors")."""

from collections.abc import Callable

import streamlit as st

from src.core.errors import UserFacingError, capture_exception


def show_error(error: UserFacingError) -> None:
    """Render a failure without technical details."""
    st.error(f"{error.message}\n\n{error.action}\n\nReference: `{error.error_ref}`")


def run_guarded[T](action: Callable[[], T], *, where: str, user_id: int | None = None) -> T | None:
    """Call a service from a page; on failure show the error box and return None, never crash."""
    try:
        return action()
    except Exception as exc:
        show_error(capture_exception(exc, where=where, user_id=user_id))
        return None
