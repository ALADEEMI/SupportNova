# ADR-016 — Retrieval (RAG) design and pipeline independence

## Context
Step 25: retrieve relevant approved policy sections with traceability. Pipeline 1 sends "complaint information,
customer context, and relevant approved knowledge-based content" to the model. Pipeline 2 must be independent.

## Decision
**Chunking (document_processing)**
- Split by detected sections (numbered clauses → DOCX heading styles → PDF font/bold heuristics → paragraphs).
- Target 600–1,200 characters per chunk; long sections split on paragraph boundaries with one-paragraph overlap;
  never merge text across sections. Each chunk: `chunk_code = <DOC>_v<ver>_s<section>_c<n>`, section_id, heading,
  page (PDF) / paragraph index (DOCX), version, status, source_reference string.

**Retrieval (knowledge_base)**
- BM25 (`rank-bm25`) over in-force, non-quarantined chunks; tokens = lowercase words, stopwords removed,
  light suffix stemming; query = normalized title + description + product name + requested resolution.
- `top_k` (default 8), `max_chunks_per_doc` (3), `max_context_chars` (12,000), `min_score` — all config.
- Each excerpt passed to the model carries: doc_code, title, category, version, status, effective date, section, source_reference.

**Independence**
- The Pipeline 1 prompt **never** contains Python-expected values, matched rule IDs, or rule-matrix rows.
- Allowed enumerations (categories, departments, levels, action codes) are passed — they are vocabulary, not decisions.

## Consequences
Hidden documents are retrievable immediately after upload (index rebuilt on change).

## SRS references
1.2, Pipeline 1, Steps 5–6, 25–27, 35, FR xxii, l.
