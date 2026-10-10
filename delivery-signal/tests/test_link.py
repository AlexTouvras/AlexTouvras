#!/usr/bin/env python3
"""Connect a tracker or import a CSV, then write the report. Tokens stay out of the project file."""

import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import link  # noqa: E402
import pipeline  # noqa: E402


CSV = "key,summary,status,priority,assignee,due\nT-1,Rotate keys,To Do,Highest,,2026-10-01\n"


class LinkTests(unittest.TestCase):
    def test_three_steps_import_then_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            source = home / "issues.csv"
            source.write_text(CSV, encoding="utf-8")
            self.assertEqual(
                link.main(["--home", str(home), "connect", "other", "--project", "WEB", "--name", "Board"]),
                0,
            )
            saved = json.loads((home / ".delivery-signal" / "project.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["tracker"], "other")
            self.assertNotIn("token", json.dumps(saved).lower())
            self.assertEqual(link.main(["--home", str(home), "import", str(source)]), 0)
            self.assertEqual(link.main(["--home", str(home), "report", "--as-of", "2026-10-10"]), 0)
            brief = json.loads((home / "out" / "brief.json").read_text(encoding="utf-8"))
            self.assertEqual(brief["portfolio"], "Board")
            self.assertEqual(brief["top_risks"][0]["id"], "unassigned:T-1")

    def test_jira_pull_uses_the_connected_site_and_skips_the_token_file(self) -> None:
        calls = []

        def transport(method, url, headers, body):
            calls.append((method, url, headers["Authorization"], json.loads(body.decode())))
            return {
                "issues": [
                    {
                        "key": "FOR-12",
                        "fields": {
                            "summary": "Carrier cutover",
                            "status": {"name": "In Progress"},
                            "issuetype": {"name": "Story"},
                            "priority": {"name": "Highest"},
                            "assignee": None,
                            "project": {"key": "FORGE", "name": "Forge"},
                            "created": "2026-08-01T10:00:00.000+0000",
                            "updated": "2026-08-02T10:00:00.000+0000",
                            "duedate": "2026-10-01",
                            "description": {"type": "doc", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Waiting on the carrier."}]}]},
                        },
                    }
                ]
            }

        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            with mock.patch.dict(os.environ, {"JIRA_EMAIL": "ada@example.com", "JIRA_API_TOKEN": "secret-token"}):
                self.assertEqual(
                    link.main(
                        [
                            "--home",
                            str(home),
                            "connect",
                            "jira",
                            "--site",
                            "https://acme.atlassian.net",
                            "--project",
                            "FORGE",
                            "--name",
                            "Forge",
                        ]
                    ),
                    0,
                )
                project_text = (home / ".delivery-signal" / "project.json").read_text(encoding="utf-8")
                self.assertNotIn("secret-token", project_text)
                self.assertNotIn("ada@example.com", project_text)
                with mock.patch.object(link, "default_transport", transport):
                    self.assertEqual(link.main(["--home", str(home), "import"]), 0)
            self.assertEqual(calls[0][0], "POST")
            self.assertEqual(calls[0][1], "https://acme.atlassian.net/rest/api/3/search/jql")
            self.assertNotIn("secret-token", calls[0][1])
            self.assertEqual(link.main(["--home", str(home), "report", "--as-of", "2026-10-10"]), 0)
            brief = json.loads((home / "out" / "brief.json").read_text(encoding="utf-8"))
            self.assertEqual(brief["source_profile"], "jira")
            self.assertEqual(brief["top_risks"][0]["id"], "unassigned:FOR-12")

    def test_ado_pull_reads_the_connected_project(self) -> None:
        def transport(method, url, headers, body):
            if url.endswith("/wiql?api-version=7.1"):
                return {"workItems": [{"id": 20}]}
            return {
                "value": [
                    {
                        "id": 20,
                        "fields": {
                            "System.TeamProject": "Fabrikam",
                            "System.Title": "Cutover",
                            "System.State": "Active",
                            "System.WorkItemType": "User Story",
                            "Microsoft.VSTS.Common.Priority": 1,
                            "System.AssignedTo": {"displayName": ""},
                            "System.ChangedDate": "2026-08-01T00:00:00Z",
                            "Microsoft.VSTS.Scheduling.DueDate": "2026-10-01T00:00:00Z",
                        },
                    }
                ]
            }

        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            with mock.patch.dict(os.environ, {"ADO_PAT": "ado-secret"}, clear=False):
                self.assertEqual(
                    link.main(
                        [
                            "--home",
                            str(home),
                            "connect",
                            "ado",
                            "--org",
                            "https://dev.azure.com/contoso",
                            "--project",
                            "Fabrikam",
                        ]
                    ),
                    0,
                )
                self.assertNotIn("ado-secret", (home / ".delivery-signal" / "project.json").read_text(encoding="utf-8"))
                with mock.patch.object(link, "default_transport", transport):
                    self.assertEqual(link.main(["--home", str(home), "import"]), 0)
            self.assertEqual(link.main(["--home", str(home), "report", "--as-of", "2026-10-10"]), 0)
            brief = json.loads((home / "out" / "brief.json").read_text(encoding="utf-8"))
            self.assertEqual(brief["source_profile"], "azure_devops")
            self.assertEqual(brief["top_risks"][0]["id"], "unassigned:20")

    def test_http_site_and_missing_token_are_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            code = link.main(
                ["--home", str(home), "connect", "jira", "--site", "http://acme.atlassian.net", "--project", "FORGE"]
            )
            self.assertEqual(code, 1)
            with mock.patch.dict(os.environ, {"JIRA_EMAIL": "", "JIRA_API_TOKEN": ""}, clear=False):
                os.environ.pop("JIRA_EMAIL", None)
                os.environ.pop("JIRA_API_TOKEN", None)
                self.assertEqual(
                    link.main(
                        ["--home", str(home), "connect", "jira", "--site", "https://acme.atlassian.net", "--project", "FORGE"]
                    ),
                    0,
                )
                code = link.main(["--home", str(home), "import"])
            self.assertEqual(code, 1)

    def test_bare_run_prints_the_three_steps(self) -> None:
        stdout = io.StringIO()
        with mock.patch("sys.stdout", stdout):
            code = pipeline.main([])
        text = stdout.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("run connect jira", text)
        self.assertIn("run import issues.csv", text)
        self.assertIn("run report", text)

    def test_pipeline_connect_writes_the_project_file_in_the_working_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            previous = os.getcwd()
            os.chdir(tmp)
            try:
                code = pipeline.main(["connect", "other", "--project", "WEB", "--name", "Board"])
            finally:
                os.chdir(previous)
            self.assertEqual(code, 0)
            saved = json.loads((Path(tmp) / ".delivery-signal" / "project.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["name"], "Board")
            self.assertNotIn("token", json.dumps(saved).lower())

    def test_plain_csv_command_still_writes_a_brief(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            csv_path = home / "Northwind.csv"
            csv_path.write_text("key,summary,status\nT-1,Rotate keys,To Do\n", encoding="utf-8")
            code = pipeline.main([str(csv_path), "--as-of", "2026-10-10", "--out", str(home / "out")])
            self.assertEqual(code, 0)
            self.assertTrue((home / "out" / "brief.html").is_file())


if __name__ == "__main__":
    unittest.main()
