"""Import Orbit and ravens .cursor directives, then categorise similar docs.

Files that do not match a shared pattern stay kind `doc`.
"""

from __future__ import annotations

import base64
import json
import shutil
import subprocess
from pathlib import Path

import catalog

TARGETS = ("AlexTouvras/Orbit", "AlexTouvras/ravens")


def _fetch(repo: str, path: str) -> str:
    result = subprocess.run(
        ["gh", "api", f"repos/{repo}/contents/{path}", "--jq", ".content"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"fetch failed {repo}/{path}")
    return base64.b64decode(result.stdout.strip()).decode("utf-8")


def _tree(repo: str) -> list[str]:
    result = subprocess.run(
        ["gh", "api", f"repos/{repo}/git/trees/HEAD?recursive=1", "--jq", ".tree[].path"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"tree failed {repo}")
    return [line for line in result.stdout.splitlines() if line]


def _wanted(path: str) -> bool:
    lower = path.lower()
    name = path.rsplit("/", 1)[-1]
    if lower.startswith(".cursor/rules/") and lower.endswith(".mdc"):
        return True
    if lower.startswith(".cursor/skills/") and lower.endswith(".md"):
        return True
    if lower.startswith(".cursor/automations/") and lower.endswith(".json"):
        return True
    if lower == ".cursor/hooks.json":
        return True
    if name in {"AGENTS.md", "CLAUDE.md", "AGENT_RULES.md"}:
        return True
    if lower.startswith("agents/") and lower.endswith(".md"):
        return True
    if lower.startswith(".state/") and lower.endswith(".md"):
        return True
    if lower in {"docs/automation-contract.md", "docs/essay-voice.md", "docs/runbook.md"}:
        return True
    if lower.startswith("docs/contracts/") and lower.endswith(".md"):
        return True
    if lower.startswith("docs/product/") and name == "AGENT_RULES.md":
        return True
    return False


def _existing() -> set[tuple[str, str]]:
    found: set[tuple[str, str]] = set()
    root = catalog.archive_root()
    if not root.is_dir():
        return found
    for meta_path in root.glob("*/meta.json"):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        found.add((meta.get("repo", ""), meta.get("source_path", "")))
    return found


def _kind_for(path: str, body: str) -> tuple[str, str]:
    suggested = catalog.suggest_category(path, "doc")
    if suggested:
        return suggested
    lower = path.lower()
    if lower.endswith(".mdc") and "/.cursor/rules/" in f"/{lower}":
        frontmatter, _rest = catalog.parse_frontmatter(body)
        return "rule", catalog.activation_from_frontmatter("rule", frontmatter)
    if "/automations/" in lower and lower.endswith(".json"):
        return "automation", "schedule"
    if lower.endswith("hooks.json"):
        return "hook", "session"
    return "doc", "manual"


def _title(body: str, path: str) -> str:
    _frontmatter, rest = catalog.parse_frontmatter(body)
    for line in rest.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()[:90]
    if path.endswith(".json"):
        try:
            return str(json.loads(body).get("name") or Path(path).stem)[:90]
        except json.JSONDecodeError:
            pass
    return Path(path).stem.replace("-", " ").replace("_", " ")


def _topics(repo: str, path: str, kind: str) -> list[str]:
    topics = [repo.split("/")[-1].lower(), kind]
    lower = path.lower()
    for token, topic in (
        ("state-management", "state"),
        ("architecture", "architecture"),
        ("essay", "essay"),
        ("weekly-write", "writing"),
        ("visual-storytelling", "storytelling"),
        ("product-kit", "product"),
        ("projectbrain", "portfolio"),
        ("huginn", "huginn"),
        ("muninn", "muninn"),
        ("heimdall", "heimdall"),
        ("automation", "automation"),
        ("skill", "skill"),
    ):
        if token in lower and topic not in topics:
            topics.append(topic)
    return topics


def _new_id(repo: str, path: str) -> str:
    import import_markdown

    return import_markdown._make_id(repo, path)


def import_cursor() -> int:
    seen = _existing()
    added = 0
    for repo in TARGETS:
        for path in _tree(repo):
            if not _wanted(path) or (repo, path) in seen:
                continue
            body = _fetch(repo, path)
            kind, activation = _kind_for(path, body)
            catalog.write_imported_item(
                {
                    "id": _new_id(repo, path),
                    "title": _title(body, path),
                    "kind": kind,
                    "repo": repo,
                    "topics": _topics(repo, path, kind),
                    "activation": activation,
                    "source_path": path,
                    "source_url": f"https://github.com/{repo}/blob/main/{path}",
                    "imported_on": "2026-09-30",
                },
                body,
            )
            seen.add((repo, path))
            added += 1
            print("add", kind, activation, repo, path)
    return added


def recategorise() -> int:
    changed = 0
    root = catalog.archive_root()
    for meta_path in sorted(root.glob("*/meta.json")):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        suggested = catalog.suggest_category(meta.get("source_path", ""), meta.get("kind", "doc"))
        if suggested is None:
            continue
        kind, activation = suggested
        topics = [topic for topic in (meta.get("topics") or []) if topic != "doc" or kind == "doc"]
        if kind not in topics:
            topics.append(kind)
        if meta.get("kind") == kind and meta.get("activation") == activation and topics == meta.get("topics"):
            continue
        meta["kind"] = kind
        meta["activation"] = activation
        meta["topics"] = topics
        meta["updated_at"] = catalog._now()
        meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        changed += 1
        print("move", meta["id"], "->", kind)
    return changed


def strip_stale_doc_topic() -> int:
    changed = 0
    for meta_path in catalog.archive_root().glob("*/meta.json"):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        topics = meta.get("topics") or []
        if meta.get("kind") == "doc" or "doc" not in topics:
            continue
        meta["topics"] = [topic for topic in topics if topic != "doc"]
        meta["updated_at"] = catalog._now()
        meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        changed += 1
    print("stripped doc topic", changed)
    return changed


def drop_orbit_stub() -> None:
    stub = catalog.archive_root() / "orbit-private"
    if stub.is_dir():
        shutil.rmtree(stub)
        print("removed orbit-private")


def main() -> None:
    drop_orbit_stub()
    added = import_cursor()
    moved = recategorise()
    strip_stale_doc_topic()
    print(f"added {added} recategorised {moved}")


if __name__ == "__main__":
    main()
