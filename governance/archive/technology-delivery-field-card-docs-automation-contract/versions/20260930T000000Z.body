# Automation contract — Technology Delivery Field Card

## Repository

| Field | Value |
|-------|-------|
| GitHub | `AlexTouvras/technology-delivery-field-card` |
| Orbit sync path | `public/delivery-field-card/index.html` |
| Default branch | `main` |

## Automations

| Name | Trigger | Output | Human gate |
|------|---------|--------|------------|
| Weekly discovery | GHA `weekly-refresh.yml` (manual) | opens PR | none |
| Weekly judgment | Cursor Fri 17:00 | PR `## Summary` | none — stop for review |
| Weekly review | Orbit Cursor Fri 18:00 | Apply review + #orbit FYI | review agent is the gate |
| Judgment watchdog | GHA `judgment-watchdog.yml` Mon | #orbit FYI if PR still open | re-run review agent |

## Required secrets

| Secret | Notes |
|--------|-------|
| `WEEKLY_WRITE_SECRET` | Must match Orbit/Vercel |
| `SLACK_ORBIT_WEBHOOK_URL` | `#orbit` notifications |

## Ship checklist

```bash
npm run ship:check
```

## Definition of done

- [ ] `npm run check:links` passes
- [ ] PR has `## Summary` with `Decision: update|no-change`
- [ ] Orbit static copy synced after Apply review
