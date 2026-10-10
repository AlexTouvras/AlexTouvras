# Plan

The sample brief works. A delivery lead can already get a close reading by pasting the same file into a chat. The work that is worth shipping is the gap between those two outputs: a result the whole team can open, check, and compare with last week.

This file is the sequence. It is not a claim that anyone has paid.

## Why someone would pay

Public products already charge for this job. [DeliverHub](https://deliverhub.ai/) lists $80, $160, and $400 a month for 4, 8, and 20 active projects, and it answers from the team's own tools with the source cited. [Lighthouse.Delivery for Jira](https://marketplace.atlassian.com/apps/724562284/lighthouse-delivery-for-jira) puts a risk signal on the issue and says when the evidence runs out. [Aversight](https://aversight.com/en/use-cases/pmo-reporting/) sells the weekly portfolio pack as a generated brief with each claim tied to a row, instead of the manual merge.

The writing itself is not the paid part. A general chat is already good at a one-off summary. The costs that show up once the same pack is produced every week are consistency, the time to check a number, and being able to show how a line was produced ([Kolena's write-up of that split](https://www.kolena.com/blog/chatgpt-document-workflow-questions/)). Project reporting is also only useful against the previous week, and a chat does not hand the steering group a file ([why a general model falls short for PM reporting](https://enji.ai/tech-articles/ai-assistants-vs-project-aware-agents/)).

So the buyer, if there is one, is the person who already builds the Monday pack from Jira or Azure DevOps and who will be asked why a project is red. The reasons to pay, in the order we can actually demonstrate, are:

1. The same export and the same rules produce the same result id. A chat does not.
2. Each material line cites a field, and a scary row that does not block delivery is set aside instead of left in the list.
3. The change since the previous export is a section, not a prompt someone has to remember.
4. The brief is one HTML file. The recipient does not need the chat, the prompt, or the exporter's login.

The price to test is still one cycle for one portfolio, then a second cycle. A monthly fee is a question for after the second cycle is cheaper to produce than the first. DeliverHub's published floor is a reference for what a subscription looks like later, not our price.

## What has to be true of the file

Jira does not export one fixed header row. Current fields follow the columns on screen, and all-fields can omit an empty custom field ([Atlassian export docs](https://support.atlassian.com/jira-software-cloud/docs/export-search-results/), [JRACLOUD-64164](https://jira.atlassian.com/browse/JRACLOUD-64164)). Azure DevOps exports the columns on the query. Microsoft's own example is `ID, Work Item Type, Title, Assigned To, State`, and Priority is a number ([CSV import docs](https://learn.microsoft.com/en-us/azure/devops/boards/queries/import-work-items-from-csv)).

Three shapes are in the product now: the canonical sheet, a Jira header row, and an Azure DevOps header row. The Northline portfolio encoded in each shape has the same result id. A renamed header is a `columns.json` file, not a code change. Dates accept ISO, Jira's `08/Oct/26 4:12 PM`, Azure DevOps' `10/08/2026 4:12:00 PM`, and `08.10.2026`.

## What the page is for

The first screen is the pulse, what changed, the open decision, and the questions for the review. Evidence stays on the page and starts collapsed, so a reader can check a line without scrolling through every field. The set-aside line is visible without opening it: the overdue legacy extract does not block the story that is already done.

## How a team tests it

The page a phone or another computer opens from this repo is the [`docs/`](../docs) folder, through [the HTML preview of `docs/index.html`](https://htmlpreview.github.io/?https://github.com/AlexTouvras/AlexTouvras/blob/cursor/delivery-signal-mvp-b09f/docs/index.html). Choose the CSV there. The export is read in that browser. The brief can be shared or downloaded as one HTML file. Android can share a CSV into the page once it is installed from its own address, and Chrome or Edge on a computer can open a CSV with it. That address is https://alextouvras.github.io/AlexTouvras/ after Pages is set to `main` and `/docs`. The repository setting could not be changed from here.

That page runs the same Python checker as this repo, so the Northline sample keeps result id `e53f514aa6`. There is no account.

In the person's own terminal, from `delivery-signal`, the three steps are the `run` command, then a project connection or a CSV import, then the report. Command Prompt uses `run`. PowerShell uses `.\run`. bash uses `./run`. An agent in this repo uses that same command. It does not install a runtime.

```bat
run connect jira --site https://acme.atlassian.net --project FORGE
run import issues.csv
run report
```

`run import` with no file reads the connected project. The token stays in `JIRA_EMAIL` and `JIRA_API_TOKEN`, or in `ADO_PAT`. It is not stored in the project file. A tracker that is not Jira or Azure DevOps is `run connect other`, then a CSV import. A single file is still `run issues.csv --previous issues-last-week.csv`.

Send the HTML file in `out/`. That is the whole handoff.

A folder with `meta.json` still works when the pack also has notes, milestones, and dependencies:

```bash
python3 delivery-signal/pipeline.py delivery-signal/samples/northline
python3 delivery-signal/tests/test_pipeline.py
```

## Next iterations

1. Run one real sanitized export. Add only the header aliases that file needs. Do not add a fourth system until a file fails.
2. When the same team sends a second week, put the change list above the risks. That is the moment to ask for a second payment.
3. Accounts and checkout wait until someone asks to pay for the next cycle. The optional live read is already `run import` after `run connect`. It does not write back to the tracker.

## Out of scope until then

A prediction that a date will be missed. A claim that a consultancy has agreed to buy. Email sending. Writing back to the project tool.
