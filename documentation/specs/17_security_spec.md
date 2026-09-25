# 17 — Security Specification

| Area | Control | SRS |
|---|---|---|
| Authentication | bcrypt (cost 12); lockout after `max_failed_logins` for `lockout_minutes`; generic error "Invalid username or password"; session idle timeout | FR i |
| Authorization | role permissions (ADR-014) checked in services + page guards; object-level filter for customers; tests for every forbidden path | FR ii, D-10 |
| Secrets | `.env` only (`OPENAI_API_KEY`, `OPENAI_BASE_URL`, `DATABASE_URL`, `APP_SECRET_KEY`); `.env.example` committed without values; key never logged/displayed; Render env vars in deployment | D-12, D-14 |
| Prompt injection | ADR-011 (isolation, detection, quarantine, outcome control) | Steps 50–51 |
| Uploads | ADR-013 (magic bytes, size, count, UUID storage, no execution, extracted text untrusted) | Steps 4, 10 |
| Input sanitization | normalization, HTML stripping, length caps; Streamlit output escaped (no `unsafe_allow_html` with user data) | Step 11 |
| Injection (SQL) | ORM only, bound parameters | — |
| Exports | CSV/Excel formula-injection guard; exports audited; role-restricted | Step 68 |
| PII / sensitive data | fictional data only; logs mask emails, phones, card-like numbers; request payloads stored redacted | 1.5, D-10 |
| Audit | ADR-015 | Step 59 |
| Dependencies | pinned `requirements.txt`; `pip-audit` in CI | 1.5 |
| Error handling | no stack traces to users; error refs; GenAI failures degrade to review | FR lxxiv |

## Security test suite (Deliverable 10) — `tests/security/`
prompt-injection complaints (≥20 variants) · unsupported refund request · fake policy statement in complaint ·
invalid policy ID in GenAI output (fixture) · unauthorized compensation request · malicious document instruction
(quarantine) · sensitive data handling (masking in logs) · unauthorized access (customer → admin page/service,
customer → other customer's complaint, agent → rule edit) · upload of disguised executable · CSV injection on export.
`reports/security_report.md` generated from the suite results.
