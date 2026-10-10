---
name: delivery-signal
description: Build a weekly delivery brief from a Jira, Azure DevOps, or other work-item export. Use when someone asks for a delivery brief, a Monday pack, or to connect a project tracker.
---

# Delivery brief

The person uses their own terminal, from the `delivery-signal` directory. Three steps.

1. Connect this folder. Command Prompt: `run`. PowerShell: `.\run`. bash: `./run`.
2. Connect a project, or import a CSV.

```bat
run connect jira --site https://acme.atlassian.net --project FORGE
run connect ado --org https://dev.azure.com/contoso --project Fabrikam
run connect other --name "Board" --project WEB
run import issues.csv
```

`run import` with no file reads the connected Jira or Azure DevOps project. Jira needs `JIRA_EMAIL` and `JIRA_API_TOKEN` in the environment. Azure DevOps needs `ADO_PAT`. Do not write the token into a file. `other` has no live read; import the CSV.

3. Get the report.

```bat
run report
```

A single CSV is still one command:

```bat
run issues.csv
```

PowerShell: `.\run issues.csv`. bash: `./run issues.csv`. Add `--previous last-week.csv` when that file exists. The name defaults to the file name. The date defaults to today.

When they ask for a brief, run that command in the shell they already have. Do not install Python, Node, a venv, or a package. Do not start a server. Do not send them to another product's CLI.

The command writes an HTML file under `out/` and prints a result id. Reply with that id and the HTML path. The CSV stays on this machine.

If the command says Python is missing, send the page link it prints. Do not install Python.
