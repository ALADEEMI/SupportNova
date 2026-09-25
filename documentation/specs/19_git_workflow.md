# 19 — Git Workflow (genuine, traceable history)

The history must reflect real development (SRS 1.8.16) and real contributions of every member (Deliverable 14).
Commit and push work **as it is built** — never batch-replay finished code.

## Branches
- `main` — protected; merges via PR only; CI must pass.
- `feat/<phase>-<slice>-<short-name>` (e.g. `feat/P05-S2-prompt-v1`), `fix/<issue>-<name>`, `test/<area>`, `docs/<topic>`, `data/<dataset-step>`.

## Commits — Conventional Commits with SRS references
`<type>(<scope>): <summary> [SRS refs]` — types: feat, fix, test, docs, refactor, chore, data, ci.
Examples: `feat(validation): enforce mandatory escalation from overlay rules [Step 39, NFR-4]`,
`test(security): add 22 prompt-injection cases [Steps 50-51]`.
Small, focused commits; one logical change each.

## Pull requests
Template `.github/pull_request_template.md`: summary, SRS items covered, acceptance criteria checklist, tests added,
screenshots (UI), AI assistance declaration (links the AI_USAGE.md entry), reviewer checklist.
Every PR gets a real review by another member (comments, requested changes, test run) before merge.

## Who commits what (honest division)
- **Lead engineer:** builds slices with Claude Code, opens PRs.
- **Team members:** review PRs, write/extend tests, run verification against the SRS/RTM, review the dataset and
  documents, write documentation sections, fix defects they find — each on their own branches and accounts.
- `documentation/team_contribution.md` records who did what (including AI assistance) — Deliverable 19.

## CI (`.github/workflows/ci.yml`)
ruff → mypy → pytest (not live_llm) with coverage → `scripts/data_gen/validate_dataset.py` → pip-audit.

## Tags
`rules-freeze-v1` (before hold-out generation), `v1.0.0` (submission).
