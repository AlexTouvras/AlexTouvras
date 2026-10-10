# Delivery Signal

A weekly delivery brief from a Jira, Azure DevOps, or canonical CSV. The page says what changed, which work needs attention, and which decision is waiting. Every material claim cites a field. The same inputs produce the same result id.

Send the HTML file. The recipient does not need an account or the original export.

The reason to pay for that, and what is deliberately not built yet, is in [PLAN.md](PLAN.md). Nobody has paid. The page does not take orders.

## Run

One export:

```bash
python3 delivery-signal/pipeline.py issues.csv --name "Northwind" --as-of 2026-10-10 --previous issues-last-week.csv
```

A folder, when you also have notes, milestones, or dependencies:

```bash
python3 delivery-signal/pipeline.py delivery-signal/samples/northline
python3 delivery-signal/tests/test_pipeline.py
```

Open `delivery-signal/samples/northline/out/brief.html`. The file to forward is next to it, named with the portfolio and the report date.

`samples/northline-jira` and `samples/northline-ado` are the same portfolio in the other two header layouts. All three briefs share one result id.

If a team renamed a column, put `columns.json` beside the export. `templates/columns.example.json` is the shape. Recognized profiles are `canonical`, `jira`, and `azure_devops`.

## What the sample shows

`samples/northline` is invented.

- Forge `FOR-12` is overdue and unassigned, and it blocks `FOR-20`.
- Lumen reports the epic 85% complete while 8 of 37 story points are Done.
- Cedar's 9 Oct note says the project is green. The open stories were last updated in August and are already overdue.
- The legacy-extract milestone is overdue, and its successor `FOR-3` is Done, so that signal is set aside on the first screen.
- Aster's note also says "on track". The export agrees, so it stays on track.

## Left for a later cycle

Live Jira or Azure DevOps connections, accounts, and payments. The next useful input is one real sanitized export, not another integration.
