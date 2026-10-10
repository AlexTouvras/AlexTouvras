#!/usr/bin/env python3
"""One shell command runs the brief. It does not ask for a second install."""

import json
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = "htmlpreview.github.io"


class CommandTests(unittest.TestCase):
    def test_shells_only_forward_to_the_checker(self) -> None:
        for name in ("run.sh", "run.ps1"):
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("pipeline.py", text, name)
            self.assertIn(PAGE, text, name)
            lowered = text.lower()
            self.assertNotIn("pip install", lowered, name)
            self.assertNotIn("npm install", lowered, name)
            self.assertNotIn("venv", lowered, name)
        cmd = (ROOT / "run.cmd").read_text(encoding="utf-8").lower()
        self.assertIn("run.ps1", cmd)
        self.assertNotIn("pip install", cmd)
        self.assertNotIn("npm install", cmd)
        skill = (ROOT.parents[0] / "skills" / "delivery-signal" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("run.sh", skill)
        self.assertIn("run.ps1", skill)
        self.assertIn("run.cmd", skill)
        self.assertIn("Do not install Python", skill)

    def test_bash_command_writes_the_brief(self) -> None:
        script = ROOT / "run.sh"
        mode = script.stat().st_mode
        self.assertTrue(mode & stat.S_IXUSR, "run.sh is executable")
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            csv_path = directory / "Northwind.csv"
            csv_path.write_text("key,summary,status\nT-1,Rotate keys,To Do\n", encoding="utf-8")
            completed = subprocess.run(
                ["bash", str(script), str(csv_path), "--as-of", "2026-10-10", "--out", str(directory / "out")],
                check=False,
                text=True,
                capture_output=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            brief = json.loads((directory / "out" / "brief.json").read_text(encoding="utf-8"))
            self.assertEqual(brief["portfolio"], "Northwind")
            self.assertEqual(brief["as_of"], "2026-10-10")
            self.assertTrue(brief["result_id"])


if __name__ == "__main__":
    unittest.main()
