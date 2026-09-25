# START HERE — SupportNova planning kit

## What is in this kit
| Path | Content |
|---|---|
| `CLAUDE.md` | Binding instructions for Claude Code (read every session) |
| `documentation/srs/` | Official SRS (source of truth) |
| `documentation/SupportNova_RTM.xlsx` | Traceability: every SRS item as a row (Status/Evidence) |
| `documentation/adr/` | 18 architecture decisions |
| `documentation/specs/` | 21 detailed specifications |
| `documentation/phases/` | 12 phases → slices with acceptance criteria |
| `schemas/complaint_intel.schema.json` | GenAI output contract (v1.0.0) |
| `prompt_templates/complaint_analysis/v1.0.0.yaml` | First prompt template |
| `config/seed/*.yaml` | Seed configuration (taxonomy, vocabularies, actions, lexicons, settings) |
| `.claude/skills/` | 4 project skills (git-ignored) |
| `.gitignore`, `AI_USAGE.md`, `.github/pull_request_template.md` | Repo scaffolding |

## Setup (once)
1. Create the GitHub repository (public) and clone it. Copy this kit's contents into the repo root.
2. Install Claude Code, open the repo folder, start Claude Code.
3. (Optional) Install official Anthropic skills: `documentation/specs/20_skills_setup.md`.
4. Create `.env` from `.env.example` (created in P01-S1): `OPENAI_API_KEY`, `OPENAI_BASE_URL` (CommandCode OpenAI-compatible URL), `DATABASE_URL`, `APP_SECRET_KEY`, seed passwords.
5. First commit: `docs: add SRS, planning kit, ADRs, specs and phase plan`.

## Working with Claude Code — session prompts
- First session: "Read CLAUDE.md and documentation/START_HERE.md. Summarize the plan and list any questions. Then run slice P01-S1 using the slice-delivery skill."
- Each next slice: "Run slice P0X-SY using the slice-delivery skill."
- In parallel (data track): "Run slice P11-S1 using the slice-delivery skill" (author documents), then P11-S2, P11-S3.
- Before merging: "Run srs-compliance-review and no-hardcode-audit on this branch."

## Order for the remaining days
Day 2: P01 → P02; data track P11-S1…S3. · Day 3: P03 → P04 → P05 → P06 → P07; P11-S4. ·
Day 4: P08 → P09 → P10; P11-S5, S6; P12-S1, S2. · Day 5: P12-S3…S7.
