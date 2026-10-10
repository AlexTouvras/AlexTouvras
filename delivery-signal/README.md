# Delivery Signal

A weekly delivery brief built from a project export. The brief says what changed, which work needs attention, and which decision is waiting. Every material claim cites a row. A person approves it before a customer sees it.

This is a sample, not a business. Nobody has paid for it, and the page does not take orders.

## Run

```bash
python3 delivery-signal/pipeline.py delivery-signal/samples/northline
python3 delivery-signal/tests/test_pipeline.py
```

Open `delivery-signal/samples/northline/out/brief.html`.

The pipeline reads a directory:

- `meta.json` — portfolio name and the report date
- `work_items.csv` — one row per Jira-style issue
- `previous_work_items.csv` — optional prior export, used only for the change list
- `milestones.csv`, `dependencies.csv`, `notes.csv` — optional

It writes `brief.json`, `brief.md`, and `brief.html`.

## What the sample is designed to show

`samples/northline` is invented. Four traps are planted, and one healthy project is left alone:

- Forge `FOR-12` is overdue and unassigned, and it blocks `FOR-20`.
- Lumen reports the epic 85% complete while 8 of 37 story points are Done.
- Cedar's 9 Oct note says the project is green. The open stories were last updated in August and are already overdue.
- The legacy-extract milestone is overdue, and its successor `FOR-3` is Done, so that signal is set aside.
- Aster's note also says "on track". The export agrees, so it stays on track.

The rules are in the brief. They are operating rules for this sample, not a predictor that a date will be missed.

## Left out on purpose

Live Jira or Azure DevOps connections, accounts, email, and payments. Those wait until a delivery lead has looked at a brief like this one and said what was useful.
