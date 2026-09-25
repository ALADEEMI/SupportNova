"""A page whose service call fails unexpectedly; it must show the error box, not a traceback."""

from src.app.components.error_box import run_guarded


def _broken_service() -> float:
    return 1 / 0


run_guarded(_broken_service, where="FailingPage.load")
