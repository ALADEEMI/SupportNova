# P04 — Rule Matrix

## P04-S1 Rule model, DSL evaluator, lexicons
- **SRS:** Step 8; 1.2; D-5 · **Read:** spec 04 §1–3, ADR-017
- **Acceptance:** all ops implemented with word-boundary, case-insensitive phrase matching; lexicon references resolve;
  invalid rule definitions rejected with precise messages; evaluation returns evidence.
- **Tests:** test_dsl_ops.py (each op, true/false), test_rule_validation.py

## P04-S2 Rule engine (Python-expected)
- **SRS:** Steps 19–24, 29–31, 36–39, 42; NFR-4 · **Read:** spec 04 §4, spec 08 §2
- **Acceptance:** deterministic; ambiguity and unclassified flags; overlays raise urgency/escalation; eligibility outcomes;
  priority mapping from config; Step-21 six tricky cases produce the documented results.
- **Tests:** test_rule_engine_classification.py, test_overlays.py, test_eligibility.py, test_urgency_priority.py

## P04-S3 Admin → Rule Matrix UI (editor, condition builder, simulator)
- **SRS:** CI-05, CI-14 · **Read:** spec 04 §8, spec 13
- **Acceptance:** create/edit/deactivate rules with versioning and audit; simulator shows per-rule matches and evidence.
- **Tests:** test_rule_service_crud.py, test_rule_versioning.py

## P04-S4 Batch import/export
- **SRS:** user requirement (batch upload), D-5 · **Read:** spec 04 §7
- **Acceptance:** downloadable template; dry-run report with row-level errors; add/upsert/replace_all modes; export CSV/XLSX/YAML;
  round-trip export→import yields identical active matrix.
- **Tests:** test_rule_import.py, test_rule_export_roundtrip.py

## P04-S5 Author the Zephyra matrix
- **SRS:** Hint (≥100 rules, ≥30 escalation) · **Read:** spec 01 §8–10, spec 04 §6
- **Tasks:** write seed files in complaint_rules/, routing_rules/, escalation_rules/; lexicons in config seed.
- **Acceptance:** ≥100 active rules, ≥30 mandatory escalation conditions, every category ≥5 classification rules, every rule cites an existing doc section; dev-set diagnostic accuracy report generated.
- **Tests:** test_matrix_coverage.py (counts, references exist)
