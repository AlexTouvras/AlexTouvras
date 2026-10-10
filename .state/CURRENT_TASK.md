# Current task

Delivery Signal sample: an evidence-linked weekly brief from a synthetic consultancy export. Demand is not validated. No orders, payments, or live project-tool connections.

## Verify

`python3 delivery-signal/tests/test_pipeline.py` exits 0.

`python3 delivery-signal/pipeline.py delivery-signal/samples/northline` writes `delivery-signal/samples/northline/out/brief.html`. The page shows five top risks, sets the overdue legacy-extract dependency aside, leaves Aster on track, and keeps approval pending.

## Done

- Deterministic pipeline in `delivery-signal/pipeline.py`
- Northline sample with planted traps: unassigned overdue work, a blocked release, a green note that disagrees with the export, a misleading 85% completion, and one overdue dependency that does not block
- Markdown, HTML, and JSON brief

## Out of scope

- Claiming a buyer or a price
- Jira or Azure DevOps integrations, email, accounts, payments

# Previous task

Daycare comparison page for Lipstikkakuja 14, Rekola. Child is 7 weeks old on 6 Oct 2026; target start is November 2027 (about 15 months).

## Verify

Open `daycare/index.html` over HTTP (`python3 -m http.server` inside `daycare/`). Map shows home and a 10 km circle. Press a marker and a list row; both open the same card. English filter leaves the four English programmes plus the lighter English-enrichment centres. Default order starts with Pilke Playschool Pohjantähti.

## Done

- 176 daycares inside 10 km: Helsinki region Service Map for Helsinki and Vantaa, OpenStreetMap plus city pages for Kerava and Tuusula
- Score weights English, toddler-age fit, whether Vantaa can actually offer the place, fee versus the municipal cap, and distance
- Map, pressable card, ranked list, filters, shortlist

## Out of scope

- Live vacancy or an application form
- A routed commute time
- Publishing the page from the profile README

## Studio

Temporary Orbit Studio route `/studio/daycare` is prepared in `governance/orbit-studio/` and committed locally on Orbit branch `cursor/studio-daycare-9c6e`. Push to AlexTouvras/Orbit returned HTTP 403 for cursor[bot]. The live Studio does not show the card until that branch is pushed by someone with write access.

## Verify

`python3 governance/tests/test_catalog.py` exits 0.

`python3 governance/server.py` serves the archive at http://127.0.0.1:8765. Filter by repo and topic, save an edit, and restore the previous version.

## Done

- Public corpus imported into `governance/archive/`
- Public markdown listed as kind `doc`
- Orbit and ravens `.cursor` rules, skills, and automations imported
- Similar docs grouped; leftovers stay kind doc
- Local editor with filters, always-on budget, save, and version restore
- Context-budget skill packaged as a Cursor plugin
- Studio page and snapshot prepared in `governance/orbit-studio/`
- Push to AlexTouvras/Orbit denied (HTTP 403). Live `/studio/directives` is not deployed.
- Local Orbit dev server (`STUDIO_DEV_OPEN=1`) served `/studio` and `/studio/directives`. Filtering to Orbit skills showed the five skill files and the visual-storytelling body. The public home page does not link the archive.

## Out of scope

- Publishing saves back to source repositories
- Writing live Cursor Automations
- Private repositories and Customize user rules
