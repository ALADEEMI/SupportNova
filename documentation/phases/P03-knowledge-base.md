# P03 — Knowledge Base

## P03-S1 Upload & validation
- **SRS:** Steps 3–4; FR vi–vii; 1.2 · **Read:** spec 10 §1, ADR-008, ADR-013
- **Tasks:** multi-file upload; magic-byte type check; size limit; empty detection; metadata header extraction + form;
  three-layer duplicate detection; decision table (ADR-008) with preview screen.
- **Acceptance:** every row of the ADR-008 table produces the documented outcome and message.
- **Tests:** test_upload_validation.py, test_versioning_decisions.py (one test per table row)

## P03-S2 Parsing
- **SRS:** Step 5; FR viii · **Read:** spec 10 §2
- **Tasks:** PDF, DOCX (incl. tables), TXT, MD parsers → blocks with page/paragraph refs.
- **Acceptance:** all 29 Zephyra docs and the 4 odd-format docs parse; page numbers correct for PDFs.
- **Tests:** test_parse_pdf.py, test_parse_docx.py, test_parse_txt_md.py

## P03-S3 Section detection & chunking
- **SRS:** Step 6; FR ix; 1.2 (Section ID, source reference) · **Read:** ADR-016
- **Acceptance:** numbered clauses become sections with correct IDs; chunk size bounds respected; every chunk has chunk_code,
  section_id, heading, page/paragraph, version, source_reference; odd-format docs still produce traceable chunks.
- **Tests:** test_chunking.py

## P03-S4 Versions, in-force logic, precedence
- **SRS:** Steps 7, 26; FR x; CI-04, CI-10 · **Read:** ADR-008, ADR-009
- **Tasks:** status transitions, draft promotion, expiry; precedence rules; conflict register; topics.
- **Acceptance:** superseded/draft/expired never returned by retrieval; precedence resolves KC-01…KC-08 as documented.
- **Tests:** test_in_force.py, test_precedence.py

## P03-S5 Injection scan & quarantine
- **SRS:** Steps 50–51; D-10 (malicious document instruction) · **Read:** ADR-011
- **Acceptance:** adversarial docs' injected chunks quarantined; admin can review/release; quarantined chunks never retrieved.
- **Tests:** tests/security/test_document_quarantine.py

## P03-S6 BM25 retrieval
- **SRS:** Step 25; FR xxii · **Read:** ADR-016
- **Acceptance:** for 20 labelled dev complaints, the authoritative policy section appears in top_k for ≥ 18; index rebuilds on document change; parameters from config.
- **Tests:** test_retrieval.py (fixture complaints → expected doc codes)

## P03-S7 Impact analysis & KB browser UI
- **SRS:** CI-04 · **Read:** spec 10 §6–7
- **Acceptance:** activating ZEP-POL-003 v4.0 (hidden pack) lists affected open complaints, flags rules `needs_review`, flags unsent responses; report file written.
- **Tests:** tests/hidden/test_pack_policy_revision.py
