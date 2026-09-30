# Automation contract

> Weekly judgment automation; JSON in-repo + Orbit backup.

**Last updated:** 2026-09-30

## Runtime

| Field | Value |
|-------|-------|
| Repo | `AlexTouvras/agentic-ai-field-card` |
| Branch | `main` |
| Primary verify | `node scripts/check-links.mjs` exits 0 when HTML/URLs changed |
| Playbook | `docs/weekly-refresh-prompt.md` |
| Automation JSON | `.cursor/automations/weekly-content-pass.json` |

## Automations

| Name | Trigger | Output | Human gate |
|------|---------|--------|------------|
| Weekly judgment | Cursor weekly-content-pass Fri 17:00 | discover + PR `## Summary` | Friday 18:00 review agent |
| Weekly review | Orbit Cursor automation Fri 18:00 | Apply review | review agent publishes |
| Judgment watchdog | GHA `judgment-watchdog.yml` Mon | `#orbit` warn/fail | human if Friday missed |

## Scope (one run = one item)

One weekly pass: discovery judgment → update **or** explicit no-change → PR `## Summary` → Friday 18:00 review publishes a card change.

Public footer `Next` is the next calendar month (`October 2026`), never `week of`. A no-change week does not move Reviewed or Next. Manual `weekly-refresh.yml` does not rewrite the stamp.

## Tool allowlist (automations)

| Allowed | Blocked |
|---------|---------|
| `npm run discover`, `node scripts/check-links.mjs`, `gh`, git | ProjectBrain MCP, browser MCP, deploy |

## Skill allowlist (automations)

| Allowed | Blocked |
|---------|---------|
| Weekly refresh prompt only | Power BI skills, harvest promote, unrelated portfolio skills |

## Read order (before acting)

1. `.state/AUTOMATION_CONTRACT.md` (this file)
2. `docs/weekly-refresh-prompt.md`
3. `data/discovery-report.md`, `index.html`
4. `.state/CURRENT_TASK.md`

Do **not** depend on ProjectBrain MCP or chat history.

## Write order (before exit)

1. `npm run discover` → decide update vs no-change
2. PR with `## Summary` + `Decision: update|no-change` (+ `## Card preview` if updating)
3. Stop. Do not notify Slack. Do not merge. Friday 18:00 review publishes.

## Out of scope

- Merge to `main` from the 17:00 content pass
- Slack Approve notify from the 17:00 content pass
- Invent docs URLs; framework picker > 7 rows
- Orbit static sync before the 18:00 review publishes

## Required secrets

| Secret | Notes |
|--------|-------|
| `WEEKLY_WRITE_SECRET` | Must match Orbit/Vercel |
| `SLACK_ORBIT_WEBHOOK_URL` | `#orbit` notifications |

## IDE coexistence

IDE sessions may use ProjectBrain MCP. Automations use this file + weekly playbook only.

Legacy index: `docs/automation-contract.md` points here.
