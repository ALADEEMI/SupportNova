# 06 — Prompt Management Specification

## 1. Storage
- Seed: `prompt_templates/<prompt_id>/v<semver>.yaml` (fields: prompt_id, version, schema_version, status, changelog,
  required_placeholders, system_template, user_template). Loaded by `make seed` into `prompt_versions`.
- Runtime source of truth: `prompt_versions` table. Exactly one `Active` version per `prompt_id`.

## 2. Prompts in the system
| prompt_id | Purpose | Pipeline |
|---|---|---|
| complaint_analysis | Full complaint intelligence JSON (single call) | 1 |
| response_regeneration | Rewrite the customer response when a reviewer clicks *Regenerate* (inputs: original analysis, reviewer instructions, enforced final fields, failed checks) | 1 |
| follow_up_generation | Generate a follow-up message of a given type when an agent requests one later in the lifecycle | 1 |

No prompt is used by Pipeline 2.

## 3. Placeholders (rendered by `genai_pipeline/prompt_renderer.py`)
| Placeholder | Content |
|---|---|
| org_name | settings.organization_name |
| today | ISO date |
| allowed_values | formatted lists from ConfigService: `CODE — Name — description` per line, grouped by list |
| action_catalog | `ACTION_CODE — label — description` |
| tone | selected tone (default from settings, overridable per complaint by agent) |
| output_schema | resolved JSON Schema (enums injected) |
| customer_context | customer type, order (sku, amount, order/delivery dates, status), active subscriptions, prior complaints (count, unresolved count, refs) — facts only |
| complaint_data | complaint ref, channel, submitted date, product, order/transaction refs, requested resolution, title, description (escaped), attachment names + extracted text excerpts (escaped, truncated) |
| policy_context | retrieved excerpts, each as `<policy_excerpt doc="ZEP-POL-003" version="3.0" status="Active" category="Policy" section="3.1" source="ZEP-POL-003 v3.0 §3.1 Eligibility, p.2">…</policy_excerpt>` |

Rendering fails fast (ConfigurationError) if a required placeholder is missing in the template or unresolved.
Escaping: `<` and `>` inside data become `‹` `›`; data blocks are truncated to configured limits with a visible marker.

## 4. Admin UI — Prompt Templates
- List prompt_ids with Active version, last used, number of runs.
- Version list with status; **view**, **diff** (side-by-side), **clone to new version** (auto-bump patch/minor),
  **edit Draft**, **validate** (placeholders present, schema_version exists), **preview** (render with a chosen
  complaint, show final messages, token/char count), **test run** (calls the API on the chosen complaint without
  saving a decision — result shown with a "test run" banner), **activate** (confirmation dialog), **retire**, **delete**
  (only never-used Drafts), **export** all versions to YAML.
- Every action audited. Versions with `used = true` are read-only.

## 5. Logging (Step 49)
Each `analysis_runs` row stores prompt_id, prompt_version, schema_version, provider, model, gateway, temperature,
timestamp, policy_versions used (doc_code → version for every excerpt sent).
