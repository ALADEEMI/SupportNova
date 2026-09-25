# ADR-007 — GenAI access through an OpenAI-compatible gateway

## Context
The team holds paid access through **CommandCode**, a gateway exposing OpenAI-compatible endpoints for several
providers. The SRS approves OpenAI API explicitly.

## Decision
- Use the official `openai` SDK. `base_url`, `model`, `temperature`, `timeout_seconds`, `max_retries`,
  `use_structured_output` come from configuration; the API key from env `OPENAI_API_KEY`.
- Select an **OpenAI model** served through the gateway so the model in use is an approved provider's model.
- Log truthfully on every run: `provider=openai`, `model=<exact id>`, `gateway=<host of base_url>`.
- Structured output: try `response_format={"type":"json_schema", ...}` (strict). If the gateway rejects it,
  fall back to `{"type":"json_object"}` + schema in prompt + `jsonschema` validation. Controlled by config flag,
  auto-detected by a startup self-test on the Admin "System Health" page.
- Switching to `api.openai.com` directly = change `base_url` only.

## Consequences
Provider/model/gateway are always visible in logs and reports (Deliverable 6).

## SRS references
Pipeline 1, Step 49, 1.9.2 item 5, Deliverable 6, Deliverable 12 (API configuration, secure key storage).
