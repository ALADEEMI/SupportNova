# P08 — Comparison, Decision, Final Result

## P08-S1 Comparison engine & verification score
- **SRS:** FR xlvi–li; D-8 columns · **Read:** spec 09, ADR-018
- **Acceptance:** comparison rows per field with deterministic explanations; score computed from checks (unit-tested formula); no hard-coded values.
- **Tests:** test_comparison.py, test_score_formula.py

## P08-S2 Decision, reasons, final result, response gating
- **SRS:** Step 57; NFR-4; architecture (Verified | Manual Review) · **Read:** ADR-010, ADR-018
- **Acceptance:** decision rules exact; six Step-57 reasons + GENAI_FAILURE/LOW_SCORE emitted; enforced fields applied; response blocked unless Verified/approved;
  complaint status, department, priority, SLA updated; everything persisted and audited.
- **Tests:** test_decision.py, test_final_result_merge.py

## P08-S3 AnalysisService orchestration + Complaint Workspace (Intelligence, Validation, Sources, GenAI JSON tabs)
- **SRS:** FR xli–xlii, lxvii · **Read:** spec 13 §2
- **Acceptance:** end-to-end within 20 s on normal conditions with step progress UI; failures degrade gracefully; all tabs populated.
- **Tests:** tests/e2e/test_complaint_flow.py (fixture LLM), timing assertion on non-LLM part (< 2 s)
