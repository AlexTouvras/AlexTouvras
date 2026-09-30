# Automation contract

> Weekly judgment automation binds here; JSON backup lives in Orbit (`website`).

**Last updated:** 2026-09-10

## Runtime

| Field | Value |
|-------|-------|
| Repo | `AlexTouvras/technology-delivery-field-card` |
| Branch | `main` |
| Primary verify | `node scripts/check-links.mjs` exits 0 when HTML/URLs changed |
| Playbook | `docs/weekly-refresh-prompt.md` |
| Automation JSON | `website/.cursor/automations/delivery-field-card-weekly-content-pass.json` |
| Live URL | https://cursor.com/automations/c85fb72e-970e-11f1-ba66-0e7d0216e441 |

## Scope (one run = one item)

One weekly pass: discovery judgment → update **or** explicit no-change → PR `## Summary` → Friday 18:00 review publishes.

## Read order (before acting)

1. `.state/AUTOMATION_CONTRACT.md` (this file)
2. `docs/weekly-refresh-prompt.md`
3. `data/discovery-report.md`, `index.html`
4. `.state/CURRENT_TASK.md`

Do **not** depend on ProjectBrain MCP.

## Write order (before exit)

1. `npm run discover` → decide update vs no-change
2. PR with `## Summary` + `## Card preview` if updating
3. Stop. Do not notify Slack. Do not merge. Friday 18:00 review publishes.

## Out of scope

- Merge to `main` from the 17:00 content pass
- Slack Approve notify from the 17:00 content pass
- Invent doc URLs; Scrum/SAFe brochure drift

## IDE coexistence

IDE sessions may use ProjectBrain MCP. Automations use this file + weekly playbook only.
