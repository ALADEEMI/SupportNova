# Architecture Decision Records — Index

| ADR | Title | Status |
|---|---|---|
| 001 | Technology stack | Accepted |
| 002 | Single relational database; no vector database | Accepted |
| 003 | Pipeline 2 is rules-only (no LLM, no ML, no embeddings) | Accepted |
| 004 | Configuration as data, managed from the Admin UI | Accepted |
| 005 | JSON Schema is the single source of truth for GenAI output | Accepted |
| 006 | Prompt template management and versioning | Accepted |
| 007 | GenAI access through an OpenAI-compatible gateway | Accepted |
| 008 | Document identity, versioning and duplicate detection | Accepted |
| 009 | Document precedence for contradictions | Accepted |
| 010 | Enforcement of critical fields ("most severe wins") | Accepted |
| 011 | Prompt-injection and adversarial-content defense | Accepted |
| 012 | Dataset generation: spec-first, with an isolated hold-out set | Accepted |
| 013 | Attachment and upload safety policy | Accepted |
| 014 | Roles and access control | Accepted |
| 015 | Append-only audit trail | Accepted |
| 016 | Retrieval (RAG) design and pipeline independence | Accepted |
| 017 | Rule matrix model: rule types and condition DSL | Accepted |
| 018 | Verification score and decision policy | Accepted |

Format of each ADR: Context → Decision → Consequences → SRS references.
