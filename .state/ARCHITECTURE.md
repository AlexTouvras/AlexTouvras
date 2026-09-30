# Architecture

`governance/catalog.py` stores one directory per directive: `meta.json`, `body`, and `versions/`. The browser talks to `governance/server.py` on localhost. Git history of those files is a second record; the version list inside each directory is what the editor restores.

Always-on budget counts directives whose activation is `always` (rules with `alwaysApply` and root `AGENTS.md`). Automation prompts, contracts, hooks, and user-rule templates are visible and are not added to that cap.

`plugins/context-governance` is the only plugin in `.cursor-plugin/marketplace.json`. Installing the marketplace does not load the archive into agent context.
