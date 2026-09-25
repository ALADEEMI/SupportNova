# P11 — Data: Documents, Master Data, Complaints, Hold-out, Hidden Packs

Starts on Day 2 in parallel with P01–P02 (documents are needed by P03, rules by P04, complaints by P06–P08).

## P11-S1 Author Zephyra documents (Markdown sources)
- **SRS:** Step 2; Hint (≥20 docs, ≥20 contradictory cases); D-4 · **Read:** spec 01 §8–10, spec 16 §1.1
- **Acceptance:** 24 doc codes / 29 versions; header metadata complete; numbered clauses; every §10 fact present once authoritatively; KC-01…KC-08 present in the designated docs; human review done by a team member (recorded in AI_USAGE.md).
- **Tests:** scripts/data_gen/check_documents.py (metadata, clause numbering, fact presence)

## P11-S2 Render DOCX/PDF + adversarial docs + odd-format docs
- **Read:** spec 16 §1.2–1.4 · **Acceptance:** files render, parse in P03, correct formats per doc; adversarial docs trigger quarantine.

## P11-S3 Master data
- **Read:** spec 16 §2 · **Acceptance:** seeded counts; referential integrity; 25 duplicate charges; mix of delivered/undelivered orders; within/outside refund & warranty windows.

## P11-S4 Complaint specs + dev texts (400)
- **SRS:** Hint quotas; D-3 · **Read:** spec 16 §3–5, ADR-012
- **Acceptance:** quotas met; validator green; labels designed (not engine-derived); diagnostic report on rule-engine agreement produced for the team.

## P11-S5 Rule freeze + hold-out (100)
- **SRS:** D-8 · **Read:** spec 16 §6 · **Acceptance:** tag `rules-freeze-v1` precedes hold-out commit; hold-out never used for tuning (documented).

## P11-S6 Hidden-readiness packs
- **SRS:** Hidden Evaluation Dataset; CI-03…CI-13 · **Read:** spec 16 §1.4
- **Acceptance:** each pack has README with admin steps + expected outcomes; tests/hidden pass using only UI/config operations (no code change).
