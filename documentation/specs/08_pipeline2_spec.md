# 08 — Pipeline 2: Python Ground-Truth Validation (deterministic)

Packages: `python_validation/` (engine, checks, eligibility), `hallucination_checks/` (claims, promises,
contradictions), `security/` (injection detector). No AI of any kind (ADR-003).

## 1. Inputs
Complaint + context (spec 04 §2), GenAI parsed output (may be absent on failure), retrieved chunk metadata,
rule matrix, configuration, documents table.

## 2. Python-expected result (rule engine, spec 04 §4)
`PythonExpected {category, subcategory, secondary[], department, supporting_departments[], urgency, priority,
escalation_required, escalation_level, required_actions[], prohibited_actions[], action_eligibility{code: permitted|not_permitted|requires_verification},
follow_up{required,type,within_hours}, policy_refs[], missing_fields[], flags[AMBIGUOUS|UNCLASSIFIED|SENSITIVE], matched_rules[{rule_id, evidence}]}`

## 3. Check catalog (each check → pass/warn/fail/n-a, severity, detail, srs_ref)
| check_id | What it verifies | Severity | SRS |
|---|---|---|---|
| SCHEMA_VALID | jsonschema + semantic ID validity (departments, actions, levels exist & active) | critical | Step 46 |
| CATEGORY_MATCH | GenAI primary category = Python category | critical | FR xlvi |
| SUBCATEGORY_MATCH | subcategory equal | minor | Step 15 |
| SECONDARY_ISSUES | Python secondary categories ⊆ GenAI (primary+secondary) | major | Step 13, CI-12 |
| DEPARTMENT_MATCH | department equal | critical | Step 23, FR xlvii |
| SUPPORTING_DEPARTMENTS | Python supporting ⊆ GenAI supporting | minor | Step 24 |
| URGENCY_MATCH | equal; if GenAI lower → fail + enforced | critical | Step 19, FR xlviii |
| PRIORITY_MATCH | equal per mapping | major | Step 20 |
| ESCALATION_MANDATORY | Python requires escalation → GenAI must too; else fail + enforced | critical | Step 39, NFR-4, FR xlix |
| ESCALATION_LEVEL | GenAI level rank ≥ Python level rank | major | Step 37 |
| POLICY_ID_VALID | every cited policy_id exists; unknown → fail ("Invalid policy ID") | critical | Step 46, D-10 |
| POLICY_SECTION_VALID | cited section exists in that document version | major | Step 25 |
| POLICY_IN_FORCE | cited version Active & in date; else Outdated → fail | critical | Steps 7, 26 |
| POLICY_APPLICABILITY | per reference: Applicable / Conditionally Applicable / Not Applicable / Outdated (algorithm §4); at least one Applicable for the primary issue | major | Step 26 |
| POLICY_PRECEDENCE | no lower-precedence doc cited when a higher one on the same topic is in force | major | CI-10 |
| REQUIRED_ACTIONS_PRESENT | all Python required actions appear in resolution_steps | critical | Step 28 |
| PROHIBITED_ACTIONS_ABSENT | none of prohibited actions appear (steps) | critical | Step 28 |
| REFUND_ELIGIBILITY | GenAI refund recommendation consistent with action_eligibility[ISSUE_REFUND] ("eligible" when not_permitted → fail) | critical | Step 29 |
| REPLACEMENT_ELIGIBILITY | same for replacement | critical | Step 30 |
| COMPENSATION_PERMITTED | compensation recommended only if permitted; amount ≤ policy cap | critical | Step 31 |
| UNSUPPORTED_PROMISES | response/follow-up contain no promise phrase (actions' promise lexicons + generic "guarantee") for a not-permitted action; no deadline not backed by SLA/excerpt | critical | Step 34, CI-09 |
| HALLUCINATED_CLAIMS | every checkable claim is grounded (§5) | critical | Step 35 |
| ENTITY_GROUNDING | extracted order/transaction refs, amounts, products exist in complaint text or DB | major | Step 16 |
| CONTRADICTIONS | internal contradictions: response promises what steps don't do; steps contain both X and prohibited X; refund "eligible" but response says denied, etc. | major | P2 list "contradictory instructions" |
| MISSING_INFO | Python missing_fields ⊆ GenAI missing_information (normalized) | major | Step 42 |
| CLARIFICATION_PRESENT | if missing_fields non-empty → ≥1 clarification question and no invented values for those fields | major | Step 43, CI-11 |
| FOLLOW_UP_REQUIRED | Python follow-up required → GenAI follow_up.required true | minor | Steps 40–41 |
| ESCALATION_NOTES_COMPLETE | required escalation → notes object with the 6 fields non-empty | minor | Step 38 |
| INJECTION_HANDLED | if detector flags injection: GenAI flag true (warn if false) and no permission-granting outcome (fail if promise/eligibility checks failed) | critical | Steps 50–51 |
| RESPONSE_QUALITY | response acknowledges, summarizes, gives next step (lexical heuristics), length bounds, tone vocabulary | minor | Step 32 |

Admin can disable a check or change its severity/weight (config), and add parameterized checks (spec 02).

## 4. Policy applicability algorithm (Step 26)
For each cited (policy_id, section):
1. Not found → **Not Applicable** + POLICY_ID_VALID fail.
2. Document/version not in force → **Outdated**.
3. Cited by a matched Python rule (same doc, same section) → **Applicable**.
4. Same doc as a matched rule but different section, or topic matches the primary category, and eligibility for the
   related action is `requires_verification` → **Conditionally Applicable**; otherwise topic match → **Applicable**.
5. Topic unrelated to primary/secondary categories → **Not Applicable**.

## 5. Claim grounding (hallucination_checks)
Extract from customer_response, follow_up.message, escalation_notes, resolution descriptions:
money amounts, percentages, durations ("within 5 business days"), dates, order/transaction/complaint refs,
policy ids/sections, product names. A claim is grounded if found in: complaint text/attachments text, customer
context (DB facts), cited in-force excerpts, SLA table, or rule outputs. Ungrounded claim → HALLUCINATED_CLAIMS fail,
listing each claim and where it was searched. Generic courtesy text is not a claim (Step 35 scope = factual claims).

## 6. Promise detection
Lexicons per action (e.g. `promise_refund`: "we will refund", "refund has been approved", "full refund", "money back";
`promise_compensation`: "compensate you", "credit of", "voucher"; generic: "guarantee", "we promise", "definitely by").
Negation window (e.g. "we cannot guarantee") avoids false positives. Deadline phrases must equal an SLA or excerpt value.

## 7. Output
`ValidationReport {python_expected, checks[], enforced_fields{field: {genai, python, final}}, flags[]}` → Comparison Engine (spec 09).
