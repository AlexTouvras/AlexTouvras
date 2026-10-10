# Delivery Signal

A weekly delivery brief from a Jira, Azure DevOps, or canonical CSV. The page says what changed, which work needs attention, and which decision is waiting. Every material claim cites a field. The same inputs produce the same result id.

Send the HTML file. The recipient does not need an account or the original export.

The reason to pay for that, and what is deliberately not built yet, is in [PLAN.md](PLAN.md). Nobody has paid. The page does not take orders.

## On a phone or a computer

Open the page from this repo:

https://htmlpreview.github.io/?https://github.com/AlexTouvras/AlexTouvras/blob/cursor/delivery-signal-mvp-b09f/docs/index.html

Choose this week's CSV. The export stays in that browser. Share or download the HTML brief. The page runs the same checker as this repo. The Northline sample produces result `e53f514aa6`.

The files live in [`docs/`](../docs). A durable address a phone can keep on the Home Screen is https://alextouvras.github.io/AlexTouvras/ after GitHub Pages is set to branch `main` and folder `/docs`. That setting is in the repository Settings, under Pages. It could not be turned on from this change.

## One command

Use the shell that is already open. The command does not install Python, Node, a package, or a server. It uses `python3`, `python`, or `py` when one of them is already on the machine. The CSV stays there.

```bash
delivery-signal/run.sh issues.csv
```

```powershell
delivery-signal/run.ps1 issues.csv
```

```bat
delivery-signal\run.cmd issues.csv
```

The name defaults to the file name. The date defaults to today. Add `--previous issues-last-week.csv` when last week's export is there.

From a machine that does not have this repo, the same scripts are one remote command:

```bash
curl -fsSL https://raw.githubusercontent.com/AlexTouvras/AlexTouvras/cursor/delivery-signal-mvp-b09f/delivery-signal/run.sh | bash -s -- issues.csv
```

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/AlexTouvras/AlexTouvras/cursor/delivery-signal-mvp-b09f/delivery-signal/run.ps1))) .\issues.csv
```

If an agent CLI is already open on this repo, ask it for the brief. `skills/delivery-signal/SKILL.md` tells that agent to run the command above and not to install anything.

If Python is not already on the machine, the command prints the page link instead of starting an installer.

## On this computer

A local page is still there for a browser on the same machine:

```bash
python3 delivery-signal/connect.py
```

The page is at http://127.0.0.1:8766. Open the Northline sample, or choose a CSV. The export stays on this machine.

From a terminal, the same checker without the page:

```bash
python3 delivery-signal/pipeline.py issues.csv --name "Northwind" --as-of 2026-10-10 --previous issues-last-week.csv

curl -F name="Northwind" -F as_of="2026-10-10" -F export=@issues.csv \
  http://127.0.0.1:8766/run -o brief.html
```

## Run

One export, without the page:

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
