---
name: delivery-signal
description: Build a weekly delivery brief from a Jira, Azure DevOps, or other work-item export. Use when someone asks for a delivery brief, a Monday pack, or to connect a project tracker.
---

# Delivery brief

The person uses their own terminal, from the `delivery-signal` directory.

`run` opens the configuration page on this computer. Command Prompt: `run`. PowerShell: `.\run`. bash: `./run`.

On that page they choose Jira, Azure DevOps, or another tracker, enter the project, and import a CSV or a token for one read. The report opens on the page. Leave the token out of every file. The project file keeps the site and the project key.

`run connect` opens the same page. `run report` writes the brief again.

A single CSV is still one command:

```bat
run issues.csv
```

PowerShell: `.\run issues.csv`. bash: `./run issues.csv`. Add `--previous last-week.csv` when that file exists. The name defaults to the file name. The date defaults to today.

When they ask for a brief and the CSV is already on disk, run `run issues.csv` in the shell they already have. When they want to connect a tracker, run `run` so the configuration page opens. Do not install Python, Node, a venv, or a package. Do not start a different server. Do not send them to another product's CLI.

The command writes an HTML file under `out/` and prints a result id. Reply with that id and the HTML path. The CSV stays on this machine.

If the command says Python is missing, send the page link it prints. Do not install Python.
