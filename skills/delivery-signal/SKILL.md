---
name: delivery-signal
description: Build a weekly delivery brief from one CSV. Use when someone asks for a delivery brief, a Monday pack, or a Jira or Azure DevOps export.
---

# Delivery brief

The person types this in their own terminal, from the `delivery-signal` directory. Command Prompt:

```bat
run issues.csv
```

PowerShell:

```powershell
.\run issues.csv
```

bash:

```bash
./run issues.csv
```

The word after `run` is their CSV. Add `--previous last-week.csv` when that file exists. The name defaults to the file name. The date defaults to today.

When they ask for a brief, run that command in the shell they already have. Do not install Python, Node, a venv, or a package. Do not start a server. Do not send them to another product's CLI.

The command writes an HTML file under `out/` next to the CSV and prints a result id. Reply with that id and the HTML path. The CSV stays on this machine.

If the command says Python is missing, send the page link it prints. Do not install Python.
