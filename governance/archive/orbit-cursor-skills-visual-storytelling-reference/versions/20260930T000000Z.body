# Visual storytelling — reference

Distilled from a visual review of the inspiration set plus Orbit’s current Hub. Use with `SKILL.md`; do not copy these sites’ tone.

## What each reference actually does

### [AI Takes Over](https://aitakesover.co/)

Scroll **chapters** as jokes → definitions → timeline → stats → myths → close. Viewport scenes, conversational narrator, stats as punchlines (70%, 85 million). Motion is the medium. Visual: PAST → PRESENT → FUTURE sticky chapter labels, pixel/8-bit display type as a graphic object, toast overlays for asides, letter morphs.

**Steal:** chaptered scroll, stats as beats, a close that lands a decision, a chapter index that tracks position.  
**Leave:** viewport-locked scroll-jacking, robot-dance theatre, joke-bot voice, 8-bit glitch as identity. Orbit is a hiring-manager HQ.

### [Light Factory](https://light-factory-ca-2022.webflow.io/)

Work as a **reel**. Services as **01–05 process** (Understand → Design → Capture → Craft → Distribute), not a card grid. Visual: asymmetric split (type left, oversized still/video right), keyword color (magenta / lime), scroll-reveal scale rather than snap-lock.

**Steal:** numbered craft sequence; horizontal proof; process verbs as the story; keyword color already maps to cyan / blue / violet on Hub craft rows.  
**Leave:** video-production chrome, manifesto proclamations, hand-drawn doodles.

### [Amanda Lee Peers](https://www.amandaleepeers.com/)

Biography as **eras** (Beginning → Success → Reality TV → Sinner → Tour). Time is the chapter mark. Visual: one hero word over a full-bleed image; catalog as framed cards; dark, photographic, little body copy above the fold.

**Steal:** About as timeline/eras, not stacked CV cards; a single thesis word at display scale.  
**Leave:** graffiti overlays, tour-poster density; Orbit’s record is employers and theses.

### [OSOS](https://osos.webflow.io/)

Typography as identity. Visual: outline type that fills, side labels, iridescent ambient objects on deep black, extreme negative space, particle field as a close.

**Steal:** type at display scale as the “image”; one-word chapters; ambient motion behind copy (Orbit already has particles + `GravityField`).  
**Leave:** illegible overlap, soap-bubble decoration, empty-hero density that hides a decision rule.

### [Haus of Words](https://www.hausofwords.com/)

Personality-first. Big numbers (6.3 million impressions). FAQ as voice. Close is a conversation. Visual: geometric pattern as a full section, snap color blocks, almost no photography.

**Steal:** oversized stats; close as a landing; questions as headlines; a geometric brand mark as a scene (Orbit: orbital rings, not a maze).  
**Leave:** pastel Bauhaus blocks, punchy agency humour that would fail `docs/essay-voice.md`.

### [Pinloop](https://pinloop.ai/)

Agent-first product page. Hero is **the product running**: a live job-feed ticker under one brutal thesis (“Humans should not scroll job boards”), then one claim per section (hourly from ATS; judged overnight). Motion *is* the proof — the stream updates; there is no stock hero photo.

**Steal:** live data stream as hero atmosphere (system visibly working); one unmissable thesis with brand secondary but present; section = one claim + one demonstration; mechanism over vanity metrics.  
**Leave:** job-board ticker content, SaaS pricing blocks, feature grids, Pinloop voice/palette, floating badges or promo chips on the hero.

## Orbit translation (already on Hub)

| Inspiration | Orbit chapter |
|-------------|----------------|
| Full-viewport open | `story-open` — “Prove what works.” |
| Live product-as-atmosphere | `story-open` — `LiveProofStream` (desk questions / system pulse under the thesis) |
| Brand made visible | `story-gravity` — `GravityField` |
| 01–05 process | `story-craft` — Delivery / Data / AI + `hudVerbs` |
| Work reel | `selected-work` — `ProofReel` |
| Questions as headlines | `story-live` — live peek reel (`LiveDeskReel`) |
| Editorial index | `story-signals` — writes as a list |
| Conversational close | `story-close` — About + contact |
| Era timeline | About `ExperienceTimeline` |
| Question-led desk | `DeskStoryHeader` on live desks |

## Tokens

- Display: Syne (`font-display`), body: IBM Plex Sans, index/kicker: JetBrains Mono
- `.text-story` — Hub thesis only (viewport open)
- `.text-display` — desk questions, interior heroes
- `.story-index` — ghost `01` behind a row
- `.story-rail` — horizontal snap; hide scrollbar
- Accents: unlayered `.orbit-accent` hex animation; never OKLCH channel `@property`
- `neon-cyan` is static; body links (Case study, Read) stay static cyan

## AppChrome

```text
/                  full-bleed story (no max-w)
/portfolio/live*   max-w-6xl
everything else    max-w-5xl
/card /qr-code     bare (no header/particles)
```

New story pages need an explicit `story` path in `AppChrome` — do not assume every route is full-bleed.

## Dashboard recipe (checklist)

When restyling or adding a live desk:

- [ ] `question` is the `h1` via `DeskStoryHeader`
- [ ] Cadence/source is the kicker, not a Badge soup
- [ ] 3–5 `StoryStat` figures answer the question before any click (`DeskCast`)
- [ ] Primary visual is full-column (`DeskPicture`), not a 16:10 card
- [ ] Interaction changes the same scene
- [ ] Close names lag, license, and what it is not (`DeskClose`)
- [ ] Missing snapshot uses the desk `question` (`DeskMissing`)
- [ ] Hub `LiveQuestions` is a peek reel (`LiveDeskReel`); question is the card headline
- [ ] Reduced-motion: map/tape still readable

## Anti-patterns seen on the old Hub

- `space-y-24` + `SectionHeading` + `Stagger` of `GlassCard`
- Competencies as three equal tiles (hides the sequence)
- Selected work as three equal case-study cards (hides cinematic proof)
- Writes as blog cards on the Hub (archive cards belong on `/writes`)
- Live desks advertised as “Not Power BI” instead of their questions
- Left-edge chapter rail covering display type (Hub uses a bottom index instead)
- Viewport-locked chapters copied from AI Takes Over (native scroll only)
- Progress line / gravity rotate / spotlight / count-up as the *only* scroll motion (pages also need `StoryReveal` + a sticky kicker so something actually happens while you scroll)
- Proof as a swipe-only rail on desktop (Hub `#selected-work` should advance to the right as you scroll down)
- Portfolio workshop / Power BI / live desks as a picker, 3-up grid, or text-only list (they are `ScrollRail`s; live cards carry sneak peeks + the question)
