# CLAUDE.md — SupportNova (Zephyra Electronics)

You are building **SupportNova**, a Generative-AI complaint-intelligence web application, for the
Aptech **Techwiz 7** competition (category: Generative AI PowerPlay, theme: ResponseX Intelligence).
The fictional client organization is **Zephyra Electronics** (see `documentation/specs/01_organization_profile.md`).

Read this file fully at the start of every session. It is binding.

---

## 1. Sources of truth (in order of authority)

1. `documentation/srs/SupportNova_SRS_v1.0.pdf` — the official SRS. **Never contradict it. Never drop a requirement.**
2. `documentation/specs/*.md` — detailed specifications derived from the SRS.
3. `documentation/adr/*.md` — architecture decisions (why things are built this way).
4. `documentation/phases/*.md` — the build plan: phases → slices → acceptance criteria.
5. `documentation/SupportNova_RTM.xlsx` — Requirements Traceability Matrix (every SRS item, one row).

If two sources conflict, or a requirement is ambiguous: **stop and ask the user**. Do not guess silently.
If you believe a spec is wrong versus the SRS, say so explicitly and propose a fix.

## 2. Language

- Code, identifiers, comments, docstrings, UI text, commit messages, docs, data files: **English only**.
- The user may talk to you in Arabic. Answer in Arabic in chat, but everything written to the repo is English.

## 3. Non-negotiable rules (violating any of these fails the competition)

1. **No hard-coded business values in code.** Never write a category, subcategory, department, product,
   urgency level, priority, escalation level, SLA value, status, policy ID, tone, or keyword list inside a
   `.py` file. They live in the database (seeded from `config/seed/` and rule files) and are edited from the Admin UI.
   Enumerations used by schemas and prompts are **loaded at runtime** from the configuration service.
2. **No prompts inside Python files.** All prompts live in `prompt_templates/` (seed) and in the
   `prompt_versions` table (runtime, editable from the Admin UI). Code references a prompt by `id@version`.
3. **Pipeline 2 (Python Ground-Truth Validation) is deterministic.** No LLM call, no ML model, no embeddings,
   no probabilistic classifier. Only rules, regex, lookups, arithmetic, string matching (ADR-003).
4. **Pipeline 1 must not receive Pipeline 2 decisions.** The GenAI prompt never contains matched rule IDs,
   Python-expected category, or Python-expected department. Independence is mandatory (ADR-016).
5. **No fabricated outputs.** No fake GenAI responses at runtime, no hard-coded classifications/responses/
   escalations, no invented confidence or verification values. Every score is computed from real checks.
   Mocked LLM responses are allowed **only inside `tests/`** and must be named `fixture_*`.
6. **Uploaded documents and complaint text are untrusted data** (prompt-injection defense, ADR-011).
7. **The rule matrix is never generated at runtime by the GenAI model.**
8. **Outdated policies (Superseded, Draft, expired) are never used as the basis of a final resolution.**
9. **No secrets in the repository.** Keys come from environment variables (`.env`, never committed).
10. **Audit log is append-only.** Never update or delete audit rows.
11. **Every user-facing error is friendly and actionable**; stack traces go to logs only, with an error reference ID shown to the user.
12. **Customer-facing responses are never released unless the complaint is `Verified` or a reviewer approved it.**

## 4. Repository layout (mandatory — SRS Deliverable 2; do not rename)

```
README.md  AI_USAGE.md  requirements.txt  LICENSE  pyproject.toml  .env.example  Makefile
src/                     # application shell
  app/                   # Streamlit UI: Home.py + pages/ + components/
  core/                  # settings, db session, errors, logging, config service, audit service, auth
  services/              # use-case orchestration (the only layer the UI calls)
  api/                   # thin FastAPI wrapper over services (health, analyze, imports) — optional, see ADR-001
templates/               # Jinja2 templates for PDF/HTML reports and follow-up message layouts
static/                  # CSS, logo, icons
complaint_processing/    # intake: validation, normalization, entity regex, dedup, repeat, missing-info
document_processing/     # upload validation, parsing (PDF/DOCX/TXT/MD/EML), chunking, versioning
knowledge_base/          # chunk store access, BM25 index, retrieval, precedence
genai_pipeline/          # Pipeline 1: LLM client, prompt rendering, context builder, call/retry, parsing
python_validation/       # Pipeline 2: rule engine, checks, eligibility, python-expected result
complaint_rules/         # rule matrix seed files: classification rules (CSV/YAML)
routing_rules/           # rule matrix seed files: routing / department mapping
escalation_rules/        # rule matrix seed files: overlay / escalation rules
prompt_templates/        # seed prompt templates (YAML), versioned
schemas/                 # JSON Schemas (single source of truth for GenAI output, imports)
comparison_engine/       # GenAI vs Python comparison, verification score, decision, final result merge
hallucination_checks/    # claim extraction and grounding, unsupported promise detection, contradictions
security/                # injection detection, sanitization, file safety, PII masking, RBAC helpers
database/                # SQLAlchemy models, repositories, Alembic migrations, seeders
tests/                   # pytest suites (unit, integration, e2e, hidden-readiness)
sample_complaints/       # dataset (dev + holdout), master data CSVs
sample_documents/        # Zephyra knowledge-base documents (PDF/DOCX/TXT/MD) + sources
hidden_test_ready/       # packs that simulate the hidden evaluation (new category, revised policy, odd formats)
documentation/           # SRS, specs, ADRs, phases, RTM, report sources, blog draft, video script
screenshots/             # UI screenshots for report/README
reports/                 # generated reports (comparison, intelligence, security)
config/                  # seed/ (initial configuration: core.yaml, lexicons.yaml, settings.yaml) — secrets never here
scripts/                 # dev tooling: data generation, doc rendering, evaluation runners
```

