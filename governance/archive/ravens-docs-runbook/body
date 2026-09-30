# Operations runbook

## Daily rhythm (Europe/Helsinki)

| Time | Agent | Expectation |
|------|-------|-------------|
| 08:00 | Huginn | `inbox/YYYY-MM-DD.md` committed to `main` |
| on that push | Muninn | knowledge/signals/index updated from last 48h inbox |
| 09:00 | Muninn (retry) | Runs only if HEAD is still `huginn:` (push trigger missed) |
| weekly / on-demand | Heimdall | `watch/` notes on `main`; consumers match by slug / Coach library / stage |

Cloud Agent compute must be enabled in the [Cloud Agents dashboard](https://cursor.com/dashboard?tab=cloud-agents).

## Verify (named gate)

From repo root:

```powershell
npm run verify
```

Must exit 0 before calling the foundation “healthy”. After each automation lands, re-run verify locally or in a follow-up agent.

## Failure modes

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| No inbox file | Huginn failed or cron/tz misconfigured | Check automation run log; run Huginn manually |
| Run history **Failed <1m** / Rate limited | Team concurrent cloud-agent cap at 06:00/07:00 pileup | Test-run after the wave; keep Huginn after 08:00, not on the 06:00/07:00 hour |
| Run history **Failed ~3m** / usage or spend limit | Cloud agent owner hit a Cursor usage cap | Open the run summary; Manage settings / wait for reset; then Test-run Muninn |
| Inbox on `cursor/*` branch, not `main` | Cloud agent branched instead of pushing `main` | Cherry-pick onto `main` (Muninn's push trigger needs `huginn:` on `main`); confirm Open PR tool is off |
| Inbox on `main` but no Muninn commit | Push trigger missed, or playbook aborted a non-`huginn:` HEAD | Check Muninn run history; Test-run Muninn |
| Muninn commit on `main` but no Slack digest | Distill run **Cancelled** when Muninn’s own push retriggers the automation (before Slack) | Playbook must **Send to Slack before push**; confirm in run log; Test-run Muninn |
| Lift names unlinked in fitness HTML/Slack | Heimdall gap or missing `Coach library:` line in watch note | Fill slug in `sight.md`; Heimdall run; then `coach-strength --sync-videos` in fitness |
| Verify fails on frontmatter | Contract drift | Fix file or bump contract version deliberately |
| Duplicate FIND/SIG ids | Non-idempotent rewrite | Dedupe; keep earliest; link in changelog |

## Manual runs

In Cursor Automations, use “Run now” on Huginn first. Muninn should start from that `huginn:` push to `main`. If it does not, Test-run Muninn (skips the `huginn:` gate).

## Extending later (not v1)

- **ProjectBrain MCP** — expose curated hubs as portfolio memory tools
- **Consumer automations** — mealplan/field-card/Orbit *read* signals and open PRs
- **Search index** — only if markdown grep becomes painful
- **World Monitor / OSINT MCP** — personal dashboard only; do not ingest into Huginn

Do not add a database until verify + volume prove the need.
