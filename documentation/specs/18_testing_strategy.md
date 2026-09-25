# 18 — Testing Strategy (Deliverable 11: 20 test categories)

| SRS test category | Test module(s) |
|---|---|
| Functional tests | tests/e2e/test_complaint_flow.py (submit → analyze → validate → decide → review → resolve) |
| Complaint-submission tests | tests/intake/test_form_submission.py, test_file_complaints.py, test_batch_import.py |
| Document-upload tests | tests/kb/test_upload_validation.py, test_versioning_decisions.py (ADR-008 table, each row) |
| Parsing tests | tests/kb/test_parse_pdf.py, test_parse_docx.py, test_parse_txt_md.py, test_parse_eml.py |
| GenAI API tests | tests/genai/test_llm_client.py (fixtures), tests/genai/test_live_smoke.py (`live_llm`) |
| JSON tests | tests/genai/test_schema_resolution.py (enum injection), test_output_validation.py, test_retry_policy.py |
| Classification tests | tests/validation/test_rule_engine_classification.py |
| Routing tests | tests/validation/test_routing.py |
| Urgency tests | tests/validation/test_urgency_priority.py (6 tricky cases of Step 21) |
| Escalation tests | tests/validation/test_escalation_enforcement.py |
| Resolution tests | tests/validation/test_actions_eligibility.py |
| Policy tests | tests/validation/test_policy_applicability.py, test_precedence.py |
| Hallucination tests | tests/hallucination/test_claim_grounding.py, test_promises.py |
| Prompt-injection tests | tests/security/test_injection_detection.py, test_injection_outcome_control.py |
| Duplicate tests | tests/intake/test_duplicates_repeats.py |
| Missing information tests | tests/intake/test_missing_info.py, tests/validation/test_clarification_check.py |
| Multi-issue tests | tests/validation/test_multi_issue.py |
| Hidden-data readiness tests | tests/hidden/test_pack_new_category.py, test_pack_policy_revision.py, test_pack_odd_formats.py, test_pack_new_escalation.py |
| Boundary tests | tests/boundary/ (min/max lengths, file size limits, SLA thresholds, retry limits, score threshold edges) |
| Security tests | tests/security/ (spec 17) |

Plus: tests/config/test_no_hardcode.py (greps for configured codes inside `.py` files outside tests/seeds),
tests/validation/test_pipeline2_has_no_ai_imports.py (fails if `openai`/ML libs imported in python_validation, hallucination_checks, comparison_engine),
tests/audit/test_append_only.py, tests/lifecycle/test_transitions.py, tests/sla/test_sla.py, tests/reports/test_exports.py.

**Evaluation runners** (`scripts/eval/`): `run_dev_eval.py` (accuracy of Python rules vs dataset labels on dev set, and of GenAI vs labels),
`run_holdout_eval.py` (Deliverable 8). Metrics: per-field match rates, confusion matrix per category, escalation recall
(must be 100% for mandatory escalation, NFR-4).

Coverage target: ≥80% on python_validation, comparison_engine, hallucination_checks, complaint_processing, document_processing.
