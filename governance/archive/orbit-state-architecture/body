# Architecture (working log)

> Tracked in git. Living decisions for this repo — not a substitute for `docs/architecture/`.

## Overview

Orbit is a Next.js personal HQ: Blog (MDX Writes), Portfolio (workshop + GitHub + Power BI screenshots + live desks at `/portfolio/live`), Related articles RSS cache, Studio (profile + week log + roadmap), architecture sync, weekly digest (Resend auto-send; test-to-self until go-live). Public discovery via `sitemap.xml` / `robots.txt` / blog `feed.xml`, plus Vercel Analytics.

**Product truth (2026-09-23):** Root `PRODUCT.md` + `docs/product/*` are authoritative for identity layers (HUd WHO / Hub WHAT / Studio WHERE / timeline HOW). Agents must Scope-check via `docs/product/AGENT_RULES.md`. Wired from `.cursor/rules/product-kit.mdc`.

## Data shapes

| Name | Shape / location | Notes |
|------|------------------|-------|
| FeedSource | `src/lib/news/sources.ts` | `name`, `url`, `category`, optional `maxItems` |
| NewsCache | `data/news-cache.json` | Fetched via `npm run news:fetch` |
| Live EU Spot | `data/live/eu-spot.json` | `npm run live:fetch-eu` (A44) + `npm run live:fetch-eu-pulse`. Price refresh keeps existing `pulses` until the pulse step rewrites them. Map category layers + per-zone desk (Finland-style pulse + mix nowcast for every zone). Power Pulse is not a separate Portfolio desk — `/portfolio/live/power` redirects here. |
| Live Helsinki Housing | `data/live/housing.json` | `npm run live:fetch-housing`. Stat.fi `ashi` monthly 15iq + quarterly 13mv (Helsinki history + HKI 1–4). CC BY 4.0. Capital-region choropleth (`HousingMap`) paints ~150 postal codes from yearly ashi 13mu €/m² (sales-weighted flats + terraced) via `housing-postal-paths.ts` (Paavo pno, CC BY 4.0) — Asuntomaatti-style grain. |
| Live Europe Power Mix | `data/live/power-mix.json` | `npm run live:fetch-mix`. Energy-Charts `public_power` last 24h → country 100% stacked shares (fossil/nuclear/wind/hydro/solar/biomass/other), sorted clean→fossil. |
| Live Europe Economy Pulse | `data/live/economy.json` | `npm run live:fetch-economy`. Eurostat HICP (`prc_hicp_manr` history merged with early `teicp000`) / unemployment / consumer confidence / GDP + ECB deposit facility + ECB press/statistics RSS (EA21) + Google News economy wires per spotlight country/EU (incl. DK, NO). Desk defaults to euro area (EA21); spotlight selector filters KPIs and headlines. |
| Published workshop projects | `data/published-projects.json` (+ `.seed.json`) | `liveUrl` = demo; `caseStudyUrl` = `/writes/...` |
| Writes | `src/content/writes/*.mdx` | `showcase: true` → Home Selected work |
| Essay feedback | `data/essay-feedback.json` | Keyed by essay slug → `{ title, entries[] }` with `rating`, optional `note`, and ISO `at` |
| Studio roadmap | `data/studio-roadmap.json` (+ `.seed.json`) | `focusNow` (public on `/card` only) + private milestones (`planned`/`active`/`evidence`/`proven`). Persist via `persistDataJson` same as profile. Store: `src/lib/studio-roadmap.ts`. |
| Newsletter digest draft | `data/newsletter-draft.json` | Titles/links only. Gitignored locally; persist send status via GitHub |
| Newsletter subscribers | Resend Audience, or `RESEND_NEWSLETTER_TEST_TO` | Emails never in git. Test-to skips the audience entirely |
| Ravens findings | GitHub Contents on `AlexTouvras/ravens` | Weekly highlights: one item per domain that moved (inbox first). `RAVENS_GITHUB_TOKEN` |
| Week log | `/studio/week` (+ `/2026-W36/fitness` etc. for other ISO weeks; legacy `?week=` redirects) via `src/lib/week-log/` | ISO week hub. Fitness lane renders `ArcStatusCard` from plan `narrative` + `daily_quest` (fitness-coach repo). Codex opens with `GateBell`: the normal curve, letter bands, and this week's gate plus stat marks. Stats order: STR, AGI, SPD, END, VIT, PER. SPD is peak velocity (max speed); omitted until the plan JSON includes `stats.spd`. `narrative.health`: max = 100 + VIT, fill = Body Battery share. Heimdall embeds inline (Technique on lifts, Watch on Ravens parenting). Auth: GitHub allowlist + 90d sliding session; password fallback; `STUDIO_DEV_OPEN` locally |
| Fleet registry | `docs/ops/fleet.yaml` | Daily unattended-job checks for `#ops-channel`; cloud evidence is GitHub + Slack only |

