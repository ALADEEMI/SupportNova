# ADR-015 — Append-only audit trail

## Decision
- Table `audit_log(id, occurred_at, actor_id, actor_role, entity_type, entity_id, event, before JSON, after JSON, reason, request_id)`.
- Written by `AuditService` for: complaint lifecycle, analysis runs, decisions, every reviewer action,
  config/rule/prompt/document changes, logins/failed logins, exports.
- Repository exposes insert and read only. A DB trigger (PostgreSQL) / test ensures no UPDATE/DELETE.
- Reviewer override: original GenAI result, Python result, final result and reviewer decision all remain (Step 59).

## SRS references
Step 59, FR lxiii–lxiv, CI-18 (audit logic not replaced by GenAI).
