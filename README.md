# SupportNova — Complaint Resolution Intelligence for Zephyra Electronics

SupportNova is a Generative-AI web application that analyses customer complaints for the fictional
consumer-electronics company **Zephyra Electronics**. Every complaint is analysed twice:

1. **Pipeline 1 — GenAI:** one structured, schema-validated call to a GenAI model grounded in the company knowledge base.
2. **Pipeline 2 — Python ground-truth validation:** a deterministic rule engine and checks (no AI).

A comparison engine merges both results, computes a verification score and decides `Verified` or `Manual Review`.

Built for the Aptech **Techwiz 7** competition (Generative AI PowerPlay — ResponseX Intelligence).

> Status: under active development. Sections marked *(to be completed)* are filled in by the slice named next to them.

## Table of contents
- [Architecture](#architecture)
- [Technology stack](#technology-stack)
- [Repository structure](#repository-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Evaluation](#evaluation)
- [Testing](#testing)
- [Assumptions](#assumptions)
- [Limitations](#limitations)
- [Blog](#blog)
- [Demonstration video](#demonstration-video)
- [AI usage](#ai-usage)
- [Team](#team)
- [License](#license)

## Architecture
Streamlit UI (thin) → `src/services` (use cases) → domain packages. A complaint flows through intake validation and
preprocessing → duplicate/repeat detection → knowledge-base retrieval (BM25 over active chunks) → Pipeline 1 →
Pipeline 2 → comparison engine → review, lifecycle and SLA → dashboards and reports. One relational database
(SQLite in development, PostgreSQL in deployment). Architecture decisions: [`documentation/adr/`](documentation/adr/).

## Technology stack
See [ADR-001](documentation/adr/ADR-001-technology-stack.md). Summary (SRS 1.9.2):

| Area | Choice |
|---|---|
| Frontend / backend | Streamlit (optional FastAPI wrapper) |
| Language | Python 3.12+ |
| IDE | Visual Studio Code / PyCharm |
| GenAI API | OpenAI API through an OpenAI-compatible gateway ([ADR-007](documentation/adr/ADR-007-genai-gateway.md)) |
| Document processing | PyMuPDF, python-docx, stdlib `email` |
| Data processing | pandas, NumPy |
| Validation | Pydantic v2, JSON Schema, regular expressions, Python rule engine |
| Retrieval | BM25 (`rank-bm25`) ([ADR-016](documentation/adr/ADR-016-retrieval-and-independence.md)) |
| Database | SQLite (local) / PostgreSQL (deployed), SQLAlchemy 2.0 + Alembic |
| Visualization | Plotly |
| Version control | Git and GitHub |
| Deployment | Render |

## Repository structure
| Path | Purpose |
|---|---|
| `src/` | Application shell: `app/` (Streamlit UI), `core/`, `services/`, `api/` |
| `templates/`, `static/` | Report/message templates; CSS and images |
| `complaint_processing/` | Intake validation, normalization, dedup, missing-info detection |
| `document_processing/` | Upload validation, parsing, chunking, versioning |
| `knowledge_base/` | Chunk store, BM25 retrieval, document precedence |
| `genai_pipeline/` | Pipeline 1 |
| `python_validation/` | Pipeline 2 (deterministic) |
| `comparison_engine/` | Comparison, verification score, decision |
| `hallucination_checks/` | Claim grounding, unsupported promises, contradictions |
| `security/` | Injection defence, sanitization, file safety, PII masking |
| `database/` | Models, repositories, migrations, seeders |
| `complaint_rules/`, `routing_rules/`, `escalation_rules/` | Rule-matrix seed files |
| `prompt_templates/`, `schemas/` | Versioned prompts; JSON Schemas |
| `config/` | Seed configuration (no secrets) |
| `sample_complaints/`, `sample_documents/`, `hidden_test_ready/` | Datasets and hidden-evaluation packs |
| `tests/` | Test suites |
| `documentation/`, `reports/`, `screenshots/` | SRS, specs, ADRs, generated reports, screenshots |
| `scripts/` | Data generation and evaluation tooling |

## Installation

### Python installation
Install Python 3.12 or newer (the pinned NumPy release requires 3.12) from [python.org](https://www.python.org/downloads/).
Check with `python --version` (Windows: `py -3.12 --version`).

### Virtual environment setup
`make setup` creates `.venv/`, installs all dependencies and the pre-commit hooks. If `python` on your PATH is not
3.12+, pass the interpreter explicitly, e.g. `make setup PYTHON="py -3.12"`. On Windows without GNU make, use
`mingw32-make` or run the commands in the `Makefile` by hand.

### Dependency installation
Runtime dependencies are pinned in `requirements.txt`; development tools in `requirements-dev.txt`
(`make setup` installs both).

### GenAI API configuration
Set `OPENAI_API_KEY` and `OPENAI_BASE_URL` in `.env`. The model id and generation settings are edited in
Admin → Configuration. *(to be completed in P01-S6)*

### Secure API-key storage
Copy `.env.example` to `.env` and fill in the values. `.env` is git-ignored; keys are read only from environment
variables and are never logged or displayed. In deployment, set them as Render environment variables.

### Database configuration
Set `DATABASE_URL` (SQLite for local use, PostgreSQL in deployment), then run `make seed`. *(to be completed in P01-S3/S4)*

### Knowledge-base setup
*(to be completed in P03 / P11)*

### Complaint dataset setup
*(to be completed in P11)*

### Application startup
`make run` starts the Streamlit app. *(to be completed in P01-S5)*

### Test execution
`make test` runs all tests except those calling the real GenAI API; `make check` runs lint, type check and tests.

### Troubleshooting
- **Windows: `pip` fails with `OSError: No such file or directory` during `make setup`.** The checkout path is too
  deep for the 260-character Windows path limit. Clone to a shorter path (e.g. `C:\dev\SupportNova`) or enable
  Windows long-path support.

*(further entries added in P12)*

## Usage
*(each flow is documented in P12-S3)*

### Login
### Upload company documents
### Configure complaint rules
### Submit complaint
### Analyze complaint
### Review GenAI output
### Run Python validation
### Review mismatches
### Generate response
### Escalate complaint
### Review manual queue
### Track complaint
### View analytics
### Generate reports

## Evaluation
*(to be completed in P12-S2)*

### Public application URL
### Evaluator credentials
### Administrator credentials
### Sample complaints
### Sample policy documents
### Testing instructions

## Testing
Test categories and their modules: [`documentation/specs/18_testing_strategy.md`](documentation/specs/18_testing_strategy.md).
Markers: `unit`, `integration`, `e2e`, `live_llm` (real API, excluded by default), `hidden`.

## Assumptions
The competition organizers were not contacted; the following are **team decisions** (also recorded in the RTM sheet
"Organizer Questions"):

1. The rule matrix and all configuration are managed from the Admin UI (add, edit, delete, import); hidden
   evaluation data never requires code changes.
2. Pipeline 2 is rules-only: no machine-learning model of any kind.
3. The format of unseen complaints is unknown, so batch import supports CSV, TSV, XLSX, JSON and JSONL with column
   mapping.
4. Design and planning within the five competition days is allowed.
5. No embeddings in Pipeline 2; knowledge-base retrieval uses BM25.
6. The GenAI provider is an OpenAI model accessed through the CommandCode OpenAI-compatible gateway
   ([ADR-007](documentation/adr/ADR-007-genai-gateway.md)); the exact model id is recorded before slice P01-S6.
7. The team has four members; there is no required format for the contribution record, so it is kept in
   `documentation/team_contribution.md`.

*(further assumptions added in P12-S3)*

## Limitations
*(to be completed in P12-S3)*

## Blog
*(link added in P12-S5)*

## Demonstration video
*(link added in P12-S4)*

## AI usage
AI assistance during development is declared in [`AI_USAGE.md`](AI_USAGE.md).

## Team
*(see `documentation/team_contribution.md`, P12-S6)*

## License
[MIT](LICENSE)
