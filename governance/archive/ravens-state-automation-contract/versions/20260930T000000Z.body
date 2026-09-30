# Automation contract

> Repo-scoped contract for Cursor Automations and other headless agent runs.
> IDE agents use the same `.state/` files plus optional ProjectBrain MCP.

**Last updated:** 2026-09-05

## Runtime

| Field | Value |
|-------|-------|
| Repo | `AlexTouvras/ravens` |
| Branch | `main` |
| Primary verify | `npm run verify` exits 0 |
| Ship gate | `npm run ship:check` (runs verify) |
| Playbooks | `agents/huginn.md`, `agents/muninn.md`, `agents/heimdall.md`, `docs/runbook.md` |

## Automations

| Name | Trigger | Output | Human gate | URL |
|------|---------|--------|------------|-----|
| Huginn | Daily 08:00 | `#ravens` + `inbox/YYYY-MM-DD.md` | review inbox | https://cursor.com/automations/732cacfb-955c-11f1-ba66-0e7d0216e441 |
| Muninn | GitHub push `huginn:` | `#ravens` knowledge signals | review signals | https://cursor.com/automations/c9afc8b1-955c-11f1-ba66-0e7d0216e441 |
| Heimdall | Sun 10:00 Helsinki | `watch/` on `main` | review clips; sync fitness snapshot | https://cursor.com/automations/6d39a6f4-9adc-11f1-ba66-0e7d0216e441 |

## Scope (one run = one item)

| Agent | One run produces |
|-------|------------------|
| Huginn | One daily inbox file |
| Muninn | Distill from one `huginn:` push |
| Heimdall | One weekly `watch/` pass |

## Read order (before acting)

1. `.state/AUTOMATION_CONTRACT.md` (this file)
2. Agent playbook (`agents/<name>.md`)
3. `.state/ARCHITECTURE.md`
4. `.state/CURRENT_TASK.md`

Do **not** depend on ProjectBrain MCP or chat history.

## Write order (before exit)

1. Complete agent output per playbook
2. `npm run verify` — must exit 0
3. Commit + push if playbook requires
4. Update `CURRENT_TASK.md` with verify output

## Out of scope

- Adding a database before verify + volume prove the need
- Inventing signals or inbox content

## IDE coexistence

IDE sessions may use ProjectBrain MCP. Automations use this file + `.state/` only.

Legacy copy: `docs/automation-contract.md` points here.
