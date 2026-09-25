# AI Tool Usage Declaration (SRS 1.8.19 and Deliverable 18)

Generative AI APIs are part of the application architecture (Pipeline 1). This file declares AI tools used
**during development**. Every AI-assisted change was reviewed, modified where required, tested and understood by the
listed team member(s).

| ID | Date | Tool (and model) | Purpose | Type of assistance | Files / modules affected | Modifications made by team | Tests performed | Verified by |
|---|---|---|---|---|---|---|---|---|
| AI-001 | YYYY-MM-DD | Claude (claude.ai) | Requirements analysis and planning | Read SRS, produced RTM, ADRs, specs, phase plan | documentation/ | Reviewed against SRS, corrected decisions (e.g. document versioning table) | Manual review against SRS | <name> |
| AI-002 | 2026-09-25 | Claude Code (claude-opus-5-5) | Implement slice P01-S1 (repository skeleton & tooling) | Generated folder structure, package docstrings, pyproject.toml, pinned requirements, Makefile, pre-commit, CI workflow, .env.example, LICENSE, README skeleton, repository tests; updated RTM | src/, 13 domain packages, data folders (README.md each), pyproject.toml, requirements*.txt, Makefile, .pre-commit-config.yaml, .github/workflows/ci.yml, .env.example, .gitattributes, LICENSE, README.md, tests/test_repo_structure.py, tests/test_repo_tooling.py, documentation/SupportNova_RTM.xlsx | Python floor raised to 3.12 (pinned NumPy requires it); <team review changes> | make setup && make check on a clean clone (89 tests), pip-audit clean | Mohanned AL-Adeemi |
| AI-003 | YYYY-MM-DD | CommandCode gateway (<model id>) | Dataset text generation | Wrote complaint texts from team-designed specs (labels by team) | sample_complaints/ | <regenerated/edited N texts> | validate_dataset.py | <name> |
| AI-004 | 2026-09-25 | Claude Code (claude-opus-5-5) | Implement slice P01-S2 (settings, logging, errors) | Generated settings loader, PII masking, JSON logging, domain exceptions, error refs, error box component and tests | src/core/settings.py, src/core/logging.py, src/core/errors.py, security/pii.py, src/app/components/error_box.py, tests/core/, documentation/SupportNova_RTM.xlsx, documentation/phases/P01-foundation.md | <team review changes> | make check (126 tests), AppTest page shows error box with reference | Pending review |
