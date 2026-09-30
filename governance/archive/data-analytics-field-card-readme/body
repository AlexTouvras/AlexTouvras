# Data Analytics Field Card

Standalone one-pager: [`index.html`](./index.html)

**Live:** after Pages is enabled â†’ `https://alextouvras.github.io/data-analytics-field-card/`

Public artifact only. Editor / maintenance notes live **here** and under `docs/`, not on the card.

## Use across channels

| Channel | How |
|---|---|
| **Browser / site** | GitHub Pages URL, or Orbit `https://alextouvras.com/analytics-field-card/` |
| **PDF** | Open â†’ Print / PDF (landscape A4) |
| **LinkedIn** | Share the Pages URL; caption can reuse the H1 + lede |
| **Email / Slack** | Attach PDF or paste link |

## What this card is (and is not)

| Is | Is not |
|---|---|
| Decision stack: ASK â†’ GRAIN â†’ TRUTH â†’ USE | A Power BI / Fabric product brochure |
| When to use curated tables, metrics layers, notebooks, scorecards, lineage | An interview flashcard deck |
| Tool picker by **constraint** | A complete catalog of vendors |

## Automation (keeps the HTML honest)

Same fail-closed pattern as the Agentic AI Field Card:

| Piece | What it does |
|---|---|
| **Friday Cursor Automation (17:00 local)** | Discovers tools, edits the card when earned, leaves the PR open |
| **Friday review agent (18:00 local)** | The publish gate: publishes or keeps the previous card |
| **Slack #orbit** | Laconic FYI after review (Review / Considered / Changed / Online + Check card). Not the gate |
| **Mon watchdog** | If Friday review never applied, warn in #orbit to re-run the review agent |
| **Broken-link issue** | Opens a labeled issue when Use/tool URLs fail |

The Friday content agent runs `npm run discover`. `weekly-refresh.yml` is manual backup only (`workflow_dispatch`). The Friday 18:00 review agent is the publish gate (`Apply review`).

### Secrets (this repo)

Copy from Orbit / Vercel / the AI field-card repo:

| Secret | Purpose |
|---|---|
| `SLACK_ORBIT_WEBHOOK_URL` (or `SLACK_WEBHOOK_URL`) | Incoming webhook for #orbit |
| `WEEKLY_WRITE_SECRET` or `CRON_SECRET` or `FIELD_CARD_ACTION_SECRET` | HMAC for Apply review tokens (must match Orbit) |

### Secrets (Orbit / Vercel)

| Secret | Purpose |
|---|---|
| `GITHUB_TOKEN` or `FIELD_CARD_GITHUB_TOKEN` | Must be able to merge/close PRs on `AlexTouvras/data-analytics-field-card` |
| Same signing secret as above | Verify Apply review tokens |

## What stays vs what churns

| Stable (edit rarely) | Churn zone (weekly OK) |
|---|---|
| 4-layer stack (ASK / GRAIN / TRUTH / USE) | Tool picker rows |
| Problem â†’ use logic | Concrete product names in examples |
| Definition vs report | Version stamp + Changed line + doc URLs |
| Ladder, anti-patterns, kill switch | â€” |

New protocols earn a **new layer** only if they solve a new job (question / grain / truth / consume). A renamed BI feature is a picker-row swap, not a redesign.

## Tool picker guidance

| Constraint | Typical pick |
|---|---|
| Versioned transforms + tests | dbt |
| Local-to-cloud analytics SQL | DuckDB / MotherDuck |
| Volume / lakehouse | Databricks |
| Exploration / features | Python / Jupyter |
| Governed consume + scorecards | Power BI / Looker |
| Shared metrics across tools | Semantic layer |
| Provenance / reconcile | OpenLineage |

## Weekly refresh checklist (human)

1. If Friday review missed, re-run the 18:00 review agent or `Apply review` — do not Slack-Approve
2. Swap tool rows if the field moved
3. Refresh example nouns if needed; keep the problem column intact
4. Leave ladder and anti-patterns alone unless the pattern itself changed
5. Keep the card tool-agnostic at the stack level â€” vendors live in the picker and examples only
