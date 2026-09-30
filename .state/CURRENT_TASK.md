# Current task

Directive archive for skills, rules, and automation prompts.

## Verify

`python3 governance/tests/test_catalog.py` exits 0.

`python3 governance/server.py` serves the archive at http://127.0.0.1:8765. Filter by repo and topic, save an edit, and restore the previous version.

## Done

- Public corpus imported into `governance/archive/`
- Public markdown listed as kind `doc`
- Orbit recorded as unreadable; known paths listed from public repos
- Local editor with filters, always-on budget, save, and version restore
- Context-budget skill packaged as a Cursor plugin

## Out of scope

- Publishing saves back to source repositories
- Writing live Cursor Automations
- Private repositories and Customize user rules
