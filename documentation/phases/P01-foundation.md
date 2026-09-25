# P01 — Foundation

## P01-S1 Repository skeleton & tooling
- **SRS:** Deliverable 2, 14; 1.9.2 · **Read:** CLAUDE.md §4, ADR-001, spec 19
- **Tasks:** create mandatory folder structure (with `__init__.py` where packages); `pyproject.toml` (ruff, mypy, pytest config, markers);
  pinned `requirements.txt`; `Makefile` targets (CLAUDE.md §9); `.env.example`; `.gitignore`; `LICENSE` (MIT); `README.md` skeleton
  with all required sections as headings; `AI_USAGE.md` with template; `.github/pull_request_template.md`; CI workflow; pre-commit.
- **Acceptance:** `make setup && make check` passes on a clean clone; all 29 mandatory paths from Deliverable 2 exist; CI runs on PR.
- **Tests:** `tests/test_repo_structure.py` asserts mandatory paths exist.

## P01-S2 Core: settings, logging, errors
- **Read:** CLAUDE.md §7, spec 17
- **Tasks:** `src/core/settings.py` (env via pydantic-settings; secrets only from env); JSON logging with PII masking filter;
  domain exception hierarchy; `error_ref` generator + `app_errors` persistence; UI error helper that shows friendly message + ref.
- **Acceptance:** missing secret → clear startup error; logs mask emails/phones/card-like numbers; unhandled exception in a service → user sees message + ref, log has stack trace.
- **Tests:** test_settings.py, test_logging_masking.py, test_error_refs.py

## P01-S3 Database & migrations
- **SRS:** Steps 5–7, 49, 59; NFR-2 · **Read:** spec 03, ADR-002, ADR-015
- **Tasks:** SQLAlchemy models for all tables in spec 03; Alembic initial migration; session management; repositories (typed);
  append-only guard for audit_log (repository has no update/delete; PostgreSQL trigger in migration).
  Register the `app_errors` ErrorSink with `set_error_sink` (hook added in P01-S2).
- **Acceptance:** `alembic upgrade head` works on SQLite and PostgreSQL; indexes present; audit update/delete impossible via repository and raises at DB level on PostgreSQL.
- **Tests:** test_models_roundtrip.py, test_audit_append_only.py

## P01-S4 Configuration service & seeding
- **SRS:** Steps 14, 20, 55; CI-05, CI-14 · **Read:** spec 02, ADR-004, `config/seed/*.yaml`
- **Tasks:** seed loader for `config/seed/` (taxonomy, departments, vocabularies, levels, priority mapping, SLA, statuses & transitions,
  actions, lexicons, settings, checks catalog, ui filters, role permissions, doc categories, topics, precedence);
  `ConfigService` (cached reads, invalidation, typed accessors, list enums for schema); export/import YAML.
- **Acceptance:** `make seed` idempotent; every list in spec 02 queryable; changing a value in DB is visible after invalidate without restart.
- **Tests:** test_seed_idempotent.py, test_config_service_cache.py

## P01-S5 Authentication & RBAC
- **SRS:** FR i–ii; D-10, D-15 · **Read:** ADR-014, spec 17
- **Tasks:** AuthService (bcrypt, lockout, idle timeout); `require_permission` decorator for services; Streamlit page guard;
  login page; role-based sidebar; seed users (admin, evaluator, manager, 2 reviewers, 4 agents, demo customers) with passwords from env `SEED_PASSWORD_*`.
- **Acceptance:** each role sees only its pages; direct URL to forbidden page shows "not authorized"; customer cannot load another customer's complaint via service; lockout works.
- **Tests:** tests/security/test_rbac_matrix.py (every permission × role), test_login_lockout.py, test_object_level_access.py

## P01-S6 LLM client & prompt registry
- **SRS:** Pipeline 1, Steps 47–49 · **Read:** ADR-006, ADR-007, spec 06, spec 07
- **Tasks:** `OpenAICompatibleClient` (base_url, model, timeout, structured-output flag, usage capture); `FixtureLLMClient` (tests only);
  prompt seed import; PromptService (get active, render with placeholder validation); System Health self-test.
- **Acceptance:** self-test reports model id, latency, structured-output support; rendering fails loudly on missing placeholder; no prompt text in `.py`.
- **Tests:** test_llm_client_fixture.py, test_prompt_render.py, test_live_smoke.py (`live_llm`)

**Gate:** app starts, login works, config seeded, self-test green.
