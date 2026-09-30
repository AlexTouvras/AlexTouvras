"""Archive of skills, rules, and automation directives.

The archive is the source of truth for review. Saving here does not publish
back to the originating repository or to Cursor Automations.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_ARCHIVE = ROOT / "archive"

ALWAYS_ON_TOKEN_CAP = 1000
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,80}$")
KINDS = (
    "rule",
    "skill",
    "automation",
    "agents",
    "contract",
    "state",
    "architecture",
    "charter",
    "brief",
    "spec",
    "schema",
    "runbook",
    "discovery",
    "source",
    "log",
    "readme",
    "user-rule",
    "hook",
    "doc",
)
ACTIVATIONS = (
    "always",
    "glob",
    "agent",
    "manual",
    "schedule",
    "session",
    "user",
    "on-run",
)
ALWAYS_ON = {"always"}
MAX_BODY_CHARS = 200_000


def archive_root() -> Path:
    override = os.environ.get("GOVERNANCE_ARCHIVE")
    return Path(override) if override else DEFAULT_ARCHIVE


def estimate_tokens(text: str) -> int:
    return max(1, (len(text) + 3) // 4) if text else 0


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _version_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[3:end].strip("\n")
    body = text[end + 4 :]
    if body.startswith("\n"):
        body = body[1:]
    fields: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.strip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip("'\"")
    return fields, body


def activation_from_frontmatter(kind: str, frontmatter: dict[str, str]) -> str:
    if kind == "automation":
        return "schedule"
    if kind == "hook":
        return "session"
    if kind == "user-rule":
        return "user"
    if kind == "contract":
        return "on-run"
    if kind in {
        "doc",
        "readme",
        "state",
        "architecture",
        "charter",
        "brief",
        "discovery",
        "spec",
        "source",
        "log",
        "schema",
        "runbook",
    }:
        return "manual"
    if kind == "skill":
        return "agent"
    if kind == "agents":
        return "always"
    always = frontmatter.get("alwaysApply", "").lower()
    globs = frontmatter.get("globs", "")
    description = frontmatter.get("description", "")
    if always == "true":
        return "always"
    if globs:
        return "glob"
    if description:
        return "agent"
    return "manual"


_KEEP_KINDS = {"rule", "skill", "automation", "hook", "user-rule", "agents", "contract"}


def suggest_category(source_path: str, current_kind: str) -> tuple[str, str] | None:
    """Upgrade an uncategorised file to a shared kind. None means leave it."""
    if current_kind in _KEEP_KINDS:
        return None
    path = (source_path or "").replace("\\", "/").lstrip("/")
    if not path:
        return None
    name = path.rsplit("/", 1)[-1]
    lower = f"/{path.lower()}"
    if name in {"AGENTS.md", "CLAUDE.md"}:
        return "agents", "always"
    if name == "AGENT_RULES.md":
        return "agents", "manual"
    if name.endswith(".md") and "/agents/" in lower:
        return "agents", "agent"
    if (
        name == "AUTOMATION_CONTRACT.md"
        or "automation-contract" in lower
        or "cursor-friday" in lower
        or "weekly-refresh-prompt" in lower
        or "weekly-review-prompt" in lower
        or lower.endswith("holdings_automation.md")
        or lower.endswith("/prompt.md")
    ):
        return "contract", "on-run"
    if name in {"CURRENT_STATE.md", "BACKLOG.md"} or "/.state/" in lower:
        return "state", "manual"
    if name.lower() == "readme.md":
        return "readme", "manual"
    if "charter" in lower:
        return "charter", "manual"
    if name == "ARCHITECTURE.md" or "/architecture/" in lower:
        return "architecture", "manual"
    if "/_brief/" in lower or "theme-review" in lower:
        return "brief", "manual"
    if lower.endswith("/essay-voice.md"):
        return "skill", "manual"
    if "discovery-report" in lower or name.lower().startswith("judgment"):
        return "discovery", "manual"
    if "/decision-specs/" in lower or "spec" in name.lower():
        return "spec", "manual"
    if name in {"SOURCE.md", "DQ_NOTES.md", "DATASETS.md", "analysis_case_summary.md"}:
        return "source", "manual"
    if name == "AGENT_LOG.md":
        return "log", "manual"
    if name.lower() == "runbook.md":
        return "runbook", "manual"
    if "/docs/contracts/" in lower:
        return "schema", "manual"
    if "/.cursor/skills/" in lower:
        return ("skill", "agent") if name == "SKILL.md" else ("skill", "manual")
    return None


def _sync_frontmatter(body: str, activation: str, kind: str) -> str:
    if kind not in {"rule", "skill"}:
        return body
    frontmatter, rest = parse_frontmatter(body)
    if kind == "skill":
        return body
    frontmatter["alwaysApply"] = "true" if activation == "always" else "false"
    if activation != "glob":
        frontmatter.pop("globs", None)
    elif "globs" not in frontmatter:
        frontmatter["globs"] = "**/*"
    lines = ["---"]
    for key in ("description", "alwaysApply", "globs", "name"):
        if key in frontmatter and frontmatter[key] != "":
            lines.append(f"{key}: {frontmatter[key]}")
    for key, value in frontmatter.items():
        if key not in {"description", "alwaysApply", "globs", "name"} and value != "":
            lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + rest.lstrip("\n")


def _check_id(item_id: str) -> str:
    if not ID_RE.match(item_id or ""):
        raise ValueError("id must be a lowercase slug")
    return item_id


def _item_dir(item_id: str) -> Path:
    return archive_root() / _check_id(item_id)


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def list_ids() -> list[str]:
    root = archive_root()
    if not root.is_dir():
        return []
    return sorted(
        path.name
        for path in root.iterdir()
        if path.is_dir() and (path / "meta.json").is_file() and (path / "body").is_file()
    )


def _version_log(item_dir: Path) -> list[dict]:
    path = item_dir / "versions" / "log.json"
    if not path.is_file():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else []


def load_item(item_id: str, *, include_version_bodies: bool = True) -> dict:
    folder = _item_dir(item_id)
    meta_path = folder / "meta.json"
    body_path = folder / "body"
    if not meta_path.is_file() or not body_path.is_file():
        raise FileNotFoundError(item_id)
    meta = _read_json(meta_path)
    body = body_path.read_text(encoding="utf-8")
    versions = []
    for entry in _version_log(folder):
        record = dict(entry)
        if include_version_bodies:
            version_path = folder / "versions" / entry["file"]
            record["body"] = version_path.read_text(encoding="utf-8") if version_path.is_file() else ""
        versions.append(record)
    frontmatter, _rest = parse_frontmatter(body)
    return {
        **meta,
        "body": body,
        "tokens": estimate_tokens(body),
        "lines": body.count("\n") + (0 if body.endswith("\n") or body == "" else 1),
        "content_hash": content_hash(body),
        "frontmatter": frontmatter,
        "versions": versions,
    }


def _summary(item: dict, copies: dict[str, int]) -> dict:
    return {
        "id": item["id"],
        "title": item["title"],
        "kind": item["kind"],
        "repo": item["repo"],
        "topics": item["topics"],
        "activation": item["activation"],
        "tokens": item["tokens"],
        "lines": item["lines"],
        "source_path": item.get("source_path", ""),
        "source_url": item.get("source_url", ""),
        "description": item.get("description", ""),
        "content_hash": item["content_hash"],
        "identical_copies": copies.get(item["content_hash"], 1),
        "updated_at": item.get("updated_at", ""),
    }


def _repo_budgets(items: list[dict]) -> list[dict]:
    buckets: dict[str, dict] = {}
    for item in items:
        repo = item["repo"] or "unassigned"
        bucket = buckets.setdefault(
            repo,
            {"repo": repo, "always_on_tokens": 0, "items": 0, "always_on_items": 0},
        )
        bucket["items"] += 1
        if item["activation"] in ALWAYS_ON:
            bucket["always_on_tokens"] += item["tokens"]
            bucket["always_on_items"] += 1
    budgets = []
    for bucket in buckets.values():
        bucket["cap"] = ALWAYS_ON_TOKEN_CAP
        bucket["over_budget"] = bucket["always_on_tokens"] > ALWAYS_ON_TOKEN_CAP
        budgets.append(bucket)
    return sorted(budgets, key=lambda row: (-row["always_on_tokens"], row["repo"]))


def catalog() -> dict:
    items = [load_item(item_id, include_version_bodies=False) for item_id in list_ids()]
    copies: dict[str, int] = {}
    for item in items:
        copies[item["content_hash"]] = copies.get(item["content_hash"], 0) + 1
    summaries = [_summary(item, copies) for item in items]
    topics = sorted({topic for item in summaries for topic in item["topics"]})
    repos = sorted({item["repo"] for item in summaries if item["repo"]})
    return {
        "cap": ALWAYS_ON_TOKEN_CAP,
        "items": summaries,
        "budgets": _repo_budgets(summaries),
        "topics": topics,
        "repos": repos,
        "kinds": list(KINDS),
        "activations": list(ACTIVATIONS),
        "gaps": [
            "Orbit rules name personal skills that are not files in these repositories: orbit-essay, anti-ai-slop-writing, and fable-method.",
            "Files that do not match a shared pattern stay kind doc.",
            "Cursor User Rules live in Customize, not in git. The archived user-rule text is the ProjectBrain template.",
            "Saving an automation prompt updates this archive. It does not change the live Cursor Automation.",
        ],
    }


def _normalize_topics(topics) -> list[str]:
    if isinstance(topics, str):
        parts = re.split(r"[,\s]+", topics)
    elif isinstance(topics, list):
        parts = [str(part) for part in topics]
    else:
        parts = []
    cleaned = []
    for part in parts:
        slug = re.sub(r"[^a-z0-9-]+", "-", part.strip().lower()).strip("-")
        if slug and slug not in cleaned:
            cleaned.append(slug)
    return cleaned


def _validate_fields(fields: dict, *, require_body: bool = True) -> dict:
    kind = fields.get("kind", "")
    activation = fields.get("activation", "")
    title = str(fields.get("title", "")).strip()
    repo = str(fields.get("repo", "")).strip()
    body = fields.get("body", "")
    if kind not in KINDS:
        raise ValueError("kind is not recognized")
    if activation not in ACTIVATIONS:
        raise ValueError("activation is not recognized")
    if not title:
        raise ValueError("title is required")
    if not repo:
        raise ValueError("repo is required")
    if require_body and not isinstance(body, str):
        raise ValueError("body is required")
    if isinstance(body, str) and len(body) > MAX_BODY_CHARS:
        raise ValueError("body is too large")
    return {
        "title": title,
        "kind": kind,
        "repo": repo,
        "activation": activation,
        "topics": _normalize_topics(fields.get("topics", [])),
        "body": body if isinstance(body, str) else "",
        "source_path": str(fields.get("source_path", "")).strip(),
    }


def _snapshot(folder: Path, body: str, note: str, meta: dict) -> None:
    versions = folder / "versions"
    versions.mkdir(parents=True, exist_ok=True)
    stamp = _version_stamp()
    filename = f"{stamp}.body"
    # Keep stamps unique if two saves land in the same second.
    counter = 2
    while (versions / filename).exists():
        filename = f"{stamp}-{counter}.body"
        counter += 1
    (versions / filename).write_text(body, encoding="utf-8")
    log = _version_log(folder)
    log.append(
        {
            "id": filename.removesuffix(".body"),
            "file": filename,
            "saved_at": _now(),
            "note": note,
            "tokens": estimate_tokens(body),
            "title": meta.get("title", ""),
            "activation": meta.get("activation", ""),
        }
    )
    _write_json(versions / "log.json", log)


def _description_from_body(body: str, title: str) -> str:
    frontmatter, rest = parse_frontmatter(body)
    description = frontmatter.get("description", "")
    if description and description not in {">", ">-", "|", "|-"}:
        return description
    for line in rest.splitlines():
        stripped = line.strip().lstrip("#").strip()
        if stripped:
            return stripped[:180]
    return title


def save_item(item_id: str, fields: dict, *, note: str = "edit") -> dict:
    folder = _item_dir(item_id)
    if not (folder / "meta.json").is_file():
        raise FileNotFoundError(item_id)
    current = load_item(item_id, include_version_bodies=False)
    incoming = _validate_fields(fields)
    body = _sync_frontmatter(incoming["body"], incoming["activation"], incoming["kind"])
    if body != current["body"]:
        _snapshot(folder, current["body"], note, current)
    meta = _read_json(folder / "meta.json")
    meta.update(
        {
            "title": incoming["title"],
            "kind": incoming["kind"],
            "repo": incoming["repo"],
            "activation": incoming["activation"],
            "topics": incoming["topics"],
            "description": _description_from_body(body, incoming["title"]),
            "updated_at": _now(),
        }
    )
    _write_json(folder / "meta.json", meta)
    (folder / "body").write_text(body, encoding="utf-8")
    saved = load_item(item_id)
    saved["budget"] = _budget_for(saved["repo"])
    return saved


def _budget_for(repo: str) -> dict:
    for row in catalog()["budgets"]:
        if row["repo"] == repo:
            return row
    return {
        "repo": repo,
        "always_on_tokens": 0,
        "items": 0,
        "always_on_items": 0,
        "cap": ALWAYS_ON_TOKEN_CAP,
        "over_budget": False,
    }


def _slug(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:40] or "item"


def create_item(fields: dict) -> dict:
    incoming = _validate_fields(fields)
    repo_slug = _slug(incoming["repo"].split("/")[-1])
    base = _slug(f"{repo_slug}-{incoming['kind']}-{incoming['title']}")[:70]
    item_id = base
    suffix = 2
    root = archive_root()
    root.mkdir(parents=True, exist_ok=True)
    while (root / item_id).exists():
        item_id = f"{base[:70]}-{suffix}"
        suffix += 1
    folder = root / item_id
    folder.mkdir(parents=True)
    body = _sync_frontmatter(incoming["body"], incoming["activation"], incoming["kind"])
    if not body.strip():
        body = _template(incoming["kind"], incoming["title"], incoming["activation"])
        body = _sync_frontmatter(body, incoming["activation"], incoming["kind"])
    now = _now()
    meta = {
        "id": item_id,
        "title": incoming["title"],
        "kind": incoming["kind"],
        "repo": incoming["repo"],
        "topics": incoming["topics"],
        "activation": incoming["activation"],
        "description": _description_from_body(body, incoming["title"]),
        "source_path": incoming["source_path"],
        "source_url": "",
        "origin": "archive",
        "imported_on": now,
        "updated_at": now,
    }
    _write_json(folder / "meta.json", meta)
    (folder / "body").write_text(body, encoding="utf-8")
    _snapshot(folder, body, "created", meta)
    saved = load_item(item_id)
    saved["budget"] = _budget_for(saved["repo"])
    return saved


def _template(kind: str, title: str, activation: str) -> str:
    if kind == "skill":
        name = _slug(title)
        return (
            f"---\nname: {name}\ndescription: Use when {title.lower()} is the task at hand.\n---\n\n"
            f"# {title}\n\n## When to use\n\n- \n\n## Instructions\n\n1. \n"
        )
    if kind == "rule":
        always = "true" if activation == "always" else "false"
        return f"---\ndescription: {title}\nalwaysApply: {always}\n---\n\n# {title}\n\n- \n"
    if kind == "automation":
        return json.dumps(
            {
                "name": title,
                "description": "",
                "workflow": {"triggers": [{"cron": {"cron": "0 9 * * 1"}}], "prompts": [{"prompt": ""}]},
            },
            indent=2,
        ) + "\n"
    return f"# {title}\n\n"


def restore_item(item_id: str, version_id: str) -> dict:
    folder = _item_dir(item_id)
    if not re.fullmatch(r"[0-9TZt-]+", version_id or ""):
        raise ValueError("unknown version")
    version_path = folder / "versions" / f"{version_id}.body"
    entry = next((row for row in _version_log(folder) if row.get("id") == version_id), None)
    if entry is None or not version_path.is_file():
        raise FileNotFoundError(version_id)
    current = load_item(item_id, include_version_bodies=False)
    restored = version_path.read_text(encoding="utf-8")
    if restored != current["body"]:
        _snapshot(folder, current["body"], f"before restore {version_id}", current)
    (folder / "body").write_text(restored, encoding="utf-8")
    meta = _read_json(folder / "meta.json")
    frontmatter, _rest = parse_frontmatter(restored)
    meta["activation"] = entry.get("activation") or activation_from_frontmatter(
        meta.get("kind", "rule"), frontmatter
    )
    meta["description"] = _description_from_body(restored, meta.get("title", item_id))
    meta["updated_at"] = _now()
    _write_json(folder / "meta.json", meta)
    return load_item(item_id)


def write_imported_item(meta: dict, body: str) -> None:
    item_id = _check_id(meta["id"])
    folder = archive_root() / item_id
    folder.mkdir(parents=True, exist_ok=True)
    record = {
        "id": item_id,
        "title": meta["title"],
        "kind": meta["kind"],
        "repo": meta["repo"],
        "topics": meta["topics"],
        "activation": meta["activation"],
        "description": meta.get("description") or _description_from_body(body, meta["title"]),
        "source_path": meta.get("source_path", ""),
        "source_url": meta.get("source_url", ""),
        "origin": "github",
        "imported_on": meta.get("imported_on", "2026-09-30"),
        "updated_at": meta.get("imported_on", "2026-09-30") + "T00:00:00Z",
    }
    _write_json(folder / "meta.json", record)
    (folder / "body").write_text(body, encoding="utf-8")
    versions = folder / "versions"
    versions.mkdir(parents=True, exist_ok=True)
    (versions / "20260930T000000Z.body").write_text(body, encoding="utf-8")
    _write_json(
        versions / "log.json",
        [
            {
                "id": "20260930T000000Z",
                "file": "20260930T000000Z.body",
                "saved_at": record["updated_at"],
                "note": "imported from GitHub",
                "tokens": estimate_tokens(body),
                "title": record["title"],
                "activation": record["activation"],
            }
        ],
    )
