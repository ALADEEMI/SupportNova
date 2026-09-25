# 09 — Comparison Engine, Verification Score, Decision and Final Result

Package: `comparison_engine/`.

## 1. Field comparison (FR xlvi–xlix, Deliverable 8 columns)
Rows: category, subcategory, secondary categories, department, supporting departments, urgency, priority,
escalation required, escalation level, policy reference(s), required actions coverage.
Each row: `field, genai_value, python_value, final_value, result: Match|Mismatch|Partial, explanation`.
Explanations are generated deterministically from check details (e.g. "Python matched R-SAF-003 on 'burning smell'
→ Critical; GenAI proposed High").

## 2. Verification score & decision
Per ADR-018. Decision reasons (Step 57 mapping):
| Reason code | Step 57 wording |
|---|---|
| SIGNIFICANT_DISAGREEMENT | GenAI and Python disagree significantly (any critical check fail) |
| POLICY_SUPPORT_MISSING | no Applicable policy for primary issue / invalid or outdated citation |
| AMBIGUOUS | rule tie or UNCLASSIFIED |
| ESCALATION_UNCLEAR | escalation mismatch or level conflict |
| POLICY_CONTRADICTION | precedence/contradiction check failed |
| SENSITIVE | matched rule requires_review or category in always-review list |
| GENAI_FAILURE | Pipeline 1 unresolved failure |
| LOW_SCORE | score below threshold |

## 3. Final result (the SRS "complaint-intelligence result")
Start from GenAI output; apply ADR-010 enforcement (urgency, priority, escalation, department); attach Python
policy refs if GenAI's were invalid/outdated; set `customer_response.status = blocked` if any critical response check
failed or decision is Manual Review; else `approved` (auto-release allowed only when Verified).
Persist `validation_results` (python_expected, checks, comparison, score, decision, reasons, final_result).
Update complaint: status Analyzed → Assigned (Verified) or Escalated/Manual Review queue; assigned department; SLA due dates.

## 4. Displays
Agent/Reviewer workspace "Validation" tab: score gauge, decision badge + reasons, comparison table with color+icon
(✓ Match / ✗ Mismatch / ◐ Partial — never color alone), checks list grouped by severity with SRS references,
matched rules with evidence, enforced-field banner ("Python enforced urgency Critical (GenAI: High)").
