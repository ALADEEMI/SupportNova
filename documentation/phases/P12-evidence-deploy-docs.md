# P12 — Evidence, Deployment, Documentation, Drills

## P12-S1 Evidence exporters
- **SRS:** D-6, D-7, D-8, D-9, D-10, D-11 · **Read:** spec 21
- **Tasks:** `scripts/eval/export_genai_evidence.py` (provider, model, prompts, versions, generation config, sample requests (redacted),
  sample structured responses, invalid responses, retry evidence from analysis_runs); validation evidence summary; `make eval-holdout`;
  intelligence report; security report; test summary.
- **Acceptance:** all files in `reports/` regenerate from real data with one command each.

## P12-S2 Deployment
- **SRS:** D-15, NFR-5 · **Tasks:** Render web service + PostgreSQL; env vars; `make seed` on first deploy; health check; evaluator & admin accounts;
  sample complaints and documents available for download in the app; uptime check.
- **Acceptance:** public URL works from a clean browser; evaluator login; self-test green; hidden packs processable in production.

## P12-S3 Project report (32 sections + 4 diagrams)
- **SRS:** D-1 · **Tasks:** Mermaid sources for DFD (levels 0–1), Use Case, Activity (complaint processing), Sequence (analysis flow) → PNG; DOCX + PDF report.

## P12-S4 README (installation 12 items, execution 14 flows, evaluation guide, assumptions, limitations, links) & video script (21 items + contradictory case)
- **SRS:** D-12, D-13, D-14, D-16

## P12-S5 Technical blog (≥2,000 words, 20 topics)
- **SRS:** D-17

## P12-S6 Final checklist, team contribution record, AI_USAGE completeness
- **SRS:** D-18, D-19 · **Acceptance:** RTM: every row Done/Verified or N/A with justification.

## P12-S8 Non-functional verification
- **SRS:** NFR-1…NFR-5
- **Tasks:** NFR-1 timing report (p50/p95 end-to-end from `analysis_runs`, split LLM vs non-LLM); NFR-2 load script that inserts
  10,000 synthetic complaints, 100 categories/subcategories and 1,000 stub documents into a test DB and measures dashboard/search
  query times; NFR-3 usability walkthrough per role (checklist + screenshots); NFR-4 escalation recall = 100% on dev + hold-out
  mandatory-escalation cases; NFR-5 external uptime monitor on the deployed URL during evaluation week.
- **Acceptance:** `reports/nfr_report.md` with measured numbers and pass/fail per NFR.

## P12-S7 Drills (Day 5)
- **Live modification (CI-14):** rehearse each of the 9 changes with a timer; document steps in `documentation/drills.md`.
- **Deliberate defect (CI-15):** team member injects a bug in each of the 6 areas; the other finds it via failing tests; record time-to-fix.
- **Traceability & interview:** every member explains any module, any rule, any check, any prompt version.
