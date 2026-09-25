# 13 — UI / UX Specification (Streamlit)

## 1. Global design rules
- **Layout**: wide layout; left sidebar = role-based navigation + user badge + logout; page header = title + one-line purpose.
- **Consistency**: one component library in `src/app/components/` (status badge, priority chip, SLA badge, score gauge,
  comparison table, empty state, error box, confirm dialog, JSON viewer, source-reference chip). No ad-hoc styling in pages.
- **Visual language**: neutral background, one brand accent (Zephyra teal), semantic colors: Critical/P0 red,
  High/P1 orange, Medium/P2 amber, Low/P3 grey-blue, Verified green, Manual Review purple. Always pair color with text/icon
  (accessibility). CSS in `static/styles.css` injected once.
- **Feedback**: every action gives feedback — spinner with step labels for long operations, success toast, inline
  field errors next to the field, confirmation dialog for destructive/irreversible actions (activate prompt, replace_all rules,
  retire document, override decision).
- **Empty states**: explain what the page is for and the next action ("No documents yet — upload your first policy").
- **Errors**: friendly message + what to do + error reference (`ERR-7F3A21`) that maps to `app_errors` log. Never show
  stack traces, SQL, or API keys. GenAI unavailable → clear banner, complaint still saved and queued for review.
- **Forms**: labels + help text, sensible defaults, dropdowns from config, disabled submit until valid, preserve input on error.
- **Tables**: pagination (25/50/100), sortable columns, filters bar (config-driven `ui_filters`), export button where allowed.
- **Dates**: `YYYY-MM-DD HH:MM` + relative ("3h ago"); SLA countdown.
- **Security in UI**: page guard on every page; hide nav items the role cannot access; re-check permission in services.
- **Performance**: cache config and reference lists (`st.cache_data` with invalidation hooks); paginate queries.

## 2. Pages by role
**Common**: Login (lockout message, no user enumeration), Home (role landing), Profile.

**Customer**
- *Submit Complaint*: form (spec 11), attachment uploader with allowed types shown, preview + submit; result page with
  complaint ref, acknowledgement, and live analysis progress; if clarification needed, shows questions.
- *My Complaints* (Step 61): ID, status, submitted date, department, latest update, resolution status; filters; detail view
  with timeline, messages, answer clarification, attachments.

**Agent**
- *Agent Dashboard* (Step 62): assigned queue (category, priority, sentiment, GenAI recommendation summary, validation
  status, SLA, escalation warning icon), follow-ups due, KPIs (my open, at risk, breached).
- *Complaint Workspace* tabs: **Overview** (complaint, customer context, history, links to duplicates/repeats, injection
  warning) · **Intelligence** (final result fields, summary, agent guidance) · **Validation** (spec 09 §4) ·
  **Sources** (cited excerpts with source references, precedence notes) · **Response** (customer response with status
  blocked/approved, tone selector, follow-up, clarification questions, release button when allowed) · **GenAI JSON**
  (raw + parsed, run metadata: prompt version, model, provider, gateway, duration, attempts) · **History** (status,
  reviews, audit).
- *New Complaint (on behalf)*, *Upload Complaint File*, *Batch Import* (upload → mapping → validation preview → run → progress → report).
- *Search* (Step 66): all 9 fields + text search.

**Reviewer**: *Manual Review Queue*, *Review Workspace* (same tabs + actions panel, spec 12).

**Manager**: *Analytics* (Step 64), *Trends* (65), *Escalations board*, *SLA Monitor*, *Reports & Export* (67–68),
*GenAI vs Python* (mismatch analysis), *Audit Log* (read).

**Admin**: *Admin Dashboard* (Step 63), *Knowledge Base* (spec 10), *Rule Matrix* (spec 04 §7–8), *Configuration*
(spec 02 sections as tabs), *Prompt Templates* (spec 06), *Users & Roles*, *System Health* (DB, GenAI self-test,
last errors, BM25 index size, active prompt/schema versions), *Audit Log*.

## 3. Responsive behaviour (FR lxxv)
Use Streamlit columns that collapse on narrow screens; avoid wide fixed tables (use `st.dataframe` with column config);
keep key actions above the fold.
