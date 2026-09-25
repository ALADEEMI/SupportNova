# 14 — Service Layer & API Specification

The UI and the optional REST API call **only** these services. All inputs/outputs are Pydantic models.
All methods take an `actor: CurrentUser` and enforce permissions.

| Service | Key methods |
|---|---|
| AuthService | login(username, password) → Session · logout · change_password · lock/unlock (admin) |
| ConfigService | get_list(name) · get_setting(key) · upsert_item(list, item) · deactivate(list, code) · export/import(yaml) · invalidate() |
| DocumentService | preview_upload(file, meta) → UploadDecision · commit_upload(preview_id) · list/get · versions(doc_code) · chunks(doc_id) · release_quarantine(chunk_id) · impact_analysis(doc_id) |
| RuleService | list/get/create/update/deactivate · validate_rule(rule) · simulate(text or complaint_id) · import_preview(file) → ImportReport · import_commit(preview_id, mode) · export(format) |
| PromptService | list · get(prompt_id, version) · clone · update_draft · validate · preview(complaint_id) · test_run(complaint_id) · activate · retire · delete_draft · export |
| ComplaintService | submit(form) · submit_file(file) · get(ref) · list(filters, page) · history(customer) · answer_clarification(ref, text) · change_status(ref, to, note) |
| ImportService | preview(file, mapping) · start(job) · progress(job_id) · error_report(job_id) |
| AnalysisService | analyze(complaint_id) → AnalysisOutcome (runs P1 → P2 → comparison, persists all) · reanalyze(complaint_id) |
| ReviewService | queue(filters) · approve · reject · modify · reclassify · reassign · escalate · regenerate_response · comment |
| ResponseService | release(response_id) · generate_follow_up(complaint_id, type) |
| SLAService | compute_due(complaint) · status(complaint) · at_risk(list) |
| AnalyticsService | kpis(filters) · distributions(dim, filters) · trends(dim, window) · mismatch_stats() |
| ReportService | generate(report_code, filters, format) → file · list_generated() |
| AuditService | record(event) · query(filters) |
| HealthService | db_ok · genai_self_test · index_stats · recent_errors |

## Optional REST API (FastAPI, `src/api/`) — after mandatory slices
`GET /health` · `POST /auth/token` · `POST /complaints` · `POST /complaints/{ref}/analyze` · `GET /complaints/{ref}` ·
`POST /imports/complaints` · `GET /imports/{job_id}` · `GET /reports/{code}?format=csv|pdf|xlsx`.
Bearer token auth, same permission checks, OpenAPI docs at `/docs`. Useful for evaluators and scripted hidden-pack runs.
