# ADR-018 — Verification score and decision policy

## Decision
- Pipeline 2 produces checks `{check_id, status: pass|warn|fail|n/a, severity: critical|major|minor, detail, srs_ref}`.
- **Verification score** = `100 × Σ(w·s) / Σ w` over evaluated checks, `s = 1 / 0.5 / 0` for pass/warn/fail;
  weights from config (critical 3, major 2, minor 1). Always computed, never typed.
- **Decision** (architecture: `Verified | Manual Review`):
  `Verified` iff schema valid AND no `critical` check failed AND score ≥ threshold (config, default 85) AND
  no matched rule has `requires_review = true` (sensitive complaints, Step 57 — e.g. injury, data exposure,
  legal threat) AND category not in `always_review_categories` (config, default empty)
  AND no injection flag combined with a failed promise/action check. Otherwise `Manual Review`
  with machine-readable reasons (the six SRS Step-57 reasons).
- Final result = GenAI output with Python-enforced critical fields (ADR-010); customer response blocked unless Verified or reviewer-approved.

## SRS references
FR xlv–li, Step 57, architecture diagram (Verification Decision), CI-17 (no fabricated values), NFR-4.
