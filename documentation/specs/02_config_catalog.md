# 02 — Configuration Catalog (everything editable from the Admin UI)

Rule: if it is a business value, it is here, stored in the DB, seeded from `config/seed/`, and edited in
**Admin → Configuration** (unless noted). Every change is audited and invalidates the `ConfigService` cache.

| # | Item | Table | Admin screen | Used by | SRS |
|---|---|---|---|---|---|
| 1 | Categories (name, code, description, active, display order) | `categories` | Taxonomy | schema enums, prompt, rules, UI, reports | Step 14, CI-05 |
| 2 | Subcategories (+ `required_fields` for missing-info) | `subcategories` | Taxonomy | same + missing-info | Steps 15, 42 |
| 3 | Departments | `departments` | Departments | routing, assignment, schema | Step 22, CI-14 |
| 4 | Products (name, sku, product_category, price, warranty_months) | `products` | Products (+CSV import) | form dropdown, entity checks, rules | 1.2, Step 9 |
| 5 | Product categories | `product_categories` | Products | rule conditions | — |
| 6 | Customer types | `customer_types` | Customers | rules (VIP case) | Step 21 |
| 7 | Channels / preferred-contact channels | `channels` | Lists | form | 1.2, Step 9 |
| 8 | Requested resolutions | `resolution_types` | Lists | form, rules | 1.2 |
| 9 | Sentiment values, emotion indicators | `vocab_items` (kind) | Lists | schema, prompt | Steps 17–18 |
| 10 | Urgency levels (name, rank) | `urgency_levels` | Levels | schema, enforcement | Step 19 |
| 11 | Priority mapping urgency → priority | `priority_rules` | Priority Logic | Pipeline 2 | Step 20, CI-14 |
| 12 | Escalation levels (name, rank) | `escalation_levels` | Levels | schema, enforcement | Step 37 |
| 13 | Action catalog (code, label, requires_eligibility, promise_lexicon) | `actions` | Actions | schema enum, checks | Steps 27–31, 34 |
| 14 | Lexicons (named keyword/regex lists) | `lexicons` | Lexicons | rule DSL, injection, promises | Steps 34, 50–51 |
| 15 | Rule matrix | `rules`, `rule_versions` | Rule Matrix | Pipeline 2 | Step 8, D-5 |
| 16 | SLA targets per priority | `sla_rules` | SLA | due dates | Step 55, CI-14 |
| 17 | SLA risk threshold (% elapsed) | `settings` | SLA | risk flag | Step 56 |
| 18 | Complaint statuses + allowed transitions | `statuses`, `status_transitions` | Lifecycle | review, UI | Step 60 |
| 19 | Follow-up types | `vocab_items` | Lists | schema, follow-ups | Step 40 |
| 20 | Response tones + default tone | `vocab_items`, `settings` | Lists | prompt | Step 33 |
| 21 | Document categories + topics | `doc_categories`, `topics` | Knowledge Base | upload, precedence | Steps 4, 26 |
| 22 | Precedence order | `precedence_rules` | Knowledge Base | contradictions | CI-10 |
| 23 | Conflict register | `conflict_register` | Knowledge Base | explanations | CI-10 |
| 24 | Upload limits (types, max size, max count) | `settings` | System | uploads | Steps 4, 10 |
| 25 | Complaint validation limits (min/max length, required form fields) | `settings` | Intake | validation | Step 10 |
| 26 | Duplicate thresholds (near-dup ratio, lookback days) | `settings` | Intake | dedup/repeat | Steps 52–54 |
| 27 | Retrieval params (top_k, max per doc, max chars, min score) | `settings` | GenAI | retrieval | Step 25 |
| 28 | GenAI params (base_url, model, temperature, timeout, max_retries, structured-output flag) | `settings` | GenAI | Pipeline 1 | Steps 47, 49 |
| 29 | Active prompt version per prompt_id | `prompt_versions` | Prompt Templates | Pipeline 1 | Steps 48–49 |
| 30 | Verification weights, pass threshold, critical checks list, always-review categories | `settings` | Verification | decision | FR li, Step 57 |
| 31 | Check catalog (enable/disable, severity) | `checks_catalog` | Verification | Pipeline 2 | CI-14 "add validation rule" |
| 32 | Trend detection window & growth threshold | `settings` | Analytics | trends | Step 65 |
| 33 | Dashboard filters (which fields are filterable) | `ui_filters` | Dashboards | search/filter | Step 66, CI-14 |
| 34 | Roles & permissions | `role_permissions` | Users & Roles | RBAC | FR ii |
| 35 | Security settings (lockout attempts, session timeout) | `settings` | System | auth | FR i |
| 36 | Organization name & branding | `settings` | System | prompt, UI | Step 1 |

Not editable from UI (by design):
- **API keys / DATABASE_URL** — environment only (security).
- **JSON Schema file** — edited as a file + version bump (ADR-005). Admin UI shows it read-only with its version.

## "Add a new validation rule" (CI-14) without code
Two paths: (a) a new **rule** in the matrix (most cases), or (b) a new **configurable check** of type
`lexicon_forbidden_in_response` / `required_action_for_category` / `field_required_for_category` created in
Admin → Verification → Checks (parameterized check templates implemented once in code).
