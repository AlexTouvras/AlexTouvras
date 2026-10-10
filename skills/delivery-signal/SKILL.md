---
name: delivery-signal
description: Build a weekly delivery brief from one CSV. Use when someone asks for a delivery brief, a Monday pack, or a Jira or Azure DevOps export.
user-invocable: true
---

# Delivery brief

People run this from the CLI their agent already uses:

```text
/delivery-signal issues.csv
```

`/skill delivery-signal issues.csv` is the same command. From an OpenClaw terminal:

```bash
openclaw agent --message "/delivery-signal issues.csv"
```

The words after the command are the CSV path and any of `--previous`, `--name`, `--as-of`, and `--profile`. The name defaults to the file name. The date defaults to today.

When that command arrives, run the checker yourself. Do not install Python, Node, a venv, or a package. Do not start a server.

```bash
bash delivery-signal/run.sh <words after the command>
```

On PowerShell, run `delivery-signal/run.ps1` with those words. On cmd, run `delivery-signal\run.cmd` with those words. From another working directory, the script is `{baseDir}/../../delivery-signal/run.sh`.

The command writes an HTML file under `out/` next to the CSV and prints a result id. Reply with that id and the HTML path. The CSV stays on this machine.

If the command says Python is missing, send the page link it prints. Do not install Python.
