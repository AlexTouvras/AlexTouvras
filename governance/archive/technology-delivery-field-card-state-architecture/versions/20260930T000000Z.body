# Architecture (working log)

> Tracked in git. Living decisions for this repo — not a substitute for `docs/`.

## Overview

Standalone Technology Delivery Field Card one-pager (`index.html`). Public artifact for browser, PDF print, LinkedIn, Slack. Weekly refresh via GitHub Actions discovery + Cursor Automation judgment (automation JSON lives here and in Orbit `website`).

## Data shapes

| Name | Shape / location | Notes |
|------|------------------|-------|
| Card HTML | `index.html` | INTENT → WINDOW → PROOF → CUTOVER stack |
| Discovery | `data/discovery-report.json` | CI + `npm run discover` |
| Watchlist | `data/watchlist.json` | `onCard` flags for ongoing tracking |
| Proposals | `data/proposed-updates.json` | Stub for Cursor Automation |
| Judgment | `data/judgment.md` | `## Summary` + `## Card preview` when the automation token cannot PATCH the PR body |

## Design patterns

- Decision stack, not a Scrum/SAFe/Azure brochure — tool picker ≤ 7 rows by **constraint**
- Verb line under H1 + Always-on foundation strip (not picker items)
- Fail-closed weekly refresh: PR `## Summary` or `data/judgment.md` required; Friday 18:00 review agent publishes
- Orbit sync: `public/delivery-field-card/index.html` via shared field-card registry

## Dependencies

| Dependency | Why introduced | Date |
|------------|----------------|------|
| Orbit field-card registry | Shared Apply review + preview | 2026-08-13 |
| GitHub Actions weekly-refresh.yml | Discovery without vendor LLM in CI | 2026-08-13 |
| Repo Actions workflow perms | `write` + allow GITHUB_TOKEN to create PRs (AI card already had this; default blocked W33) | 2026-08-14 |

## Canonical paths

| What | Path |
|------|------|
| Local workspace | `C:\Users\kater\.cursor\projects\technology-delivery-field-card` |
| Automation draft | `C:\Users\kater\.cursor\projects\website\.cursor\automations\delivery-field-card-weekly-content-pass.json` |
| Orbit static copy | `website/public/delivery-field-card/index.html` |

## Verify

```bash
npm run check:links
```
