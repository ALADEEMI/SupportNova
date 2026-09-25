# 04 — Complaint Resolution Rule Matrix Specification

The matrix is the ground truth of Pipeline 2 (SRS Step 8, 1.2, Deliverable 5). The team authors it from the
approved Zephyra documents; it is never generated at runtime by the GenAI model. It is managed in
**Admin → Rule Matrix** and can be uploaded in batch.

## 1. Columns (import/export format — CSV, XLSX or YAML)
| Column | Req. | Description | Deliverable 5 |
|---|---|---|---|
| rule_id | ✓ | Unique code, e.g. `R-SAF-003` | Rule ID |
| rule_type | ✓ | `classification` / `overlay` / `eligibility` | — |
| status | ✓ | `active` / `inactive` / `draft` | — |
| version | ✓ | integer, auto-incremented on edit | — |
| category | c | category code (classification: required; overlay: optional) | Category |
| subcategory | c | subcategory code | Subcategory |
| applies_to_categories | | overlay/eligibility scope: `*` or `|`-separated codes | — |
| conditions | ✓ | JSON condition (DSL §3) | Conditions |
| department | c | department code (classification required) | Department |
| supporting_department | | department code | — |
| urgency | c | urgency code (classification required; overlay = floor) | Urgency |
| priority | | priority code; empty = use priority_rules mapping | Priority |
| escalation_required | | true/false | Escalation |
| escalation_level | | escalation level code | Escalation |
| required_actions | | `|`-separated action codes | Required actions |
| prohibited_actions | | `|`-separated action codes | Prohibited actions |
| permitted_actions | e | eligibility: actions this rule permits | — |
| follow_up_required | | true/false | Follow-up |
| follow_up_type | | follow-up type code | Follow-up |
| follow_up_within_hours | | integer | Follow-up |
| policy_id | ✓ | doc_code, e.g. `ZEP-POL-010` | Policy |
| policy_section | ✓ | section, e.g. `3.1` | Policy |
| weight | | classification score weight (default 1) | — |
| requires_review | | true = sensitive → always Manual Review | — |
| description | ✓ | human explanation | — |

Seed files are split for readability (the SRS repo structure): `complaint_rules/` (classification + eligibility),
`routing_rules/` (department/supporting-department overrides), `escalation_rules/` (overlays). All load into one `rules` table.

## 2. Complaint context (fields available to conditions) — computed deterministically
| Field | Type | Source |
|---|---|---|
| text | string | normalized title + description (lowercase, whitespace/char normalized) |
| title | string | normalized title |
| product_category | code | product → product_category |
| product_sku | string | product |
| customer_type | code | customer profile |
| channel | code | complaint |
| requested_resolution | code | complaint |
| order_amount | number | order |
| max_amount_mentioned | number | regex amounts in text |
| days_since_order / days_since_delivery | number | order dates vs submitted_at |
| warranty_active | bool | delivery_date + product.warranty_months |
| subscription_active | bool | subscriptions |
| prior_complaints_count | number | same customer |
| prior_unresolved_same_item | number | same customer & (same order or product) & status not Resolved/Closed |
| is_repeat / is_duplicate | bool | intake linking |
| has_attachment / attachment_count | bool/number | attachments |
| missing_fields | list | missing-info detector |
| injection_suspected | bool | security detector |

## 3. Condition DSL
```json
{"all": [ <cond>, ... ], "any": [ <cond>, ... ], "none": [ <cond>, ... ]}
<cond> = {"field": "<context field>", "op": "<op>", "value": <value>}   or a nested group {"all"/"any"/"none": [...]}
```
Semantics: `all` → every cond true; `any` → at least one true (if present); `none` → no cond true. Empty group = true.
Ops: `contains_any`, `contains_all`, `not_contains` (word-boundary, case-insensitive phrase matching),
`regex`, `eq`, `neq`, `in`, `not_in`, `gt`, `gte`, `lt`, `lte`, `is_true`, `is_false`, `is_empty`, `not_empty`.
`value` may be a lexicon reference `"@lexicon:<code>"` (resolved at evaluation time).
Validation: unknown field/op, wrong value type, unknown lexicon → import/editor error with row number and reason.

Match evidence: every true text condition returns the matched phrases (shown in UI and stored in `matched_rules`).

## 4. Evaluation algorithm (python_validation/rule_engine.py)
1. Build context (§2). Load active rules (cached).
2. **Classification**: evaluate all `classification` rules. Score = `weight × (1 + number_of_distinct_matched_phrases)`.
   Group by category → category score = max rule score.
   - Primary = highest score category/subcategory rule. If top two categories within `tie_margin` (config) → flag `AMBIGUOUS` (Step 57).
   - Secondary issues = other categories with score ≥ `min_secondary_score` (config).
   - No match → `UNCLASSIFIED` (→ Manual Review; never guess).
