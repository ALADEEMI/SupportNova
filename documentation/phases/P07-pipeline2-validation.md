# P07 — Pipeline 2: Python Ground-Truth Validation

## P07-S1 Check framework & catalog
- **Read:** spec 08 §3, ADR-003, ADR-018
- **Acceptance:** checks registered from `checks_catalog`; enable/disable/severity/weight from config; each result carries srs_ref; parameterized check templates (spec 02) work.
- **Tests:** test_check_framework.py, test_pipeline2_has_no_ai_imports.py

## P07-S2 Classification, routing, urgency, priority, escalation checks
- **SRS:** Steps 19–24, 36–39; FR xlv–xlix; NFR-4; CI-06, CI-07 · **Read:** spec 08, ADR-010
- **Acceptance:** each check behaves per catalog; enforced fields recorded; mandatory escalation recall 100% on dev fixtures.
- **Tests:** test_routing.py, test_escalation_enforcement.py, test_multi_issue.py

## P07-S3 Policy checks
- **SRS:** Steps 25–26; FR xxiii, l; CI-10; D-10 (invalid policy ID) · **Read:** spec 08 §4, ADR-009
- **Acceptance:** 4 applicability statuses produced correctly; invalid ID, wrong section, outdated version, precedence violations detected.
- **Tests:** test_policy_applicability.py, test_precedence_check.py

## P07-S4 Actions, eligibility, compensation
- **SRS:** Steps 28–31; FR xxv–xxviii
- **Acceptance:** required/prohibited actions; refund/replacement/compensation consistency with eligibility; compensation cap.
- **Tests:** test_actions_eligibility.py

## P07-S5 Promises, hallucinations, entity grounding, contradictions
- **SRS:** Steps 34–35, 16; FR xxxi–xxxii; P2 list · **Read:** spec 08 §5–6
- **Acceptance:** 30+ fixture responses (supported/unsupported promises, negations, deadlines, invented amounts, IDs) classified correctly.
- **Tests:** test_promises.py, test_claim_grounding.py, test_contradictions.py

## P07-S6 Missing info, clarification, follow-up, notes, injection handling, response quality
- **SRS:** Steps 32, 38, 40–43, 50–51 · **Acceptance:** per catalog. **Tests:** test_clarification_check.py, test_injection_outcome_control.py
