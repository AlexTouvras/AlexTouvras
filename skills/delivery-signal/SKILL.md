---
name: delivery-signal
description: Build a weekly delivery brief from one CSV. Use when someone asks for a delivery brief, a Monday pack, or a Jira or Azure DevOps export.
user-invocable: true
---

# Delivery brief

Run one command in the shell that is already open. Do not install Python, Node, a venv, or a package. Do not start a server.

From the repository root:

```bash
delivery-signal/run.sh path/to/issues.csv
```

```powershell
delivery-signal/run.ps1 path/to/issues.csv
```

```bat
delivery-signal\run.cmd path/to/issues.csv
```

Add `--previous path/to/last-week.csv` when a previous export exists. Add `--name "Northwind"`, `--as-of YYYY-MM-DD`, or `--profile jira` only when the defaults are wrong. The name defaults to the file name. The date defaults to today.

The command writes an HTML file under `out/` next to the CSV and prints a result id. Report that id. The CSV stays on this machine.

If the command prints that Python is missing, give the person the page link from that message. Do not install Python.
