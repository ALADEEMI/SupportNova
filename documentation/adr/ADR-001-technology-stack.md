# ADR-001 — Technology stack

## Context
SRS 1.9.2 allows Streamlit/Flask/Django/FastAPI, Python, several DBs and GenAI APIs. We have four days,
five user roles, many dashboards, and must deploy with ≥99% availability (NFR-5).

## Decision
| Layer | Choice |
|---|---|
| UI | **Streamlit** multipage app (`src/app`), role-guarded pages |
| Application logic | Python service layer (`src/services`) — pure Python, UI-independent, Pydantic I/O |
| Optional REST API | **FastAPI** thin wrapper (`src/api`) over the same services: `/health`, `/complaints`, `/complaints/{id}/analyze`, `/imports` — built only after all mandatory slices pass |
| Persistence | SQLAlchemy 2.0 + Alembic; SQLite (local) / PostgreSQL (deployed) |
| Validation | Pydantic v2 + `jsonschema` |
| Documents | PyMuPDF (PDF), python-docx (DOCX), stdlib `email` (EML), plain readers (TXT/MD) |
| Retrieval | `rank-bm25` (ADR-016) |
| Similarity for dedup | `rapidfuzz` (deterministic string similarity) |
| GenAI | `openai` Python SDK with configurable `base_url` (ADR-007) |
| Charts | Plotly |
| Exports | pandas (CSV), openpyxl (Excel), ReportLab or WeasyPrint-free HTML→PDF via ReportLab (PDF) |
| Auth | bcrypt password hashing, Streamlit session state |
| Tests | pytest, pytest-cov; Playwright (optional UI smoke) |
| Quality | ruff, mypy, pre-commit, GitHub Actions CI, pip-audit |
| Deployment | Render: one web service (Streamlit) + managed PostgreSQL; paid instance during evaluation |

## Consequences
- Fastest path to many role dashboards; logic stays testable outside Streamlit.
- Streamlit runs long calls synchronously; batch jobs run in a background worker thread with progress stored in DB (`import_jobs`).
- Free hosting tiers sleep when idle — use a paid instance during evaluation week to satisfy NFR-5.

## SRS references
1.2 (web-based, Python, GenAI APIs), 1.9.2, NFR-1, NFR-3, NFR-5.
