"""Import a local harvest of public GitHub files into the archive.

The harvest directory mirrors repository names, for example
`harvest/pixels/.cursor/rules/00-state-management.mdc`.
Re-running overwrites archive bodies and resets version history for those ids.
"""

from __future__ import annotations

import sys
from pathlib import Path

import catalog

ITEMS = [
    {
        "id": "pixels-state-management",
        "title": "State management",
        "kind": "rule",
        "repo": "AlexTouvras/pixels",
        "topics": ["state", "context"],
        "activation": "always",
        "source_path": ".cursor/rules/00-state-management.mdc",
        "local": "pixels/.cursor/rules/00-state-management.mdc",
    },
    {
        "id": "pixels-agents",
        "title": "Next.js agent rules",
        "kind": "agents",
        "repo": "AlexTouvras/pixels",
        "topics": ["nextjs", "generated"],
        "activation": "always",
        "source_path": "AGENTS.md",
        "local": "pixels/AGENTS.md",
        "description": "Generated Next.js agent instructions",
    },
    {
        "id": "projectbrain-portfolio",
        "title": "ProjectBrain portfolio",
        "kind": "rule",
        "repo": "AlexTouvras/ProjectBrain",
        "topics": ["portfolio", "memory", "mcp"],
        "activation": "always",
        "source_path": ".cursor/rules/projectbrain-portfolio.mdc",
        "local": "ProjectBrain/.cursor/rules/projectbrain-portfolio.mdc",
    },
    {
        "id": "projectbrain-hub",
        "title": "ProjectBrain hub",
        "kind": "rule",
        "repo": "AlexTouvras/ProjectBrain",
        "topics": ["portfolio", "projectbrain"],
        "activation": "always",
        "source_path": ".cursor/rules/projectbrain.mdc",
        "local": "ProjectBrain/.cursor/rules/projectbrain.mdc",
    },
    {
        "id": "projectbrain-architecture-docs",
        "title": "Architecture documentation",
        "kind": "rule",
        "repo": "AlexTouvras/ProjectBrain",
        "topics": ["architecture", "docs"],
        "activation": "always",
        "source_path": ".cursor/rules/architecture-docs.mdc",
        "local": "ProjectBrain/.cursor/rules/architecture-docs.mdc",
    },
    {
        "id": "projectbrain-hooks",
        "title": "ProjectBrain session hooks",
        "kind": "hook",
        "repo": "AlexTouvras/ProjectBrain",
        "topics": ["projectbrain", "session"],
        "activation": "session",
        "source_path": ".cursor/hooks.json",
        "local": "ProjectBrain/.cursor/hooks.json",
        "description": "sessionStart and sessionEnd hooks for ProjectBrain",
    },
    {
        "id": "projectbrain-user-rules",
        "title": "ProjectBrain user rules template",
        "kind": "user-rule",
        "repo": "AlexTouvras/ProjectBrain",
        "topics": ["portfolio", "memory"],
        "activation": "user",
        "source_path": "templates/cursor/USER_RULES.txt",
        "local": "ProjectBrain/templates/cursor/USER_RULES.txt",
        "description": "Template for Cursor User Rules. The live text is in Customize.",
    },
    {
        "id": "projectbrain-portfolio-template",
        "title": "Portfolio rule installer template",
        "kind": "rule",
        "repo": "AlexTouvras/ProjectBrain",
        "topics": ["portfolio", "distribution"],
        "activation": "manual",
        "source_path": "templates/cursor/rules/projectbrain-portfolio.mdc",
        "local": "ProjectBrain/templates/cursor/rules/projectbrain-portfolio.mdc",
        "description": "Rule copied into other repositories by install_cursor_rules",
    },
    {
        "id": "technology-delivery-weekly",
        "title": "Weekly delivery field card",
        "kind": "automation",
        "repo": "AlexTouvras/technology-delivery-field-card",
        "topics": ["field-card", "delivery", "schedule"],
        "activation": "schedule",
        "source_path": ".cursor/automations/weekly-content-pass.json",
        "local": "technology-delivery-field-card/.cursor/automations/weekly-content-pass.json",
        "description": "Friday content pass. Archive copy of the automation prompt.",
    },
    {
        "id": "technology-delivery-state",
        "title": "State management",
        "kind": "rule",
        "repo": "AlexTouvras/technology-delivery-field-card",
        "topics": ["state", "context"],
        "activation": "always",
        "source_path": ".cursor/rules/00-state-management.mdc",
        "local": "technology-delivery-field-card/.cursor/rules/00-state-management.mdc",
    },
    {
        "id": "technology-delivery-contract",
        "title": "Delivery automation contract",
        "kind": "contract",
        "repo": "AlexTouvras/technology-delivery-field-card",
        "topics": ["governance", "allowlist", "delivery"],
        "activation": "on-run",
        "source_path": ".state/AUTOMATION_CONTRACT.md",
        "local": "technology-delivery-field-card/.state/AUTOMATION_CONTRACT.md",
        "description": "Read order, write order, and scope for the weekly delivery automation",
    },
    {
        "id": "agentic-ai-weekly",
        "title": "Weekly agentic field card",
        "kind": "automation",
        "repo": "AlexTouvras/agentic-ai-field-card",
        "topics": ["field-card", "agents", "schedule"],
        "activation": "schedule",
        "source_path": ".cursor/automations/weekly-content-pass.json",
        "local": "agentic-ai-field-card/.cursor/automations/weekly-content-pass.json",
        "description": "Friday content pass. Archive copy of the automation prompt.",
    },
    {
        "id": "agentic-ai-state",
        "title": "State management",
        "kind": "rule",
        "repo": "AlexTouvras/agentic-ai-field-card",
        "topics": ["state", "context"],
        "activation": "always",
        "source_path": ".cursor/rules/00-state-management.mdc",
        "local": "agentic-ai-field-card/.cursor/rules/00-state-management.mdc",
    },
    {
        "id": "agentic-ai-contract",
        "title": "Agentic automation contract",
        "kind": "contract",
        "repo": "AlexTouvras/agentic-ai-field-card",
        "topics": ["governance", "allowlist", "agents"],
        "activation": "on-run",
        "source_path": ".state/AUTOMATION_CONTRACT.md",
        "local": "agentic-ai-field-card/.state/AUTOMATION_CONTRACT.md",
        "description": "Skill and tool allowlist for the weekly agentic field card automation",
    },
    {
        "id": "data-analytics-weekly",
        "title": "Weekly analytics field card",
        "kind": "automation",
        "repo": "AlexTouvras/data-analytics-field-card",
        "topics": ["field-card", "analytics", "schedule"],
        "activation": "schedule",
        "source_path": ".cursor/automations/weekly-content-pass.json",
        "local": "data-analytics-field-card/.cursor/automations/weekly-content-pass.json",
        "description": "Friday content pass. Archive copy of the automation prompt.",
    },
    {
        "id": "data-analytics-state",
        "title": "State management",
        "kind": "rule",
        "repo": "AlexTouvras/data-analytics-field-card",
        "topics": ["state", "context"],
        "activation": "always",
        "source_path": ".cursor/rules/00-state-management.mdc",
        "local": "data-analytics-field-card/.cursor/rules/00-state-management.mdc",
    },
    {
        "id": "data-analytics-contract",
        "title": "Analytics automation contract",
        "kind": "contract",
        "repo": "AlexTouvras/data-analytics-field-card",
        "topics": ["governance", "allowlist", "analytics"],
        "activation": "on-run",
        "source_path": ".state/AUTOMATION_CONTRACT.md",
        "local": "data-analytics-field-card/.state/AUTOMATION_CONTRACT.md",
        "description": "Read order and scope for the weekly analytics automation",
    },
    {
        "id": "storytelling-state",
        "title": "State management",
        "kind": "rule",
        "repo": "AlexTouvras/storytelling",
        "topics": ["state", "context"],
        "activation": "always",
        "source_path": ".cursor/rules/00-state-management.mdc",
        "local": "storytelling/.cursor/rules/00-state-management.mdc",
    },
    {
        "id": "storytelling-story-engine",
        "title": "Interactive decision storytelling",
        "kind": "rule",
        "repo": "AlexTouvras/storytelling",
        "topics": ["storytelling", "decisions"],
        "activation": "always",
        "source_path": ".cursor/rules/story-engine.mdc",
        "local": "storytelling/.cursor/rules/story-engine.mdc",
    },
    {
        "id": "storytelling-agents",
        "title": "Next.js agent rules",
        "kind": "agents",
        "repo": "AlexTouvras/storytelling",
        "topics": ["nextjs", "generated"],
        "activation": "always",
        "source_path": "AGENTS.md",
        "local": "storytelling/AGENTS.md",
        "description": "Generated Next.js agent instructions",
    },
    {
        "id": "ledger-state",
        "title": "State management",
        "kind": "rule",
        "repo": "AlexTouvras/ledger",
        "topics": ["state", "context"],
        "activation": "always",
        "source_path": ".cursor/rules/00-state-management.mdc",
        "local": "ledger/.cursor/rules/00-state-management.mdc",
    },
]


def main() -> None:
    harvest = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/harvest")
    for item in ITEMS:
        path = harvest / item["local"]
        body = path.read_text(encoding="utf-8")
        repo = item["repo"]
        source = item["source_path"]
        meta = {
            **item,
            "source_url": f"https://github.com/{repo}/blob/main/{source}",
            "imported_on": "2026-09-30",
        }
        catalog.write_imported_item(meta, body)
        print(item["id"])


if __name__ == "__main__":
    main()
