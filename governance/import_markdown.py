"""List every public markdown file, plus the Orbit paths named from those files.

Agent directives already in the archive are left as they are. Newly found
markdown is stored as kind `doc` unless the path is an agent prompt or contract.
AlexTouvras/Orbit returns 404 to this credential, so that repo is recorded
from the paths public files already name.
"""

from __future__ import annotations

import base64
import hashlib
import json
import re
import subprocess
from pathlib import Path

import catalog

OWNER = "AlexTouvras"
ORBIT_REPO = "AlexTouvras/Orbit"
ORBIT_ID = "orbit-private"

CONTRACT_MARKERS = (
    "automation-contract",
    "cursor-friday-automation",
    "weekly-refresh-prompt",
    "weekly-review-prompt",
    "holdings_automation",
    "automation_contract",
    "/prompt.md",
)


def _gh_json(args: list[str]):
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "gh failed")
    return json.loads(result.stdout)


def _repos() -> list[str]:
    rows = _gh_json(["repo", "list", OWNER, "--limit", "100", "--json", "name"])
    return [row["name"] for row in rows]


def _tree(repo: str) -> list[str]:
    result = subprocess.run(
        ["gh", "api", f"repos/{repo}/git/trees/HEAD?recursive=1", "--jq", ".tree[].path"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"skip tree {repo}")
        return []
    return [line for line in result.stdout.splitlines() if line]


def _fetch(repo: str, path: str) -> str:
    result = subprocess.run(
        ["gh", "api", f"repos/{repo}/contents/{path}", "--jq", ".content"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"fetch failed {repo}/{path}")
    return base64.b64decode(result.stdout.strip()).decode("utf-8")


def _existing() -> set[tuple[str, str]]:
    found: set[tuple[str, str]] = set()
    root = catalog.archive_root()
    if not root.is_dir():
        return found
    for meta_path in root.glob("*/meta.json"):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        found.add((meta.get("repo", ""), meta.get("source_path", "")))
    return found


def _title(body: str, path: str) -> str:
    _frontmatter, rest = catalog.parse_frontmatter(body)
    for line in rest.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(">") or stripped.startswith("|"):
            continue
        heading = stripped.lstrip("#").strip()
        if heading and not heading.startswith("<!--"):
            return heading[:90]
    return Path(path).stem.replace("_", " ").replace("-", " ")


def _topics(repo: str, path: str, kind: str) -> list[str]:
    topics: list[str] = []
    repo_name = repo.split("/")[-1].lower()
    aliases = {
        "powerbi-portfolio": "powerbi",
        "agentic-ai-field-card": "field-card",
        "data-analytics-field-card": "field-card",
        "technology-delivery-field-card": "field-card",
        "projectbrain": "projectbrain",
    }
    topics.append(aliases.get(repo_name, repo_name))
    lower = path.lower()
    if ".state/" in lower or lower.startswith(".state/"):
        topics.append("state")
    if "architecture" in lower:
        topics.append("architecture")
    if lower.endswith("readme.md"):
        topics.append("readme")
    if "charter" in lower:
        topics.append("charter")
    if "/_brief/" in lower:
        topics.append("brief")
    if "decision-spec" in lower:
        topics.append("decisions")
    if any(marker in lower for marker in ("automat", "prompt")):
        topics.append("automation")
    if kind == "agents":
        topics.append("agents")
    if kind == "contract":
        topics.append("governance")
    cleaned: list[str] = []
    for topic in topics:
        slug = re.sub(r"[^a-z0-9-]+", "-", topic).strip("-")
        if slug and slug not in cleaned:
            cleaned.append(slug)
    return cleaned


def _classify(path: str) -> tuple[str, str]:
    name = path.rsplit("/", 1)[-1]
    lower = path.lower()
    if name in {"AGENTS.md", "CLAUDE.md"}:
        return "agents", "always"
    if "/.cursor/rules/" in f"/{lower}" and lower.endswith(".mdc"):
        return "rule", "always"
    if name == "hooks.json":
        return "hook", "session"
    if "user_rules" in lower:
        return "user-rule", "user"
    if "/automations/" in lower and lower.endswith(".json"):
        return "automation", "schedule"
    if any(marker in lower for marker in CONTRACT_MARKERS):
        return "contract", "on-run"
    return "doc", "manual"


def _make_id(repo: str, path: str) -> str:
    repo_slug = re.sub(r"[^a-z0-9]+", "-", repo.split("/")[-1].lower()).strip("-")
    stem = re.sub(r"\.(md|mdc|json|txt)$", "", path, flags=re.IGNORECASE)
    path_slug = re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")
    base = f"{repo_slug}-{path_slug}".strip("-")
    if len(base) > 81:
        digest = hashlib.sha1(f"{repo}/{path}".encode()).hexdigest()[:8]
        base = base[:72].rstrip("-") + "-" + digest
    if not catalog.ID_RE.match(base):
        base = "doc-" + hashlib.sha1(f"{repo}/{path}".encode()).hexdigest()[:16]
    root = catalog.archive_root()
    candidate = base
    suffix = 2
    while (root / candidate).exists():
        candidate = f"{base[:70].rstrip('-')}-{suffix}"
        suffix += 1
    return candidate


def _write(repo: str, path: str, body: str, kind: str, activation: str, extra_topics: list[str] | None = None) -> None:
    if kind == "rule":
        frontmatter, _rest = catalog.parse_frontmatter(body)
        activation = catalog.activation_from_frontmatter(kind, frontmatter)
    topics = _topics(repo, path, kind)
    for topic in extra_topics or []:
        if topic not in topics:
            topics.append(topic)
    catalog.write_imported_item(
        {
            "id": _make_id(repo, path),
            "title": _title(body, path),
            "kind": kind,
            "repo": repo,
            "topics": topics,
            "activation": activation,
            "source_path": path,
            "source_url": f"https://github.com/{repo}/blob/main/{path}",
            "imported_on": "2026-09-30",
        },
        body,
    )


def _orbit_entry() -> None:
    if (catalog.archive_root() / ORBIT_ID).exists():
        print("keep", ORBIT_ID)
        return
    body = """# AlexTouvras/Orbit

GitHub returns 404 for this repository with the credential that built the archive, so its files are not copied here. Public repositories already name it.

## What points at Orbit

- `storytelling/.github/workflows/notify-orbit.yml` dispatches `storytelling-sync` to `AlexTouvras/Orbit` on push to `main`.
- `technology-delivery-field-card` stores its automation backup at `website/.cursor/automations/delivery-field-card-weekly-content-pass.json` inside Orbit.
- `data-analytics-field-card` stores its automation backup at `website/.cursor/automations/analytics-field-card-weekly-content-pass.json` inside Orbit.
- `agentic-ai-field-card` keeps the Friday 18:00 review automation on Orbit, and its signing secret must match Orbit / Vercel.
- ProjectBrain syncs architecture diagrams from Orbit's `website/` folder.
- The storytelling rule treats the local Orbit checkout as a separate product: portfolio teaser, then `/stories`.

Grant this archive read access to `AlexTouvras/Orbit` to import its rules, skills, and markdown.
"""
    folder_id = ORBIT_ID
    catalog.write_imported_item(
        {
            "id": folder_id,
            "title": "Orbit (private to this archive)",
            "kind": "doc",
            "repo": ORBIT_REPO,
            "topics": ["orbit", "private", "website"],
            "activation": "manual",
            "description": "Orbit is not readable with this credential. Known paths only.",
            "source_path": "",
            "source_url": "https://github.com/AlexTouvras/Orbit",
            "imported_on": "2026-09-30",
        },
        body,
    )
    print("add", folder_id)


def main() -> None:
    catalog.archive_root().mkdir(parents=True, exist_ok=True)
    seen = _existing()
    added = 0
    for name in _repos():
        repo = f"{OWNER}/{name}"
        for path in _tree(repo):
            lower = path.lower()
            if not lower.endswith(".md"):
                continue
            if (repo, path) in seen:
                print("keep", repo, path)
                continue
            try:
                body = _fetch(repo, path)
            except (RuntimeError, UnicodeDecodeError) as exc:
                print("fail", repo, path, exc)
                continue
            if len(body) > catalog.MAX_BODY_CHARS:
                print("skip large", repo, path)
                continue
            kind, activation = _classify(path)
            _write(repo, path, body, kind, activation)
            seen.add((repo, path))
            added += 1
            print("add", kind, repo, path)
    _orbit_entry()
    print(f"added {added}")


if __name__ == "__main__":
    main()
