# P02 — Configuration & Taxonomy Admin

## P02-S1 Admin → Configuration screens
- **SRS:** Steps 14–15, 20, 22, 33, 37, 55–56, 60, 66; CI-05, CI-14 · **Read:** spec 02, spec 13 §1
- **Tasks:** tabbed screens for every item in spec 02 (Taxonomy, Departments, Products (+CSV import), Customer types, Lists,
  Levels, Priority logic, SLA, Lifecycle, Actions, Lexicons, Verification (weights, threshold, critical checks, checks catalog),
  Retrieval/GenAI params, Upload limits, Intake limits, Trend params, Dashboard filters, Security, Organization).
  Generic CRUD component with validation, deactivate instead of delete when referenced, audit on every change, cache invalidation.
- **Acceptance:** adding a category + subcategory appears immediately in form dropdowns, schema enums, prompt allowed values,
  rule editor dropdowns and dashboard filters; referenced items cannot be hard-deleted (clear message); every change in audit log.
- **Tests:** tests/config/test_add_category_propagates.py, test_referential_protection.py, test_config_audit.py

## P02-S2 Configuration export/import
- **Tasks:** export all configuration to YAML; import with dry-run diff and confirmation.
- **Acceptance:** export → import on a fresh DB reproduces identical configuration.
- **Tests:** test_config_export_import_roundtrip.py
