#!/usr/bin/env python3
"""Write the read-only snapshot Orbit Studio serves at /studio/directives.

The archive in this repository stays the edit/save copy. The JSON file is a
published view. Saving here does not update Orbit until this snapshot is
copied to data/directive-archive.json in AlexTouvras/Orbit and that site
redeploys.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from catalog import ALWAYS_ON_TOKEN_CAP, catalog, load_item

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "governance" / "orbit-studio" / "data" / "directive-archive.json"


def build_snapshot(*, source_branch: str, published_at: str) -> dict:
    data = catalog()
    items = []
    for summary in data["items"]:
        full = load_item(summary["id"], include_version_bodies=False)
        items.append(
            {
                "id": summary["id"],
                "title": summary["title"],
                "kind": summary["kind"],
                "repo": summary["repo"],
                "topics": summary["topics"],
                "activation": summary["activation"],
                "tokens": summary["tokens"],
                "sourcePath": summary.get("source_path", ""),
                "sourceUrl": summary.get("source_url", ""),
                "body": full["body"],
            }
        )
    return {
        "sourceRepo": "AlexTouvras/AlexTouvras",
        "sourceBranch": source_branch,
        "publishedAt": published_at,
        "alwaysOnTokenCap": ALWAYS_ON_TOKEN_CAP,
        "items": items,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Path to write")
    parser.add_argument("--branch", default="cursor/directive-archive-5895")
    parser.add_argument("--published-at", default=date.today().isoformat())
    args = parser.parse_args()
    payload = build_snapshot(source_branch=args.branch, published_at=args.published_at)
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    with open(args.out, "w", encoding="utf-8") as handle:
        handle.write(text)
    print(f"wrote {len(payload['items'])} items to {args.out}")


if __name__ == "__main__":
    main()