## 5. Architecture in one paragraph

Streamlit UI (thin) → `src/services` (use cases) → domain packages. A complaint flows:
intake validation & preprocessing → dedup/repeat → KB retrieval (BM25 over Active chunks) →
**Pipeline 1** (one structured GenAI call, schema-validated, bounded retry) → **Pipeline 2**
(rule engine computes Python-expected result + ~25 checks on the GenAI output) → **Comparison Engine**
(field-by-field, verification score, decision `Verified | Manual Review`, final result with Python-enforced
critical fields) → review/lifecycle/SLA → dashboards & reports. One relational DB (SQLite dev / PostgreSQL prod).

## 6. How to execute a slice (always follow this loop)

1. Read the slice in `documentation/phases/`, then every spec/ADR it references. Re-read the SRS items it cites.
2. State a short plan (files to create/change, tests to write) before coding.
3. Implement in small, readable functions. Services contain logic; UI only renders and calls services.
4. Write tests that prove each acceptance criterion. Run `make check` (lint + typecheck + tests).
5. Update `documentation/SupportNova_RTM.xlsx` rows touched: Status = Done, Evidence = test names / files.
   Use the `rtm-update` skill.
6. Add an entry to `AI_USAGE.md` describing AI assistance for this slice (tool, purpose, files, changes, tests).
7. Commit using the conventions in `documentation/specs/19_git_workflow.md`.
8. Run the `srs-compliance-review` and `no-hardcode-audit` skills before declaring the slice done.

## 7. Code standards (human, readable, maintainable)

- Python 3.11+. Type hints everywhere. `ruff` for lint+format, `mypy` (non-strict) for types.
- Small modules, small functions (aim < 40 lines), clear names, no clever metaprogramming.
- Docstrings explain **why** and reference SRS items when relevant, e.g. `"""Enforces mandatory escalation (SRS Step 39, NFR-4)."""`
- Pydantic v2 models for all service inputs/outputs. SQLAlchemy 2.0 ORM for persistence (no raw string SQL).
- Errors: raise domain exceptions from `src/core/errors.py` (`ValidationError`, `NotFoundError`,
  `PermissionDeniedError`, `ExternalServiceError`, `ConfigurationError`). Services never return `None` for failures.
- Logging: standard `logging` with JSON formatter from `src/core/logging.py`. No `print`. PII masked.
- Configuration access only via `src/core/config_service.py` (cached, invalidated on admin change).
- No dead code, no commented-out code, no TODO without an issue reference.

## 8. Testing standards

- `pytest` with markers: `unit`, `integration`, `e2e`, `live_llm` (real API, skipped by default), `hidden`.
- Unit tests never hit the network. LLM calls are replaced by recorded fixtures in `tests/fixtures/llm/`.
- Every acceptance criterion in a slice maps to at least one test. Test names describe behavior:
  `test_calm_safety_complaint_is_forced_to_critical_and_escalated`.
- See `documentation/specs/18_testing_strategy.md` for the 20 SRS test categories and file mapping.

## 9. Commands

```
make setup        # venv + install + pre-commit
make seed         # create DB schema (alembic upgrade) and load config/seed + rule files + sample docs
make run          # streamlit run src/app/Home.py
make api          # uvicorn src.api.main:app (optional)
make test         # pytest -m "not live_llm"
make check        # ruff + mypy + tests
make eval-holdout # run the 100 hold-out complaints and write reports/comparison_report.*
```

## 10. Skills installed for this project (in `.claude/skills/`, git-ignored)

- `slice-delivery` — the slice execution loop and Definition of Done.
- `srs-compliance-review` — checks a change against the SRS items it claims to satisfy.
- `no-hardcode-audit` — scans for hard-coded business values, prompts in code, LLM use in Pipeline 2.
- `rtm-update` — updates the RTM workbook status/evidence.
- Official Anthropic skills (see `documentation/specs/20_skills_setup.md`): `docx`, `pdf`, `xlsx` for
  document generation and export; `webapp-testing` for UI tests if available.

## 11. Definition of Done (every slice)

- [ ] All acceptance criteria met and demonstrated by tests.
- [ ] `make check` green.
- [ ] No hard-coded business values; no prompts in code; Pipeline 2 has no AI.
- [ ] Friendly error handling on every new user path.
- [ ] RTM rows updated with evidence.
- [ ] `AI_USAGE.md` entry added.
- [ ] Conventional commit(s) referencing SRS items.

## 12. When in doubt

Ask. A 30-second question is cheaper than a wrong module. Never invent SRS requirements and never silently skip one.
