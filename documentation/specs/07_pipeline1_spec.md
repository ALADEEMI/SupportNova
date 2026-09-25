# 07 — Pipeline 1: Python GenAI Complaint Intelligence

Package: `genai_pipeline/`. Orchestrated by `src/services/analysis_service.py`.

## 1. Steps
1. **Load** complaint + customer context (repositories).
2. **Retrieve** KB excerpts (`knowledge_base.retrieve(complaint)`, ADR-016). Record chunk codes and doc versions.
3. **Render** the active `complaint_analysis` prompt (spec 06) with the resolved schema (enums injected from config;
   for nullable enum properties the enum also includes `null`).
4. **Call** the model via `LLMClient` (ADR-007):
   - `temperature` (default 0), `timeout_seconds` (default 18 so the whole flow fits NFR-1's 20 s under normal conditions),
     structured output mode per config/self-test.
5. **Parse**: strip code fences if present → `json.loads` → `jsonschema` validation (Step 46 structural part).
6. **Retry policy** (Step 47):
   | Failure | Retry? | Retry message |
   |---|---|---|
   | Timeout / 5xx / rate limit | yes, exponential backoff (1s, 3s) | same request |
   | Invalid JSON | yes | append: "Your previous output was not valid JSON: <error>. Return only the JSON object." |
   | Schema violation | yes | append the list of validation errors (paths + messages) |
   | Auth / 4xx config errors | no | — |
   Max attempts = 1 + `max_retries` (default 2) → **never infinite**. Every attempt logged in `analysis_runs.attempt_errors`.
7. **Unresolved failure** → `analysis_runs.status = invalid_output|api_error|timeout`, complaint → Manual Review
   with reason `GENAI_FAILURE`; Pipeline 2 still computes Python-expected so the reviewer has ground truth; customer sees
   the system acknowledgement template.
8. **Persist** `analysis_runs` (raw output kept verbatim for Deliverable 6 "invalid responses" evidence).

## 2. LLMClient interface
```python
class LLMClient(Protocol):
    def complete_json(self, *, system: str, user: str, schema: dict, settings: GenAISettings) -> LLMResult: ...
# LLMResult: text, model, provider, gateway, latency_ms, usage (tokens), finish_reason
```
Implementation: `OpenAICompatibleClient`. Tests use `FixtureLLMClient` (tests only).

## 3. Self-test (Admin → System Health)
Button "Test GenAI connection": tiny request verifying auth, latency, model id and structured-output support; stores
the detected capability in settings (`use_structured_output`).

## 4. Other generation flows
- **Regenerate response** (reviewer action): prompt `response_regeneration`; inputs include enforced final fields and
  the failed checks so the new text avoids them; output schema `{customer_response, follow_up}`; re-validated by Pipeline 2 checks
  for promises/hallucinations before it can be approved.
- **Follow-up generation** on demand (agent chooses type): prompt `follow_up_generation`; validated by promise/hallucination checks.

## 5. Performance budget (NFR-1, 20 s)
Preprocess+retrieve < 0.5 s · LLM ≤ 15 s typical · Pipeline 2 + comparison < 1 s · DB writes < 0.5 s.
The analysis page shows step progress (Retrieving → Analyzing → Validating → Comparing). Duration stored per run
and reported (p50/p95) in the GenAI evidence report.

## 6. Acceptance summary
Valid JSON for normal complaints; retries bounded and logged; failures routed to review; prompt/model/provider/policy
versions logged on every run; no Python-expected data in the prompt.
