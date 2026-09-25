# 20 — Claude Code Skills Setup (project-local, git-ignored)

Claude Code loads project skills from `.claude/skills/<skill-name>/SKILL.md` in the repository root.
Per team decision, the whole `.claude/skills/` folder is **git-ignored** (see `.gitignore`).

## 1. Project-specific skills (provided in this kit — copy as-is)
| Skill | Purpose |
|---|---|
| slice-delivery | Execute a slice end-to-end with the Definition of Done |
| srs-compliance-review | Verify a change against the SRS items it claims |
| no-hardcode-audit | Detect hard-coded business values, prompts in code, AI in Pipeline 2 |
| rtm-update | Update RTM Status/Evidence columns safely |

## 2. Official Anthropic skills (optional, recommended)
Anthropic publishes example skills in the public repository `github.com/anthropics/skills`. Useful here:
`docx` and `pdf` (render company documents, PDF reports), `xlsx` (Excel exports and the RTM), and
`webapp-testing` (browser-level UI smoke tests) — **verify these folders exist in the repository at install time**;
names and contents may change.
```bash
git clone --depth 1 https://github.com/anthropics/skills /tmp/anthropic-skills
ls /tmp/anthropic-skills/skills            # confirm available skill folders
for s in docx pdf xlsx webapp-testing; do
  [ -d /tmp/anthropic-skills/skills/$s ] && cp -r /tmp/anthropic-skills/skills/$s .claude/skills/
done
```
Restart Claude Code after installing so it discovers the skills. Review each skill's license file before use.

## 3. Rule
Skills help Claude Code; they never replace the specs. If a skill conflicts with CLAUDE.md or the SRS, CLAUDE.md and the SRS win.
