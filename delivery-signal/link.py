"""Connect a tracker, import its work items, and write the brief.

The token stays in the environment. The project file records the site and the
project key only.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import urllib.error
import urllib.parse
import urllib.request
from base64 import b64encode
from pathlib import Path

import extract
import pipeline


class LinkError(Exception):
    pass


TRACKERS = ("jira", "ado", "other")
MAX_ITEMS = 500
JIRA_FIELDS = [
    "summary",
    "status",
    "issuetype",
    "priority",
    "assignee",
    "project",
    "created",
    "updated",
    "duedate",
    "parent",
    "description",
]
ADO_FIELDS = [
    "System.TeamProject",
    "System.AreaPath",
    "System.WorkItemType",
    "System.Title",
    "System.State",
    "Microsoft.VSTS.Common.Priority",
    "System.AssignedTo",
    "System.CreatedDate",
    "System.ChangedDate",
    "Microsoft.VSTS.Scheduling.DueDate",
    "System.Parent",
    "System.Description",
]

USAGE = """1. Connect this folder to your terminal. The command is run.
   Command Prompt: run
   PowerShell: .\\run
   bash: ./run
2. Connect a project, or import a CSV.
   run connect jira --site https://acme.atlassian.net --project FORGE
   run connect ado --org https://dev.azure.com/contoso --project Fabrikam
   run connect other --name "Board" --project WEB
   run import issues.csv
3. Get the report.
   run report
