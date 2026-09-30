# Contract: inbox day file

**Path:** `inbox/YYYY-MM-DD.md`  
**Producer:** Huginn  
**Consumers:** Muninn (primary), humans (review)

## Rules

1. One file per calendar day (local Finland time, Europe/Helsinki).
2. Filename is the scan date, not the publish date of sources.
3. If a prior file exists for today, **append** a new run section — do not overwrite earlier findings.
4. Every finding needs a stable `id`, domain, source URL, and claim that can be checked. `source_url` is the publisher, not an aggregator.

## Template

```markdown
---
schema: ravens.inbox/v1
date: YYYY-MM-DD
raven: huginn
run_id: YYYY-MM-DD-HHMM
timezone: Europe/Helsinki
watchlist_hash: <short hash or "unhashed">
status: complete | partial | failed
summary: "One sentence: what mattered today."
---

# Inbox YYYY-MM-DD

## Run YYYY-MM-DD HH:MM (Europe/Helsinki)

### ai-agents

#### FIND-YYYYMMDD-001

- **title:** Short factual title
- **claim:** One sentence of what changed or was learned
- **why_it_matters:** Who/what in the portfolio cares (field-card, mealplan, …)
- **domain:** ai-agents
- **topics:** [mcp, cursor-skills]
- **source_url:** https://…
- **source_title:** Publisher or page title
- **published:** YYYY-MM-DD or unknown
- **corroboration_url:** (optional; required before Muninn promotes finance opportunity/macro items)
- **found_at:** YYYY-MM-DDTHH:MM:SS+03:00
- **confidence:** high | medium | low
- **novelty:** new | update | rumor
- **action_hint:** none | monitor | promote-candidate
- **quotes:** (optional, ≤2 short quotes)

### data-bi
…

## Empty domains

List domains scanned with zero hits:

- finance: no high-signal items

## Scan gaps

Preferred-source families that failed, timed out, or were paywalled. `none` if the scan completed. Empty domains are not gaps.

- none
```

## ID scheme

`FIND-YYYYMMDD-NNN` — zero-padded sequence per day across all domains (001, 002, …).

## Minimum bar

Huginn may leave a domain empty. It must **not** invent sources. Prefer fewer high-signal findings over a long digest. List **Scan gaps** when a preferred source family was blocked; do not omit the heading.

Journalism items need a parseable `published` date inside Gate 0. Living official docs may use `published: unknown` (see `docs/quality.md`).

Parenting findings should include exactly one age-bucket tag (`late-pregnancy`, `labor`, `age-0-72h`, `age-3-14d`, `age-2-8w`, or `age-2-6m`) from the **source’s** age range, and `why_it_matters` must name **household**. Do not require `week-N` or a **Parenting week** block (week-of-life planning is out of ravens’ scope). Existing inbox files that still have that block remain valid.
