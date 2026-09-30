# Contract: signal card

**Path:** `signals/SIG-YYYYMMDD-NNN.md`  
**Producer:** Muninn  
**Purpose:** Short-lived, actionable “watch this” items that are not yet (or not only) durable knowledge.

Signals expire. Knowledge persists.

## Template

```markdown
---
schema: ravens.signal/v1
id: SIG-20260811-001
domain: ai-agents
title: MCP spec revision worth monitoring
status: watching | acted | expired | dropped
priority: p1 | p2 | p3
opened: YYYY-MM-DD
expires: YYYY-MM-DD
source_findings:
  - FIND-20260811-003
related_knowledge: []   # KNOW-… when promoted
consumers:              # optional hints — no auto-writes in v1
  - agentic-ai-field-card
---

# MCP spec revision worth monitoring

## Why open

One paragraph.

## Watch for

Concrete triggers that would promote, act, or expire this signal.

## Resolution log

| Date | Note |
|------|------|
| YYYY-MM-DD | Opened from inbox |
```

## Lifecycle

| Status | Meaning |
|--------|---------|
| `watching` | Active; Muninn re-checks on later runs |
| `acted` | Human or downstream project used it; keep for audit |
| `expired` | Past `expires` with no promotion |
| `dropped` | Failed quality / duplicate / noise |

Default expiry: **14 days** from `opened`, unless the finding is time-bound (then use that date).
