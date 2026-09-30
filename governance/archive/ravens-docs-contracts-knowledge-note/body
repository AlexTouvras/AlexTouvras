# Contract: knowledge note

**Path:** `knowledge/<domain>/<slug>.md` (plus domain `README.md` as hub)  
**Producer:** Muninn  
**Consumers:** Humans, future Orbit/mealplan/field-card readers, ProjectBrain (later)

## Domain hubs

Each domain has `knowledge/<domain>/README.md`:

```markdown
---
schema: ravens.domain-hub/v1
domain: fitness
updated: YYYY-MM-DD
status: active
---

# Fitness

One paragraph: what this domain is for.

## Current guidance

Bullet list of durable rules currently in force (link to note slugs).

## Active signals

- [SIG-…](../../signals/SIG-….md) — one-line status

## Note index

| Slug | Title | Updated | Status |
|------|-------|---------|--------|
| lean-deload | Deload during lean cuts | YYYY-MM-DD | active |

## Changelog

| Date | Change |
|------|--------|
| YYYY-MM-DD | … |
```

## Knowledge notes

**Path:** `knowledge/<domain>/<slug>.md`  
Slug: lowercase kebab-case, stable once published.

```markdown
---
schema: ravens.knowledge/v1
id: KNOW-<domain>-<slug>
domain: fitness
title: Deload during lean cuts
status: active | superseded | disputed
updated: YYYY-MM-DD
created: YYYY-MM-DD
confidence: high | medium | low
tags: [lean, recovery, programming]
supersedes: []          # KNOW-… ids
superseded_by: null     # KNOW-… id when retired
source_findings:        # FIND-… ids from inbox
  - FIND-20260811-001
canonical_sources:
  - url: https://…
    title: …
    accessed: YYYY-MM-DD
---

# Deload during lean cuts

## Guidance

Normative bullets an agent or human can apply.

## Rationale

Why this is durable (not just news).

## Limits / do not apply when

Edge cases and exclusions.

## Related

- Domain hub, sibling notes, signals
```

## Rules

1. Promote only findings that pass [quality.md](../quality.md).
2. Prefer updating an existing note over creating near-duplicates.
3. When guidance changes, mark the old note `superseded` and set `superseded_by`.
4. Never delete history without leaving a supersession trail.
