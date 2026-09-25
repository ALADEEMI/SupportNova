# ADR-011 — Prompt-injection and adversarial-content defense

## Context
Steps 50–51, FR liv–lv, CI-08, Deliverable 10 (prompt injection, fake policy statement, invalid policy ID,
unauthorized compensation, malicious document instruction).

## Decision (defense in depth)
1. **Structural isolation**: complaint text and document excerpts are placed in clearly delimited data blocks
   (`<complaint_data>`, `<policy_excerpt ...>`); angle brackets inside data are escaped. The system prompt states that
   data blocks are untrusted and never instructions.
2. **Detection** (Python, deterministic): configurable pattern lexicon (e.g. "ignore (all|your) (rules|instructions)",
   "as (an|the) admin", "system prompt", "approve (my|a) (full )?refund", fake policy IDs, "policy says" claims) →
   `injection_suspected` flag with matched evidence, shown to agents.
3. **Documents**: chunks matching injection patterns at upload are **quarantined** (excluded from retrieval) until an
   admin reviews them.
4. **Outcome control (the real guarantee)**: whatever the model says, Pipeline 2 checks every promise, action,
   compensation and policy ID against rules; unsupported ones fail → response blocked → Manual Review.
5. Customer-supplied "policy claims" are never treated as policy; only DB documents are sources.

## SRS references
Steps 50–51, 34–35, FR liv–lv, CI-08, CI-09, Deliverable 10, Hidden pack (prompt-injection complaint).
