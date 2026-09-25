# ADR-003 — Pipeline 2 is rules-only

## Context
SRS: "This pipeline must not use a Generative AI API to approve the output of Pipeline 1."
1.9.2 lists validation methods: Pydantic, JSON Schema, regular expressions, Python rule engine, or other
**deterministic** methods. Anti-shortcut 18: GenAI must not replace business rules, ground-truth validation,
schema validation, policy precedence, escalation enforcement, audit or security logic.
Team decision: no learned models of any kind in Pipeline 2.

## Decision
Pipeline 2 uses only: the rule matrix (ADR-017), configuration tables, regex/lexicons, arithmetic,
database lookups, and deterministic string matching. It computes its own **Python-expected result** and runs
checks on the GenAI output. No LLM, no ML classifier, no embeddings.

## Consequences
- Fully explainable: every Python decision cites the rule IDs and the check that produced it.
- Coverage depends on rule quality → the matrix is large (~110 rules) and every hidden-pack change is added via Admin UI.
- If no classification rule matches with sufficient score, the complaint is `Unclassified by rules` → Manual Review (never a guess).

## SRS references
Pipeline 2 section, Steps 23, 28–31, 39, 46, CI-07, CI-18, NFR-4.
