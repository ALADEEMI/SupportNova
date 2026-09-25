# ADR-006 — Prompt template management and versioning

## Context
Step 48: prompts centrally stored and versioned; no uncontrolled prompts in source code.
Step 49: each analysis stores prompt version, provider, model, timestamp, policy version.
User requirement: prompts editable, addable, deletable from the UI with traceability.

## Decision
- Seed templates live in `prompt_templates/<prompt_id>/v<semver>.yaml`, imported at first seed.
- Runtime store: `prompt_versions` table (prompt_id, version, status Draft/Active/Retired, system_template,
  user_template, required_placeholders, changelog, author, created_at, activated_at, schema_version).
- Admin UI: list, view, diff two versions, **clone to new version**, edit Draft, preview-render with a sample
  complaint, validate placeholders, activate (exactly one Active per prompt_id), retire.
- Versions that have been used by an analysis run are **immutable** (editing creates a new version).
  "Delete" is allowed only for never-used Drafts; otherwise "Retire".
- Export all versions back to YAML files (for the repo and the report's "Prompt versions" section).

## Consequences
Full reproducibility of every analysis; evidence for Deliverable 6.

## SRS references
Steps 48–49, FR lii–liii, Deliverable 6, CI-15 (prompt template defect).
