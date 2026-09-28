"""Tests for check_brain.py. Run: python -m unittest discover -s scripts -p "test_*.py" """
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_brain  # noqa: E402


def note(root, rel, body, tag="memory/core"):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\ntags:\n  - {tag}\n---\n{body}\n", encoding="utf-8")


class CheckBrainTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        self.addCleanup(setattr, check_brain, "ROOT", check_brain.ROOT)
        check_brain.ROOT = self.root
        note(self.root, "CORTEX.md", "Router: [[THALAMUS|THALAMUS]]")
        note(self.root, "THALAMUS.md", "Back: [[CORTEX|CORTEX]]")

    def run_checks(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), mock.patch.object(sys, "argv", ["check_brain.py"]):
            code = check_brain.main()
        return code, out.getvalue()

    def test_clean_vault_passes(self):
        code, out = self.run_checks()
        self.assertEqual(code, 0, out)
        self.assertIn("0 errors, 0 warnings", out)

    def test_ambiguous_bare_link_is_an_error(self):
        note(self.root, "NEOCORTEX/BUSINESS.md", "Shared.")
        note(self.root, "PREFRONTAL/PROJECTS/Acme/BUSINESS.md", "Acme.", tag="project/acme")
        note(self.root, "THALAMUS.md", "Back: [[CORTEX|CORTEX]] and [[BUSINESS]]")
        code, out = self.run_checks()
        self.assertEqual(code, 1)
        self.assertIn("ambiguous link [[BUSINESS]]", out)

    def test_full_path_link_is_not_ambiguous(self):
        note(self.root, "NEOCORTEX/BUSINESS.md", "Shared.")
        note(self.root, "PREFRONTAL/PROJECTS/Acme/BUSINESS.md", "Acme.", tag="project/acme")
        note(self.root, "THALAMUS.md", "Back: [[CORTEX|CORTEX]] and [[NEOCORTEX/BUSINESS|BUSINESS]]")
        code, out = self.run_checks()
        self.assertNotIn("ambiguous", out)

    def test_tracked_note_linking_personal_note_is_an_error(self):
        note(self.root, "PREFRONTAL/STYLE.md", "## CODING\n- Plain logs.", tag="memory/personal")
        note(self.root, "THALAMUS.md", "Back: [[CORTEX|CORTEX]] and [[PREFRONTAL/STYLE#CODING|STYLE]]")
        code, out = self.run_checks()
        self.assertEqual(code, 1)
        self.assertIn("tracked note links to personal note [[PREFRONTAL/STYLE]]", out)

    def test_personal_notes_link_freely_and_guides_count_as_tracked(self):
        note(self.root, "PREFRONTAL/STYLE.md", "## CODING\n- Plain logs.", tag="memory/personal")
        note(self.root, "PREFRONTAL/PREFRONTAL.md", "Guide.", tag="memory/personal")
        note(self.root, "LIMBIC/AMYGDALA.md", "## CODING\n- [[PREFRONTAL/STYLE#CODING|STYLE › CODING]]", tag="memory/personal")
        note(self.root, "THALAMUS.md", "Back: [[CORTEX|CORTEX]] and [[PREFRONTAL/PREFRONTAL|PREFRONTAL]]")
        code, out = self.run_checks()
        self.assertEqual(code, 0, out)

    def test_orphan_note_warns_but_roots_do_not(self):
        note(self.root, "NEOCORTEX/LONELY.md", "Links to itself: [[NEOCORTEX/LONELY|LONELY]]")
        note(self.root, "LIMBIC/AMYGDALA.md", "Router.", tag="memory/personal")
        code, out = self.run_checks()
        self.assertEqual(code, 0, out)
        self.assertIn("NEOCORTEX/LONELY.md: orphan: no note links here", out)
        self.assertNotIn("CORTEX.md: orphan", out)
        self.assertNotIn("AMYGDALA.md: orphan", out)

    def test_docs_folder_is_skipped(self):
        (self.root / "docs").mkdir()
        (self.root / "docs" / "spec.md").write_text("No tags here.\nSecond plain line.\n", encoding="utf-8")
        code, out = self.run_checks()
        self.assertEqual(code, 0, out)


if __name__ == "__main__":
    unittest.main()
