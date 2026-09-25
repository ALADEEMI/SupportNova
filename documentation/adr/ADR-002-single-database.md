# ADR-002 — Single relational database; no vector database

## Context
SRS lists several databases and semantic-retrieval tools. We need one consistent store for configuration,
rules, documents, chunks, complaints, analyses, reviews and audit.

## Decision
- One relational database. SQLite for local development, PostgreSQL in deployment. Same SQLAlchemy models; switch by `DATABASE_URL`.
- JSON columns (`JSON` type) for flexible structures: rule conditions, analysis outputs, check results.
- No vector database. Retrieval uses BM25 built in memory from the `chunks` table and rebuilt when documents change (ADR-016).
- Files (original documents, attachments) are stored on disk under `storage/` (git-ignored) with SHA-256 hash and metadata in DB.

## Consequences
- Simple deployment, one backup target, transactional consistency.
- BM25 index rebuild on document change is cheap at our scale (≤1,000 documents, NFR-2).

## SRS references
1.9.2 items 9–10, NFR-2, Steps 5–7, 25.
