# 05 — GenAI Output Contract (`schemas/complaint_intel.schema.json`)

Unifies the three SRS lists: 1.2 complaint-intelligence result (15 items), Pipeline 1 "must" list (17 items),
and the sample JSON (1.2). Every field below is required in the JSON (nullable where noted) so strict structured
output works. `x-enum-source` values are injected from configuration at runtime (ADR-005).

| Field | Type | Enum source | SRS |
|---|---|---|---|
| schema_version | string | const | Step 49 |
| complaint_id | string | — | sample JSON |
| primary_issue.summary | string | — | Step 12 |
| primary_issue.category | string | categories | Step 14 |
| primary_issue.subcategory | string | subcategories | Step 15 |
| secondary_issues[] {summary, category, subcategory} | array | categories/subcategories | Step 13 |
| sentiment | string | sentiment | Step 17 |
| emotion_indicators[] | array | emotion | Step 18 |
| urgency | string | urgency_levels | Step 19 |
| urgency_rationale | string | — | Step 19 (explain objective factors) |
| priority | string | priorities | Step 20 |
| entities {products[], order_refs[], transaction_refs[], dates[], amounts[{value,currency}], locations[], complaint_refs[], departments_mentioned[]} | object | — | Step 16 |
| department | string | departments | Step 22 |
| supporting_departments[] | array | departments | Step 24 |
| policy_references[] {policy_id, section, version, relevance} | array | — (validated by Python) | Steps 25–26 |
| resolution_steps[] {action_code, description, policy_id, section} | array | actions | Step 27 |
| refund_assessment {requested, recommendation: eligible/not_eligible/requires_verification/not_applicable, rationale} | object | — | Step 29 |
| replacement_assessment {same shape} | object | — | Step 30 |
| compensation {recommended, type, amount (nullable), rationale} | object | — | Step 31 |
| escalation {required, level, reason, triggers[]} | object | escalation_levels | Steps 36–37 |
| escalation_notes {complaint_summary, key_facts[], reason, actions_already_taken[], relevant_policy, required_next_action} (nullable when not required) | object | — | Step 38 |
| response_type | string | — | sample JSON |
| tone | string | tones | Step 33 |
| customer_response | string | — | Step 32 |
| follow_up {required, type, message, suggested_after_hours} | object | follow_up_types | Steps 40–41 |
| missing_information[] | array | — | Step 42 |
| clarification_questions[] | array | — | Step 43 |
| complaint_summary | string | — | Step 44 |
| agent_guidance[] | array | — | Step 45 |
| injection_suspected | boolean | — | Step 50 |
| injection_notes | string (nullable) | — | Step 51 |

Deliberately excluded: model "confidence" (CI-17). Python never trusts any GenAI field without checks.

Validation (Step 46): `jsonschema` (types, required, enums) + Python semantic checks (department IDs exist and active,
policy IDs exist, sections exist in that document, action codes exist, escalation level consistent with required flag).
