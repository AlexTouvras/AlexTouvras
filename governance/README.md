# Directive archive

Local catalog of skills, rules, and Cursor automation directives. Filter by repository and topic, edit the text, save it, and restore an earlier version.

This archive is the review copy. Saving here does not update the source repository and does not change a live Cursor Automation. Cursor only loads a directive when it is installed in the project, in your user skills, or through a plugin.

## Run

```bash
python3 governance/server.py
```

Open http://127.0.0.1:8765

## What is imported

Rules, agent files, automation prompts, and contracts from the public repositories, plus the other public Markdown files. Grouped notes are not part of the always-on budget.

Orbit and ravens are included from their `.cursor` folders: rules, skills, automation JSON, plus the agent role files and contracts those folders point at. Similar notes are grouped (readme, state, architecture, charter, brief, spec, schema, runbook, discovery, source, log). Anything that does not match a shared pattern stays kind `doc`.

Personal skills named by Orbit rules (`orbit-essay`, `anti-ai-slop-writing`, `fable-method`) are not files in these repositories. Live Automations dashboard objects and the User Rules stored in Cursor Customize are outside this import.

## Budget

Always-on text (`alwaysApply` rules and `AGENTS.md`) is counted per repository. The cap is 1000 approximate tokens, at about 4 characters per token. Scheduled automation prompts are shown, and they are not added to that cap, because they load on a run rather than on every editor turn.

## Tests

```bash
python3 governance/tests/test_catalog.py
```

## Refresh the public import

```bash
python3 governance/import_harvest.py /path/to/harvest
python3 governance/import_markdown.py
python3 governance/categorize.py
```

`import_markdown.py` reads public GitHub repositories and adds markdown that is not already archived. The harvest directory for `import_harvest.py` is organized as `<repo>/<path-in-repo>`.
