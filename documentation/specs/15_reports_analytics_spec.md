# 15 — Dashboards, Analytics, Trends, Reports, Export

## 1. Admin dashboard (Step 63)
KPIs: total complaints, open, escalations, manual-review cases, SLA at risk, SLA breached, GenAI/Python mismatch rate,
average verification score. Charts: category distribution, department distribution, priority levels, resolution status.

## 2. Analytics (Step 64) — filters: date range, category, product, department, priority, channel
Volume over time; by category; by product/service; by department; by urgency; by sentiment; escalations over time;
resolution time (median, p90) by category/department; repeat complaints rate.

## 3. Trend detection (Step 65) — deterministic
For each dimension value (category, subcategory, product, department, escalation count): compare current window
(config, default 7 days) vs previous window. Flag **Rising** when count ≥ min_count AND growth ≥ threshold %;
"Recurring product issue" when same product+subcategory appears ≥ N times in window; "Escalation spike" when escalations
growth ≥ threshold. Shown as trend cards with sparkline and the numbers behind the flag.

## 4. Reports (Step 67) — each available as CSV, Excel, PDF (Step 68)
| Code | Report | Content |
|---|---|---|
| R1 | Complaint Analysis | per complaint: ref, dates, category, subcategory, priority, sentiment, department, status, decision, score |
| R2 | Department Performance | volume, open, resolved, median resolution time, SLA compliance %, escalations per department |
| R3 | Escalations | escalated complaints, level, triggers, time to escalate |
| R4 | SLA Status | on track / at risk / breached per priority and department |
| R5 | Policy Usage | citations per document/section, outdated citations, precedence corrections |
| R6 | Resolution Compliance | required actions present %, prohibited actions found, promises blocked, hallucinations flagged |
| R7 | GenAI vs Python Comparison | Deliverable 8 columns per complaint + match rates per field + disagreement explanations |
| R8 | Manual Reviews | queue history, reasons, reviewer actions, overrides (original vs final) |
| D9 | Complaint Intelligence Report | Deliverable 9 bundle: category/priority/sentiment distributions, routing, escalations, repeats, SLA risk, policy usage, disagreements, manual reviews |
| D10 | Security & Adversarial Report | results of the adversarial test suite + injection-flag statistics |

PDF: ReportLab with Jinja-free simple layout (title, filters, generated_at, tables, charts as PNG via Plotly/kaleido if available,
else tables only). Excel: one sheet per table. CSV: UTF-8 with header. **CSV/Excel injection guard**: prefix cells
starting with `= + - @` with `'`. Exports audited.
