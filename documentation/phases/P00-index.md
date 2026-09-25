# Build Plan — Phases and Slices

Each slice = one branch + one PR. A slice is **Done** only when its acceptance criteria are proven by tests and the
Definition of Done in CLAUDE.md §11 is met. Phase gates (✅) must pass before dependent phases start.

| Phase | Name | Depends on | Target day |
|---|---|---|---|
| P01 | Foundation (repo, config, DB, auth, LLM client, prompts) | — | Day 2 |
| P02 | Configuration & taxonomy admin | P01 | Day 2 |
| P03 | Knowledge base | P01 | Day 2–3 |
| P04 | Rule matrix | P02 | Day 3 |
| P05 | Complaint intake | P02 | Day 3 |
| P06 | Pipeline 1 — GenAI | P03, P05 | Day 3 |
| P07 | Pipeline 2 — Python validation | P04, P05 | Day 3 |
| P08 | Comparison, decision, final result | P06, P07 | Day 3–4 |
| P09 | Review, lifecycle, SLA, follow-ups | P08 | Day 4 |
| P10 | Dashboards, analytics, trends, reports, export | P09 | Day 4 |
| P11 | Data: documents, master data, 500 complaints, hold-out, hidden packs | P01 (starts Day 2 in parallel) | Day 2–4 |
| P12 | Evidence, deployment, documentation, drills | all | Day 4–5 |

## Phase gates
- **G1 (end Day 2):** P01+P02 done; documents authored & rendered; master data seeded; app runs with login.
- **G2 (end Day 3):** a complaint flows end-to-end: submit → P1 → P2 → decision visible in workspace; rules ≥100 loaded; dev set 400 generated.
- **G3 (end Day 4):** all FR implemented; deployed; hold-out evaluated; reports generated.
- **G4 (Day 5):** evidence, report, blog, video, drills complete; RTM 100% Done/Verified or N/A with justification.

## Every slice file lists
Goal · SRS references · Specs/ADRs to read · Tasks · Acceptance criteria (testable) · Tests · Evidence (RTM).
