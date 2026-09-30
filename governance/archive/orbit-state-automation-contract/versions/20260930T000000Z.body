# Automation contract

> Orbit hosts automation JSON backups; some automations bind to other repos.
> IDE agents use the same `.state/` files plus optional ProjectBrain MCP.

**Last updated:** 2026-09-21

## Runtime (this workspace)

| Field | Value |
|-------|-------|
| Repo | `AlexTouvras/Orbit` |
| Branch | `main` |
| Playbooks | `.cursor/automations/*.json`, `docs/ops/daily-check.md` |

## Cadence (all six Hub field cards)

Every Hub field card refreshes **monthly**. There is no Friday field-card loop.

| When (EEST) | What | Cards |
|-------------|------|-------|
| 1st 17:00 (`0 14 1 * *` UTC) | Discover / judge picker and jobs | All six: Agentic AI, Analytics, Delivery, SDLC, Credit Risk, Story |
| 1st 18:00 (`0 15 1 * *` UTC) | Apply review (source-repo publish) | Agentic AI, Analytics, Delivery |
| First weekday on/after the 2nd | Fleet check | Leftover `chore/monthly-refresh-*` / missing hosted PR |

Public footers use `Next: <month>`, not “week of”.

## Automations managed from Orbit

| Name | Binds to | Trigger | Backup JSON | Live Cursor |
|------|----------|---------|-------------|-------------|
| Daily ops check | `AlexTouvras/Orbit` | Daily 08:00 Helsinki | `.cursor/automations/daily-ops-check.json` | *(not in account — create or restore)* |
| Agentic AI field card | `AlexTouvras/agentic-ai-field-card` | 1st 17:00 | `.cursor/automations/agentic-field-card-weekly-content-pass.json` | [c0138489…](https://cursor.com/automations/c0138489-8c1c-11f1-b532-320a589b8025) — **Monthly agentic AI field card content pass**, enabled |
| Analytics field card | `AlexTouvras/data-analytics-field-card` | 1st 17:00 | `.cursor/automations/analytics-field-card-weekly-content-pass.json` | [dd4bad7c…](https://cursor.com/automations/dd4bad7c-9558-11f1-ba66-0e7d0216e441) — **Monthly analytics field card content pass**, enabled |
| Delivery field card | `AlexTouvras/technology-delivery-field-card` | 1st 17:00 | `.cursor/automations/delivery-field-card-weekly-content-pass.json` | [c85fb72e…](https://cursor.com/automations/c85fb72e-970e-11f1-ba66-0e7d0216e441) — **Monthly delivery field card content pass**, enabled |
| Field card review | `AlexTouvras/Orbit` (gates the three source-repo cards) | 1st 18:00 | `.cursor/automations/field-card-review.json` | [a1c0b46b…](https://cursor.com/automations/a1c0b46b-9a09-11f1-ba66-0e7d0216e441) — **Monthly field card review**, enabled |
| Hosted SDLC + Credit Risk + Story | `AlexTouvras/Orbit` | 1st 17:00 | `.cursor/automations/hosted-field-card-monthly-review.json` | *(paste UUID if local created it — this Cloud Agent cannot list automations)* |

Looked up 2026-09-21 via GetAutomation after the local session: the four source-repo automations are **named Monthly** and enabled. Cron is still not returned from here. Hosted SDLC+Credit UUID is unknown unless pasted in.

**Who can mutate live automations:** a **local** Cursor session (`cursor-backend-control` `update_automation` / `/automate`). Cloud Agents on this repo do not get those tools.

## Primary verify

| Automation | Verify |
|------------|--------|
| Daily ops | Propose-only run complete; `#ops-channel` silent when green |
| Field card monthly | `node scripts/check-links.mjs` clean if HTML changed; PR `## Summary` has update/no-change decision |

## Scope (one run = one item)

One automation invocation → one judgment pass (ops digest, or one field-card monthly PR).

## Read order (before acting)

1. `.state/AUTOMATION_CONTRACT.md` (this file)
2. Matching `.cursor/automations/<name>.json`
3. Target repo playbook (`docs/ops/daily-check.md`, `docs/weekly-refresh-prompt.md`, …)
4. `.state/CURRENT_TASK.md`

Do **not** depend on ProjectBrain MCP. Cloud cannot see `~/.cursor/`.

## Write order (before exit)

| Automation | Writes |
|------------|--------|
| Daily ops | Slack `#ops-channel` only when issues; memories update |
| Source-repo field card (AI / analytics / delivery) | PR `chore/monthly-refresh-YYYY-MM`; stop for 18:00 review. Do not Slack-Approve from 17:00. |
| Hosted SDLC / Credit Risk | Orbit PR `chore/monthly-field-cards-YYYY-MM`. SDLC Summary lists opened URLs and `Decision: update` or `Decision: no-change`. Do not merge. |

## Out of scope

- Daily ops: no commit/push/merge from the agent
- Source-repo field cards: no merge except via 1st 18:00 review agent (`Apply review`). Slack is FYI.

## IDE coexistence

IDE sessions may use ProjectBrain MCP. Automations use playbooks + target repo state only.

Live Cursor automation **config** (cron, prompt, name) is mutated from a local Cursor session. Cloud Agents here only have GetAutomation metadata.
