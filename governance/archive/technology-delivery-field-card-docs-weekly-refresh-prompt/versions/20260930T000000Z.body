# Weekly Technology Delivery field card — Cursor Automation

Each Friday the automation **judges whether the public card should change**, applies updates when earned, and leaves the weekly PR open. A separate **review** agent publishes or keeps the previous card. Do not assume CI left ready-to-merge HTML on main.

Discovery alone is not enough. Every run must end with an explicit **update** or **no HTML change** decision.

## Slack

Do **not** post Approve links from this run. The review agent is the gate. If that agent misses, Monday watchdog posts a FYI in #orbit — finish by re-running the 18:00 review (or `Apply review`), not Slack Approve.

## Scope (keep this card honest)

This is **not** a Scrum / SAFe / Azure DevOps product card. The stable spine is:

- **INTENT → WINDOW → PROOF → CUTOVER** stack
- Verb line under the H1 (`Name → calendar → prove → cut over`) — do not drop
- **Always on** foundation strip (Security, Governance, Observability, Evals, Human Approve) — not picker items
- Problem → use → example jobs (calendars, dependencies, flags, rollback, priority, observability…)
- Tool picker by **constraint** (batch size, CI, reversible cutover, IaC, watch, visibility, human gate)
- Ladder + anti-patterns + kill switch

Churn zone: tool picker rows, concrete product nouns in examples, doc URLs, version stamp. Do **not** redesign the stack for a renamed vendor feature.

## Steps

1. Check out `AlexTouvras/technology-delivery-field-card`. Prefer open branch `chore/weekly-refresh-YYYY-Www` for this ISO week; otherwise create/update it from `main`.
2. Run `npm run discover` (GitHub access via `gh` in the Cloud Agent). Read `data/discovery-report.md` and the current `index.html`.
3. **Decide (required):**
   - **Update card** if a picker swap, docs URL fix, or new *job* in the decision table is earned.
   - **No HTML change** if candidates are noise, picker is full with better incumbents, or nothing new belongs on a one-pager.
   - Write the decision in the PR `## Summary` either way. Never skip this step.
4. If updating `index.html`:
   - Tool picker ≤ 7 rows; swap by constraint (batch-size, ci, reversible-cutover, iac, observability, visibility, human-gate…) — not hype or star count alone.
   - Do not invent docs URLs; use discovery report, watchlist, or existing card links.
   - Decision table: only if a new *job* appeared (new brand ≠ new layer).
   - Keep Use labels short and linked; nuance in Example.
   - No editor notes on the public HTML.
   - Prefer delivery language (sequence, owner, window, rollback, held). Avoid making Scrum, SAFe, or Azure DevOps the whole card.
   - Update the footer **Changed** line; bump version with `npm run bump:version` when the card content changed.
5. If **no HTML change**: leave picker/table alone. Keep the weekly stamp CI (or you) already bumped. Stamp-only still ships — the review agent **approves** it. Still commit discovery artifacts if you re-ran discover on this branch.
6. Run `node scripts/check-links.mjs` and fix failures on any URLs you touched.
7. Update `data/watchlist.json` for tools you confirm for ongoing tracking (`onCard` true/false).
8. Commit and push to the weekly PR. Do not merge. Do not force-push `main`.
9. Rewrite the PR body to include at least:
   - `## Summary` — 3–6 bullets: what changed on the card **or** why nothing changed; what was deferred.
   - `## Card preview` — one line: the review agent will compare this HTML to live.
10. Stop. Do not notify Slack. Do not merge. The Friday 18:00 review agent publishes (including stamp-only). It declines only when the PR would make the live card worse.

## Done when

- Discovery ran this session
- Explicit update **or** no-change decision is in `## Summary`
- Link check exits 0 (if HTML or links changed)
- PR left open for the review agent
