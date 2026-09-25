# 03 — Data Model (SQLAlchemy 2.0; SQLite dev / PostgreSQL prod)

Conventions: integer PK `id`; `code` business keys unique; timestamps UTC `created_at`, `updated_at`;
soft activation via `is_active`; JSON columns for flexible structures. Alembic migrations for every change.

## A. Configuration (seeded, Admin-editable)
- `settings(key PK, value JSON, description, updated_by, updated_at)`
- `categories(id, code, name, description, is_active, sort_order)`
- `subcategories(id, category_id FK, code, name, required_fields JSON, is_active)`
- `departments(id, code, name, description, is_active)`
- `product_categories(id, code, name)`
- `products(id, sku, name, product_category_id FK, price, warranty_months, is_active)`
- `customer_types(id, code, name, description)`
- `channels(id, code, name, kind: complaint|contact)`
- `resolution_types(id, code, name)`
- `vocab_items(id, kind: sentiment|emotion|tone|follow_up_type|applicability, code, name, sort_order)`
- `urgency_levels(id, code, name, rank)` · `escalation_levels(id, code, name, rank)`
- `priority_rules(id, urgency_code, priority_code, description)` · `priorities(id, code, label, rank)`
- `sla_rules(id, priority_code, response_hours, resolution_hours)`
- `statuses(id, code, name, is_terminal)` · `status_transitions(from_code, to_code, allowed_roles JSON)`
- `actions(id, code, label, description, requires_eligibility bool, promise_lexicon_code)`
- `lexicons(id, code, name, kind: keywords|regex, entries JSON, description)`
- `doc_categories(id, code, name)` · `topics(id, code, name, category_codes JSON)`
- `precedence_rules(id, doc_category_code, rank)`
- `conflict_register(id, code, topic_code, description, doc_a_ref, doc_b_ref, resolution_note)`
- `checks_catalog(id, check_id, name, severity, weight, enabled, params JSON, srs_ref)`
- `ui_filters(id, page, field, label, enabled, sort_order)`
- `role_permissions(role, permission)`

## B. Identity & business data
- `users(id, username, full_name, email, password_hash, role, department_id FK null, is_active, failed_logins, locked_until, last_login_at)`
- `customers(id, customer_ref, user_id FK null, full_name, email, customer_type_code, created_at)` — fictional
- `orders(id, order_ref, customer_id FK, product_id FK, quantity, amount, order_date, delivery_date null, status)`
- `transactions(id, transaction_ref, order_id FK null, customer_id FK, amount, kind: charge|refund|installment, occurred_at, status)`
- `subscriptions(id, customer_id FK, service_code, status, renewal_date, price)`

## C. Knowledge base
- `documents(id, doc_code, title, doc_category_code, version, status: Active|Previous|Superseded|Draft, effective_date, expiry_date null, topics JSON, file_name, file_path, file_hash, content_hash, mime, size_bytes, page_count, uploaded_by, uploaded_at, supersedes_id FK null, notes)`
  unique(doc_code, version)
- `chunks(id, document_id FK, chunk_code, section_id, heading, page null, paragraph_index null, text, char_count, quarantined bool, quarantine_reason, source_reference)`
- `document_events(id, document_id, event: uploaded|activated|superseded|drafted|expired|quarantine_released, at, by, detail JSON)`

## D. Rules
- `rules(id, rule_code unique, rule_type, status, version, category_code null, subcategory_code null, applies_to_categories JSON null, conditions JSON, department_code null, supporting_department_code null, urgency_code null, priority_code null, escalation_required bool null, escalation_level_code null, required_actions JSON, prohibited_actions JSON, permitted_actions JSON, follow_up JSON, policy_doc_code, policy_section, weight int, requires_review bool, needs_review bool, description, updated_by, updated_at)`
- `rule_versions(id, rule_id, version, snapshot JSON, changed_by, changed_at, change_note)`
- `rule_import_jobs(id, file_name, mode: add|upsert|replace_all, status, total, created, updated, failed, report JSON, created_by, created_at)`

## E. Prompts
- `prompt_versions(id, prompt_id, version, status: Draft|Active|Retired, system_template, user_template, required_placeholders JSON, schema_version, changelog, created_by, created_at, activated_at, used bool)`

## F. Complaints
- `complaints(id, complaint_ref unique, customer_id FK, submitted_by FK users, channel_code, preferred_contact_code, product_id FK null, product_other_text null, order_id FK null, transaction_id FK null, previous_complaint_id FK null, requested_resolution_code null, title, description, normalized_text, text_hash, submitted_at, status_code, assigned_department_code null, assigned_agent_id null, priority_code null, urgency_code null, escalation_level_code null, sla_response_due_at, sla_resolution_due_at, first_response_at null, resolved_at null, is_duplicate bool, duplicate_of_id null, is_repeat bool, repeat_of_id null, injection_suspected bool, source: form|file|batch, import_job_id null)`
- `attachments(id, complaint_id, original_name, stored_name, mime, size_bytes, sha256, extracted_text null, uploaded_at)`
- `complaint_links(id, complaint_id, related_complaint_id, link_type: exact_duplicate|near_duplicate|repeat, score)`
- `complaint_import_jobs(id, file_name, format, column_mapping JSON, status, total, processed, failed, errors JSON, created_by, created_at, finished_at)`

## G. Processing & results
- `analysis_runs(id, complaint_id, run_no, started_at, finished_at, duration_ms, prompt_id, prompt_version, schema_version, provider, model, gateway, temperature, policy_versions JSON, retrieved_chunks JSON, request_payload JSON (redacted), raw_output TEXT, parsed_output JSON null, attempts int, attempt_errors JSON, status: success|invalid_output|api_error|timeout)`
- `validation_results(id, analysis_run_id, python_expected JSON, matched_rules JSON, checks JSON, comparison JSON, verification_score float, decision: Verified|Manual Review, decision_reasons JSON, final_result JSON, created_at)`
- `review_actions(id, complaint_id, validation_result_id, reviewer_id, action: approve|reject|modify|reclassify|reassign|escalate|regenerate|comment, before JSON, after JSON, comment, created_at)`
- `responses(id, complaint_id, kind: customer_response|follow_up|clarification|acknowledgement, body, source: genai|reviewer|system_template, status: draft|blocked|approved|sent, approved_by, approved_at)`
- `follow_ups(id, complaint_id, follow_up_type_code, due_at, message_response_id FK null, status: scheduled|done|overdue, created_at)`
- `status_history(id, complaint_id, from_code, to_code, changed_by, changed_at, note)`

## H. Audit & ops
- `audit_log(...)` — see ADR-015 (append-only)
- `app_errors(id, error_ref, occurred_at, where, message, user_id null)` — for the System Health page

## Indexes (NFR-1/NFR-2)
complaints(status_code, assigned_department_code, priority_code, submitted_at), complaints(customer_id),
complaints(text_hash), chunks(document_id), documents(doc_code, status), analysis_runs(complaint_id), audit_log(entity_type, entity_id).
