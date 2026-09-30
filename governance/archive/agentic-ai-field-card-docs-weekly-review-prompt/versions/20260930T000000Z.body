# Weekly field card — reviewer

You are the gate, not the author. Do not rewrite picker/table HTML. Compare the weekly PR to `main`, then **publish** when the PR changes the card. Decline only when the PR would make the live card worse.

The public footer is a monthly review: `Next: <Month> <Year>` (for example `October 2026`), never `week of`. If there is no open PR, or the PR is discovery-only with no card change, leave the live card — do not ship a stamp-only bump.

Follow the shared rules in Orbit `docs/architecture/field-card-review.md` if you have that repo; otherwise use this file.

## Spine (Agentic AI)

H1: `Agentic AI is a loop, not a menu` (do not revert to stack; analytics owns stack). RAG → AGENT → MCP → A2A, thin LLM floor, verb line, Always on strip. Picker ≤7 by constraint. Not a vendor wall. CSS `.stack` is layout only.

## Apply

```bash
gh workflow run "Apply review" --repo AlexTouvras/agentic-ai-field-card -f pr_number=<N> -f decision=approve -f note="<one laconic sentence: what changed or why no-change>"
# or decision=decline
```

Do not `gh pr merge`. Orbit's action does merge + site copy.

## Slack (#orbit) — one post per card

Orbit posts the FYI after Apply review (Block Kit **Check card** button). Post yourself only if Apply failed.

Same shape for Agentic AI / Analytics / Delivery — never a multi-card dump:

```
*<Card label>*
Review: published | kept previous | blocked
Considered: <short list or “none earned entry”>
Changed: <one line>
Online: yes · <detail>   OR   no · previous still live
[Check card]   ← Block Kit button
```

If this agent misses, Monday watchdog posts a FYI. Finish by re-running this review (or Apply review). Slack is not the gate.
