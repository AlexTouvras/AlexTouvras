#!/usr/bin/env python3
"""The sample is only useful if the planted traps are found and the noise is not."""

import csv
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import extract  # noqa: E402
import pipeline  # noqa: E402


SAMPLE = Path(__file__).resolve().parents[1] / "samples" / "northline"
COLUMNS = [
    "key",
    "project",
    "project_name",
    "type",
    "summary",
    "status",
    "priority",
    "assignee",
    "story_points",
    "percent_complete",
    "created",
    "updated",
    "due",
    "parent",
    "blocked_by",
    "comment",
]


def write_items(directory: Path, rows: list[dict]) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "work_items.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        for row in rows:
            full = {column: "" for column in COLUMNS}
            full.update(row)
            writer.writerow(full)


class NorthlineSampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.brief = pipeline.build(SAMPLE)

    def test_planted_traps_are_the_top_risks(self) -> None:
        ids = [finding["id"] for finding in self.brief["top_risks"]]
        self.assertEqual(
            ids,
            [
                "unassigned:FOR-12",
                "unassigned:LUM-4",
                "note_conflict:N-1",
                "blocked:FOR-20",
                "completion:LUM-1",
            ],
        )

    def test_overdue_dependency_that_does_not_block_is_set_aside(self) -> None:
        aside = {finding["id"] for finding in self.brief["set_aside"]}
        self.assertEqual(aside, {"non_blocking:DEP-LEG"})
        self.assertNotIn("non_blocking:DEP-LEG", {finding["id"] for finding in self.brief["top_risks"]})
        text = self.brief["set_aside"][0]["summary"]
        self.assertIn("FOR-3", text)
        self.assertIn("Done", text)

    def test_misleading_completion_uses_story_points(self) -> None:
        finding = next(item for item in self.brief["top_risks"] if item["id"] == "completion:LUM-1")
        self.assertIn("85", finding["title"])
        self.assertIn("8 of 37", finding["title"])
        self.assertIn("N-2", finding["summary"])
        self.assertEqual(finding["confidence"], "fact")

    def test_green_note_is_an_inference_and_the_healthy_note_is_not(self) -> None:
        cedar = next(item for item in self.brief["top_risks"] if item["id"] == "note_conflict:N-1")
        self.assertEqual(cedar["confidence"], "inference")
        self.assertIn("CED-2", cedar["summary"])
        self.assertIn("CED-3", cedar["summary"])
        blob = json.dumps(self.brief["top_risks"] + self.brief["also_noted"])
        self.assertNotIn("N-4", blob)
        aster = next(row for row in self.brief["pulse"] if row["id"] == "ASTER")
        self.assertEqual(aster["state"], "on_track")

    def test_decision_is_queued_with_the_missing_owner(self) -> None:
        self.assertNotIn("LUM-9", {finding["id"] for finding in self.brief["top_risks"]})
        decision = next(item for item in self.brief["decisions"] if item["key"] == "LUM-9")
        self.assertEqual(decision["owner"], "missing")
        self.assertTrue(decision["overdue"])
        self.assertIn("owner", decision["unknowns"])
        self.assertEqual(decision["successors"], ["LUM-4"])

    def test_changes_are_limited_to_the_previous_export(self) -> None:
        by_key = {change["key"]: change for change in self.brief["changes"]}
        self.assertEqual(set(by_key), {"FOR-12", "LUM-3"})
        assignee = next(field for field in by_key["FOR-12"]["fields"] if field["field"] == "assignee")
        self.assertEqual(assignee["before"], "Alex Rahman")
        self.assertEqual(assignee["after"], "blank")
        status = next(field for field in by_key["LUM-3"]["fields"] if field["field"] == "status")
        self.assertEqual(status["before"], "In Progress")
        self.assertEqual(status["after"], "Done")

    def test_every_claim_cites_a_real_row(self) -> None:
        loaded = pipeline.load_portfolio(SAMPLE)
        known = {
            "work_items": set(loaded["by_key"]),
            "notes": {note["id"] for note in loaded["notes"]},
            "milestones": set(loaded["milestone_by_id"]),
            "dependencies": {dep["id"] for dep in loaded["dependencies"]},
        }
        findings = self.brief["top_risks"] + self.brief["also_noted"] + self.brief["set_aside"]
        self.assertTrue(findings)
        for finding in findings:
            self.assertTrue(finding["evidence"])
            for evidence in finding["evidence"]:
                self.assertIn(evidence["id"], known[evidence["source"]])
                self.assertTrue(evidence["field"])
        self.assertEqual(self.brief["data_quality"], [])
        self.assertTrue(self.brief["quality"]["traceable"])
        self.assertEqual(self.brief["approval"], "pending")

    def test_brief_does_not_forecast_a_missed_date(self) -> None:
        text = pipeline.render_markdown(self.brief).lower()
        for phrase in ("will miss", "predicted", "guarantee", "on schedule to fail"):
            self.assertNotIn(phrase, text)
        self.assertIn("does not forecast", text)

    def test_forge_is_blocked_and_lumen_needs_attention(self) -> None:
        states = {row["id"]: row["state"] for row in self.brief["pulse"]}
        self.assertEqual(states["FORGE"], "blocked")
        self.assertEqual(states["LUMEN"], "needs_attention")
        self.assertEqual(states["CEDAR"], "needs_attention")