3. **Base result** from the primary rule: department, urgency, priority, required/prohibited actions, follow-up, policy ref.
   Supporting departments = departments of secondary categories + rule `supporting_department`.
4. **Overlays**: evaluate `overlay` rules whose scope includes the primary (or any) category.
   urgency = max(rank); escalation_required = OR; escalation_level = max(rank); union actions; add supporting departments;
   `requires_review` OR.
5. **Priority**: overlay/primary explicit priority if set, else `priority_rules[urgency]`.
6. **Eligibility**: for each action with `requires_eligibility` (e.g. `ISSUE_REFUND`, `ISSUE_REPLACEMENT`,
   `OFFER_GOODWILL_CREDIT`, `WAIVE_FEE`): `permitted` if an active eligibility rule permitting it matches;
   `requires_verification` if a rule would match but depends on a missing field; else `not_permitted`.
7. Output `PythonExpected` (+ `matched_rules` with evidence). Deterministic: same input → same output (unit-tested).

## 5. Example rules (seed style)
```yaml
- rule_id: R-SAF-003
  rule_type: classification
  status: active
  category: PRODUCT_SAFETY
  subcategory: OVERHEATING_FIRE_RISK
  conditions: {"any":[{"field":"text","op":"contains_any","value":"@lexicon:overheating_terms"}]}
  department: PRODUCT_SAFETY
  supporting_department: WARRANTY_REPAIRS
  urgency: CRITICAL
  escalation_required: true
  escalation_level: CRITICAL_MANAGEMENT
  required_actions: [ADVISE_STOP_USE, OPEN_SAFETY_CASE]
  prohibited_actions: [PROMISE_REFUND_BEFORE_INSPECTION, ADVISE_CONTINUED_USE]
  follow_up: {required: true, type: ESCALATION_ACK, within_hours: 2}
  policy_id: ZEP-POL-010
  policy_section: "3.1"
  requires_review: false
  description: Overheating, smoke, burning smell or swelling battery is a Critical safety incident.

- rule_id: R-ESC-LEGAL-01
  rule_type: overlay
  applies_to_categories: "*"
  conditions: {"any":[{"field":"text","op":"contains_any","value":"@lexicon:legal_threat_terms"}]}
  urgency: HIGH
  escalation_required: true
  escalation_level: COMPLIANCE_REVIEW
  supporting_department: PRIVACY_COMPLIANCE
  required_actions: [NOTIFY_COMPLIANCE]
  prohibited_actions: [ADMIT_LIABILITY]
  policy_id: ZEP-CMP-001
  policy_section: "2.1"
  requires_review: true
  description: Legal-threat language requires Compliance Review regardless of category.

- rule_id: R-ELG-REF-01
  rule_type: eligibility
  applies_to_categories: "REFUND|RETURNS_REPLACEMENT|PRODUCT_DEFECT"
  conditions: {"all":[{"field":"days_since_delivery","op":"lte","value":30}]}
  permitted_actions: [ISSUE_REFUND]
  policy_id: ZEP-POL-003
  policy_section: "3.1"
  description: Refund permitted within 30 days of delivery (conditions verified by agent).
```

## 6. Coverage targets (Hint)
≥100 rules total (target ~110: ~70 classification, ~30 overlay, ~10 eligibility) and ≥30 mandatory escalation
conditions (overlays + classification rules with `escalation_required=true`). Every category has ≥5 classification rules.
Required overlay families: safety injury/fire, child involved, data exposure, account takeover, legal threat,
regulator/media mention, high-value (order_amount ≥ 1000), repeat unresolved (≥2), VIP + critical impact,
policy-exception request, severe service failure (multiple failed deliveries), security breach indicators.

## 7. Import (batch upload) — Admin → Rule Matrix → Import
1. Upload CSV/XLSX/YAML (template downloadable from the same screen).
2. **Dry run**: parse → validate every row (required columns, codes exist in config, JSON condition valid,
   lexicons exist, policy doc exists (warning if not in force), duplicates in file) → report table (row, rule_id, status, errors).
3. Choose mode: `add` (new only), `upsert` (create or new version), `replace_all` (deactivate rules not in file; requires confirmation).
4. Commit in one transaction; write `rule_versions` snapshots and audit entries; invalidate cache; show summary.
Export: current active matrix to CSV/XLSX/YAML (also used for Deliverable 5).

## 8. Editor & simulator (UX)
- Table with filters (type, category, status, needs_review), row click → form editor.
- Condition builder (field/op/value rows, group type) with live JSON preview; advanced raw JSON editor with validation.
- **Simulator**: paste text or pick a complaint → shows context, each rule's match result and evidence, final PythonExpected.
- `needs_review` badge when the cited policy document changed (impact analysis).
