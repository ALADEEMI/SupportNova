# ADR-012 — Dataset generation: spec-first, with an isolated hold-out set

## Context
Hint: ≥500 complaints with quotas; Deliverable 3 requires expected routing/urgency/escalation; Deliverable 8
requires comparison on ≥100 **unseen** complaints; CI-02 unique dataset; AI tool use must be declared.

## Decision
- **Spec-first**: a script builds a *specification* for each complaint (category, subcategory, secondary issues,
  expected department/urgency/priority/escalation, difficulty tags, referenced order/customer) from the rule matrix
  and quotas. An LLM (via CommandCode, a development tool) writes **only the complaint text** for each spec.
  Labels are never produced by an LLM.
- A consistency validator checks every text against its spec (required trigger present for calm-critical, no
  anger words in calm cases, injection string present for adversarial cases, missing fields actually missing…).
- **Dev set: 400** complaints for building and tuning rules/prompts.
- **Hold-out: 100** complaints generated **after the rule freeze**, stored in `sample_complaints/holdout/`,
  never used for tuning; used only by `make eval-holdout` for Deliverable 8.
- All generation is logged in `AI_USAGE.md`.

## SRS references
Hint, Deliverables 3, 4, 8; CI-01, CI-02, CI-19.
