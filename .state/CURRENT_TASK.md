# Current task

Directive archive for skills, rules, and automation prompts.

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
