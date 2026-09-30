# Agent Rules

## Hard non-goals (read first)

Agents often treat “next level” as “add things.” Foundation is **coherence**, not feature expansion.

**Forbidden unless the owner explicitly asks:**

- New repo / fork of the site
- Hub or live-desk visual-storytelling redesign
- Decision Intelligence Lab / new live desk
- Restyling Studio or `/card` as cinematic chapters
- JARVIS / ProjectHelm / cockpit revival
- Employer-confidential detail in git or public pages
- Newsletter audience go-live
- New career evidence / achievement projects as part of Foundation
- Turning HUd into a progress dashboard
- Silent “while I was here” extras (nav polish, new Hub viz, drive-by refactors)

## Product hierarchy

When deciding:

1. Existing working functionality
2. Product vision (`PRODUCT.md` + `docs/product/*`)
3. Explicit feature specification / owner gate
4. Current milestone
5. Agent implementation preference

Do not change product direction because an implementation seems easier or cooler.

## Product vs implementation

| Product decision (docs / owner) | Implementation decision (agent) |
|---------------------------------|----------------------------------|
| HUd is a 15–30s identity card | Reuse card components; STATEMENT only on `/card` |
| Hub answers WHAT / HOW HE THINKS | Copy alignment only; keep chapter grammar |
| Studio tracks trajectory | Smallest persistence compatible with existing Studio |

Agents may choose the second only inside the first.

## Mandatory Scope check

**Before implementing anything:**

1. What product requirement does this satisfy?
2. Which `PRODUCT.md` / `docs/product/*` document authorizes it?
3. Which existing functionality does it modify?
4. What is explicitly out of scope?
5. Does this introduce a new concept, route, visual language, or architecture?
6. If yes → **STOP and ask the owner.**

## Preserve before replacing

1. Inspect the current implementation
2. Identify what already works
3. Identify the intended user experience
4. Make the smallest change that moves toward the spec

Do not rebuild from scratch unless explicitly requested.

## HUd rule

`/card` is an existing product. Iterative improvement only. STATEMENT on the card; `focusNow` stays in Studio.

## Studio rule

Private-by-convention. Do not expose Studio content publicly unless the owner explicitly marks it for a public surface.

## Design rule

Prefer clarity, hierarchy, progressive disclosure, strong typography, restrained motion, coherent systems.

Avoid decorative animation, generic dashboards, feature creep, fashionable “AI” chrome.

## Engineering rule

Before a new component: search the codebase, reuse, check design system and data contracts, avoid duplicate representations.

For Studio data: use existing `persistDataJson` / profile-store patterns. Do not invent a second persistence architecture.

## Objective

**Clear identity + credible evidence + coherent professional trajectory.**

More features ≠ progress.
