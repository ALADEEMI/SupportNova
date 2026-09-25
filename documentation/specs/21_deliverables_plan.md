# 21 — Deliverables Plan (SRS 1.10 → where it is produced)

| # | Deliverable | Produced by | Location |
|---|---|---|---|
| 1 | Project report (32 sections incl. DFD, Use Case, Activity, Sequence diagrams) | P12-S3; diagrams in Mermaid → exported PNG | documentation/report/SupportNova_Project_Report.docx + .pdf |
| 2 | Source code (mandatory structure) | all phases | repo root |
| 3 | Complaint dataset (500 + metadata + expected labels + difficult cases) | P11 | sample_complaints/ |
| 4 | Knowledge-base dataset (policies, SOPs, FAQs, rules, metadata, versions, conflicts) | P11 | sample_documents/, complaint_rules/, routing_rules/, escalation_rules/ |
| 5 | Rule matrix (12 columns) | P03 + export | complaint_rules/…, reports/rule_matrix.xlsx |
| 6 | GenAI pipeline evidence (provider, model, prompts, versions, config, sample requests/responses, invalid responses, retries) | P12-S1 exporter from analysis_runs | reports/genai_evidence/ |
| 7 | Python validation evidence (10 items) | test reports + P12-S1 | reports/validation_evidence.md |
| 8 | GenAI vs Python comparison (≥100 unseen) | `make eval-holdout` | reports/comparison_report.{csv,xlsx,pdf} |
| 9 | Complaint intelligence report | ReportService D9 | reports/complaint_intelligence_report.pdf |
| 10 | Security & adversarial report | tests/security + generator | reports/security_report.md/.pdf |
| 11 | Test cases (20 categories) | tests/ + `reports/test_summary.md` | tests/, reports/ |
| 12 | Installation instructions | README.md §Installation | README.md |
| 13 | Execution instructions (14 flows) | README.md §Usage | README.md |
| 14 | GitHub repository requirements | ongoing | GitHub |
| 15 | Deployed app + evaluator/admin credentials + samples + testing instructions | P12-S2 | README.md §Evaluation |
| 16 | Demonstration video (.mp4, 21 items) | P12-S4 script → recording | documentation/video_script.md |
| 17 | Technical blog ≥2,000 words (20 topics) | P12-S5 | documentation/blog/ + published URL in README |
| 18 | AI_USAGE.md | every slice | AI_USAGE.md |
| 19 | Final checklist + team contribution record | P12-S6 | documentation/final_checklist.md, documentation/team_contribution.md |
