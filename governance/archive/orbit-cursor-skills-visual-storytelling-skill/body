---
name: visual-storytelling
description: >-
  Restyle Orbit public pages and live desks as chaptered visual stories
  (not card grids). Use when changing Hub, About, Portfolio heroes, live
  dashboards, or when the user asks for visual storytelling, cinematic
  scroll, or dashboard narrative.
---

# Visual storytelling (Orbit)

Turn a page into a **scroll story**: numbered chapters, oversized type, one idea per beat. Keep the cyber/space brand. Do not rebuild a Webflow theatre.

## When this applies

- Hub, About, Portfolio, live desks (`/portfolio/live/*`)
- User asks for visual storytelling, cinematic layout, or narrative dashboards
- Adding a new public section that would otherwise become a 3-up `GlassCard` grid

Interior tools stay tools: Studio, week log, `/card`, `/qr-code`.

## Named verify

Primary: Hub `/` renders chapter ids `story-open`, `story-gravity`, `story-craft`, `selected-work`, `story-live`, `story-signals`, `story-close`; `npm run build` exits 0.

Then a browser walk (desktop + a ~390px viewport):

1. Scroll Hub end to end; the top line fills; Gravity rings turn; craft rows spotlight. There is no fixed chapter bar.
2. Competency rows are plain `<a href>` to field cards (not `next/link`)
3. Proof reel: scrolling down advances the cards to the right; Case study and architecture still work. Reduced motion: swipe the rail.
4. Live peek reel: sneak-peek image + `desk.question` as the headline; scrolling down advances cards; the card opens `/portfolio/live/{slug}`. Reduced motion: swipe the rail.
5. About experience reads as a timeline, not stacked glass cards
6. `/portfolio` is the shared headline, then flagship teaser (`FlagshipTeaser` → `/stories`) → workshop reel → live peek reel → Power BI reel → GitHub list. No copied Home close. `/portfolio/live` uses the same reel. Home uses the same `max-w-5xl` column as Blog.
7. `prefers-reduced-motion`: story still readable; no required animation

## Minimum evidence (open before editing)

1. This skill + `reference.md`
2. Brand tokens in `src/app/globals.css` (`.orbit-accent`, `.text-story`, reduced-motion block)
3. Existing copy in `src/content/profile.ts` / `src/content/live-desks.ts` — re-hierarchy, do not invent slogan copy
4. `docs/essay-voice.md` stranger test for any new sentence a visitor will read

## Scene grammar

A page is a sequence of **chapters**, not a stack of sections.

| Beat | Job | Orbit example |
|------|-----|----------------|
| Open | One thesis in huge type; identity is supporting; live product-as-atmosphere under the thesis | Hub: “Prove what works.” + name as kicker + `LiveProofStream` |
| Metaphor | Make the brand visible | Gravity field: center + satellites |
| Craft | Numbered process (how the work actually happens) | Delivery → Data → AI with `hudVerbs` |
| Proof | Horizontal reel of evidence | Showcase writes |
| Live | Peek reel of questions | sneak peek + `desk.question` → `/portfolio/live/{slug}` |
| Signals | Horizontal reel of essays | Category · title · date |
| Close | Landing, not another grid | About + contact |

Rules:

- **One idea per chapter.** If you need a card grid to “fit three things,” you do not have a scene yet.
- **Type is the primary image.** Photography/video is optional; Orbit’s image is Syne at `.text-story` / `.text-display` plus the orbit ring.
- **Numbers are characters.** Cadence, zone count, €/m² — `StoryStat` / `.orbit-accent` display figures, not a muted mono row.
- **No scroll-jacking.** Do not hijack vertical scroll (no `preventDefault` on wheel, no vertical snap, no pin-jack libraries). Scroll-linked motion is allowed: progress line, ring rotate, in-view spotlight, count-up, `StoryReveal`, and sticky **reels** (`ScrollRail`) whose `translateX` is driven by native vertical scroll. The track moves on the first scroll once the reel reaches the top of the viewport. Every reel uses `ScrollRailCard` with no viewport-width override. Craft, GitHub, and the About timeline stay vertical. Signals is a reel. No fixed chapter bar. Copy must remain readable without the motion.
- **Reduced motion always works.** `motion-safe:` only. Reels fall back to a swipe rail. Copy must not depend on animation.
- **Field cards** live as static HTML in `public/`. Home competency links stay plain `<a>`.

## Component map

