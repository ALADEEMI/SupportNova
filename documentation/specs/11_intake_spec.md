# 11 — Complaint Intake Specification

Package: `complaint_processing/`. Services: `complaint_service.py`, `import_service.py`.

## 1. Entry points
| Entry | Who | Notes |
|---|---|---|
| Web form | customer (own), agent (on behalf, selects customer) | primary (1.2) |
| Complaint file upload | customer/agent | PDF/DOCX/TXT/MD/EML → text becomes description; EML: From/Subject/Date/body parsed, channel=Email |
| Batch import | agent/admin | CSV/TSV/XLSX/JSON/JSONL with **column mapping** UI (auto-map by header names, saved mapping presets); processed by background worker with progress |

## 2. Form fields (1.2 ∪ Step 9)
title*, description*, product (dropdown from active products; "Other / Not listed" + free text), order reference
(dropdown of customer's orders; agent may type), transaction reference (dropdown of customer's transactions),
previous complaint reference (dropdown of customer's complaints), requested resolution (dropdown), complaint channel
(auto Web Form; agent can choose), preferred contact channel (dropdown), supporting documents (attachments, ADR-013).
Customer type, date and complaint history are system-derived (shown read-only). (* = required by default; configurable.)
Batch/file complaints may omit anything except description → missing-info detection handles gaps (CI-11).

## 3. Validation (Step 10) — messages are specific
Empty complaint · extremely short (config min chars/words) · too long (config) · duplicate (see §5) ·
invalid reference IDs (format regex + existence + belongs to the same customer) · missing mandatory fields (config) ·
unsupported attachments (ADR-013). Batch: per-row error report downloadable as CSV; valid rows proceed.

## 4. Pre-processing (Step 11)
Unicode NFKC normalization, whitespace collapse, control-char removal, HTML tag stripping, zero-width char removal,
length cap; metadata extraction by regex (order/transaction/complaint refs, amounts+currency, dates, emails/phones →
masked in logs); `normalized_text` and `text_hash` stored. Original text kept verbatim.

## 5. Duplicate, history and repeat (Steps 52–54)
- **Exact duplicate**: same customer + same `text_hash` within lookback days → reject on form ("You already submitted this complaint: CMP-…"), link in batch.
- **Near duplicate**: rapidfuzz `token_set_ratio` ≥ threshold against same customer's complaints in lookback → accept, flag, link.
- **Repeat unresolved**: same customer AND (same order OR same product) AND a prior complaint not Resolved/Closed,
  or Resolved then complaint within reopen window → `is_repeat`, link, `prior_unresolved_same_item` count feeds rules (overlay raises escalation).
  Wording-independent (CI-13).
- History panel shows all prior complaints for the customer.

## 6. Missing information (Step 42)
Required fields per subcategory (config, e.g. Duplicate Charge → transaction_ref; Delayed Delivery → order_ref;
Product Defect → product + problem description; Warranty Claim → order_ref + evidence). Also generic: product missing
when "Other" selected, problem description too vague (below min words). Result feeds Pipeline 2 and clarification.

## 7. After intake
Create complaint (status New) → send system acknowledgement (template, not GenAI) → trigger analysis
(synchronous for form with progress UI; background for batch). Audit every step.
