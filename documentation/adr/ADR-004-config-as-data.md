# ADR-004 — Configuration as data, managed from the Admin UI

## Context
Hidden evaluation adds new categories, subcategories, routing rules and escalation conditions and must be
processed **without changing core source code**. Live modification asks to add a category/department, change
priority logic, escalation thresholds, SLA, validation rules, dashboard filters (CI-14).

## Decision
- Every business list and threshold is a database row, seeded from `config/seed/*.yaml` and rule files, and
  editable from the Admin UI (full catalog: `specs/02_config_catalog.md`).
- Code reads configuration only through `ConfigService` (cached; cache invalidated on every admin write).
- Enumerations for JSON Schema, prompts, dropdowns and filters are generated from configuration at runtime.
- Every admin change writes an audit entry (who, when, before, after).
- Export/Import of configuration and rules (YAML/CSV/XLSX) for backup and batch changes.

## Consequences
- A new category appears everywhere (prompt, schema, validation, UI, reports) with zero code changes.
- Tests must include a "new category added at runtime" scenario (`tests/hidden/`).

## SRS references
Steps 14, 20, 22, 33, 37, 55, 60, 66; CI-03, CI-05, CI-14; Hidden Evaluation Dataset.