"""


def state_dir(home: Path) -> Path:
    return home / ".delivery-signal"


def project_path(home: Path) -> Path:
    return state_dir(home) / "project.json"


def load_project(home: Path) -> dict:
    path = project_path(home)
    if not path.is_file():
        raise LinkError("Connect a project or import a CSV first.")
    return json.loads(path.read_text(encoding="utf-8"))


def save_project(home: Path, project: dict) -> None:
    directory = state_dir(home)
    directory.mkdir(parents=True, exist_ok=True)
    project_path(home).write_text(json.dumps(project, indent=2) + "\n", encoding="utf-8")


def _https(url: str, label: str) -> str:
    text = url.strip().rstrip("/")
    parsed = urllib.parse.urlparse(text)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise LinkError(f"{label} must be an https URL without a password.")
    return text


def connect(home: Path, tracker: str, project_key: str, name: str, site: str, org: str) -> dict:
    if tracker not in TRACKERS:
        raise LinkError("Tracker must be jira, ado, or other.")
    key = project_key.strip()
    if not key:
        raise LinkError("A project key is required.")
    record = load_project(home) if project_path(home).is_file() else {}
    record.update(
        {
            "tracker": tracker,
            "project": key,
            "name": (name or record.get("name") or key).strip(),
        }
    )
    if tracker == "jira":
        if not site:
            raise LinkError("A Jira connection needs --site https://your-site.atlassian.net.")
        record["site"] = _https(site, "Jira --site")
        record.pop("org", None)
    elif tracker == "ado":
        if not org:
            raise LinkError("An Azure DevOps connection needs --org https://dev.azure.com/your-org.")
        record["org"] = _https(org, "Azure DevOps --org")
        record.pop("site", None)
    else:
        record.pop("site", None)
        record.pop("org", None)
    save_project(home, record)
    return record


def _day(value: object) -> str:
    text = "" if value is None else str(value).strip()
    if len(text) >= 10 and text[4] == "-" and text[7] == "-":
        return text[:10]
    return text


def _person(value: object) -> str:
    if isinstance(value, dict):
        return str(value.get("displayName") or value.get("uniqueName") or "").strip()
    return "" if value is None else str(value).strip()


def _adf(node: object) -> str:
    if isinstance(node, str):
        return node
    if isinstance(node, dict):
        parts = []
        if node.get("text"):
            parts.append(str(node["text"]))
        for child in node.get("content") or []:
            parts.append(_adf(child))
        return " ".join(part for part in parts if part).strip()
    if isinstance(node, list):
        return " ".join(_adf(item) for item in node).strip()
    return ""


def _write_rows(path: Path, headers: list[str], rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(rows)


def remember_import(home: Path, source: Path, previous: Path | None, name: str | None) -> dict:
    directory = state_dir(home)
    directory.mkdir(parents=True, exist_ok=True)
    dest = directory / "work_items.csv"
    prior = directory / "previous_work_items.csv"
    if previous is not None:
        shutil.copyfile(previous, prior)
    elif dest.is_file():
        shutil.copyfile(dest, prior)
    elif prior.is_file():
        prior.unlink()
    shutil.copyfile(source, dest)
    headers, _table = extract.read_table(dest)
    try:
        profile = extract.detect_profile(headers)
    except extract.InputError:
        profile = ""
    record = load_project(home) if project_path(home).is_file() else {
        "tracker": "other",
        "project": source.stem or "Portfolio",
        "name": source.stem or "Portfolio",
    }
    if name:
        record["name"] = name
    elif not record.get("name"):
        record["name"] = source.stem or "Portfolio"
    record["profile"] = profile
    record["imported"] = dest.name
    save_project(home, record)
    return record


def default_transport(method: str, url: str, headers: dict[str, str], body: bytes | None) -> dict:
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raise LinkError(f"The tracker returned HTTP {exc.code}.") from exc
    except urllib.error.URLError as exc:
        raise LinkError(f"The tracker could not be reached: {exc.reason}.") from exc
    try:
        return json.loads(payload)
    except json.JSONDecodeError as exc:
        raise LinkError("The tracker returned a response that is not JSON.") from exc


def _basic(user: str, secret: str) -> str:
    return "Basic " + b64encode(f"{user}:{secret}".encode()).decode("ascii")


def fetch_jira(site: str, project_key: str, email: str, token: str, transport=None) -> list[list[str]]:
    transport = default_transport if transport is None else transport
    headers = {
        "Authorization": _basic(email, token),
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    rows: list[list[str]] = []
    page = ""
    while len(rows) < MAX_ITEMS:
        safe_key = project_key.replace("\\", "\\\\").replace('"', '\\"')
        body = {
            "jql": f'project = "{safe_key}" ORDER BY key',
            "maxResults": 100,
            "fields": JIRA_FIELDS,
        }
        if page:
            body["nextPageToken"] = page
        payload = transport(
            "POST",
            site.rstrip("/") + "/rest/api/3/search/jql",
            headers,
            json.dumps(body).encode("utf-8"),
        )
        for issue in payload.get("issues") or []:
            fields = issue.get("fields") or {}
            project = fields.get("project") or {}
            status = fields.get("status") or {}
            priority = fields.get("priority") or {}
            issue_type = fields.get("issuetype") or {}
            parent = fields.get("parent") or {}
            rows.append(
                [
                    str(issue.get("key") or ""),
                    str(project.get("key") or project_key),
                    str(project.get("name") or project_key),
                    str(issue_type.get("name") or ""),
                    str(fields.get("summary") or ""),
                    str(status.get("name") or ""),
                    str(priority.get("name") or ""),
                    _person(fields.get("assignee")),
                    _day(fields.get("created")),
                    _day(fields.get("updated")),
                    _day(fields.get("duedate")),
                    str(parent.get("key") or ""),
                    _adf(fields.get("description"))[:500],
                ]
            )
            if len(rows) >= MAX_ITEMS:
                break
        page = str(payload.get("nextPageToken") or "")
        if not page:
            break
    return rows


def fetch_ado(org: str, project_key: str, token: str, transport=None) -> list[list[str]]:
    transport = default_transport if transport is None else transport
    headers = {
        "Authorization": _basic("", token),
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    safe_project = project_key.replace("'", "''")
    quoted = urllib.parse.quote(project_key)
    base = org.rstrip("/") + "/" + quoted
    wiql = transport(
        "POST",
        base + "/_apis/wit/wiql?api-version=7.1",
        headers,
        json.dumps({"query": f"SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = '{safe_project}'"}).encode(),
    )
    identifiers = [int(item["id"]) for item in (wiql.get("workItems") or [])][:MAX_ITEMS]
    rows: list[list[str]] = []
    for start in range(0, len(identifiers), 200):
        chunk = identifiers[start : start + 200]
        payload = transport(
            "POST",
            base + "/_apis/wit/workitemsbatch?api-version=7.1",
            headers,
            json.dumps({"ids": chunk, "fields": ADO_FIELDS}).encode("utf-8"),
        )
        for item in payload.get("value") or []:
            fields = item.get("fields") or {}
            rows.append(
                [
                    str(item.get("id") or ""),
                    str(fields.get("System.TeamProject") or project_key),
                    str(fields.get("System.AreaPath") or ""),
                    str(fields.get("System.WorkItemType") or ""),
                    str(fields.get("System.Title") or ""),
                    str(fields.get("System.State") or ""),
                    "" if fields.get("Microsoft.VSTS.Common.Priority") is None else str(fields.get("Microsoft.VSTS.Common.Priority")),
                    _person(fields.get("System.AssignedTo")),
                    _day(fields.get("System.CreatedDate")),
                    _day(fields.get("System.ChangedDate")),
                    _day(fields.get("Microsoft.VSTS.Scheduling.DueDate")),
                    "" if fields.get("System.Parent") is None else str(fields.get("System.Parent")),
                    _adf(fields.get("System.Description"))[:500],
                ]
            )
    return rows


JIRA_HEADERS = [
    "Issue key",
    "Project key",
    "Project name",
    "Issue Type",
    "Summary",
    "Status",
    "Priority",
    "Assignee",
    "Created",
    "Updated",
    "Due date",
    "Parent",
    "Comment",
]
ADO_HEADERS = [
    "ID",
    "Team Project",
    "Area Path",
    "Work Item Type",
    "Title",
    "State",
    "Priority",
    "Assigned To",
    "Created Date",
    "Changed Date",
    "Due Date",
    "Parent",
    "Description",
]


def pull(home: Path, transport=None) -> Path:
    transport = default_transport if transport is None else transport
    record = load_project(home)
    tracker = record.get("tracker")
    directory = state_dir(home)
    directory.mkdir(parents=True, exist_ok=True)
    dest = directory / "incoming.csv"
    if tracker == "jira":
        email = os.environ.get("JIRA_EMAIL", "").strip()
        token = os.environ.get("JIRA_API_TOKEN", "").strip()
        if not email or not token:
            raise LinkError("Set JIRA_EMAIL and JIRA_API_TOKEN, or run import with a CSV. The token is not stored.")
        rows = fetch_jira(record["site"], record["project"], email, token, transport)
        headers = JIRA_HEADERS
    elif tracker == "ado":
        token = (os.environ.get("ADO_PAT") or os.environ.get("AZURE_DEVOPS_EXT_PAT") or "").strip()
        if not token:
            raise LinkError("Set ADO_PAT, or run import with a CSV. The token is not stored.")
        rows = fetch_ado(record["org"], record["project"], token, transport)
        headers = ADO_HEADERS
    else:
        raise LinkError("This tracker has no live read. Run import with a CSV.")
    if not rows:
        raise LinkError("The project query returned no work items.")
    _write_rows(dest, headers, rows)
    return dest


def report(home: Path, as_of: str | None, output: Path | None) -> dict:
    record = load_project(home)
    source = state_dir(home) / "work_items.csv"
    if not source.is_file():
        raise LinkError("Import work items before the report. Run import issues.csv")
    previous_path = state_dir(home) / "previous_work_items.csv"
    previous = previous_path if previous_path.is_file() else None
    profile = record.get("profile") or None
    if profile not in extract.PROFILES:
        profile = None
    brief = pipeline.brief_from_csv(
        source,
        record.get("name") or record.get("project") or "Portfolio",
        as_of or pipeline.date.today().isoformat(),
        previous,
        profile,
        None,
    )
    pipeline.write_brief(brief, output or (home / "out"))
    return brief


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="run", description="Connect a project and write the delivery brief.")
    parser.add_argument("--home", type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest="command")

    connect_parser = sub.add_parser("connect")
    connect_parser.add_argument("tracker", choices=TRACKERS)
    connect_parser.add_argument("--site", default="")
    connect_parser.add_argument("--org", default="")
    connect_parser.add_argument("--project", required=True)
    connect_parser.add_argument("--name", default="")

    import_parser = sub.add_parser("import")
    import_parser.add_argument("file", nargs="?", type=Path)
    import_parser.add_argument("--previous", type=Path)
    import_parser.add_argument("--name", default="")

    report_parser = sub.add_parser("report")
    report_parser.add_argument("--as-of", default="")

    sub.add_parser("help")
    args = parser.parse_args(argv)
    home = args.home
    try:
        if args.command in {None, "help"}:
            print(USAGE, end="")
            return 0
        if args.command == "connect":
            record = connect(home, args.tracker, args.project, args.name, args.site, args.org)
            print(f"Connected {record['tracker']} project {record['project']}.")
            if record["tracker"] == "other":
                print("Next: run import issues.csv")
            else:
                print("Next: run import issues.csv, or run import to read the project.")
            return 0
        if args.command == "import":
            if args.file is None:
                source = pull(home)
            else:
                if not args.file.is_file():
                    raise LinkError(f"CSV not found: {args.file}")
                source = args.file
            record = remember_import(home, source, args.previous, args.name or None)
            print(f"Imported work items for {record['name']}.")
            print("Next: run report")
            return 0
        brief = report(home, args.as_of or None, None)
    except (LinkError, pipeline.InputError, json.JSONDecodeError, OSError) as exc:
        print(str(exc), file=__import__("sys").stderr)
        return 1
    if not brief["quality"]["traceable"]:
        print("Brief has a finding without evidence.", file=__import__("sys").stderr)
        return 1
    print(
        f"{brief['portfolio']}: {brief['source_profile']}, {len(brief['top_risks'])} top risks, "
        f"{len(brief['set_aside'])} set aside, result {brief['result_id']}, approval {brief['approval']}"
    )
    return 0
