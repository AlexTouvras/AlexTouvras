# Contract: watch note

**Path:** `watch/<domain>/<slug>.md` (plus `watch/README.md` as catalog index)  
**Producer:** Heimdall  
**Consumers:** Humans, fitness coach (read-only), household. Muninn does not distill these. Heimdall does **not** Slack — consumers match from `watch/` on `main` (see `docs/consumers.md`).

One note per topic (a lift, a parenting how-to). This is a catalog, not a daily inbox. Prefer updating the existing slug over adding a second clip for the same movement.

## Consumer hooks (required for matching)

| Consumer | Required in note |
|----------|------------------|
| `fitness` form-check | Frontmatter `consumer: fitness`; body line `Coach library: <exact lift name>` under **Related** (must match fitness coach library JSON names). |
| `fitness` motivate | Frontmatter `intent: motivate`; join by slug (`gym-anime`, `lift-motivation`). No `Coach library` line. |
| `household` parenting | Frontmatter `consumer: household`; `stage` matches `knowledge/parenting/README.md` Current stage window. |

## Rules

1. Filename slug is lowercase kebab-case and stable once published.
2. `primary_url` must be a real YouTube watch URL that oEmbed (or an equivalent check) can resolve. Do not invent video ids.
3. Instagram / TikTok / Reels are **paste-only**: catalog a URL the human supplied. Do not search or scrape those platforms.
4. v1 domains are `fitness` and `parenting` only.
5. Parenting notes must include exactly one age/stage tag matching `knowledge/parenting/README.md` Current stage week-of-life bucket (or one adjacent window).
6. Fixture ids `WATCH-20990101-*` live only under `examples/`.

## Template

```markdown
---
schema: ravens.watch/v1
id: WATCH-fitness-back-squat
domain: fitness
slug: back-squat
title: Back squat — form check
status: active
intent: form-check
consumer: fitness
stage: none
primary_url: https://www.youtube.com/watch?v=…
primary_title: How To Squat Correctly
channel: Squat University
duration: 7:38
accessed: YYYY-MM-DD
confidence: high
---

# Back squat — form check

## Why this clip

One paragraph: credentials, camera angle, match to our programming.

## Cues to steal

- Short bullets you can use on the platform.

## Limits / do not apply when

- Not a substitute for pain that needs a clinician.
- Pregnancy: use ACOG notes under `knowledge/fitness/`; this is a general barbell pattern.

## Related

- Coach library movement name
- Sibling watch notes
```

## Frontmatter

| Field | Values |
|-------|--------|
| `status` | `active` \| `stale` \| `superseded` |
| `intent` | `form-check` \| `how-to` \| `idea` \| `motivate` |
| `consumer` | `fitness` \| `household` |
| `stage` | `none` for fitness; parenting uses age-bucket tags (`age-2-8w`, …) so household can match |
| `confidence` | `high` \| `medium` \| `low` |

## ID scheme

`WATCH-<domain>-<slug>` — one live id per topic. When a better clip replaces the URL, keep the id and bump `accessed`.
