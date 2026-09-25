# P05 — Complaint Intake

## P05-S1 Complaint form (customer & agent on behalf)
- **SRS:** 1.2, Step 9, FR iii · **Read:** spec 11 §2, spec 13
- **Acceptance:** all 13 fields handled (system-derived ones read-only); dropdowns from DB scoped to the customer;
  "Other / Not listed" product path; attachments validated; input preserved on error; acknowledgement shown with complaint ref.
- **Tests:** test_form_submission.py

## P05-S2 Validation & pre-processing
- **SRS:** Steps 10–11, FR iv–v · **Read:** spec 11 §3–4
- **Acceptance:** each Step-10 condition yields its specific message; normalization idempotent; entities/refs extracted; text_hash stored.
- **Tests:** test_complaint_validation.py, test_preprocessing.py, tests/boundary/test_lengths.py

## P05-S3 Complaint files (PDF/DOCX/TXT/MD/EML)
- **Acceptance:** each format produces a complaint; EML sets channel Email and uses sender/date/subject; extracted text treated as untrusted.
- **Tests:** test_file_complaints.py

## P05-S4 Batch import with column mapping
- **SRS:** Hidden dataset (unknown format), D-3, D-8 · **Read:** spec 11 §1
- **Acceptance:** CSV/TSV/XLSX/JSON/JSONL; auto-mapping by header synonyms; manual mapping UI; saved presets; background processing with progress;
  per-row error report; valid rows proceed; analysis optionally triggered with concurrency limit (config).
- **Tests:** test_batch_import.py (each format), test_mapping_presets.py

## P05-S5 Duplicates, history, repeats
- **SRS:** Steps 52–54; FR lvi–lviii; CI-13 · **Read:** spec 11 §5
- **Acceptance:** exact duplicate blocked on form & linked in batch; near-duplicate flagged; repeat detected with different wording via order/product linkage; counts feed rule context.
- **Tests:** test_duplicates_repeats.py

## P05-S6 Missing-information detection
- **SRS:** Step 42; FR xxxix; CI-11 · **Read:** spec 11 §6
- **Acceptance:** required fields per subcategory from config; results stored and shown; feeds Pipeline 2.
- **Tests:** test_missing_info.py