## Design patterns

- Hub is a **chaptered scroll story inside the same `max-w-5xl` column as Blog**. Open → Gravity → Craft → Proof reel → Live peek reel → Signals reel → Close (Home only). Shared primitives live in `src/components/story/` (`StoryHeadline`, `StoryScene`, `ChapterMark`, `GravityField`, `DeskStoryHeader`, `DeskCast`, `DeskPicture`, `DeskClose`, `DeskMissing`, `StoryStat`, `ScrollLine`, `ScrollSpot`, `StoryReveal`, `ScrollRail`). Public pages share `max-w-5xl`; only `/portfolio/live/[slug]` is `max-w-6xl`. `StoryHeadline` (mono kicker + two display lines) is the title on Home, Blog, Portfolio, About, Contact, Related, Newsletter, and the live index — each page has its own line. No fixed chapter bar. Scroll-linked motion is native: a top `ScrollLine`, Gravity rings/satellites that turn with the chapter’s scroll (sticky diagram on `lg+`), `ScrollSpot` on lists, `StoryReveal` scale-in, `StoryStat` count-up, and `ScrollRail` on **reels** (Hub Proof, live desks, Portfolio workshop, Power BI). Every reel card is `w-[min(40rem,86cqw)]` against the column. Vertical scroll translates the track as soon as the reel reaches the top of the viewport. After the first measure, a scroll event refreshes progress so the opening card does not jump to the end. Lists stay vertical. No wheel capture / vertical snap. AppChrome paints `ScrollLine` on `/`, `/about`, `/portfolio`, `/writes`, `/contact`, `/radar`, `/newsletter`, and `/portfolio/live`. `prefers-reduced-motion` keeps reels as swipe rails.
- `/portfolio` uses the same column and title: Open (“What survived / the cut.”) → **flagship teaser** (`FlagshipTeaser` → `/stories`) → workshop `ScrollRail` → live peek reel (`LiveDeskReel`) → Power BI `ScrollRail` of report pictures (pages stay on the card; enlarge lightbox) → GitHub as an editorial list. No copied Home close. Not a wrapping `GlassCard` grid. Portfolio `#live` and `/portfolio/live` share the same peek reel. Desk questions are plain (“Where is electricity expensive today?”). Workshop and Power BI pass `fit` on `ScrollRail`: the sticky frame is `100dvh - 7.5rem` and cannot grow past the phone. The card body (project blurb, report preview) shrinks before the links and page controls. Other reels keep the growing frame.
- **Interactive Decision Storytelling (flagship)** is authored in `AlexTouvras/storytelling` and mirrored into this repo by `npm run stories:sync` (`scripts/sync-storytelling.mjs`). A push to storytelling `main` dispatches `storytelling-sync`; the Orbit workflow copies the engine, builds, and pushes so Vercel redeploys `/stories`. Routes: `/stories` (landing), `/stories/[slug]`, `/stories/[slug]/method`, `/stories/<slug>/film`, `/stories/lab/*`. Engine under whatever `src/components/<folder>` storytelling has (storytelling, film, director, reader, onepager, and the next one) + `src/illustrations/` (`.riv` binaries) + `src/stories/` + `src/lib/loadStory.ts` / `sim/` / `director/` / `reader/` / `rive/` + `data/figures/`. Component folders, lib subfolders, and loose lib files are discovered from the storytelling checkout (`cn.ts` and `prefers-reduced-motion.ts` stay skipped; their imports are rewritten). The workflow stages those parent trees, so a new engine folder ships without a second allowlist edit. A new npm dependency still has to be added to Orbit `package.json`, or the pre-publish build fails and nothing ships (2026-09-28: `how-much-fast-reserve` needed reader, director, illustrations, and Rive; 2026-09-29: share cards needed `src/components/onepager`). Sync rewrites `@/lib/cn` → `@/lib/utils`, `prefers-reduced-motion` → `use-prefers-reduced-motion`, and storytelling home links to `/stories`. StoryHero keeps the tighter top padding because `/stories` has no absolute header. `src/app/stories/page.tsx` stays Orbit-owned except `LISTED_SLUGS`. Depends on `zod` + `react-scrollama` + `@rive-app/canvas` / `@rive-app/react-canvas` (pinned to storytelling's versions). AppChrome gives `/stories*` full-bleed with no site header. Canonical positioning remains in the sibling repo’s `docs/FLAGSHIP.md`.
- Live desk tiles (`LiveDeskTile` inside `LiveDeskReel`) carry a sneak peek + the desk **question** as the headline: EU Spot paints the live baseload SVG; Nordic Equity paints a treemap from `heatmap-web` `board.json` (not an iframe of the board page); Helsinki Housing paints a monthly €/m² sparkline; Europe Power Mix paints mini 100% stacked country bars; Europe Economy Pulse paints euro-area HICP. Hub `/`, `/portfolio` `#live`, and `/portfolio/live` all use this reel (`ScrollRail`; vertical scroll drives the track). Each live desk page is Open → Cast → Picture → Move → Close: `DeskStoryHeader` (question as `h1`), 3–5 `StoryStat` figures before any click, full-column map/tape/mix, interaction on the same scene, then source/lag/what-it-is-not. Missing snapshots use `DeskMissing` with the desk `question`, not the dataset name. Nordic Equity Cast is computed server-side from `fetchHeatmapBoard()` (up/down/leader).
- SEO: App Router `sitemap.ts` / `robots.ts`; site URL from `getSiteUrl()` (`NEXT_PUBLIC_SITE_URL`); JSON-LD Person/WebSite/Blog in layout + BlogPosting/BreadcrumbList on Writes; per-Write OG via `writes/[slug]/opengraph-image.tsx` (shared `src/lib/seo/og-card.tsx`); optional Write frontmatter `updated` for freshness; blog RSS at `/feed.xml`; `public/llms.txt`; app `icon.tsx`. New MDX Writes inherit SEO automatically from frontmatter — no per-post meta authoring.
- Field-card static HTML in `public/*-field-card/` should keep `canonical` + `og:url` + `og:image` (points at site `/opengraph-image`). Source field-card repos own the HTML and may overwrite on sync — preserve those meta tags when refreshing cards.
- Homepage field cards mount one storytelling robot (`public/field-card-robot.mjs`, storytelling PR 25). The script reads that commit's six bubble lines and accent from `field-cards.ts` (`ai`, `delivery`, `analytics`, `sdlc`, `credit`, `story`). SDLC uses Delivery violet; Story uses AI cyan. It stays off when the sheet is iframed by `/stories/<card>`, and it hides in print. The Agentic AI sheet keeps its own script (it sets only `line`; the file defaults are that card). Approve re-inserts the tag on Analytics and Delivery via `ensureFieldCardRobot` so a source-repo sync does not drop it. Bayes is a method card and does not get the robot.
- **Story field card** (`public/story-field-card/`) uses the shared field-card sheet grammar (hero + layer stack, problem→use→example, tri, kill list, foundation). Message is the OS spine: Question → Evidence → Tension → Narrative → Experience → Decision; craft five-words as the always-on strip. No scroll-graph instrument.
- Portfolio cards: Case study link from `caseStudyUrl`, or from `liveUrl` when it is already a `/writes/` path
- Showcase essays for featured workshop projects (Ledger, Power BI, Orbit, Heatmap)
- Personal-ops projects (mealplan, fitness coach) stay non-featured; Write + `/architecture/` case study, not Home Selected work
- Essay footer feedback is anonymous, rate-limited, persisted to JSON, and still uses `localStorage` only as a one-browser re-submit gate.
- Essay pages read their own feedback entries server-side and render a newest-first note list below the feedback CTA.
- Essay feedback Slack notifications prefer `SLACK_ORBIT_WEBHOOK_URL` (for `#orbit`) and fall back to `SLACK_WEBHOOK_URL`.
- Weekly Write Slack draft / publish / skip notifications prefer `SLACK_ORBIT_WEBHOOK_URL` (`#orbit`) and fall back to `SLACK_WEBHOOK_URL`.
- Weekly digest: **GitHub Actions Tuesday 07:15 UTC is primary** (Vercel Hobby cron went silent after 2026-08-18). Vercel `/api/cron/newsletter` Tue 08:00 UTC is backup; `already_sent_this_week` via `data/newsletter-draft.json` on GitHub prevents doubles. `RESEND_NEWSLETTER_TEST_TO` mails only that inbox; unset it to broadcast. **No Slack** for digest content — email only. Public subscribe stays closed while test-to is set. Ravens section is **one highlight per domain that moved this week**, not a vault dump.
- Daily ops check is a separate Cursor Automation on `Orbit`/`main` at 08:00 GMT+3 posting only exceptions to `#ops-channel`. It is propose-only and must not infer local state from `~/.cursor`; registry and playbook must exist on GitHub `main`.
- Studio week log is owner-only (`STUDIO_PASSWORD` emergency + GitHub OAuth allowlist + `noindex`). Token chain: `OPS_GITHUB_TOKEN` → `RAVENS_GITHUB_TOKEN` → `GITHUB_TOKEN`. Do not put the week log in public nav. Heimdall embeds inline with `youtube-nocookie` (Technique on fitness lifts; parenting Watch on Ravens); falls back to the watch URL.
- Fitness course strip on `/studio/week/fitness` writes sibling `fitness-coach` via `coach-course` locally. On Vercel, Apply dispatches `studio-apply-course` on fitness-coach (GitHub Action regenerates the week and commits). Needs `OPS_GITHUB_TOKEN` Contents: Read and write on fitness-coach. Skin (Arc) is not a weekly slicer. Past race dates expire out of taper.
- Brand accent orbit: hex keyframes on unlayered `.orbit-accent` (direct `color` animation) + `@property --orbit-accent` `<color>` for bg/border/mix. Tailwind `neon-cyan` is a **fixed** rest-state cyan (`--accent-cyan`); body links (Case study, Read, nav CTAs) do not ride the loop. Section eyebrows and hero totals do, via `.orbit-accent`. `--orbit-fg-delay` is applied after hydrate (`OrbitSync` layout effect, not a `Date.now()` SSR script) so new mounts join mid-cycle without a hydration mismatch. Avoid `oklch()` in animated tokens (LightningCSS → lab/@supports; Chromium can blank `color: var(...)`). Never animate OKLCH channels via `@property <number>`. Topic AI uses fixed `--accent-ai` / `neon-ai`. Violet/blue stay fixed.
- Studio profile save: local always writes `data/profile.json`; Vercel requires `GITHUB_TOKEN` and commits for redeploy. UI must show the real server message (not a blanket "Live site updated").
- Vercel `ignoreCommand` (`scripts/vercel-ignore.mjs`) skips rebuilds when a commit only touches runtime-read GitHub JSON (news cache, essay feedback, newsletter/weekly-write drafts). Profile, published projects, Writes, field cards, and Power BI screenshots still build. Fail-open: if git cannot list files, Vercel builds.
- ProjectBrain showcase (2026-09-02): essay `when-the-portfolio-needs-a-memory.mdx` (`featured` + `showcase`); portfolio card + `/architecture/projectbrain` synced from `Memory/docs/architecture/`.
- Public Writes are stranger-first (`docs/essay-voice.md`): gloss workshop nicknames; category follows the decision rule (rotate Delivery/Learning/Career/general data; do not default Power BI). Active clone for Writes is this `website/` repo; `Documents/Orbit` can lag.

## Dependencies

| Dependency | Why introduced | Date |
|------------|----------------|------|
| `@vercel/analytics` | Privacy-light page analytics on Vercel | 2026-07-26 |
| `uqr` | Encode on-screen QR for `/qr-code` → `/card` | 2026-09-09 |
| `zod` | Decision-story manifest validation | 2026-09-24 |
| `react-scrollama` | Sticky scroll-scene step enter for `/stories` | 2026-09-24 |

## File structure

```text
src/lib/news/
├── sources.ts      # RSS registry
├── balance.ts      # interleaveByCategory
├── fetcher.ts
└── cache*.ts
src/lib/site.ts                 # getSiteUrl()
src/lib/seo/
├── writes.ts       # modified date + absolute Write/OG URLs
└── og-card.tsx     # shared ImageResponse layouts (site + Write)
src/app/icon.tsx
src/app/writes/[slug]/opengraph-image.tsx
public/llms.txt
src/content/live-desks.ts
src/content/live/eu-zone-paths.ts
src/content/live/housing-map-paths.ts  # municipality outlines (legacy)
src/content/live/housing-postal-paths.ts  # Paavo postal SVG paths for HousingMap choropleth
scripts/live/build-housing-postal-paths.mjs
src/lib/live/
src/lib/live/housing-map-fill.ts
src/components/story/           # Hub/desk visual-storytelling primitives
src/components/live/
src/components/live/HousingMap.tsx
src/app/portfolio/live/
data/live/power.json
data/live/eu-spot.json
data/live/housing.json
src/scripts/fetch-live-power.ts
src/scripts/fetch-live-eu-spot.ts
src/scripts/fetch-live-housing.ts
scripts/live/build-eu-zone-paths.mjs
src/app/robots.ts
src/app/feed.xml/route.ts
src/components/seo/
├── JsonLd.tsx
└── ArticleJsonLd.tsx
data/published-projects.json
src/content/writes/
public/field-card/index.html            # Agentic AI Field Card (home AI competency)
public/analytics-field-card/index.html  # Data Analytics Field Card (home Data competency)
public/delivery-field-card/index.html   # Technology Delivery Field Card (home Delivery competency)
public/sdlc-field-card/index.html       # SDLC Field Card (home SDLC competency; Orbit-hosted until source repo)
public/credit-risk-field-card/index.html # Credit Risk Field Card (origination + IFRS 9; Orbit-hosted until source repo)
public/story-field-card/index.html      # Data & visual storytelling (Hub Story competency; Orbit-hosted)
src/lib/field-card/registry.ts          # Multi-card Apply review sync map (repo → Orbit path)
src/lib/field-card/slack.ts             # Laconic one-post-per-card #orbit FYI (Review/Considered/Changed/Online + Check card)
src/app/card/page.tsx                   # Public identity HUD (chrome-light)
src/app/qr-code/page.tsx                # On-screen QR to /card
src/components/card/                    # IdentityHud + CardQr; href.ts is the portrait → Arc HUD link
src/components/layout/AppChrome.tsx     # Hides header/footer/particles on /card and /qr-code
src/app/api/field-card/{preview,action}/ # Shared preview / Apply review for all registered cards
src/lib/newsletter/
├── digest.ts
├── ravens.ts       # all domains from AlexTouvras/ravens (no allowlist)
├── deliver.ts      # test-to or Resend Broadcast (no Approve)
├── run.ts
└── tokens.ts
src/app/newsletter/page.tsx
src/app/api/cron/newsletter/
src/lib/week-log/            # Studio /studio/week loaders + Heimdall matcher
src/lib/studio-roadmap.ts    # focusNow + milestones; persistDataJson like profile
src/app/studio/week/         # Hub + topic pages
src/app/studio/roadmap/      # Private trajectory editor (feeds /card NOW)
src/components/studio/week/  # Topic panels + HeimdallEmbed
src/components/studio/RoadmapEditor.tsx
data/studio-roadmap.json
data/studio-roadmap.seed.json
PRODUCT.md
docs/product/                # VISION, POSITIONING, HUD_SPEC, STUDIO_ROADMAP, WEBSITE_ARCHITECTURE, AGENT_RULES
canvases/                    # Cursor IDE only; gitignored + tsconfig exclude
.state/
```

## Key decisions

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-09-30 | One storytelling robot on every homepage field card | Storytelling PR 25 binds six lines and an accent. Orbit sheets load that character from `main` (`public/field-card-robot.mjs`). Agentic AI keeps its own script. Approve re-inserts the tag on Analytics and Delivery. Bayes stays without it. |
| 2026-09-30 | Public title under the name is `profile.role` (`AI & Data Systems Lead`); the portrait opens `/card?face=arc` | Owner: website title matches the Arc HUD, and pressing the avatar opens that HUD. Hub and About kickers use the role (sentence case). Pillars stay on the Home ticker. `IdentityCardFlip` starts on the Arc face when `face=arc` and `/api/card/arc` returns a gate; strangers still get the identity card. The portrait on the identity face flips the same way. Arc header shows `profile.role`. |
| 2026-09-30 | Agentic field-card discovery should also search practice writing | GitHub framework search never surfaced essays. Discover should read Anthropic Engineering, Ars Contextus, and filtered Simon Willison entries, plus four web queries. Hits can earn a job row, not a picker row. Seen URLs live in that repo's `data/practice-seen.json`. Patch: `docs/ops/agentic-field-card-practice-search.patch` (this agent cannot push `agentic-ai-field-card`). |
| 2026-09-29 | Storytelling sync discovers engine folders | A handwritten mirror list plus a second `git add` list dropped every new folder (`onepager` share cards, earlier reader/director/Rive). The pre-publish build then failed and the push never landed. Discovery plus staging the parent trees stops that. New npm dependencies still need `package.json`. |
| 2026-09-21 | Hub is a chaptered visual story; live desks keep question-as-h1 | Owner asked to leave the traditional card-grid HQ for storytelling (inspiration: AI Takes Over, Light Factory, Amanda Lee Peers, OSOS, Haus of Words) without Webflow theatre. Skill: `.cursor/skills/visual-storytelling`. |
| 2026-09-21 | Hub scroll story: things happen as you scroll, without jacking | Owner: inspiration sites move as you read down; Orbit was still a static chapter stack. Allowed: progress line, gravity rotate/orbit, sticky kicker, in-view spotlight, count-up, `StoryReveal`. Forbidden: pin-jack / vertical snap. |
| 2026-09-21 | Reels (Proof, workshop, Power BI, live desks) track vertical scroll | Owner: should Systems I've built — and PBI — move right as you scroll down. Live desks later needed sneak peeks + the question on the same rail. Lists stay vertical. `ScrollRail` is the primitive. |
| 2026-09-21 | Live desks follow Open → Cast → Picture → Move → Close | Owner: apply the Hub recipe on `/portfolio/live/*`. Cast answers the question before a click; missing states keep the question as `h1`. |
| 2026-09-21 | `/portfolio` follows Hub grammar without full-bleed | Owner: apply storytelling to the remaining public card-grid HQ. Workshop is a reel; GitHub is a list; live desks are a peek reel; Power BI is a report picture reel. |
| 2026-08-29 | Newsletter is email-only — no Slack digest FYI | Owner: do not post newsletter contents to Slack |
| 2026-08-29 | Newsletter primary = GHA Tue 07:15 UTC; Vercel cron Tue 08:00 backup | Vercel-only path produced zero Resend sends after 2026-08-18; GHA catch-up worked |
| 2026-08-31 | Fleet ops field-card check: skip open `chore/weekly-refresh-*` when same repo already merged that ISO week | Delivery W35 had PR #3 live + orphaned discovery PR #4; daily check kept paging #ops-channel |
| 2026-08-29 | Weekly Write Approve: hard-gate Slack notify until draft verified on GitHub default branch + NEXT_PUBLIC_SITE_URL set; link origin never defaults to localhost | Preview/Approve opened dead hosts or "Draft not found" — gitignored draft is not on Vercel FS; Slack links signed as localhost when notify ran locally |
| 2026-08-17 | Digest Ravens = one highlight per domain this week | Test email was a vault dump; owner asked for weekly highlights only |
| 2026-09-22 | Ravens frontmatter with an unquoted colon is quoted and retried; one bad note cannot zero the section | `fi-first-latch` title (`latch: let`) threw js-yaml and `fetchRavensForDigest` returned `[]`, so Tue 22 Sep mail had no beats |
| 2026-08-17 | Private week log at `/studio/week` behind Studio session, not a secret URL | Reuse existing password + noindex; lanes read git artifacts including CareerOps daily-digest / weekly-scan |
| 2026-08-17 | Digest auto-sends; `RESEND_NEWSLETTER_TEST_TO` for solo validation | Owner will judge the email in-inbox, not via Slack Approve |
| 2026-08-11 | Fitness coach systems Write + non-featured portfolio card | Ops loop (git/Slack/Automations/Intervals), not training diary; same personal-ops lane as mealplan |
| 2026-08-11 | Data Analytics Field Card + shared Orbit field-card registry | Same weekly discovery → Cursor judgment → #orbit Approve process as AI card; stack is ASK/GRAIN/TRUTH/USE (not a Fabric brochure) |
| 2026-08-13 | Technology Delivery Field Card + Hub competency href | Same weekly discovery → Cursor judgment → #orbit Approve as AI/analytics; stack is INTENT/WINDOW/PROOF/CUTOVER (not a Scrum/SAFe brochure) |
| 2026-08-13 | Field cards: verb lede + Always-on strip; AI gets LLM floor | Family pattern from poster comparison; MCP stays tool reach, not orchestration |
| 2026-08-03 | Weekly Write Slack posts full essay in-channel (chunked sections); `githubSynced` required for preview/Approve | Teaser + browser preview 404'd when Cloud Automation left the pending draft on a feature branch only |
| 2026-07-26 | Orbit `caseStudyUrl` → `/writes/building-orbit` | Essay existed; card lacked Case study link |
| 2026-07-26 | Heatmap case study Write + `caseStudyUrl` | Featured live board had no write-up |
| 2026-07-26 | Dropped ProjectHelm Write; JARVIS `/architecture/jarvis` remains historical-only backlink | Essay was present-tense under a retired banner; Hub voice pass preferred removing it over rewriting |
| 2026-07-26 | Vercel Analytics over Plausible/GA; link-out Garmin skipped | Hosted on Vercel; zero-config traffic; no hobby surface this phase |
| 2026-07-27 | Essay feedback persists to `data/essay-feedback.json` by slug, with Slack ping on submit | Keeps feedback close to the essay corpus and easy to surface later in Studio without adding a DB |
| 2026-07-27 | Weekly Write Slack target → `#orbit` via `SLACK_ORBIT_WEBHOOK_URL` | Keep essay drafts with Orbit feedback in one channel instead of `#career-ops` |
| 2026-07-24 | Optional `thesisUrl` / `thesisTitle` on `CvEducation`; About education cards link out when set (ProjectCard-style) | Surface theses without Portfolio clutter; Bachelor stays static |
| 2026-07-24 | Trim AI to OpenAI + Simon `entries` (max 8 each); drop InfoQ DevOps + TDS + Personal Kanban; add Databricks/DuckDB/MotherDuck/Dagster + RADACAD/Data Mozart + Scrum.org | Chronological feed and weekly essays read as AI-only despite balanced cache counts |
| 2026-07-30 | Agentic field card hosted as static `public/field-card/`; home AI competency links there | Keep standalone HTML (print/LinkedIn) outside Orbit chrome; competency is the discovery path |
| 2026-08-03 | Slack Approve syncs field-card `index.html` → Orbit `public/field-card/` | Pages updated on merge; site copy was stale until this lockstep commit + Vercel redeploy |
| 2026-08-10 | Vercel `WEEKLY_WRITE_SECRET` must match Cloud Automation / local signing secret (preferred over bare `CRON_SECRET`) | Preview/Approve tokens failed with `invalid signature` when Vercel `CRON_SECRET` drifted from the automation signer; draft must also live on GitHub default branch |
| 2026-08-11 | Field-card pipeline fail-closed: discovery Slack ping + Sat/Mon judgment watchdog + Approve notify requires `## Summary` | W32 stalled silently when Friday Cursor Automation missed; silence meant “nothing happened” |
| 2026-09-05 | Field-card judgment watchdog: drop Saturday cron; keep Friday pass + Monday escalate | Saturday after Friday is redundant; owner asked to keep Friday only |
| 2026-09-05 | Field-card week always ships (stamp-only counts); discovery CI moves to Thursday and skips if the week already merged | Late Friday GHA opened duplicate PRs after review; agentic/analytics never published W36 |
| 2026-08-11 | Field-card pipeline fail-closed: discovery Slack ping + Sat/Mon judgment watchdog + Approve notify requires `## Summary` | W32 stalled silently when Friday Cursor Automation missed; silence meant “nothing happened” |
| 2026-08-11 | Field-card repo must carry the same `WEEKLY_WRITE_SECRET` as Orbit/Vercel (not only stale `CRON_SECRET`) | Preview/Approve tokens signed in field-card CI failed with `invalid signature` on production |
| 2026-08-12 | Public "Why Orbit" brand copy on Hub, About, and `building-orbit.mdx` | Name/metaphor was internal-only; visitors need the center-of-gravity story without reading maintainer docs |
| 2026-08-12 | Canonical local clone is `website/` only | Removed stale `Orbit/` duplicate and Cursor shadow folders pointing at the same repo |
| 2026-08-12 | Pixel avatar beside name on Hub + About (`profile.avatarUrl`, `PixelAvatar`) | Stylized identity mark without weakening typography-first heroes; JSON-LD Person `image` when set |
| 2026-08-13 | Brand foreground accents: unlayered `.orbit-accent` + hex `color` keyframes; `--orbit-accent` `<color>` (hex) for bg/border only | Channel `@property` + `oklch(var(--orbit-l)…)` and even `color: var(--orbit-accent)` went white on prod Chromium after LightningCSS; owner confirmed hex fg animation |
| 2026-08-13 | Hub accent targets = “Why the name”, header hexagon, cyan OrbitSignature, MissionHero stats, **all** `SectionHeading` eyebrows | Owner: labels like Core competencies should orbit together, not only one |
| 2026-08-13 | About CV role titles use `.orbit-accent` | Same cyan→purple loop as section eyebrows; were static `text-neon-cyan` |
| 2026-08-13 | Home About is a plain section (no GlassCard); About page Background / Why Orbit prose unboxed too | Boxed blurb sat next to unboxed section headings |
| 2026-08-13 | `neon-cyan` is static; only `.orbit-accent` / `--orbit-accent` bg-border utilities orbit | Home Case study / Read: inherited animated `text-neon-cyan` painted on one sibling only; all-or-none → none |
| 2026-08-13 | `SLACK_ORBIT_WEBHOOK_URL` on Vercel + GH Actions (Orbit + field-card repos); weekly CI prefers `#orbit` | P1-02; legacy `SLACK_WEBHOOK_URL` remains fallback only |
| 2026-09-05 | Fitness course strip on Studio week fitness: event date + stance + lift intent/density as Sunday input | Owner evaluates on localhost; past race dates must not stick in taper |
| 2026-09-05 | Cursor `canvases/` stay local (gitignore + tsconfig exclude) | First committed `.canvas.tsx` failed ship-check: Next cannot resolve `cursor/canvas` |
| 2026-09-05 | Studio Apply on Vercel = `repository_dispatch` → fitness-coach GHA | Vercel has no fitness `.venv`; `OPS_GITHUB_TOKEN` must be Contents write on fitness-coach |
| 2026-09-09 | Arc remaining HP: max = 100 + VIT, fill = Body Battery share | VIT formula unchanged; bar not in the gate letter |
| 2026-09-22 | SDLC opening is the life cycle in plain steps: plan, specify, design, build, test | “Gate chain / layers / lanes” did not read. Cutover still sits on the Delivery card. |
| 2026-09-30 | SDLC hosted pass reads `public/sdlc-field-card/PLAYBOOK.md` | The playbook holds the three lines that must stay: a one-page plan, a spec is not shared understanding, a person drops tests that do not fail for the right reason. Not an AI-native brochure. |
| 2026-09-30 | Hosted SDLC month starts with research, then update or no-change | The 17:00 pass was re-judging rows already on the card. `PLAYBOOK.md` “Monthly research” requires opened sources in the PR Summary. Credit, Story, and Bayes stay picker/jobs judgment. Fleet `bad_output` if the hosted PR has no SDLC research note. |
| 2026-09-24 | Data & visual storytelling field card on Hub/HUD (`/story-field-card/`). Spine DWELL → CLAIM → SKETCH → LEAD → OPEN. Orbit-hosted. Not in FIELD_CARDS. | Owner rejected the first card as a checklist. Rewritten from Lupi, Cairo, and Segel & Heer as an art: a life, a sentence, a mark, a path, a visible doubt. |
| 2026-09-24 | `/card` flips to the fitness Arc HUD only for a Studio session (`/api/card/arc`, `Cache-Control: private, no-store`). Public HTML stays the identity card. | Owner asked to join the two cards. Visitors do not get a progress dashboard. |
| 2026-09-21 | SDLC + Credit Risk field cards on Hub/HUD as Orbit-hosted HTML | Distinct spines from Delivery (cutover) and Analytics (grain). Weekly source repos later — do not register phantom GitHub repos in FIELD_CARDS |
| 2026-09-21 | Public field-card review is monthly | Footers say Next: month, not week of. SDLC/Credit stamped on Orbit (`hosted-field-card-monthly-review.json`). |
| 2026-09-21 | Field-card discovery is monthly too | All five Hub cards: 1st 17:00 discover + 1st 18:00 source-repo review. Fleet `monthly_after` on the 2nd. Local IDE renamed the four live automations to Monthly (GetAutomation). Hosted SDLC/Credit UUID not listed from Cloud Agent. |
| 2026-09-09 | Public identity HUD at `/card`; on-screen QR at `/qr-code`; About avatar opens the HUD | Calling card for IRL scans. No extra About hero button. QR encodes current origin so localhost/LAN works. `/qr-code` is noindex. |
| 2026-09-09 | HUD lane hints use field-card thesis (`hudTitle` / `hudVerbs` / `hudDescription`); Home keeps skill blurbs | Phone scan should show stack-not-dashboard / sequence-not-ticket, not the Hub competency paragraph |
| 2026-09-30 | HUD tap lines and the Delivery / Credit field-card heroes share one summary | Owner still saw the old headlines on the sheets. Delivery hero is “Match the calendars, then cut over.” Credit hero is “Credit risk is for a lifetime. Act early.” Hub pillars say Storytelling. Delivery’s source repo can overwrite `public/delivery-field-card/` on the next monthly publish. |
| 2026-09-11 | EU Spot map uses real bidding-zone polygons (entsoe-py GeoJSON → SVG), not country choropleth | Owner asked for actual map; MIT-licensed zone shapes |
| 2026-09-22 | Visual storytelling stays on live desks | Owner: the Anthropic-style reading order (question, cast of figures, picture, a comparison you can move) is for `/portfolio/live/*`, not weekly Writes. Essays stay MDX prose. |
| 2026-09-23 | Orbit 2.0 Foundation: `PRODUCT.md` + `docs/product/*`; HUd WHO / Hub WHAT / Studio WHERE; HUD NOW = `focusNow` only; Foundation = infrastructure not career achievements | Owner-locked identity (AI & Data Systems Lead); agents Scope-check via AGENT_RULES; branch `orbit-2-foundation` |
| 2026-09-23 | After Foundation ship: next phase = Evidence Layer (audit → gap → one flagship). Lab is candidate only. `/card` shows STATEMENT only (no NOW box). Foundation website milestones = EVIDENCE; archetype not PROVEN. | Owner direction 2026-09-23 |
| 2026-09-22 | Native live desks refresh on GHA `Refresh live desks` (13:00 UTC); commit triggers a Vercel rebuild | Nordic Equity fetches heatmap-web at request time. EU Spot, Housing, Power Mix, and Economy are JSON in the deployment bundle. Do not `[skip vercel]`. EU Spot scripts use `tsx --conditions=react-server` because `entsoe-xml` / `eu-categories` import `server-only` (plain `tsx` throws). EU Spot runs only when `ENTSOE_SECURITY_TOKEN` is a repo secret. |
| 2026-09-11 | EU Spot prices from ENTSO-E A44 when `ENTSOE_SECURITY_TOKEN` set; Energy-Charts fallback | Owner generated API token; clears localhost-only license gate |
| 2026-09-11 | Finland Power Pulse folded into EU Spot; mix nowcast on every zone | Owner: remove Pulse from Portfolio; press-a-zone desk is the same reading order for FI as for every other bidding zone. Nowcast is hourly OLS on ENTSO-E mix, not Energy-Charts 15-min FI. |
| 2026-09-11 | EU Spot mix peek: dock under the map on small screens; float inset-clamped on `md+` | Phone tap clipped the overlay (`overflow-hidden` + `w-72` at the finger). In-flow card shows the full window. |
| 2026-09-11 | Write SEO is frontmatter-driven and automatic | Per-slug OG + BlogPosting/Breadcrumbs + sitemap freshness from `date`/`updated`; authors never hand-write meta for new posts |
| 2026-09-11 | Helsinki Housing Pulse live desk from Stat.fi `ashi` (monthly 15iq + quarterly 13mv) | Next queued desk after EU Spot; CC BY 4.0; refuse empty snapshot; flats-only grain matches liquid Helsinki market |
| 2026-09-25 | Storytelling `main` pushes sync into Orbit and redeploy `/stories` | Owner: updates should show without a manual port. Private read is a deploy key; storytelling dispatches `storytelling-sync`. |
