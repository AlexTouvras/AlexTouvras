# Directive archive

Local catalog of skills, rules, and Cursor automation directives. Filter by repository and topic, edit the text, save it, and restore an earlier version.

This archive is the review copy. Saving here does not update the source repository and does not change a live Cursor Automation. Cursor only loads a directive when it is installed in the project, in your user skills, or through a plugin.

## Run

```bash
python3 governance/server.py
```

Open http://127.0.0.1:8765

## What is in the first import

Public files from pixels, ProjectBrain, the three field-card repos, storytelling, and ledger. No `SKILL.md` files were in those repositories. Private repositories, live Automations dashboard objects, and the User Rules stored in Cursor Customize are outside this import. The ProjectBrain user-rule file is the template, not a live export.

## Budget

Always-on text (`alwaysApply` rules and `AGENTS.md`) is counted per repository. The cap is 1000 approximate tokens, at about 4 characters per token. Scheduled automation prompts are shown, and they are not added to that cap, because they load on a run rather than on every editor turn.

## Tests

```bash
python3 governance/tests/test_catalog.py
```

## Refresh the public import

```bash
python3 governance/import_harvest.py /path/to/harvest
```

The harvest directory is organized as `<repo>/<path-in-repo>`.
