# 12 — Review, Lifecycle, SLA and Follow-ups

## 1. Manual review queue (Step 57, FR lxi)
Items: decision = Manual Review. Columns: complaint ref, category, priority, SLA remaining, reasons (chips), score,
age, assigned reviewer. Sort default: priority rank, then SLA remaining. Filters: reason, category, department, priority.

## 2. Reviewer actions (Step 58, FR lxii) — each opens a form, requires comment for reject/modify/reclassify/reassign/escalate
| Action | Effect |
|---|---|
| Approve | accepts final result; releases response (status approved) |
| Reject | rejects recommendation; complaint returns to agent with reason; response stays blocked |
| Modify | edit final fields (dropdowns from config) and/or response text; edited response re-checked for promises/claims |
| Reclassify | change category/subcategory → Pipeline 2 recomputes expected + checks for the new classification |
| Reassign | change department / agent |
| Escalate | set escalation level (≥ current), status Escalated, escalation notes editable |
| Regenerate response | Pipeline 1 `response_regeneration` → re-validated |
| Add comment | note on the complaint |
All actions write `review_actions` with before/after and `audit_log`; originals never overwritten (Step 59).

## 3. Status lifecycle (Step 60, FR lxv)
Default transitions (configurable): New→Analyzed (auto) → Assigned (auto if Verified) → In Progress → Awaiting Customer
⇄ In Progress → Resolved → Closed; Resolved/Closed → Reopened → In Progress; any open → Escalated → In Progress.
Illegal transitions blocked with a message. `status_history` records every change.

## 4. SLA (Steps 55–56, FR lix–lx)
At analysis: `sla_response_due_at = submitted_at + response_hours(priority)`, `sla_resolution_due_at = submitted_at + resolution_hours(priority)`.
Recomputed when priority changes (audited). States: On Track / At Risk (elapsed ≥ risk threshold %) / Breached.
`first_response_at` set when first approved response is released. SLA badges on all lists; SLA monitor page.
Assumption (documented): calendar hours, not business hours.

## 5. Follow-ups (Steps 40–41, FR xxxvii–xxxviii)
When follow-up required: create `follow_ups` row (type, due_at from rule within_hours or GenAI suggestion capped by rule).
Agent dashboard "Follow-ups due". Agent can generate a follow-up message of any type (prompt follow_up_generation → validated).
Messages are shown to the customer in their dashboard and formatted per preferred contact channel (email subject+body,
chat short text) for manual sending — no live channel integration (SRS 1.4).

## 6. Customer communication
Customer sees: acknowledgement (system template), approved responses, clarification questions (can answer in the
complaint thread → status Awaiting Customer → In Progress; answer appended, re-analysis available), follow-ups, status timeline.
Never sees: internal notes, scores, GenAI raw output, agent guidance.
