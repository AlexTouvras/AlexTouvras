# Current task

Local connect page so a team can try Delivery Signal from a browser, a terminal, or a script. No account and no hosted upload.

## Verify

`python3 delivery-signal/tests/test_connect.py` exits 0. It loads the page, opens the sample, posts a CSV, and rejects a form with no file.

`python3 delivery-signal/connect.py` serves http://127.0.0.1:8766. The sample link fills the brief frame. A chosen CSV builds a brief in that frame.

## Done

- `connect.py` page with the sample, the export form, and the terminal commands
- `POST /run` for the form and for curl
- Column profiles for canonical, Jira, and Azure DevOps, plus `columns.json`
- One command for a single CSV
- Executive HTML and a dated file meant to be forwarded
- Plan for why a team would pay, and what waits until a second cycle

## Out of scope

- Accounts, checkout, live Jira or Azure DevOps connections
- A claim that a buyer has agreed to pay

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
