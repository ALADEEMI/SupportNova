# ADR-017 — Rule matrix model: rule types and condition DSL

## Decision
Every rule has the 12 Deliverable-5 columns plus `rule_type`, `conditions`, `status`, `version`, `weight`.

**Rule types**
- `classification` — detects a category/subcategory and sets its defaults (department, base urgency, priority,
  required/prohibited actions, follow-up, policy reference).
- `overlay` — applies on top of any (or listed) category: raises urgency floor, forces escalation/level, adds
  required/prohibited actions, adds a supporting department (e.g. legal threat, repeat unresolved, high-value dispute).
- `eligibility` — decides whether an action that needs eligibility (refund, replacement, compensation, fee waiver)
  is `permitted`, `not_permitted`, or `requires_verification` (data missing).

**Condition DSL (JSON)**: `{"all":[...], "any":[...], "none":[...]}` of `{"field","op","value"}`.
Fields come from a computed *complaint context* (text, product_category, customer_type, amounts, days since
order/delivery, warranty/subscription active, prior complaints, attachments, requested_resolution, channel…).
Ops: `contains_any, contains_all, not_contains, regex, eq, neq, in, not_in, gt, gte, lt, lte, is_true, is_false, is_empty, not_empty`.
Values may reference reusable lexicons: `"@lexicon:safety_terms"`.
Full specification: `specs/04_rule_matrix_spec.md`.

**Admin UI**: table editor, form-based condition builder + validated JSON editor, **rule simulator** (test a rule
against any text/complaint), import/export CSV/XLSX/YAML with dry-run validation report, versioned edits.

## SRS references
Step 8, 1.2 (matrix contents), Deliverable 5, Steps 20–23, 28–31, 36–39, CI-05, CI-07, CI-14, Hint (≥100 rules, ≥30 escalation).
