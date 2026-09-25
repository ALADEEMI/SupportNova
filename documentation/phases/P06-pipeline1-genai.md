# P06 — Pipeline 1: GenAI Complaint Intelligence

## P06-S1 Schema resolution & validation
- **SRS:** Steps 46; FR xliii–xliv; CI-14 · **Read:** ADR-005, spec 05, `schemas/complaint_intel.schema.json`
- **Acceptance:** enums injected from config (incl. null for nullable enums); a newly added category is accepted without code change;
  invalid outputs produce path-level error lists.
- **Tests:** test_schema_resolution.py, test_output_validation.py

## P06-S2 Context builder & prompt rendering
- **SRS:** Pipeline 1 inputs; Steps 25, 50 · **Read:** spec 06 §3, ADR-011, ADR-016
- **Acceptance:** customer context contains facts only; complaint data escaped & delimited; excerpts carry full source metadata;
  **no Python-expected values in the prompt** (test asserts); rendered prompt stored (redacted) in the run.
- **Tests:** test_context_builder.py, test_prompt_independence.py

## P06-S3 Call, parse, bounded retry, logging
- **SRS:** Steps 47, 49; FR xii, liii; D-6 · **Read:** spec 07 §1
- **Acceptance:** retry table behaviour exactly as spec; max attempts respected; every attempt logged; unresolved failure → Manual Review with GENAI_FAILURE;
  run stores prompt/schema versions, provider, model, gateway, temperature, policy versions, duration.
- **Tests:** test_retry_policy.py (fixtures: invalid JSON, schema violation, timeout, 401), test_run_logging.py

## P06-S4 Regenerate-response & follow-up prompts
- **SRS:** Steps 40, 58 (regenerate) · **Read:** spec 07 §4
- **Acceptance:** outputs re-validated by promise/claim checks before approval.
- **Tests:** test_regenerate_response.py

## P06-S5 Prompt Templates admin UI
- **SRS:** Step 48; user requirement (edit/add/delete with traceability) · **Read:** spec 06 §4
- **Acceptance:** clone/edit/validate/preview/test-run/activate/retire/delete-draft/export; used versions immutable; all audited.
- **Tests:** test_prompt_service.py
