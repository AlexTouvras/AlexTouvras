# Weekly field card — Cursor Automation

Each Friday the automation **judges whether the public card should change**, applies updates when earned, and leaves the weekly PR open. A separate **review** agent publishes or keeps the previous card. Do not assume CI left ready-to-merge HTML on main.

Discovery alone is not enough. Every run must end with an explicit **update** or **no HTML change** decision.

## Slack

Do **not** post Approve links from this run. The review agent is the gate. If that agent misses, Monday watchdog posts a FYI in #orbit — finish by re-running the 18:00 review (or `Apply review`), not Slack Approve.

## Scope (keep this card honest)

This is a decision sequence, not a capability glossary. Public H1 is loop/not a menu — analytics owns “stack”. The stable spine is:

- H1: `Agentic AI is a loop, not a menu` (do not revert this to stack; analytics owns that word)
- **RAG → AGENT → MCP → A2A** hero codes (do not merge MCP into A2A / “Agentic AI”)
- Thin **LLM** floor band above RAG (`Language — prompted chat`); ladder step 1 stays `LLM / prompted chat`
- Verb line under the H1 (`Understand → find → act → orchestrate`) — do not drop
- **Always on** foundation strip (Security, Governance, Observability, Evals, Human Approve) — not picker items
- Problem → use → example table, Rules vs skills, ladder + kill switch, anti-patterns
- Framework picker by **constraint**
- The storytelling robot module inlined at the bottom of `index.html` (same source as `robot.js`). Orbit publishes only `index.html` to `/field-card/`, so the module has to live in that file. It is chrome, loaded live from `AlexTouvras/storytelling`. Do not remove it, do not vendor `robot.riv`, and do not treat it as a card-content change.

Do not add capability icon walls, ACP as a hero protocol, or an evolution-as-progress timeline.

## Steps

1. Check out `AlexTouvras/agentic-ai-field-card`. Prefer open branch `chore/weekly-refresh-YYYY-Www` for this ISO week; otherwise create/update it from `main`.
2. Run `npm run discover` (GitHub access via `gh` in the Cloud Agent). Read `data/discovery-report.md` and the current `index.html`.
3. **Decide (required):**
   - **Update card** if a picker swap, docs URL fix, or new *job* in the decision table is earned.
   - **No HTML change** if candidates are noise, picker is full with better incumbents, or nothing new belongs on a one-pager.
   - Write the decision in the PR `## Summary` either way. Never skip this step.
4. If updating `index.html`:
   - Framework picker ≤ 7 rows; swap by constraint (control, speed, data, enterprise, handoffs, typed, google, …) — not hype or star count alone.
   - Do not invent docs URLs; use discovery report, watchlist, or existing card links.
   - Decision table: only if a new *job* appeared (new brand ≠ new layer).
   - Keep Use labels short and linked; nuance in Example.
   - Do not change the public H1.
   - No editor notes on the public HTML.
   - Update the footer **Changed** line; bump version with `npm run bump:version` when the card content changed.
   - Footer **Next** is the following calendar month (`October 2026`), never `week of`. `bump:version` writes that shape.
5. If **no HTML change**: leave picker, table, Reviewed, and Next alone. Do not open a stamp-only bump. A no-change week does not move the monthly footer. Still commit discovery artifacts if you re-ran discover on this branch.
6. Run `node scripts/check-links.mjs` and fix failures on any URLs you touched.
7. Update `data/watchlist.json` for tools you confirm for ongoing tracking (`onCard` true/false).
8. Commit and push to the weekly PR. Do not merge. Do not force-push `main`.
9. Rewrite the PR body to include at least:
   - `## Summary` — 3–6 bullets: what changed on the card **or** why nothing changed; what was deferred.
   - `## Card preview` — one line: the review agent will compare this HTML to live.
10. Stop. Do not notify Slack. Do not merge. The Friday 18:00 review agent publishes a card change, or leaves the previous card when nothing changed. It declines only when the PR would make the live card worse.

## Done when

- Discovery ran this session
- Explicit update **or** no-change decision is in `## Summary`
- Link check exits 0 (if HTML or links changed)
- PR left open for the review agent
