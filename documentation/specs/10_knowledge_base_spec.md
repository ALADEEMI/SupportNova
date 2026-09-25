# 10 — Knowledge Base Specification

Packages: `document_processing/`, `knowledge_base/`. Service: `document_service.py`. Admin → Knowledge Base.

## 1. Upload flow (Admin)
1. Select file(s) (PDF/DOCX mandatory; TXT/MD optional) — multi-file upload supported.
2. System extracts text and tries to read a **metadata header** (lines `Document ID:`, `Title:`, `Category:`,
   `Version:`, `Status:`, `Effective Date:`, `Expiry Date:`, `Supersedes:`, `Owner:`) → pre-fills the metadata form.
3. Admin confirms/edits metadata (doc_code, title, category, version, effective date, expiry date, topics).
   Filename-based hint: "Looks like an update of ZEP-POL-003 — use this Document ID?" (ADR-008 rule 10).
4. Validation (Step 4): file type (magic bytes), size, empty (no extractable text → reject with hint), duplicates (3 layers),
   Document ID format (config regex, default `^[A-Z]{2,5}-[A-Z]{2,5}-\d{3}$`), version format (`\d+(\.\d+){0,2}`),
   effective date valid, expiry after effective, category exists.
5. Decision per ADR-008 table → preview: "Will become Active; v2.0 will become Superseded; 3 open complaints and 4 rules affected".
6. Confirm → parse, chunk, injection scan (quarantine), store, rebuild BM25, audit, impact analysis.

## 2. Parsing (Step 5)
- PDF (PyMuPDF): per page text blocks with font size/bold flags; page numbers kept.
- DOCX (python-docx): paragraphs with style names (Heading 1–3), tables flattened row-wise ("col: value"), paragraph index kept.
- TXT/MD: Markdown headings `#` or numbered lines as sections.
- Output: ordered `Block(text, page, paragraph_index, style_hint, is_heading)`.

## 3. Section detection & chunking (Step 6, ADR-016)
Heading detection order: numbered clause (`^\d+(\.\d+)*\s+\S`) → DOCX Heading style → PDF larger/bold font line →
Markdown heading → fallback: paragraph groups. Section id = clause number when present, else `S<n>`.
Chunk fields: chunk_code, section_id, heading, page, paragraph_index, text, source_reference
(`ZEP-POL-003 v3.0 §3.1 "Eligibility" (p.2)`).

## 4. Versions & in-force logic (Step 7) — ADR-008
Background check at app start and every page load of Admin (cheap): promote due Drafts, mark expired.

## 5. Precedence & contradictions — ADR-009

## 6. Impact analysis (CI-04) — shown after activation and on demand
- Open complaints whose latest analysis cited the superseded version → list; bulk action "Re-analyze" (creates new runs) or mark "Requires Revision".
- Rules citing the doc_code → `needs_review=true` (badge in Rule Matrix).
- Escalation-rule changes: rules of type overlay citing the doc highlighted separately ("escalation rules may have changed").
- Generated responses (not yet sent) based on old version → flagged "Response requires revision".
Stored as a report in `reports/impact_<doc>_<date>.md` and shown in UI.

## 7. KB browser
Documents table (filters: category, status, topic), version history timeline, chunk viewer with source references,
quarantined chunks with release/keep actions, download original file.

## 8. Retrieval (Step 25) — ADR-016 parameters from config.
