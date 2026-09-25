# P09 — Review, Lifecycle, SLA, Follow-ups

## P09-S1 Manual review queue & reviewer actions
- **SRS:** Steps 57–59; FR lxi–lxiv · **Read:** spec 12 §1–2
- **Acceptance:** 8 actions work with required comments; before/after stored; originals preserved; audit entries.
- **Tests:** test_review_actions.py, test_override_audit.py

## P09-S2 Status lifecycle
- **SRS:** Step 60; FR lxv · **Acceptance:** configured transitions enforced; history recorded. **Tests:** test_transitions.py

## P09-S3 SLA tracking & risk
- **SRS:** Steps 55–56; FR lix–lx · **Acceptance:** due dates, at-risk, breached; recompute on priority change; SLA monitor page. **Tests:** test_sla.py

## P09-S4 Follow-ups & customer communication
- **SRS:** Steps 40–41, 43; FR xxxvii–xl, lxvi · **Read:** spec 12 §5–6
- **Acceptance:** follow-ups scheduled and listed; customer sees only approved messages; clarification answer loop works.
- **Tests:** test_follow_ups.py, test_customer_visibility.py
