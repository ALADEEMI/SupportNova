# ADR-013 — Attachment and upload safety policy

## Decision
- Allowed complaint attachments (config): PDF, DOCX, JPG, PNG. Allowed KB documents: PDF, DOCX (mandatory), TXT, MD.
  Complaint files: PDF, DOCX, TXT, MD, EML. Batch imports: CSV, TSV, XLSX, JSON, JSONL. Rule imports: CSV, XLSX, YAML.
- Type check by **magic bytes**, not only extension. Size and count limits from config.
- Stored under `storage/` with UUID filenames; original name kept as metadata; SHA-256 recorded.
- Text extracted from PDF/DOCX attachments is untrusted (ADR-011); images are stored as evidence only (no OCR — not in SRS).
- An attachment satisfies rules requiring "evidence"; absence yields "Missing evidence" (Step 42).
- Rejections return a clear message naming the rule broken ("File type .exe is not allowed. Allowed: PDF, DOCX, JPG, PNG.").

## SRS references
Steps 3, 4, 9, 10, 42; Deliverable 10 (malicious document instruction).
