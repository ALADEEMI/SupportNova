# ADR-005 — JSON Schema is the single source of truth for GenAI output

## Context
Step 46 requires validating required fields, data types, valid categories, urgency values, department IDs,
policy IDs and escalation status. CI-14 may ask to **change the JSON schema** live.

## Decision
- `schemas/complaint_intel.schema.json` defines the GenAI output. Properties that must take configured values
  carry a custom keyword `"x-enum-source": "<config list>"`; the loader injects the current enum at runtime.
- The same resolved schema is: (1) embedded in the prompt, (2) passed to the API as structured-output format when
  supported, (3) used by `jsonschema` validation, (4) used to render the "GenAI JSON" view in the UI generically.
- Schema changes = edit the file + bump `schema_version` + create a new prompt version. No code change for adding
  optional fields; UI renders unknown fields generically.
- No self-reported "confidence" field (would look like a fabricated confidence value, CI-17).

## Consequences
One edit propagates everywhere. Schema version is stored with every analysis run.

## SRS references
1.2 sample JSON, Pipeline 1 ("predefined structured JSON"), Steps 46–47, FR xliii–xliv, CI-14, CI-17.
