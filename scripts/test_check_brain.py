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
        note(self.root, "CORTEX.md", "Areas: [[NEOCORTEX/NEOCORTEX|NEOCORTEX]]")
        note(self.root, "NEOCORTEX/NEOCORTEX.md", "Up: [[CORTEX|CORTEX]]")

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
        note(self.root, "NEOCORTEX/NEOCORTEX.md", "Up: [[CORTEX|CORTEX]] and [[BUSINESS]]")
        code, out = self.run_checks()
        self.assertEqual(code, 1)
        self.assertIn("ambiguous link [[BUSINESS]]", out)

    def test_full_path_link_is_not_ambiguous(self):
        note(self.root, "NEOCORTEX/BUSINESS.md", "Shared.")
        note(self.root, "PREFRONTAL/PROJECTS/Acme/BUSINESS.md", "Acme.", tag="project/acme")
        note(self.root, "NEOCORTEX/NEOCORTEX.md", "Up: [[CORTEX|CORTEX]] and [[NEOCORTEX/BUSINESS|BUSINESS]]")
        code, out = self.run_checks()
        self.assertNotIn("ambiguous", out)

    def test_tracked_note_linking_personal_note_is_an_error(self):
        note(self.root, "PREFRONTAL/STYLE.md", "## CODING\n- Plain logs.", tag="memory/personal")
        note(self.root, "PREFRONTAL/PREFRONTAL.md", "Up: [[CORTEX|CORTEX]] and [[PREFRONTAL/STYLE#CODING|STYLE]]", tag="memory/personal")
        code, out = self.run_checks()
        self.assertEqual(code, 1)
        self.assertIn("tracked note links to untracked note [[PREFRONTAL/STYLE]]", out)

    def test_tracked_guide_linking_a_project_hub_is_an_error(self):
        note(self.root, "NEOCORTEX/PROJECTS/PROJECTS.md", "Up: [[NEOCORTEX/NEOCORTEX|NEOCORTEX]]; [[NEOCORTEX/PROJECTS/Acme/ACME|ACME]]", tag="project")
        note(self.root, "NEOCORTEX/PROJECTS/Acme/ACME.md", "> Up: [[NEOCORTEX/PROJECTS/PROJECTS|PROJECTS]]", tag="project/acme")
        code, out = self.run_checks()
        self.assertEqual(code, 1)
        self.assertIn("tracked note links to untracked note [[NEOCORTEX/PROJECTS/Acme/ACME]]", out)

    def test_mirrored_layout_passes(self):
        note(self.root, "CORTEX.md", "[[NEOCORTEX/NEOCORTEX|NEOCORTEX]] and [[PREFRONTAL/PREFRONTAL|PREFRONTAL]]")
        note(self.root, "NEOCORTEX/NEOCORTEX.md", "Up: [[CORTEX|CORTEX]]; [[NEOCORTEX/INSTRUCTIONS/INSTRUCTIONS|INSTRUCTIONS]], "
             "[[NEOCORTEX/KNOWLEDGE/KNOWLEDGE|KNOWLEDGE]], [[NEOCORTEX/PROJECTS/PROJECTS|PROJECTS]]")
        note(self.root, "NEOCORTEX/INSTRUCTIONS/INSTRUCTIONS.md", "Up: [[NEOCORTEX/NEOCORTEX|NEOCORTEX]]; "
             "[[NEOCORTEX/INSTRUCTIONS/CODING\\|CODING]]; next door: [[NEOCORTEX/KNOWLEDGE/KNOWLEDGE\\|KNOWLEDGE]]")
        note(self.root, "NEOCORTEX/INSTRUCTIONS/CODING.md", "Pairs with `KNOWLEDGE`.", tag="memory/technical")
        note(self.root, "NEOCORTEX/KNOWLEDGE/KNOWLEDGE.md", "Up: [[NEOCORTEX/NEOCORTEX|NEOCORTEX]]", tag="knowledge")
        note(self.root, "NEOCORTEX/KNOWLEDGE/RETRIES.md", "> Up: [[NEOCORTEX/KNOWLEDGE/KNOWLEDGE|KNOWLEDGE]]", tag="knowledge\nsources:\n  - docs")
        note(self.root, "NEOCORTEX/PROJECTS/PROJECTS.md", "Up: [[NEOCORTEX/NEOCORTEX|NEOCORTEX]]", tag="project")
        note(self.root, "NEOCORTEX/PROJECTS/HUB.md", "> Up: [[NEOCORTEX/PROJECTS/PROJECTS|PROJECTS]]; "
             "[[NEOCORTEX/PROJECTS/Acme/ACME|ACME]]", tag="project")
        note(self.root, "NEOCORTEX/PROJECTS/Acme/ACME.md", "> Up: [[NEOCORTEX/PROJECTS/PROJECTS|PROJECTS]]", tag="project/acme")
        note(self.root, "PREFRONTAL/PREFRONTAL.md", "Up: [[CORTEX|CORTEX]]", tag="persona")
        # A user's folder links the way the brain shows it to them: PREFRONTAL/<user>/X reads as PREFRONTAL/X.
        note(self.root, "PREFRONTAL/U1/INSTRUCTIONS/INSTRUCTIONS.md", "> Up: [[PREFRONTAL/PREFRONTAL|PREFRONTAL]]; "
             "[[PREFRONTAL/INSTRUCTIONS/STYLE|STYLE]]", tag="persona")
        note(self.root, "PREFRONTAL/U1/INSTRUCTIONS/STYLE.md", "> Up: [[PREFRONTAL/INSTRUCTIONS/INSTRUCTIONS|INSTRUCTIONS]]\n\n"
             "## CODING\n- Plain logs.", tag="persona")
        code, out = self.run_checks()
        self.assertEqual(code, 0, out)
        self.assertIn("0 errors, 0 warnings", out)

    def test_long_personal_section_in_a_user_folder_warns(self):
        note(self.root, "PREFRONTAL/PREFRONTAL.md", "Up: [[CORTEX|CORTEX]]", tag="persona")
        note(self.root, "PREFRONTAL/U1/INSTRUCTIONS/STYLE.md", "> Up: [[PREFRONTAL/PREFRONTAL|PREFRONTAL]]\n\n## CODING\n"
             + "\n".join(f"- rule {i}" for i in range(160)), tag="persona")
        code, out = self.run_checks()
        self.assertIn("section 'CODING' has", out)

    def test_personal_notes_link_up_to_the_guide(self):
        note(self.root, "CORTEX.md", "[[NEOCORTEX/NEOCORTEX|NEOCORTEX]] and [[PREFRONTAL/PREFRONTAL|PREFRONTAL]]")
        note(self.root, "PREFRONTAL/PREFRONTAL.md", "Up: [[CORTEX|CORTEX]]", tag="memory/personal")
        note(self.root, "PREFRONTAL/STYLE.md", "> Up: [[PREFRONTAL/PREFRONTAL|PREFRONTAL]]\n\n## CODING\n- Plain logs.", tag="memory/personal")
        note(self.root, "PREFRONTAL/PROJECTS/PROJECTS.md", "> Up: [[PREFRONTAL/PREFRONTAL|PREFRONTAL]]", tag="project")
        code, out = self.run_checks()
        self.assertEqual(code, 0, out)
        self.assertIn("0 errors, 0 warnings", out)  # a note that only links up isn't an orphan

    def test_orphan_note_warns_but_roots_do_not(self):
        note(self.root, "NEOCORTEX/LONELY.md", "Links to itself: [[NEOCORTEX/LONELY|LONELY]]")
        code, out = self.run_checks()
        self.assertEqual(code, 0, out)
        self.assertIn("NEOCORTEX/LONELY.md: orphan: no link in or out", out)
        self.assertNotIn("CORTEX.md: orphan", out)

    def test_link_that_leaves_the_tree_warns(self):
        note(self.root, "CORTEX.md", "[[NEOCORTEX/NEOCORTEX|NEOCORTEX]], [[HIPPOCAMPUS/HIPPOCAMPUS|HIPPOCAMPUS]], "
             "[[PREFRONTAL/PREFRONTAL|PREFRONTAL]] and a shortcut to [[NEOCORTEX/CODING|CODING]]")
        note(self.root, "NEOCORTEX/NEOCORTEX.md", "Up: [[CORTEX|CORTEX]]; areas: [[NEOCORTEX/CODING\\|CODING]], "
             "[[NEOCORTEX/WRITING\\|WRITING]]; next door: [[PREFRONTAL/PREFRONTAL|PREFRONTAL]]")
        note(self.root, "NEOCORTEX/CODING.md", "Pairs with [[NEOCORTEX/WRITING|WRITING]] and [[PREFRONTAL/PREFRONTAL|PREFRONTAL]]")
        note(self.root, "NEOCORTEX/WRITING.md", "Index: [[NEOCORTEX/NEOCORTEX#Areas|NEOCORTEX › Areas]]")
        note(self.root, "HIPPOCAMPUS/HIPPOCAMPUS.md", "Up: [[CORTEX|CORTEX]]; [[HIPPOCAMPUS/ENGRAM|ENGRAM]]", tag="hippocampus")
        note(self.root, "HIPPOCAMPUS/ENGRAM.md", "Lands in [[NEOCORTEX/NEOCORTEX|NEOCORTEX]]", tag="hippocampus")
        note(self.root, "PREFRONTAL/PREFRONTAL.md", "Up: [[CORTEX|CORTEX]]", tag="memory/personal")
        code, out = self.run_checks()
        self.assertEqual(code, 1, out)  # only the dead #Areas heading is an error
        leaves = [line for line in out.splitlines() if "leaves the tree" in line]
        self.assertEqual(len(leaves), 3, out)
        self.assertTrue(any(line.startswith("CORTEX.md:") and "[[NEOCORTEX/CODING]]" in line for line in leaves), out)
        self.assertTrue(any(line.startswith("NEOCORTEX/NEOCORTEX.md:") for line in leaves), out)  # region to region
        self.assertTrue(any(line.startswith("NEOCORTEX/CODING.md:") and "PREFRONTAL" in line for line in leaves), out)

    def test_same_subject_twice_warns_but_project_notes_are_scoped(self):
        note(self.root, "NEOCORTEX/KNOWLEDGE/KNOWLEDGE.md", "Up: [[NEOCORTEX/NEOCORTEX|NEOCORTEX]]", tag="knowledge")
        note(self.root, "NEOCORTEX/KNOWLEDGE/NAS.md", "---", tag="knowledge")
        note(self.root, "PREFRONTAL/U1/KNOWLEDGE/NAS.md", "Mine.", tag="persona")
        note(self.root, "NEOCORTEX/PROJECTS/acme/overview/OVERVIEW.md", "Acme.", tag="project/acme")
        note(self.root, "NEOCORTEX/PROJECTS/beta/overview/OVERVIEW.md", "Beta.", tag="project/beta")
        note(self.root, "NEOCORTEX/PROJECTS/acme/DATA.md", "Acme data.", tag="project/acme")
        note(self.root, "NEOCORTEX/PROJECTS/beta/DATA.md", "Beta data.", tag="project/beta")
        warnings = []
        check_brain.check_health(sorted(self.root.rglob("*.md")), warnings)
        same = [line for line in warnings if "same note name" in line]
        self.assertEqual(len(same), 1, warnings)
        self.assertIn("across the brain", same[0])
        self.assertIn("NAS.md", same[0])

    def test_knowledge_note_without_sources_warns(self):
        (self.root / "NEOCORTEX/KNOWLEDGE").mkdir(parents=True)
        (self.root / "NEOCORTEX/KNOWLEDGE/RETRIES.md").write_text("---\ntags:\n  - knowledge\nsources:\n  - docs\n---\nx\n", encoding="utf-8")
        note(self.root, "NEOCORTEX/KNOWLEDGE/BACKOFF.md", "y", tag="knowledge")
        warnings = []
        check_brain.check_health(sorted(self.root.rglob("*.md")), warnings)
        self.assertEqual(warnings, ["NEOCORTEX/KNOWLEDGE/BACKOFF.md: knowledge note without sources in its frontmatter"])

    def test_stale_active_hub_warns(self):
        header = "# ACME\nGoal: x · Status: {status} · Updated: 2026-09-01"
        note(self.root, "NEOCORTEX/PROJECTS/acme/ACME.md", header.format(status="active"), tag="project/acme")
        note(self.root, "NEOCORTEX/PROJECTS/beta/BETA.md", header.format(status="paused"), tag="project/beta")
        note(self.root, "NEOCORTEX/PROJECTS/gamma/GAMMA.md", "Goal: x · Status: active", tag="project/gamma")
        warnings = []
        check_brain.check_health(sorted(self.root.rglob("*.md")), warnings, today=check_brain.datetime.date(2026, 10, 8))
        self.assertEqual(sorted(warnings), [
            "NEOCORTEX/PROJECTS/acme/ACME.md: active project hub not updated for 37 days: refresh ## Now or change its Status",
            "NEOCORTEX/PROJECTS/gamma/GAMMA.md: active project hub not updated (no Updated date): refresh ## Now or change its Status",
        ])

    def test_docs_folder_is_skipped(self):
        (self.root / "docs").mkdir()
        (self.root / "docs" / "spec.md").write_text("No tags here.\nSecond plain line.\n", encoding="utf-8")
        code, out = self.run_checks()
        self.assertEqual(code, 0, out)


if __name__ == "__main__":
    unittest.main()