class RuleTests(unittest.TestCase):
    def test_clean_portfolio_has_no_risk(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "meta.json").write_text(
                json.dumps(
                    {
                        "portfolio": "Clean",
                        "as_of": "2026-10-10",
                        "audience": "Delivery director",
                        "synthetic": True,
                    }
                ),
                encoding="utf-8",
            )
            write_items(
                directory,
                [
                    {
                        "key": "CLN-1",
                        "project": "CLEAN",
                        "project_name": "Clean export",
                        "type": "Story",
                        "summary": "Scheduler",
                        "status": "In Progress",
                        "priority": "Medium",
                        "assignee": "Mina Cho",
                        "story_points": "3",
                        "updated": "2026-10-09",
                        "due": "2026-10-24",
                    }
                ],
            )
            (directory / "notes.csv").write_text(
                "id,date,project,author,text\nN-1,2026-10-09,CLEAN,Mina Cho,The scheduler is on track. No blockers.\n",
                encoding="utf-8",
            )
            brief = pipeline.build(directory)
        self.assertEqual(brief["top_risks"], [])
        self.assertEqual(brief["pulse"][0]["state"], "on_track")

    def test_missing_column_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "meta.json").write_text(
                json.dumps({"portfolio": "Broken", "as_of": "2026-10-10"}),
                encoding="utf-8",
            )
            (directory / "work_items.csv").write_text("key,summary\nA-1,Hello\n", encoding="utf-8")
            with self.assertRaises(pipeline.InputError):
                pipeline.build(directory)

    def test_duplicate_key_is_data_quality_not_a_crash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "meta.json").write_text(
                json.dumps({"portfolio": "Dupes", "as_of": "2026-10-10"}),
                encoding="utf-8",
            )
            write_items(
                directory,
                [
                    {
                        "key": "DUP-1",
                        "project": "DUP",
                        "project_name": "Dupes",
                        "type": "Task",
                        "summary": "First",
                        "status": "Done",
                        "assignee": "Samir Adeyemi",
                    },
                    {
                        "key": "DUP-1",
                        "project": "DUP",
                        "project_name": "Dupes",
                        "type": "Task",
                        "summary": "Second",
                        "status": "In Progress",
                        "priority": "Highest",
                        "due": "2026-10-01",
                    },
                ],
            )
            brief = pipeline.build(directory)
        self.assertTrue(any("duplicate work item DUP-1" in issue for issue in brief["data_quality"]))
        self.assertEqual(brief["top_risks"], [])

    def test_cli_writes_the_three_brief_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            code = pipeline.main([str(SAMPLE), "--out", str(output)])
            self.assertEqual(code, 0)
            for name in ("brief.json", "brief.md", "brief.html"):
                self.assertTrue((output / name).is_file())
            html = (output / "brief.html").read_text(encoding="utf-8")
            self.assertIn("Northline Advisory", html)
            self.assertIn("Checked and set aside", html)
            self.assertIn("FOR-3 is Done", html)
            self.assertIn("<details", html)
            self.assertIn("pending approval", html.lower())
            self.assertTrue((output / "Northline-Advisory-2026-10-10.html").is_file())


class ProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = pipeline.build(SAMPLE)

    def test_jira_and_azure_devops_match_the_canonical_result(self) -> None:
        root = SAMPLE.parent
        for folder in ("northline-jira", "northline-ado"):
            brief = pipeline.build(root / folder)
            self.assertEqual(brief["result_id"], self.base["result_id"])
            self.assertEqual(
                [item["id"] for item in brief["top_risks"]],
                [item["id"] for item in self.base["top_risks"]],
            )
            self.assertEqual(brief["data_quality"], [])
        self.assertEqual(pipeline.build(root / "northline-jira")["source_profile"], "jira")
        self.assertEqual(pipeline.build(root / "northline-ado")["source_profile"], "azure_devops")

    def test_rewritten_profiles_match_too(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for profile in ("jira", "azure_devops"):
                dest = Path(tmp) / profile
                extract.write_profile_copy(SAMPLE, dest, profile)
                brief = pipeline.build(dest)
                self.assertEqual(brief["result_id"], self.base["result_id"])
                self.assertEqual(brief["source_profile"], profile)

    def test_export_dates_and_joined_comments(self) -> None:
        self.assertEqual(extract.parse_date("08/Oct/26 4:12 PM", "jira"), date(2026, 10, 8))
        self.assertEqual(extract.parse_date("10/08/2026 4:12:00 PM", "azure_devops"), date(2026, 10, 8))
        self.assertEqual(extract.parse_date("08.10.2026", "jira"), date(2026, 10, 8))
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "meta.json").write_text(
                json.dumps({"portfolio": "Comments", "as_of": "2026-10-10", "profile": "jira"}),
                encoding="utf-8",
            )
            (directory / "work_items.csv").write_text(
                "Issue key,Summary,Status,Comment,Comment\n"
                "C-1,Join me,Done,First note.,Second note.\n",
                encoding="utf-8",
            )
            loaded = pipeline.load_portfolio(directory)
        self.assertEqual(loaded["items"][0].comment, "First note. Second note.")

    def test_column_override_and_single_csv_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "meta.json").write_text(
                json.dumps({"portfolio": "Renamed", "as_of": "2026-10-10"}),
                encoding="utf-8",
            )
            (directory / "columns.json").write_text(
                json.dumps({"profile": "canonical", "columns": {"key": "Ticket"}}),
                encoding="utf-8",
            )
            write_items(
                directory,
                [
                    {
                        "key": "T-1",
                        "project": "ONE",
                        "project_name": "One",
                        "type": "Task",
                        "summary": "Named ticket",
                        "status": "Done",
                        "assignee": "Mina Cho",
                    }
                ],
            )
            text = (directory / "work_items.csv").read_text(encoding="utf-8").replace("key,", "Ticket,", 1)
            (directory / "work_items.csv").write_text(text, encoding="utf-8")
            brief = pipeline.build(directory)
            self.assertEqual(brief["item_count"], 1)
            code = pipeline.main(
                [
                    str(directory / "work_items.csv"),
                    "--name",
                    "From a file",
                    "--as-of",
                    "2026-10-10",
                    "--columns",
                    str(directory / "columns.json"),
                    "--out",
                    str(directory / "out"),
                ]
            )
            self.assertEqual(code, 0)
            self.assertTrue((directory / "out" / "From-a-file-2026-10-10.html").is_file())

    def test_unknown_headers_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "meta.json").write_text(
                json.dumps({"portfolio": "Odd", "as_of": "2026-10-10"}),
                encoding="utf-8",
            )
            (directory / "work_items.csv").write_text("Foo,Bar\nA,B\n", encoding="utf-8")
            with self.assertRaises(pipeline.InputError):
                pipeline.build(directory)


if __name__ == "__main__":
    unittest.main()
