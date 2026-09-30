import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ["GOVERNANCE_ARCHIVE"] = tempfile.mkdtemp(prefix="governance-test-")

import catalog  # noqa: E402


def _rule(always: str = "true") -> str:
    return f"---\ndescription: Keep state in files\nalwaysApply: {always}\n---\n\n# State\n\nRead .state before acting.\n"


class CatalogTests(unittest.TestCase):
    def setUp(self) -> None:
        root = Path(os.environ["GOVERNANCE_ARCHIVE"])
        if root.exists():
            shutil.rmtree(root)
        root.mkdir()

    def test_import_budget_and_duplicates(self) -> None:
        body = _rule()
        catalog.write_imported_item(
            {
                "id": "alpha-state",
                "title": "State",
                "kind": "rule",
                "repo": "AlexTouvras/alpha",
                "topics": ["state", "context"],
                "activation": "always",
                "source_path": ".cursor/rules/state.mdc",
            },
            body,
        )
        catalog.write_imported_item(
            {
                "id": "beta-state",
                "title": "State",
                "kind": "rule",
                "repo": "AlexTouvras/beta",
                "topics": ["state"],
                "activation": "always",
                "source_path": ".cursor/rules/state.mdc",
            },
            body,
        )
        data = catalog.catalog()
        self.assertEqual(len(data["items"]), 2)
        self.assertEqual(data["items"][0]["identical_copies"], 2)
        alpha = next(row for row in data["budgets"] if row["repo"] == "AlexTouvras/alpha")
        self.assertGreater(alpha["always_on_tokens"], 0)
        self.assertFalse(alpha["over_budget"])

    def test_save_snapshots_previous_body_and_syncs_frontmatter(self) -> None:
        catalog.write_imported_item(
            {
                "id": "alpha-state",
                "title": "State",
                "kind": "rule",
                "repo": "AlexTouvras/alpha",
                "topics": ["state"],
                "activation": "always",
                "source_path": ".cursor/rules/state.mdc",
            },
            _rule(),
        )
        saved = catalog.save_item(
            "alpha-state",
            {
                "title": "State files",
                "kind": "rule",
                "repo": "AlexTouvras/alpha",
                "topics": "state, budget",
                "activation": "manual",
                "body": _rule() + "\nOnly when asked.\n",
            },
        )
        self.assertEqual(saved["title"], "State files")
        self.assertEqual(saved["topics"], ["state", "budget"])
        self.assertEqual(saved["activation"], "manual")
        self.assertIn("alwaysApply: false", saved["body"])
        self.assertEqual(saved["versions"][-1]["note"], "edit")
        self.assertIn("Read .state before acting.", saved["versions"][0]["body"])

    def test_restore_returns_prior_text(self) -> None:
        catalog.write_imported_item(
            {
                "id": "alpha-state",
                "title": "State",
                "kind": "rule",
                "repo": "AlexTouvras/alpha",
                "topics": ["state"],
                "activation": "always",
                "source_path": ".cursor/rules/state.mdc",
            },
            _rule(),
        )
        catalog.save_item(
            "alpha-state",
            {
                "title": "State",
                "kind": "rule",
                "repo": "AlexTouvras/alpha",
                "topics": ["state"],
                "activation": "always",
                "body": _rule() + "\nChanged.\n",
            },
        )
        restored = catalog.restore_item("alpha-state", "20260930T000000Z")
        self.assertIn("Read .state before acting.", restored["body"])
        self.assertNotIn("Changed.", restored["body"])
        self.assertEqual(restored["activation"], "always")

    def test_create_skill_and_reject_bad_kind(self) -> None:
        created = catalog.create_item(
            {
                "title": "Review a field card",
                "kind": "skill",
                "repo": "AlexTouvras/agentic-ai-field-card",
                "topics": ["field-card"],
                "activation": "agent",
                "body": "",
            }
        )
        self.assertTrue(created["id"].startswith("agentic-ai-field-card-skill-"))
        self.assertIn("name:", created["body"])
        with self.assertRaises(ValueError):
            catalog.create_item(
                {
                    "title": "Nope",
                    "kind": "spell",
                    "repo": "AlexTouvras/alpha",
                    "topics": [],
                    "activation": "always",
                    "body": "x",
                }
            )

    def test_similar_docs_get_a_shared_kind(self) -> None:
        self.assertEqual(catalog.suggest_category("README.md", "doc"), ("readme", "manual"))
        self.assertEqual(
            catalog.suggest_category(".state/BACKLOG.md", "doc"),
            ("state", "manual"),
        )
        self.assertEqual(
            catalog.suggest_category("docs/architecture/system-overview.md", "doc"),
            ("architecture", "manual"),
        )
        self.assertEqual(
            catalog.suggest_category("agents/huginn.md", "doc"),
            ("agents", "agent"),
        )
        self.assertEqual(
            catalog.suggest_category(".cursor/skills/visual-storytelling/SKILL.md", "doc"),
            ("skill", "agent"),
        )
        self.assertEqual(
            catalog.suggest_category("docs/contracts/signal.md", "doc"),
            ("schema", "manual"),
        )
        self.assertEqual(
            catalog.suggest_category("docs/essay-voice.md", "doc"),
            ("skill", "manual"),
        )
        self.assertEqual(
            catalog.suggest_category("_shared/themes/THEME-REVIEW.md", "doc"),
            ("brief", "manual"),
        )
        self.assertIsNone(catalog.suggest_category("docs/FLAGSHIP.md", "doc"))
        self.assertIsNone(catalog.suggest_category(".cursor/rules/core.mdc", "rule"))

    def test_doc_is_outside_the_always_on_budget(self) -> None:
        catalog.write_imported_item(
            {
                "id": "alpha-notes",
                "title": "Notes",
                "kind": "doc",
                "repo": "AlexTouvras/alpha",
                "topics": ["readme"],
                "activation": "manual",
                "source_path": "docs/NOTES.md",
            },
            "# Notes\n\n" + ("word " * 800),
        )
        budget = next(row for row in catalog.catalog()["budgets"] if row["repo"] == "AlexTouvras/alpha")
        self.assertEqual(budget["always_on_tokens"], 0)
        self.assertFalse(budget["over_budget"])

    def test_over_budget_flag(self) -> None:
        catalog.write_imported_item(
            {
                "id": "heavy",
                "title": "Heavy",
                "kind": "rule",
                "repo": "AlexTouvras/heavy",
                "topics": ["context"],
                "activation": "always",
                "source_path": ".cursor/rules/heavy.mdc",
            },
            "---\ndescription: Heavy\nalwaysApply: true\n---\n\n" + ("word " * 1200),
        )
        budget = catalog.catalog()["budgets"][0]
        self.assertTrue(budget["over_budget"])
        self.assertGreater(budget["always_on_tokens"], catalog.ALWAYS_ON_TOKEN_CAP)


if __name__ == "__main__":
    unittest.main()