| Primitive | Path | Use |
|-----------|------|-----|
| `LiveProofStream` | `src/components/hub/LiveProofStream.tsx` | Hub Open atmosphere: desk questions + system pulse (Pinloop cue) |
| `StoryScene` | `src/components/story/StoryScene.tsx` | Chapter inside the shared `max-w-5xl` column |
| `ChapterMark` | `src/components/story/ChapterMark.tsx` | `01 / Craft` + title + lede |
| `StoryHeadline` | `src/components/story/StoryHeadline.tsx` | Shared two-line title on public pages |
| `GravityField` | `src/components/story/GravityField.tsx` | Brand diagram |
| `StoryStat` | `src/components/story/StoryStat.tsx` | Oversized KPI |
| `DeskStoryHeader` | `src/components/story/DeskStoryHeader.tsx` | Live desk opening: cadence → question |
| `DeskCast` | `src/components/story/DeskCast.tsx` | 3–5 `StoryStat` figures before the map |
| `DeskPicture` | `src/components/story/DeskPicture.tsx` | Primary visual (map / tape / mix / board) |
| `DeskClose` | `src/components/story/DeskClose.tsx` | Source, lag, what this is not |
| `DeskMissing` | `src/components/story/DeskMissing.tsx` | Snapshot missing; `question` as `h1` |
| `ScrollLine` | `src/components/story/ScrollLine.tsx` | Top read bar; Hub / Portfolio / About / live (via AppChrome) |
| `ScrollSpot` | `src/components/story/ScrollSpot.tsx` | Brightens the row in the viewport midline |
| `StoryReveal` | `src/components/story/StoryReveal.tsx` | Scale/rise when a beat enters view |
| `ScrollRail` | `src/components/story/ScrollRail.tsx` | Reels (Hub Proof, live, Signals, Portfolio workshop, Power BI): vertical scroll moves cards immediately; swipe if reduced motion |
| `LiveDeskReel` | `src/components/live/LiveDeskReel.tsx` | Hub / Portfolio / live index: peek + question on a `ScrollRail` |
| `LiveDeskTile` | `src/components/live/LiveDeskTile.tsx` | One desk card: sneak peek + `desk.question` as headline |

AppChrome: public pages share `max-w-5xl`. A single live desk (`/portfolio/live/[slug]`) may use `max-w-6xl` for the picture. Do not full-bleed Home. Do not silently widen Studio.

## Live dashboards (next applications)

A desk is already a story if it keeps **one question**. Visual storytelling means the **reading order**, not a new chart library.

1. **Open** — `DeskStoryHeader` (cadence kicker + question as `h1`). Never title the desk with the dataset name first.
2. **Cast** — 3–5 `StoryStat` figures that answer the question before interaction (latest €/m², FI price, HICP). Do not bury them under the map.
3. **Picture** — the map, tape, or mix is the scene. Full width of the live column. Do not wrap the primary visual in `GlassCard` unless it is a peek/tile.
4. **Move** — hover/press changes the same scene (zone desk, spotlight country). Do not open a second page for the default drill.
5. **Close** — source, lag, and what this is not (“delayed quotes; not a trading terminal”). Missing snapshots use `DeskMissing` with the desk `question`, not the dataset name.

When adding a new desk:

- Put `question` on `LiveDesk` in `src/content/live-desks.ts` first
- Surface it on Hub / Portfolio / `/portfolio/live` via `LiveQuestions` / `LiveDeskReel` (sneak peek + question as the card headline)
- Build the desk as Open → Cast → Picture → Move → Close
- Verify the live reel still shows the peek and the question

Do not: iframe a Power BI report as the story; duplicate Hub glass cards onto the desk; add a marketing hero above the question.

## Quality gates (reject / rewrite if any fail)

| Gate | Fail if |
|------|---------|
| Card relapse | New Hub/About block is a 3-up `GlassCard` grid with eyebrow + title + description |
| Scroll theatre | Vertical scroll-snap, pin-jacking, parallax that hides copy, or motion required to read |
| Slogan drift | New headlines that a stranger cannot map to `profile.ts` / desk `question` |
| SEO identity | Hub `h1` omits the person’s name (name may be the kicker inside `h1`, thesis the display span) |
| Field-card SPA | Competency uses `next/link` to `/field-card/` (soft-nav 404) |
| Orbit paint | Animated OKLCH channels or `color: var(--orbit-accent)` for text (see ARCHITECTURE brand notes) |
| Interior leak | Studio / week log / card HUD restyled as cinematic chapters |
| Desk rename | Live desk `h1` is the dataset name instead of the question |

## Out of scope

- Replacing tsParticles with video
- Webflow-style page transitions
- Rewriting essay MDX into scrollytelling. Owner 2026-09-22: the cast, the picture, and a comparison the reader can move stay on live desks. Weekly Writes stay prose.
- Garmin / hobby embeds
