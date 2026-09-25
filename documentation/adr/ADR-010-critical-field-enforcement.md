# ADR-010 — Enforcement of critical fields ("most severe wins")

## Context
NFR-4: all mandatory escalation conditions and critical routing rules must be enforced **before** final
verification. Step 39: a critical complaint must not remain un-escalated because GenAI missed it.
Step 19 / CI-06: urgency must not be based solely on emotion.

## Decision
In the final result:
- `urgency = max(GenAI urgency, Python urgency)` by configured severity rank.
- `priority` = configured mapping of final urgency (plus overlay overrides).
- `escalation_required = GenAI OR Python`; `escalation_level` = highest rank of both.
- `department` = Python department when a classification rule matched with sufficient score; GenAI's is kept for comparison.
- Sentiment and emotion indicators are **never inputs** to Python urgency.
- Any enforcement that changed a GenAI value is recorded as a check with status `fail` → decision Manual Review,
  but the enforced values are applied immediately (safety first; the queue shows the reason).

## SRS references
Steps 18–21, 23, 36–39, NFR-4, CI-06, CI-07.
