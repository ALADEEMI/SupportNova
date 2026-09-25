# ADR-008 — Document identity, versioning and duplicate detection

## Context
Step 4 (validate duplicates, Document ID, version, effective/expiry dates, category), Step 7 (Active / Previous /
Superseded / Draft), Step 26 (Outdated), CI-04 (hidden policy update). The SRS does not define upload decision
rules; these are our documented assumptions.

## Decision
**Identity** = `doc_code` (Document ID) + `version`. The filename is only a hint.
Metadata source: the upload form (authoritative), pre-filled by automatic extraction from a header block when present.

**Duplicate detection — three layers**
1. File SHA-256 equal to an existing file → reject "Duplicate document".
2. Normalized-text SHA-256 equal (any doc_code) → reject "Duplicate content".
3. Near-duplicate (`rapidfuzz` ratio ≥ config threshold) → accept with warning, admin confirms.

**Decision table (first match wins)**
| # | Situation | Result |
|---|---|---|
| 1 | Unsupported type / empty / too large | Reject |
| 2 | Missing required metadata | Reject until completed |
| 3 | Same file hash | Reject |
| 4 | Same content hash | Reject |
| 5 | Same doc_code + same version + different content | Reject: "increment the version" |
| 6 | Same doc_code + higher version, effective date reached | New = **Active**, old = **Superseded**, run impact analysis |
| 7 | Same doc_code + higher version, effective date in future | New = **Draft** until effective date |
| 8 | Same doc_code + lower version than Active | Stored as **Previous** (archive) with warning |
| 9 | New doc_code, high similarity to existing doc | Accept + ask "same document?" |
| 10 | New doc_code, same filename as existing doc | Accept + ask "is this an update of X?" |
| 11 | New doc_code, no similarity | **Active** (or Draft if future-dated) |

Definitions: **Superseded** = was Active and replaced. **Previous** = older version stored for reference, never Active.
At use time: a document is *in force* only if status = Active and today is within [effective_date, expiry_date].
Citations to not-in-force documents get applicability **Outdated** (Step 26).
A daily/at-login job promotes due Drafts and marks expired documents not in force.

**Impact analysis on a new Active version (CI-04):** list open complaints whose analysis cited the old version
(→ "Requires Revision"), rules citing the doc (→ "Needs Review"), responses generated from it.

## SRS references
Steps 4, 7, 25–26, 1.2 (Document ID, Section ID, version, effective date, source reference), CI-04, CI-10, Hidden pack.
