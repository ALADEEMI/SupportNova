"""PII masking for logs and stored payloads (spec 17 "PII / sensitive data", SRS 1.5).

The patterns are a technical security control, not business configuration: logging must be able
to mask data before the database or the configuration service is available. Over-masking is
preferred to leaking.
"""

import re

EMAIL_MASK = "[EMAIL]"
CARD_MASK = "[CARD]"
PHONE_MASK = "[PHONE]"

_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# 13-19 digits, optionally grouped by spaces or dashes; not glued to letters or identifier dashes.
_CARD = re.compile(r"(?<![\w-])(?:\d[ -]?){12,18}\d(?![\w-])")
# Optional +country code, then digit groups separated by space, dot, dash or parentheses.
_PHONE = re.compile(r"(?<![\w-])(?:\+\d{1,3}[\s.-]?)?(?:\(?\d{2,5}\)?[\s.-]?){1,4}\d{2,7}(?![\w-])")
_ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_MIN_PHONE_DIGITS = 9
_MAX_PHONE_DIGITS = 15


def _mask_phone(match: re.Match[str]) -> str:
    candidate = match.group(0)
    digits = sum(ch.isdigit() for ch in candidate)
    if _ISO_DATE.match(candidate):  # "2026-09-25 12:30" is a timestamp, not a phone
        return candidate
    if _MIN_PHONE_DIGITS <= digits <= _MAX_PHONE_DIGITS:
        return PHONE_MASK
    return candidate


def mask_pii(text: str) -> str:
    """Replace emails, card-like numbers and phone numbers with placeholders.

    Cards are masked before phones so a card number is never reported as a phone.
    """
    masked = _EMAIL.sub(EMAIL_MASK, text)
    masked = _CARD.sub(CARD_MASK, masked)
    return _PHONE.sub(_mask_phone, masked)
