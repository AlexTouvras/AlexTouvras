# Agentic AI Field Card

Standalone one-pager: [`index.html`](./index.html)

**Live:** after Pages is enabled → `https://alextouvras.github.io/agentic-ai-field-card/`

The storytelling robot sits on this page the same way it does on [alextouvras.com/stories/ai-card](https://alextouvras.com/stories/ai-card): bottom-right chrome, a tap tucks it into the corner. The module in `index.html` (kept in step with `robot.js`) loads `robot.riv`, its view-model contract, and the Rive runtime from the current `main` commit of `AlexTouvras/storytelling`, so a new robot there shows up here without copying the file. The homepage card is [alextouvras.com/field-card](https://alextouvras.com/field-card/), which Orbit fills from `index.html` alone, so the module is inline rather than a second file. Inside the story iframe the script stays quiet, because that page already draws the robot. Print / PDF leaves it off.

Public artifact only. Editor / maintenance notes live **here** and under `docs/`, not on the card.

## Use across channels

| Channel | How |
|---|---|
| **Browser / site** | GitHub Pages URL, or host `index.html` anywhere static |
| **PDF** | Open → Print / PDF (landscape A4) |
| **LinkedIn** | Share the Pages URL; caption can reuse the H1 + lede |
| **Email / Slack** | Attach PDF or paste link |

## Automation (keeps the HTML honest)

| Piece | What it does |
|---|---|
| **Friday Cursor Automation (17:00 local)** | Discovers tools, edits the card when earned, leaves the PR open |
| **Friday review agent (18:00 local)** | The publish gate: publishes or keeps the previous card |
| **Slack #orbit** | Laconic FYI after review (Review / Considered / Changed / Online + Check card). Not the gate |
| **Mon watchdog** | If Friday review never applied, warn in #orbit to re-run the review agent |
| **Broken-link issue** | Opens a labeled issue when Use/framework URLs fail |

The Friday content agent runs `npm run discover`. `weekly-refresh.yml` is manual backup only (`workflow_dispatch`). The Friday 18:00 review agent is the publish gate (`Apply review`).

The public footer is a monthly review (`Next: October 2026` on the card), not a weekly stamp. A Friday with nothing new leaves Reviewed and Next where they are.

### Secrets (field-card repo)

Copy from Orbit / Vercel as needed:

| Secret | Purpose |
|---|---|
| `SLACK_ORBIT_WEBHOOK_URL` (or `SLACK_WEBHOOK_URL`) | Incoming webhook for #orbit |
| `WEEKLY_WRITE_SECRET` or `CRON_SECRET` or `FIELD_CARD_ACTION_SECRET` | HMAC for Apply review tokens (must match Orbit) |

### Secrets (Orbit / Vercel)

| Secret | Purpose |
|---|---|
| `GITHUB_TOKEN` or `FIELD_CARD_GITHUB_TOKEN` | Must be able to merge/close PRs on `AlexTouvras/agentic-ai-field-card` |
| Same signing secret as above | Verify Apply review tokens |

## What stays vs what churns

| Stable (edit rarely) | Churn zone (weekly OK) |
|---|---|
| 4-layer stack | Framework picker rows |
| Problem → use logic | Concrete product names in examples |
| Rules vs skills | Version stamp + Changed line + doc URLs |
| Ladder, anti-patterns, kill switch | — |

New protocols earn a **new layer** only if they solve a new job (knowledge / control / tools / peers / behavior). A renamed framework is a picker-row swap, not a redesign.

## Framework picker guidance

| Constraint | Typical pick |
|---|---|
| Control / HITL / durable state | LangGraph |
| Speed to role-based demo | CrewAI |
| RAG / data-first | LlamaIndex |
| Azure / .NET | MS Agent Framework |
| Handoffs or Anthropic-native | OpenAI / Claude SDKs |
| Schema-first typed Python | Pydantic AI |

## Doc links (Use column + frameworks)

| Label | Destination |
|---|---|
| RAG | https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview |
| MCP | https://modelcontextprotocol.io/ |
| Direct tools | https://platform.openai.com/docs/guides/function-calling |
| Workflow / Agent | https://www.anthropic.com/engineering/building-effective-agents |
| Rules | https://cursor.com/docs/rules |
| Skill | https://cursor.com/docs/skills |
| Human gate | https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop |
| Fine-tune | https://platform.openai.com/docs/guides/fine-tuning |
| A2A | https://a2a-protocol.org/ |
| Evals | https://platform.openai.com/docs/guides/evals |
| Bayesian opt | https://alextouvras.com/bayes-field-card/ |
| LangGraph | https://langchain-ai.github.io/langgraph/ |
| CrewAI | https://docs.crewai.com/ |
| LlamaIndex | https://docs.llamaindex.ai/ |
| MS Agent Framework | https://learn.microsoft.com/en-us/agent-framework/overview/ |
| OpenAI Agents SDK | https://openai.github.io/openai-agents-python/ |
| Claude Agent SDK | https://code.claude.com/docs/en/agent-sdk/overview |
| Pydantic AI | https://ai.pydantic.dev/ |

## Weekly refresh checklist (human)

1. If Friday review missed, re-run the 18:00 review agent or `Apply review` — do not Slack-Approve
2. Swap framework rows if the field moved
3. Refresh example nouns if needed; keep the problem column intact
4. Leave ladder and anti-patterns alone unless the pattern itself changed
