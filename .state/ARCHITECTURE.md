# Architecture

`governance/catalog.py` stores one directory per directive: `meta.json`, `body`, and `versions/`. The browser talks to `governance/server.py` on localhost. Git history of those files is a second record; the version list inside each directory is what the editor restores.

Always-on budget counts directives whose activation is `always` (rules with `alwaysApply`, root `AGENTS.md`, and `CLAUDE.md`). Automation prompts, contracts, hooks, user-rule templates, and kind `doc` markdown are visible and are not added to that cap. Orbit and ravens contribute `.cursor` rules, skills, and automations. `suggest_category` groups similar markdown; files that do not match stay kind `doc`.

`plugins/context-governance` is the only plugin in `.cursor-plugin/marketplace.json`. Installing the marketplace does not load the archive into agent context.

`governance/export_studio_snapshot.py` writes `governance/orbit-studio/data/directive-archive.json` for Orbit's private `/studio/directives` page. That page reads the snapshot. It does not edit the archive.
