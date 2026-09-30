# Automation contract

> Weekly judgment automation; JSON backup in Orbit (`website`).

**Last updated:** 2026-09-10

## Runtime

| Field | Value |
|-------|-------|
| Repo | `AlexTouvras/data-analytics-field-card` |
| Branch | `main` |
| Primary verify | `node scripts/check-links.mjs` exits 0 when HTML/URLs changed |
| Playbook | `docs/weekly-refresh-prompt.md` |
| Automation JSON | `website/.cursor/automations/analytics-field-card-weekly-content-pass.json` |

## Scope (one run = one item)

One weekly pass: discovery judgment → update **or** explicit no-change → PR `## Summary` → Friday 18:00 review publishes.

## Read order (before acting)

1. `.state/AUTOMATION_CONTRACT.md` (this file)
2. `docs/weekly-refresh-prompt.md`
3. `data/discovery-report.md`, `index.html`

Do **not** depend on ProjectBrain MCP.

## Write order (before exit)

1. `npm run discover` → decide update vs no-change
2. PR with `## Summary` + `## Card preview` if updating
3. Stop. Do not notify Slack. Do not merge. Friday 18:00 review publishes.

## IDE coexistence

IDE sessions may use ProjectBrain MCP. Automations use this file + weekly playbook only.
