# AI Tool Usage Declaration (SRS 1.8.19 and Deliverable 18)

Generative AI APIs are part of the application architecture (Pipeline 1). This file declares AI tools used
**during development**. Every AI-assisted change was reviewed, modified where required, tested and understood by the
listed team member(s).

| ID | Date | Tool (and model) | Purpose | Type of assistance | Files / modules affected | Modifications made by team | Tests performed | Verified by |
|---|---|---|---|---|---|---|---|---|
| AI-001 | YYYY-MM-DD | Claude (claude.ai) | Requirements analysis and planning | Read SRS, produced RTM, ADRs, specs, phase plan | documentation/ | Reviewed against SRS, corrected decisions (e.g. document versioning table) | Manual review against SRS | <name> |
| AI-002 | YYYY-MM-DD | Claude Code | Implement slice P01-S1 | Code generation | <paths> | <what the team changed> | make check | <name> |
| AI-003 | YYYY-MM-DD | CommandCode gateway (<model id>) | Dataset text generation | Wrote complaint texts from team-designed specs (labels by team) | sample_complaints/ | <regenerated/edited N texts> | validate_dataset.py | <name> |
