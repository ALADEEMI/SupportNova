# ADR-009 — Document precedence for contradictions

## Context
CI-10: evaluators provide an active policy, an outdated SOP and a conflicting FAQ; the application must apply
**documented** policy-precedence rules.

## Decision
- Precedence is configuration (`precedence_rules` table), default order by document category:
  `Policy (Active)` > `SLA` > `SOP (Active)` > `Escalation Procedure` > `Guidelines` > `Response Templates` > `FAQ`.
  Superseded, Previous, Draft and expired documents are never eligible.
- Every document has `topics` (configured tags linked to categories, e.g. `refund`, `delivery`).
- Contradiction rule: if the GenAI cites a lower-precedence document on a topic for which an in-force
  higher-precedence document exists, Pipeline 2 raises `CONTRADICTION_PRECEDENCE` and the final result cites the
  higher-precedence source.
- A curated **conflict register** (admin-editable) lists known conflicting clauses (e.g. FAQ 14-day refund vs
  Policy 30-day) — used for explanation in the UI and reports.
- The precedence order is documented in `sample_documents` as `ZEP-PRC-001 Document Precedence Rules`.

## SRS references
CI-10, Step 7, Step 26, Step 57 (policy contradiction → manual review), Hint (≥20 contradictory policy cases).
