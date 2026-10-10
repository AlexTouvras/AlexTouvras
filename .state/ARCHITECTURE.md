# Architecture

`governance/catalog.py` stores one directory per directive: `meta.json`, `body`, and `versions/`. The browser talks to `governance/server.py` on localhost. Git history of those files is a second record; the version list inside each directory is what the editor restores.

Always-on budget counts directives whose activation is `always` (rules with `alwaysApply`, root `AGENTS.md`, and `CLAUDE.md`). Automation prompts, contracts, hooks, user-rule templates, and kind `doc` markdown are visible and are not added to that cap. Orbit and ravens contribute `.cursor` rules, skills, and automations. `suggest_category` groups similar markdown; files that do not match stay kind `doc`.

`plugins/context-governance` is the only plugin in `.cursor-plugin/marketplace.json`. Installing the marketplace does not load the archive into agent context.

`governance/export_studio_snapshot.py` writes `governance/orbit-studio/data/directive-archive.json` for Orbit's private `/studio/directives` page. That page reads the snapshot. It does not edit the archive.

`delivery-signal/pipeline.py` reads one export directory and writes `brief.json`, `brief.md`, and `brief.html`. Rules are deterministic: unassigned high-priority work, blocked items, stale updates contradicted by an optimistic note, and an epic percent that does not match child story points. An overdue predecessor whose successor is Done is set aside. Findings without evidence are dropped. The sample portfolio is `delivery-signal/samples/northline`. Approval stays `pending`.

`daycare/` is a static page. `scripts/build_data.py` writes `data.json` from the Helsinki region Service Map (service node 868, 10 km of 60.3381055, 25.0572163) and OpenStreetMap kindergartens for Kerava and Tuusula. `app.js` scores each row in the browser from stored factors and the weights in `data.json`, so the sliders do not need a rebuild. Serve the folder over HTTP; `fetch("data.json")` does not run from a `file://` open.

The same page is staged for Orbit Studio at `governance/orbit-studio/`. `/studio/daycare` is owner-only: the page checks `isStudioAccessible()`, and `data/studio-daycare/` is not under `public/`. `AppChrome` treats `/studio/daycare` as a bare route so the map can use the viewport. Push to `AlexTouvras/Orbit` is denied for this agent.
