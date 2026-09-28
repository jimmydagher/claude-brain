---
tags:
  - plan
---
# Brain Anatomy Layout Implementation Plan

> **Status:** Tasks 0-8 executed 2026-09-27. The layout was then revised on 2026-09-28 (THALAMUS into `NEOCORTEX/NEOCORTEX.md`, LIMBIC and AMYGDALA into `PREFRONTAL/PREFRONTAL.md`, links follow the tree); see the spec's Revision section. Paths below describe the first rollout.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize the claude-brain vault into CORTEX (entry) + THALAMUS (router) + NEOCORTEX (shared memory, lobes as tags) + HIPPOCAMPUS (intake) + LIMBIC (personal router AMYGDALA) + PREFRONTAL (all personal memory and projects), and ship a matching Cortex MCP server release.

**Architecture:** Vault work happens on branch `brain-anatomy` in `claude-brain`, one commit per step, each verified by an upgraded `scripts/check_brain.py`. Renames are done by small byte-level Python rewrites so line endings survive. Server work happens on branch `brain-anatomy` in `cortex`: new layout keys, `!` exemptions in the protected list, the router in `cortex_load`, and an audit warning for unprotected layout folders.

**Tech Stack:** Markdown (Obsidian vault), Python 3 stdlib (`check_brain.py`, `unittest`), Python 3.14 + Starlette + MCP SDK + pytest/ruff/mypy (Cortex).

**Spec:** `docs/superpowers/specs/2026-09-27-brain-anatomy-layout-design.md`

## Global Constraints

- Paths: vault root `C:\Users\jdagher\Development\projects\claude-brain`; server repo `C:\Users\jdagher\Development\projects\cortex`. Run commands from the repo root of the task's repo (Git Bash).
- Every vault note starts with `tags` frontmatter; no hard wraps (a paragraph or list item is one line); no em dashes; wikilinks carry the vault path (`[[NEOCORTEX/CODING|CODING]]`, `[[NEOCORTEX/CODING\|CODING]]` in tables).
- File rewrites read and write bytes (`read_bytes().decode("utf-8")` / `write_bytes(...encode("utf-8"))`) so LF endings are kept.
- Never stage a personal file: everything in `LIMBIC/` and `PREFRONTAL/` except `LIMBIC/LIMBIC.md` and `PREFRONTAL/PREFRONTAL.md`, plus `HIPPOCAMPUS/SYNAPSE.md`, `HIPPOCAMPUS/ENGRAM.md`, `.remember/`.
- `MEMORY/CODING.md` carries a local, uncommitted personal line. Task 0 saves it as a patch and reverts it; Task 9 reapplies it to `NEOCORTEX/CODING.md`. It is never committed. Interactive git (`git add -p`, `-i`) is unavailable: stage whole files only.
- ENGRAM is history: never rewrite `HIPPOCAMPUS/ENGRAM.md` entries.
- Cortex: `python scripts/python/check.py` (ruff, mypy strict, pytest) must pass before each commit; every user- or operator-visible change adds a bullet to `CHANGELOG.md` › 🚧 Unreleased; never touch the human's uncommitted GUI work.
- Commits end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- No push, merge to `main`, release or NAS deploy without the human's explicit yes in chat.
- The Claude Code hook in `claude-brain/.claude/settings.json` runs `check_brain.py` after every write; errors it prints mid-task are expected until the task's verify step.

## Review Focus

- Untracked personal files lost or left behind by the move: expect every file from `CEREBELLUM/` and `PROJECTS/` to reappear under `LIMBIC/` or `PREFRONTAL/`. Pinned by Task 4 Step 7 (file-count comparison against the backup).
- Project hub writes refused after projects move under the protected `PREFRONTAL/`: expect `cortex_write` on `PREFRONTAL/PROJECTS/...` to succeed. Pinned by Task 7 test `test_projects_are_writable_inside_the_protected_personal_layer`.
- A deployed server keeping its old protected list (`MEMORY/`, `CEREBELLUM/`) so NEOCORTEX is silently writable: expect `cortex_check` to warn. Pinned by Task 9 test `test_check_warns_when_a_layout_folder_is_unprotected`.
- Bare-name links hitting two notes (`[[BUSINESS]]` exists in NEOCORTEX and in a project): expect an error. Pinned by Task 1 test `test_ambiguous_bare_link_is_an_error`.
- Personal content leaking into the public repo (a tracked note linking into PREFRONTAL, or a personal file staged): expect a checker error and `git check-ignore` to cover every personal file. Pinned by Task 1 test `test_tracked_note_linking_personal_note_is_an_error` and Task 4 Step 8.

---

### Task 0: Preflight (human decisions, backup, branches)

**Files:** none changed in the repos.

- [ ] **Step 1: Ask the human about uncommitted work (one message)**

Current uncommitted changes in `claude-brain`: `CORTEX.md` (adds Behavior rule 16 "Persona check"), `MEMORY/LEARNING.md` (drops the `> #think` line), `MEMORY/CODING.md` (personal line, stays local), `.obsidian/app.json`, `.obsidian/appearance.json`, `.obsidian/graph.json`. In `cortex`: GUI graph-options work (`CHANGELOG.md`, `src/cortex/static/*`, `src/cortex/web.py`, `tests/test_app.py`, untracked `Waiting`). Ask: (a) commit the CORTEX and LEARNING edits on `main` first? (recommended: yes); (b) commit the `.obsidian` changes? (c) commit the Cortex GUI work before the server branch starts? Wait for answers; do what they say.

- [ ] **Step 2: Back up untracked personal files**

```bash
BACKUP="/c/Users/jdagher/Development/projects/_backup/claude-brain-personal-2026-09-27"
mkdir -p "$BACKUP"
cp -a CEREBELLUM PROJECTS HIPPOCAMPUS "$BACKUP"/
find "$BACKUP" -name "*.md" | wc -l
```

- Expected: a count equal to `find CEREBELLUM PROJECTS HIPPOCAMPUS -name "*.md" | wc -l` in the vault. Write both numbers in the task log.

- [ ] **Step 3: Set aside the local CODING.md line**

```bash
git diff MEMORY/CODING.md > "$BACKUP/coding-local.patch"
git checkout -- MEMORY/CODING.md
git status --short MEMORY/CODING.md
```

- Expected: the patch file is non-empty and `git status` shows nothing for `MEMORY/CODING.md`.

- [ ] **Step 3b: Ask the human to close Obsidian**, so it doesn't rewrite links during moves. Wait for confirmation.

- [ ] **Step 4: Create the vault branch**

```bash
git switch -c brain-anatomy
```

---

### Task 1: check_brain.py: new link checks and docs exclusion

**Files:**
- Modify: `scripts/check_brain.py`
- Create: `scripts/test_check_brain.py`
- Modify: `.obsidian/app.json`

**Interfaces:**
- Produces: `check_brain.is_personal(key: str) -> bool`; `check_note(path, slop, index, errors, warnings, linked: set[str])`; new error texts `ambiguous link [[X]]` and `tracked note links to personal note [[X]]`; warning text `orphan: no note links here`; `docs/` skipped.

- [ ] **Step 1: Write the failing tests**

Create `scripts/test_check_brain.py`:

```python
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
```

- [ ] **Step 2: Run the tests to verify they fail**

- Run: `python -m unittest discover -s scripts -p "test_*.py" -v`
- Expected: FAIL or ERROR. `test_clean_vault_passes` errors with `AttributeError: '_io.StringIO' object has no attribute 'reconfigure'`; the new-check tests fail on missing messages.

- [ ] **Step 3: Implement**

In `scripts/check_brain.py`:

1. Update the docstring's Errors/Warnings lines to:

```text
Errors: dead wikilinks and heading links, ambiguous bare-name links, tracked notes linking to personal notes, hard wraps, em dashes, chatbot residue, missing tags, SYNAPSE IDs.
Warnings: slop-list hits (they mark a passage to test, not a verdict), repeated long lines, orphan notes and personal sections over the size cap.
```

2. Replace the constants block's `SKIP_DIRS` line and add three constants after `HIPPOCAMPUS = ...`:

```python
SKIP_DIRS = {".obsidian", ".trash", ".git", ".claude", ".remember", "scripts", "docs"}
```

```python
PERSONAL = ("limbic/", "prefrontal/")
PERSONAL_GUIDES = {"limbic/limbic", "prefrontal/prefrontal"}
ROOTS = {"cortex", "readme", "limbic/amygdala", "hippocampus/synapse", "hippocampus/engram"}
```

3. Add after `rel()`:

```python
def is_personal(key):
    """Whether a lowercase vault key (path without .md) is an untracked personal note."""
    return key.startswith(PERSONAL) and key not in PERSONAL_GUIDES
```

4. Replace `check_note` with:

```python
def check_note(path, slop, index, errors, warnings, linked):
    name = rel(path)
    lines = path.read_text(encoding="utf-8").splitlines()
    front = frontmatter(lines)
    if name not in UNTAGGED_OK and not (front and any(line.startswith("tags:") for line in front)):
        errors.append(f"{name}:1: missing tags frontmatter")
    paths, names, heads = index
    own = name[:-3].lower()
    tracked = not is_personal(own) and name not in HIPPOCAMPUS
    prev_plain = False
    for n, text, section in body(lines):
        plain = bool(text.strip()) and not BLOCK.match(text)
        if plain and prev_plain:
            errors.append(f"{name}:{n}: hard wrap: join this line with the one above")
        prev_plain = plain
        for target, heading in LINK.findall(text):
            key = target.strip().lower().removesuffix(".md")
            found = ([key] if key in paths else []) if "/" in key else names.get(key, [])
            if not found:
                errors.append(f"{name}:{n}: dead link [[{target.strip()}]]")
                continue
            if "/" not in key and len(found) > 1:
                errors.append(f"{name}:{n}: ambiguous link [[{target.strip()}]] matches {', '.join(sorted(found))}: use the full path")
            if tracked and any(is_personal(f) for f in found):
                errors.append(f"{name}:{n}: tracked note links to personal note [[{target.strip()}]]: only AMYGDALA points into PREFRONTAL")
            linked.update(f for f in found if f != own)
            if heading and not heading.startswith("^") and not any(heading.strip().lower() in heads[f] for f in found):
                errors.append(f"{name}:{n}: dead heading link [[{target.strip()}#{heading.strip()}]]")
        if "—" in text:
            errors.append(f"{name}:{n}: em dash")
        residue = RESIDUE.search(text)
        if residue:
            errors.append(f"{name}:{n}: chatbot residue '{residue.group(0)}'")
        if slop and not re.match("Avoid|Slop list", section):
            hit = slop.search(QUOTED.sub("", text))
            if hit:
                warnings.append(f"{name}:{n}: slop marker '{hit.group(0)}': test the passage, don't auto-cut")
```

5. Add after `check_repeats`:

```python
def check_orphans(files, linked, warnings):
    """Warn about notes no other note links to (roots excepted)."""
    for path in files:
        key = rel(path)[:-3].lower()
        if key not in linked and key not in ROOTS:
            warnings.append(f"{rel(path)}: orphan: no note links here")
```

6. In `main()`: replace the reconfigure loop and wire the new pieces:

```python
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
```

```python
    errors, warnings, linked = [], [], set()
    slop, index = slop_pattern(), build_index()
    for path in files:
        check_note(path, slop, index, errors, warnings, linked)
    if not hook or rel(files[0]) in HIPPOCAMPUS:
        check_ids(errors)
    if not hook and not args:
        check_repeats(warnings)
        check_orphans(files, linked, warnings)
        check_cerebellum(warnings)
```

- [ ] **Step 4: Run the tests to verify they pass**

- Run: `python -m unittest discover -s scripts -p "test_*.py" -v`
- Expected: 7 tests, OK.

- [ ] **Step 5: Exclude docs/ from Obsidian**

Set `.obsidian/app.json` to include the key (keep any other keys the file has):

```json
{
  "userIgnoreFilters": ["docs/"]
}
```

- [ ] **Step 6: Run the checker on the real vault**

- Run: `python scripts/check_brain.py`
- Expected: `0 errors`. Orphan warnings are allowed at this stage (for example `PROJECTS/INDEX.md`, which gains a link from AMYGDALA in Task 4); list them in the task log.

- [ ] **Step 7: Commit**

```bash
git add scripts/check_brain.py scripts/test_check_brain.py .obsidian/app.json
git commit -m "Check ambiguous, personal and orphan links; skip docs/

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

(Task 0 settled the human's own `app.json` changes: committed first, or reverted, so only `userIgnoreFilters` is new here.)

---

### Task 2: MEMORY/ → NEOCORTEX/

**Files:**
- Move: `MEMORY/*.md` → `NEOCORTEX/*.md`
- Modify: every vault `.md` that mentions `MEMORY` (except `HIPPOCAMPUS/ENGRAM.md` and `docs/`), `scripts/check_brain.py`

**Interfaces:**
- Produces: area files at `NEOCORTEX/<AREA>.md`; `check_brain.py` reads `NEOCORTEX/WRITING.md` for the slop list.

- [ ] **Step 1: Move the folder**

```bash
git mv MEMORY NEOCORTEX
```

- Expected: `git status` shows 18 renames; `NEOCORTEX/CODING.md` keeps its unstaged local line.

- [ ] **Step 2: Rewrite every uppercase MEMORY word**

Every uppercase `MEMORY` in the vault is the folder name (checked 2026-09-27), so a word-boundary rewrite is safe:

```bash
python - <<'EOF'
import re
from pathlib import Path
SKIP = {".git", ".obsidian", ".remember", ".trash", "docs"}
files = [p for p in Path(".").rglob("*.md") if not SKIP & set(p.parts) and p.as_posix() != "HIPPOCAMPUS/ENGRAM.md"]
files.append(Path("scripts/check_brain.py"))
for p in files:
    text = p.read_bytes().decode("utf-8")
    new = re.sub(r"\bMEMORY\b", "NEOCORTEX", text)
    if new != text:
        p.write_bytes(new.encode("utf-8"))
        print("rewrote", p.as_posix())
EOF
```

- [ ] **Step 3: Verify**

- Run: `python scripts/check_brain.py`
- Expected: `0 errors`.

- Run: `grep -rn "MEMORY" --include=*.md --include=*.py . --exclude-dir=.remember --exclude-dir=docs --exclude-dir=.git | grep -v "HIPPOCAMPUS/ENGRAM.md"`
- Expected: no output.

- [ ] **Step 4: Commit**

```bash
git add -A NEOCORTEX
git add CORTEX.md README.md HIPPOCAMPUS/HIPPOCAMPUS.md CEREBELLUM/CEREBELLUM.md scripts/check_brain.py
git status --short
git commit -m "Rename MEMORY to NEOCORTEX

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

Before committing, `git status --short` must show no file under `PROJECTS/`, `CEREBELLUM/` other than the guide, or `HIPPOCAMPUS/` other than the guide.

---

### Task 3: Split CORTEX into CORTEX + THALAMUS

**Files:**
- Create: `THALAMUS.md`
- Modify: `CORTEX.md`, `NEOCORTEX/MECHANICS.md`, `NEOCORTEX/PROJECTS.md`, `CEREBELLUM/CEREBELLUM.md`

**Interfaces:**
- Produces: headings `THALAMUS#Routing Rules`, `THALAMUS#Routing Table`, `CORTEX#Conflicts`, `CORTEX#Behavior`, `CORTEX#Brain Upkeep` (links in later tasks target these).

- [ ] **Step 1: Create THALAMUS.md**

Create `THALAMUS.md` with this header and rules, then paste the `## Routing Table` section (heading, blank line, and the whole table) cut from `CORTEX.md` in Step 2 at the end:

```markdown
---
tags:
  - memory/core
---
# THALAMUS

The **router**: it tells you where to go, not what to know. The linked files tell you what to do. It loads with [[CORTEX|CORTEX]], once per session.

**Do not read everything.** Identify the task, then read **only the relevant instruction file(s)**.

## Routing Rules
1. Identify the **primary intent**.
2. Go directly to its instruction file.
3. Inform the human which part of the brain (memory) you are using, as your first line: `Brain: CODING + SECURITY`. Multiple sections is ok to use **if required by the intent**.
4. Read additional files **only when required**: at most 3 brain files besides CORTEX, THALAMUS and the personal map before answering.
5. Follow links from that file when deeper context is needed: one hop, no chains. Personal layer: if `CEREBELLUM/MAP.md` exists, it loads with CORTEX and THALAMUS; load only the sections it lists for the task's area (and its `Always` ones); they don't count toward the 3-file cap. No map: skip. Rules: [[CEREBELLUM/CEREBELLUM|CEREBELLUM]].
6. Do not load unrelated knowledge. Don't re-read a file already loaded this session unless it changed or the human says "reload the brain".
7. Prefer existing knowledge over creating duplicates.
8. When creating knowledge, add appropriate `[[wikilinks]]`.
```

- [ ] **Step 2: Rewrite the top of CORTEX.md and cut the table**

In `CORTEX.md`, replace everything from the line starting `This is the **routing file**` down to, but not including, `## Always-on Rules` with:

```markdown
This is the **entrypoint**: the rules that apply to every task and how the brain changes. Where each task goes is [[THALAMUS|THALAMUS]], the router; the files it links to tell you what to do.

Load this file once per session, when the human says "use the cortex" or "use your brain"; it then applies to every task in that session. Loading also reads THALAMUS and, when it exists, the personal map (`CEREBELLUM/MAP.md`). How loading works: [[NEOCORTEX/MECHANICS|MECHANICS]].

## Conflicts
The human's latest message > project note > CEREBELLUM > area file > this file and THALAMUS, except the Token economy rules, which only the human can relax. CEREBELLUM overrides an area's Defaults, never its Core Rules, a standard, the Token economy rules or rule 14. Point out the conflict so it gets fixed.

```

Then cut the whole `## Routing Table` section (heading through the last table row) out of `CORTEX.md` and paste it at the end of `THALAMUS.md`. `## Always-on Rules` (rules 1-16, including local rule 16) and `## Brain Upkeep` stay unchanged.

- [ ] **Step 3: Turn numbered cross-file references into heading links**

In `NEOCORTEX/MECHANICS.md`:
- RULE#1: `Then read \`CORTEX.md\` once` → `Then read \`CORTEX.md\` and \`THALAMUS.md\` once`.
- RULE#3: `Re-read CORTEX and the area files in use` → `Re-read CORTEX, THALAMUS and the area files in use`.
- Session: `Per-task announcements follow CORTEX rule 3` → `Per-task announcements follow [[THALAMUS#Routing Rules|THALAMUS › Routing Rules]] (rule 3)`.
- Avoid: `use wikilinks (CORTEX rule 8)` → `use wikilinks ([[THALAMUS#Routing Rules|THALAMUS › Routing Rules]], rule 8)`.

In `NEOCORTEX/PROJECTS.md`: `(CORTEX rule 9)` → `([[CORTEX#Conflicts|CORTEX › Conflicts]])`.

In `CEREBELLUM/CEREBELLUM.md`: `the guardrails in CORTEX rule 14` → `the guardrails in [[CORTEX#Behavior|CORTEX › Behavior]] (rule 14)`; `It doesn't count toward CORTEX's 3-file cap.` → `It doesn't count toward the 3-file cap in [[THALAMUS#Routing Rules|THALAMUS › Routing Rules]].`

- [ ] **Step 4: Verify**

- Run: `python scripts/check_brain.py`
- Expected: `0 errors`.

- Run: `grep -rnE "CORTEX('s)? rule|CORTEX's 3-file" --include=*.md . --exclude-dir=.remember --exclude-dir=docs`
- Expected: no output.

- [ ] **Step 5: Commit**

```bash
git add THALAMUS.md CORTEX.md NEOCORTEX/MECHANICS.md NEOCORTEX/PROJECTS.md CEREBELLUM/CEREBELLUM.md
git commit -m "Split routing out of CORTEX into THALAMUS

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

If the human chose in Task 0 not to commit rule 16 separately, it is committed here with the rewrite; tell the human.

---

### Task 4: Personal layer: LIMBIC, AMYGDALA, PREFRONTAL

**Files:**
- Create: `LIMBIC/LIMBIC.md` (tracked), `PREFRONTAL/PREFRONTAL.md` (tracked)
- Move (untracked): `CEREBELLUM/MAP.md` → `LIMBIC/AMYGDALA.md`; `CEREBELLUM/<topic>.md` → `PREFRONTAL/<topic>.md`; `PROJECTS/` → `PREFRONTAL/PROJECTS/`; `PREFRONTAL/PROJECTS/INDEX.md` → `PREFRONTAL/PROJECTS/PROJECTS.md`
- Delete: `CEREBELLUM/CEREBELLUM.md`, `NEOCORTEX/PROJECTS.md`
- Modify: `.gitignore`, `scripts/check_brain.py`, and every note the rewrite touches

**Interfaces:**
- Consumes: `THALAMUS#Routing Rules`, `CORTEX#Conflicts`, `CORTEX#Behavior`, `CORTEX#Brain Upkeep` (Task 3).
- Produces: `LIMBIC/LIMBIC.md` headings `Core Rules (non-negotiable)`, `Where a lesson goes`, `AMYGDALA`; `PREFRONTAL/PREFRONTAL.md` headings `Preferences`, `Projects`, `Hub template`; AMYGDALA heading `Projects`.

- [ ] **Step 1: Move the untracked files**

```bash
mkdir -p LIMBIC PREFRONTAL
mv CEREBELLUM/MAP.md LIMBIC/AMYGDALA.md
for f in CEREBELLUM/*.md; do [ "$f" = "CEREBELLUM/CEREBELLUM.md" ] || mv "$f" PREFRONTAL/; done
mv PROJECTS PREFRONTAL/PROJECTS
mv PREFRONTAL/PROJECTS/INDEX.md PREFRONTAL/PROJECTS/PROJECTS.md
```

- [ ] **Step 2: Rewrite references across the vault**

Ordered replacements over every vault note except ENGRAM, `docs/`, and the two guides written in Step 3:

```bash
python - <<'EOF'
import re
from pathlib import Path
SKIP = {".git", ".obsidian", ".remember", ".trash", "docs"}
KEEP = {"HIPPOCAMPUS/ENGRAM.md", "CEREBELLUM/CEREBELLUM.md", "NEOCORTEX/PROJECTS.md"}
RULES = [
    (r"\[\[NEOCORTEX/PROJECTS(\\?)\|PROJECTS\]\]", r"[[PREFRONTAL/PREFRONTAL\1|PREFRONTAL]]"),
    (r"CEREBELLUM/MAP", "LIMBIC/AMYGDALA"),
    (r"\[\[CEREBELLUM/CEREBELLUM(\\?)\|CEREBELLUM\]\]", r"[[LIMBIC/LIMBIC\1|LIMBIC]]"),
    (r"CEREBELLUM/CEREBELLUM", "LIMBIC/LIMBIC"),
    (r"CEREBELLUM/", "PREFRONTAL/"),
    (r"\bCEREBELLUM\b", "PREFRONTAL"),
    (r"(?<![A-Za-z/])PROJECTS/INDEX\.md", "PREFRONTAL/PROJECTS/PROJECTS.md"),
    (r"\[\[Projects/", "[[PREFRONTAL/PROJECTS/"),
    (r"(?<![A-Za-z/])PROJECTS/", "PREFRONTAL/PROJECTS/"),
    (r"\[\[ARIEL\]\]", "[[PREFRONTAL/PROJECTS/Cornerstone/ARIEL|ARIEL]]"),
    (r"\[\[WEBSITE\]\]", "[[PREFRONTAL/PROJECTS/Flammeau/WEBSITE|WEBSITE]]"),
]
for p in Path(".").rglob("*.md"):
    if SKIP & set(p.parts) or p.as_posix() in KEEP:
        continue
    text = p.read_bytes().decode("utf-8")
    new = text
    for pattern, repl in RULES:
        new = re.sub(pattern, repl, new)
    if new != text:
        p.write_bytes(new.encode("utf-8"))
        print("rewrote", p.as_posix())
EOF
```

Then in `scripts/check_brain.py` rename `check_cerebellum` to `check_prefrontal` (both the def and the call), change its docstring to `"""Warn when a PREFRONTAL preference section outgrows the cap: it splits into its own file."""`, its loop to `for path in sorted((ROOT / "PREFRONTAL").glob("*.md")):` and its skip to `if path.name == "PREFRONTAL.md":`, and the docstring's `personal sections over the size cap` stays.

- [ ] **Step 3: Write the two tracked guides**

Create `LIMBIC/LIMBIC.md` from `CEREBELLUM/CEREBELLUM.md` with these changes, then delete the old guide:
- Tags stay `memory/personal`. Scope line becomes: `> Scope: the human's own layer: who owns it, where a lesson goes, and how AMYGDALA routes to it · Storage: [[PREFRONTAL/PREFRONTAL|PREFRONTAL]] · Process: [[CORTEX#Brain Upkeep|CORTEX › Brain Upkeep]]`
- RULE#1 body: `Preferences reach PREFRONTAL, and rows reach AMYGDALA, only through SYNAPSE (see [[HIPPOCAMPUS/HIPPOCAMPUS|HIPPOCAMPUS]]), and only the human approves them. The AI proposes and previews; it never edits them outside a commit the human asked for. Project hubs are the exception: their state is written directly ([[PREFRONTAL/PREFRONTAL#Projects|PREFRONTAL › Projects]]).`
- RULE#2 table Home column: Standard → `SDSI or the team standard`; Universal rule → `a NEOCORTEX area file`; Me, all projects → `a PREFRONTAL topic file`; One project → `the project hub in PREFRONTAL/PROJECTS`; One machine → `PREFRONTAL, environment file`.
- RULE#3 keeps the `[[CORTEX#Behavior|CORTEX › Behavior]] (rule 14)` link from Task 3.
- Delete RULE#4 (it moves to PREFRONTAL › Preferences); renumber old RULE#5 to RULE#4 with body: `Everything in LIMBIC and PREFRONTAL except their guides is untracked by git, so the public repo stays generic. No tracked file links to a personal file, names a personal topic or quotes a personal entry; AMYGDALA is the only index into PREFRONTAL.`
- `## Where a lesson goes`: unchanged except test 1 reads `Yes: NEOCORTEX. No: PREFRONTAL.` and the last line reads: `The destination goes in the SYNAPSE entry: \`→ CODING\` for global, \`→ PREFRONTAL/ENVIRONMENT#CODING\` for personal.`
- Replace `## Files and links` with:

```markdown
## AMYGDALA
`LIMBIC/AMYGDALA.md` is the personal router. It loads with CORTEX and THALAMUS, once per session, if it exists; no AMYGDALA (a fresh clone): skip silently.
- One `##` section per area, named exactly like the area file (`## CODING`), each a list of deep links: `- [[PREFRONTAL/ENVIRONMENT#CODING|ENVIRONMENT › CODING]]`. Several areas may point into the same file.
- `## Always` lists cross-cutting sections (persona, mood, mindset) that load with AMYGDALA. Keep them very short: they load every session.
- `## Projects` holds one link, to `PREFRONTAL/PROJECTS/PROJECTS.md`, the project list.
- Load only the sections listed for the task's area; they don't count toward the 3-file cap in [[THALAMUS#Routing Rules|THALAMUS › Routing Rules]].
- A new PREFRONTAL file or section adds its AMYGDALA row in the same commit.
```

- `## Avoid`: `A personal choice stored in a NEOCORTEX area file, or a universal rule stored in PREFRONTAL.`; `Loading a whole PREFRONTAL file when one section was linked.`; keep the secrets and `## MACHINE` bullets.

Create `PREFRONTAL/PREFRONTAL.md`:

```markdown
---
tags:
  - memory/personal
---
> Scope: working memory: the human's preferences and active projects · Router: AMYGDALA (`LIMBIC/AMYGDALA.md`) · Rules and scope ladder: [[LIMBIC/LIMBIC|LIMBIC]] · Process: [[CORTEX#Brain Upkeep|CORTEX › Brain Upkeep]]

Everything here except this guide is personal and untracked by git; a fresh clone has none of it.

## Preferences
- Files are named by topic (`ENVIRONMENT`, `STYLE`, `PERSONA`, `MINDSET`), not mirrored from the areas. A file exists only after SYNAPSE has routed an entry to it.
- One `##` section per area inside a file, named exactly like the area (`## CODING`). New entries append to that section.
- Facts shared by many areas live once in a small `## MACHINE` section, not repeated.
- Read only the section AMYGDALA lists for the task's area, never the whole file.
- Preferences change only through SYNAPSE; a new file or section adds its AMYGDALA row in the same commit, and no tracked file changes.
- Section names are part of the link contract. Rename them in Obsidian or with `rename_heading` so links update; the audit flags dead heading links.
- A section over ~150 lines splits into its own file; only the link target changes.

## Projects
Project hubs are working memory: written directly, not through SYNAPSE. The project list is `PREFRONTAL/PROJECTS/PROJECTS.md`. Missing? The human has no projects yet: use the template below. Pairs with: [[NEOCORTEX/PLANNING|PLANNING]], [[NEOCORTEX/KNOWLEDGE|KNOWLEDGE]]
1. A project note overrides general area rules for that project ([[CORTEX#Conflicts|CORTEX › Conflicts]]).
2. Changing state lives in the hub (status, decisions, next actions); stable how-to rules live in NEOCORTEX.
3. Log decisions in the hub as `YYYY-MM-DD: decision (why)`, newest last.
4. Code projects: `/sdsi:core` ([[NEOCORTEX/CODING|CODING]] RULE#1).
5. New project: create `PREFRONTAL/PROJECTS/<Name>/<NAME>.md` from the template below, tag it and its sub-notes `project/<name>`, and add a row to `PREFRONTAL/PROJECTS/PROJECTS.md`. Link sub-notes by full path (`[[PREFRONTAL/PROJECTS/<Name>/<NOTE>|NOTE]]`).
6. Every hub has a `## Now` section (8 lines max): where things stand and the next step. Read it first when resuming; rewrite it on "wrap up".
```

Then append a `## Hub template` section copied verbatim from `NEOCORTEX/PROJECTS.md` (the heading and its fenced `markdown` block). Then:

```bash
git rm -q CEREBELLUM/CEREBELLUM.md NEOCORTEX/PROJECTS.md
rmdir CEREBELLUM
```

- [ ] **Step 4: Rewrite AMYGDALA and the project list**

`LIMBIC/AMYGDALA.md` (untracked; keep any `##` sections and rows it already has, below the comment):

```markdown
---
tags:
  - memory/personal
---
> Which PREFRONTAL sections to load, by area. Loads with CORTEX and THALAMUS; load only the listed sections. Rules: [[LIMBIC/LIMBIC|LIMBIC]]

<!-- Format: one ## section per area, named like the area file (CODING, WRITING…); "Always" loads with this router; "Projects" links the project list. Row: `- [[PREFRONTAL/FILE#Section|FILE › Section]]` -->

## Projects
- [[PREFRONTAL/PROJECTS/PROJECTS|PROJECTS]]
```

In `PREFRONTAL/PROJECTS/PROJECTS.md` the header line should now read `> Your project list: not tracked by git. Rules and the hub template: [[PREFRONTAL/PREFRONTAL|PREFRONTAL]]` and the hub links `[[PREFRONTAL/PROJECTS/<Name>/<NAME>\|<NAME>]]` (Step 2 did this; fix by hand if not).

- [ ] **Step 5: Update .gitignore**

Replace the personal-layer block (from `# Personal layers:` through `.remember/`) with:

```text
# Personal layers: live in the vault, never in the public repo (the LIMBIC and PREFRONTAL guides stay: they are generic)
LIMBIC/*
!LIMBIC/LIMBIC.md
PREFRONTAL/*
!PREFRONTAL/PREFRONTAL.md
.remember/
```

- [ ] **Step 6: Verify links**

- Run: `python scripts/check_brain.py`
- Expected: `0 errors`. No orphan warning for `PREFRONTAL/PROJECTS/PROJECTS.md` or `LIMBIC/LIMBIC.md`.

- Run: `grep -rnE "CEREBELLUM|MAP\.md|INDEX\.md|NEOCORTEX/PROJECTS" --include=*.md --include=*.py . --exclude-dir=.remember --exclude-dir=docs --exclude-dir=.git | grep -v "HIPPOCAMPUS/ENGRAM.md"`
- Expected: no output.

- [ ] **Step 7: Verify no personal file was lost**

```bash
BACKUP="/c/Users/jdagher/Development/projects/_backup/claude-brain-personal-2026-09-27"
echo "before: $(find "$BACKUP/CEREBELLUM" "$BACKUP/PROJECTS" -name '*.md' ! -name CEREBELLUM.md | wc -l)"
echo "after:  $(find LIMBIC/AMYGDALA.md PREFRONTAL -name '*.md' ! -name PREFRONTAL.md | wc -l)"
```

- Expected: equal counts.

- [ ] **Step 8: Verify git ignores every personal file**

```bash
find LIMBIC PREFRONTAL -name "*.md" ! -name LIMBIC.md ! -name PREFRONTAL.md | git check-ignore --stdin -v | wc -l
find LIMBIC PREFRONTAL -name "*.md" ! -name LIMBIC.md ! -name PREFRONTAL.md | wc -l
git status --short
```

- Expected: the two counts are equal; `git status` lists only `.gitignore`, `LIMBIC/LIMBIC.md`, `PREFRONTAL/PREFRONTAL.md`, deletions of `CEREBELLUM/CEREBELLUM.md` and `NEOCORTEX/PROJECTS.md`, `scripts/check_brain.py` and tracked notes the rewrite touched.

- [ ] **Step 9: Commit**

```bash
git add .gitignore LIMBIC/LIMBIC.md PREFRONTAL/PREFRONTAL.md scripts/check_brain.py CORTEX.md THALAMUS.md README.md HIPPOCAMPUS/HIPPOCAMPUS.md
git add -u NEOCORTEX CEREBELLUM
git commit -m "Move the personal layer to LIMBIC (AMYGDALA router) and PREFRONTAL

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: Lobes, MECHANICS and README

**Files:**
- Create: `NEOCORTEX/NEOCORTEX.md`
- Modify: `THALAMUS.md` (routing table), `NEOCORTEX/MECHANICS.md` (Session, Tags), `README.md`, `CORTEX.md` (rule 14 wording)

- [ ] **Step 1: Create NEOCORTEX/NEOCORTEX.md**

```markdown
---
tags:
  - memory/core
---
> Scope: long-term shared memory: what a lobe is and the shape area files share · Index: [[THALAMUS#Routing Table|THALAMUS › Routing Table]] · Process: [[CORTEX#Brain Upkeep|CORTEX › Brain Upkeep]]

## Lobes
- A lobe is a family of areas that serve the same kind of task. It is a tag, not a folder: every area file sits directly in `NEOCORTEX/`, so moving an area to another lobe is a one-tag edit and no link breaks.
- Membership is listed in one place only: THALAMUS's routing table.
- Each area has one home lobe, the one whose tasks it serves most often. Never copy a file into a second lobe.
- Cross-lobe connections are the `Pairs with` wikilinks in each area's scope line: the synapses between lobes. An area that often works with another adds it there.
- A new area joins an existing lobe: a new lobe would need a sixth graph color, which can't be told apart from the other five in both themes.

| Lobe | Tag | Covers | Graph color |
| --- | --- | --- | --- |
| Core | `memory/core` | the brain itself: loading, Markdown, prompts and rules | blue `#2a78d6` |
| Technical | `memory/technical` | build, operate, secure, data | green `#008300` |
| Thinking | `memory/thinking` | reason, plan, research, review, learn, file knowledge | aqua `#1baf7a` |
| Communication | `memory/communication` | write, translate, design, sell, converse | gold `#c98500` |

## Area file shape
- `tags` frontmatter with the area's lobe tag.
- A scope line: `> Scope: … · Pairs with: [[NEOCORTEX/X|X]], …`.
- `## Core Rules (non-negotiable)` with `### RULE#n` headings, then `## Defaults` (PREFRONTAL preferences may override these), `## Avoid` and `## Output`. Reference areas such as MECHANICS may replace Defaults and Output with their own sections.
- Under ~80 lines. Corrections don't pile up as add-ons: committing one rewrites the rule it changes.
```

- [ ] **Step 2: Regroup THALAMUS's routing table by lobe**

Replace the whole `## Routing Table` section of `THALAMUS.md` with:

```markdown
## Routing Table
Areas live in [[NEOCORTEX/NEOCORTEX|NEOCORTEX]], grouped into lobes; a lobe is a tag family, not a folder.

### Core lobe
|     | Task (Memory)          | Load when the task is about…                               | Go To                                |
| --- | ---------------------- | ---------------------------------------------------------- | ------------------------------------ |
| 🧩  | Prompts \| skills      | prompts, skills, agents, CLAUDE.md, rules for this brain   | [[NEOCORTEX/PROMPTING\|PROMPTING]]   |
| 🔧  | Mechanics \| Markdown  | writing any .md file; how the brain loads, caches, reloads | [[NEOCORTEX/MECHANICS\|MECHANICS]]   |

### Technical lobe
|     | Task (Memory)          | Load when the task is about…                               | Go To                                |
| --- | ---------------------- | ---------------------------------------------------------- | ------------------------------------ |
| 💻  | Code \| technical      | writing, fixing, debugging or refactoring code and scripts | [[NEOCORTEX/CODING\|CODING]]         |
| 🤖  | Agents \| tools \| MCP | multi-step autonomous work, tool use, subagents, MCP       | [[NEOCORTEX/AUTOPILOT\|AUTOPILOT]]   |
| 🛡️ | Security \| safety     | secrets, permissions, destructive actions, untrusted input | [[NEOCORTEX/SECURITY\|SECURITY]]     |
| 📊  | Data \| analysis       | datasets, SQL, metrics, statistics, spreadsheets           | [[NEOCORTEX/ANALYTICS\|ANALYTICS]]   |

### Thinking lobe
|     | Task (Memory)              | Load when the task is about…                            | Go To                                |
| --- | -------------------------- | ------------------------------------------------------- | ------------------------------------ |
| 🧠  | Thinking \| decisions      | choosing between options, trade-offs, "should I…"       | [[NEOCORTEX/THINKING\|THINKING]]     |
| 📋  | Planning \| projects       | turning goals into briefs, specs, roadmaps, task lists  | [[NEOCORTEX/PLANNING\|PLANNING]]     |
| 🔎  | Research \| investigation  | finding, verifying or comparing information and sources | [[NEOCORTEX/RESEARCH\|RESEARCH]]     |
| 🔄  | Review \| reflection       | critiquing a draft, plan or code; retros; feedback      | [[NEOCORTEX/REVIEW\|REVIEW]]         |
| 📚  | Knowledge \| summarization | summarizing, extracting, filing notes in this vault     | [[NEOCORTEX/KNOWLEDGE\|KNOWLEDGE]]   |
| 🎓  | Learning \| teaching       | "teach me", tutoring, quizzes, study plans              | [[NEOCORTEX/LEARNING\|LEARNING]]     |

### Communication lobe
|     | Task (Memory)             | Load when the task is about…                         | Go To                                |
| --- | ------------------------- | ---------------------------------------------------- | ------------------------------------ |
| ✍️  | Writing \| communication  | emails, docs, posts, messages, editing prose         | [[NEOCORTEX/WRITING\|WRITING]]       |
| 🌐  | Translation \| language   | translating, localizing, proofreading                | [[NEOCORTEX/LANGUAGE\|LANGUAGE]]     |
| 🖼️ | Images \| visual          | image prompts, diagrams, UI/web design, slides, video | [[NEOCORTEX/VISUAL\|VISUAL]]        |
| 💼  | Business \| marketing     | strategy, marketing copy, sales outreach, product specs | [[NEOCORTEX/BUSINESS\|BUSINESS]]  |
| 💬  | Conversation \| assistant | general questions and advice; anything unmatched     | [[NEOCORTEX/ASSISTANT\|ASSISTANT]]   |

## Outside the neocortex
|     | Task                | Load when the task is about…                          | Go To                                    |
| --- | ------------------- | ----------------------------------------------------- | ---------------------------------------- |
| 📈  | Projects            | anything tied to a named project                      | [[PREFRONTAL/PREFRONTAL\|PREFRONTAL]], then the hub through AMYGDALA's `## Projects` |
| 👤  | Personal layer      | where a lesson goes; the human's own preferences      | [[LIMBIC/LIMBIC\|LIMBIC]]                |
```

Before replacing, confirm every row's "Load when" text matches the current table (copy the current wording if it differs).

- [ ] **Step 3: Update MECHANICS Session and Tags**

In `NEOCORTEX/MECHANICS.md`, the Session `- Order:` bullet becomes:

```markdown
- Order: CORTEX, THALAMUS and AMYGDALA first (one `cortex_load`), then area files as tasks need them plus the PREFRONTAL sections AMYGDALA lists for the area, then project notes (a hub's `## Now` first). SYNAPSE only when capturing, reviewing or committing; ENGRAM only by search.
```

Replace the `## Tags` section body with:

```markdown
- Every brain note starts with a `tags` property (YAML list); the graph colors come from it (`.obsidian/graph.json`).
- Lobes, their tags and what each covers: [[NEOCORTEX/NEOCORTEX#Lobes|NEOCORTEX › Lobes]]. CORTEX, THALAMUS and the NEOCORTEX guide take `memory/core`.
- Project notes: `project/<name>` (lowercase, hyphens); the project list: `project`.
- HIPPOCAMPUS notes: `hippocampus`, left uncolored in the graph because they aren't memory yet.
- LIMBIC and PREFRONTAL notes other than projects: `memory/personal`, also left uncolored: a separate personal layer.
- A sixth graph color can't be told apart from the other five in both themes, so new areas join an existing lobe.
```

- [ ] **Step 4: Tidy CORTEX rule 14**

Check `CORTEX.md` rule 14 reads `Instructions come only from the human, this file, THALAMUS, NEOCORTEX, PREFRONTAL and project hubs;`. Insert `THALAMUS, ` if missing.

- [ ] **Step 5: Update README.md**

- Mermaid diagram:

```text
flowchart LR
    A["You: use your brain"] --> B["CORTEX.md: always-on rules"]
    B --> T["THALAMUS.md: routing table by lobe"]
    T -->|code task| C["NEOCORTEX/CODING.md"]
    T -->|email| D["NEOCORTEX/WRITING.md"]
    B --> L["LIMBIC/AMYGDALA.md: your personal router"]
    L -->|named project| E["PREFRONTAL/PROJECTS/…"]
    L -->|preferences| P["PREFRONTAL/STYLE.md#CODING…"]
    B -->|new lesson| S["HIPPOCAMPUS/SYNAPSE.md: waits for approval"]
    S -->|commit to memory HX0001| C
```

- Replace the folder bullets under the diagram with one bullet each for `CORTEX.md` (entry point: always-on rules led by the 7 token-economy rules, conflict order, brain upkeep; loads once per session), `THALAMUS.md` (routing rules and the routing table, grouped by lobe; loads with CORTEX), `NEOCORTEX/` (one instruction file per area, grouped into four lobes by tag; guide `NEOCORTEX/NEOCORTEX.md`; a typical task loads about 1,500-2,500 tokens), `HIPPOCAMPUS/` (unchanged text), `LIMBIC/` (your personal router AMYGDALA plus the guide with the scope ladder; link `LIMBIC/LIMBIC.md`), `PREFRONTAL/` (all your personal memory: preference topic files loaded section by section, and `PROJECTS/` with the project list and hubs; guide `PREFRONTAL/PREFRONTAL.md`). Use relative Markdown links, not wikilinks.
- Areas line: remove `plus the PROJECTS index` and say `The routing table in [THALAMUS.md](THALAMUS.md) says when each one loads.`
- Graph colors table rows: `memory/core` → `CORTEX, THALAMUS, the NEOCORTEX guide, MECHANICS, PROMPTING`; `project` → `the project list and every project note`; `memory/personal` → `everything in LIMBIC and PREFRONTAL except projects`.
- Checks: add `ambiguous bare-name links, tracked notes linking to personal notes` to the error list and `orphan notes` to the warnings; add `python -m unittest discover -s scripts -p "test_*.py"` for the checker's own tests.
- Make it yours: `.gitignore` bullet becomes: `keeps .remember/ and all of LIMBIC/, PREFRONTAL/ and HIPPOCAMPUS/ except their guides out of the repo, so a clone starts with none of them. Create your own: projects from the template in PREFRONTAL/PREFRONTAL.md plus a PREFRONTAL/PROJECTS/PROJECTS.md list, and personal preferences through SYNAPSE into PREFRONTAL/.` (with relative links); `MEMORY/MECHANICS.md` link → `NEOCORTEX/MECHANICS.md`.

- [ ] **Step 6: Verify the whole graph**

- Run: `python scripts/check_brain.py`
- Expected: `0 errors, 0 warnings` (no orphans).

- Run: `python -m unittest discover -s scripts -p "test_*.py"`
- Expected: OK.

Ask the human to open Obsidian, run **Reload app without saving**, open the graph and confirm: no unresolved (grey, dashed) nodes, no orphans, `docs/` absent, NEOCORTEX areas colored by lobe.

- [ ] **Step 7: Commit**

```bash
git add NEOCORTEX/NEOCORTEX.md THALAMUS.md NEOCORTEX/MECHANICS.md README.md CORTEX.md
git commit -m "Group areas into lobes; document the new layout

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: Cortex: layout keys, `!` exemptions, skeleton and path text

Repo: `cortex`. Start only after Task 0 Step 1(c) is resolved.

**Files:**
- Modify: `config/default.yaml`, `src/cortex/config.py`, `src/cortex/brain.py` (`configure`, `is_protected`), `src/cortex/synapse.py`, `src/cortex/vault.py`, `src/cortex/logs.py`, `src/cortex/mcp_tools.py` (`INSTRUCTIONS`, `synapse_queue` description), `README.md`, `docs/cheat-sheet.md`, `CLAUDE.md`, `CHANGELOG.md`
- Move: `src/cortex/skeleton/MEMORY/GENERAL.md` → `src/cortex/skeleton/NEOCORTEX/GENERAL.md`
- Create: `src/cortex/skeleton/THALAMUS.md`
- Modify: `src/cortex/skeleton/CORTEX.md`
- Test: `tests/conftest.py`, `tests/test_app.py`, `tests/test_e2e.py`, `tests/test_integration.py`, `tests/test_synapse.py`, `tests/test_vault.py`

**Interfaces:**
- Produces: `LayoutConfig.router`, `LayoutConfig.limbic`, `LayoutConfig.projects` (all `str`); protected rules may start with `!`; `Brain._rule_matches(rule: str, lowered: str) -> bool` (staticmethod); fixture brain with `THALAMUS.md`, `NEOCORTEX/`, `LIMBIC/`, `PREFRONTAL/`, `PREFRONTAL/PROJECTS/Acme/`.

- [ ] **Step 1: Branch**

```bash
git switch -c brain-anatomy
```

- [ ] **Step 2: Move the test brain to the new layout**

```bash
python - <<'EOF'
import re
from pathlib import Path
RULES = [
    (r"CEREBELLUM/MAP", "LIMBIC/AMYGDALA"),
    (r"CEREBELLUM/CEREBELLUM", "LIMBIC/LIMBIC"),
    (r"CEREBELLUM/", "PREFRONTAL/"),
    (r"MEMORY/", "NEOCORTEX/"),
    (r"(?<!PREFRONTAL/)PROJECTS/Acme", "PREFRONTAL/PROJECTS/Acme"),
]
for p in sorted(Path("tests").glob("*.py")):
    text = p.read_bytes().decode("utf-8")
    new = text
    for pattern, repl in RULES:
        new = re.sub(pattern, repl, new)
    if new != text:
        p.write_bytes(new.encode("utf-8"))
        print("rewrote", p.as_posix())
EOF
```

Then in `tests/conftest.py` `brain_dir`: keep the fixture CORTEX's existing fenced `text` block (the `NOT/A/LINK` sample) at the end of its string, unchanged; it is left out below only for brevity. Move the routing table out of the fixture's `CORTEX.md` into a new `THALAMUS.md` note, and link it from CORTEX:

```python
    write(root, "CORTEX.md", """
        ---
        tags:
          - memory/core
        ---
        # AI Second Brain

        Routing: [[THALAMUS]]. Personal layer: if `LIMBIC/AMYGDALA.md` exists, it loads too. Rules: [[LIMBIC/LIMBIC|LIMBIC]].

        ## Brain Upkeep
        Queue in [[HIPPOCAMPUS/SYNAPSE|SYNAPSE]]; trail in [[HIPPOCAMPUS/ENGRAM|ENGRAM]]; templates in [[HIPPOCAMPUS/HIPPOCAMPUS|HIPPOCAMPUS]].
        """)
    write(root, "THALAMUS.md", """
        ---
        tags:
          - memory/core
        ---
        # THALAMUS

        | Task | Go To |
        | --- | --- |
        | Code | [[NEOCORTEX/CODING\\|CODING]] |
        | Writing | [[NEOCORTEX/WRITING\\|WRITING]] |
        """)
```

- [ ] **Step 3: Update the blank-setup and integration expectations**

In `tests/test_app.py::test_setup_blank_brain`:

```python
        assert status["protected"] == ["CORTEX.md", "THALAMUS.md", "NEOCORTEX/", "LIMBIC/", "PREFRONTAL/",
                                       "HIPPOCAMPUS/HIPPOCAMPUS.md", "!PREFRONTAL/PROJECTS/"]
        graph = client.get("/api/graph").json()
        assert {node["id"] for node in graph["nodes"]} == {"CORTEX.md", "THALAMUS.md", "NEOCORTEX/GENERAL.md",
                                                           "HIPPOCAMPUS/SYNAPSE.md", "HIPPOCAMPUS/ENGRAM.md"}
```

In `tests/test_integration.py` (lines 24-29):

```python
    assert (empty / "HIPPOCAMPUS" / "HIPPOCAMPUS.md").is_file() and (empty / "LIMBIC" / "LIMBIC.md").is_file()
    assert (empty / "PREFRONTAL" / "PREFRONTAL.md").is_file() and (empty / "THALAMUS.md").is_file()
```

```python
    assert "Next ID: HX0001" in synapse and "PREFRONTAL/FILE#Section" in synapse  # the guide's template, not Cortex's fallback
    assert brain.is_protected("PREFRONTAL/ANY.md") and brain.is_protected("HIPPOCAMPUS/HIPPOCAMPUS.md")
    assert not brain.is_protected("PREFRONTAL/PROJECTS/Any/ANY.md")
```

- [ ] **Step 4: Write the failing exemption tests**

Add to `tests/test_app.py` after `test_personal_layer_and_guide_are_protected`:

```python
def test_projects_are_writable_inside_the_protected_personal_layer(client: TestClient, brain_dir: Path) -> None:
    # PREFRONTAL is protected, but project hubs are working memory: `!PREFRONTAL/PROJECTS/` exempts them.
    key = new_key(client)
    for note in ("PREFRONTAL/STYLE.md", "LIMBIC/AMYGDALA.md", "LIMBIC/NEW.md"):
        failed, text = call(client, key, "cortex_write", note=note, content="x")
        assert failed and "protected" in text, note
    failed, text = call(client, key, "cortex_write", note="PREFRONTAL/PROJECTS/Acme/NEW.md",
                        content="---\ntags:\n  - project/acme\n---\nNew.\n")
    assert not failed, text
    assert (brain_dir / "PREFRONTAL/PROJECTS/Acme/NEW.md").is_file()


def test_exemption_wins_but_never_over_the_hippocampus(config: Config, logger: Logger, errors: ErrorHandler) -> None:
    app = create_app(config, logger, Secrets(config.secrets), errors)
    brain = app.state.brain
    brain.configure("CORTEX.md", protected=["PREFRONTAL/", "!PREFRONTAL/PROJECTS/", "!HIPPOCAMPUS/"])
    assert brain.is_protected("PREFRONTAL/STYLE.md")
    assert brain.is_protected("prefrontal/style")
    assert not brain.is_protected("PREFRONTAL/PROJECTS/Acme/ACME.md")
    assert brain.is_protected("HIPPOCAMPUS/SYNAPSE.md")
```

- [ ] **Step 5: Run the tests to verify they fail**

- Run: `python -m pytest tests -q`
- Expected: failures, including `test_projects_are_writable_inside_the_protected_personal_layer` (LIMBIC not protected, projects refused), `test_exemption_wins_but_never_over_the_hippocampus`, `test_setup_blank_brain` (protected list, graph nodes).

- [ ] **Step 6: Implement config and protection**

`config/default.yaml` layout block:

```yaml
# Where the brain's parts sit, relative to its CORTEX.md. Used when setup can't find
# SYNAPSE/ENGRAM, to seed the protected list, and to load the routers.
layout:
  synapse: HIPPOCAMPUS/SYNAPSE.md
  engram: HIPPOCAMPUS/ENGRAM.md
  # The guide holding SYNAPSE's and ENGRAM's templates, used when either file is missing.
  hippocampus_guide: HIPPOCAMPUS/HIPPOCAMPUS.md
  # The router cortex_load returns with CORTEX.md.
  router: THALAMUS.md
  memory: NEOCORTEX/
  # The personal router's folder, and the router: which personal sections each area loads.
  limbic: LIMBIC/
  personal_map: LIMBIC/AMYGDALA.md
  # All personal memory (protected), and its projects (exempt: hubs are written directly).
  personal: PREFRONTAL/
  projects: PREFRONTAL/PROJECTS/
```

`src/cortex/config.py` `LayoutConfig`:

```python
class LayoutConfig(_Section):
    synapse: str = Field(min_length=1)
    engram: str = Field(min_length=1)
    hippocampus_guide: str = Field(min_length=1)
    router: str = Field(min_length=1)
    memory: str = Field(min_length=1)
    limbic: str = Field(min_length=1)
    personal: str = Field(min_length=1)
    personal_map: str = Field(min_length=1)
    projects: str = Field(min_length=1)
```

`src/cortex/brain.py` `configure`: docstring line for `protected` becomes `protected paths; when omitted, CORTEX.md, the router, the memory areas, the personal router's folder, the personal layer and the HIPPOCAMPUS guide (config \`layout\`), plus an exemption for projects, whether or not they exist yet, so a folder created later is protected from the start.` and the default:

```python
        if protected is None:
            protected = [cortex, base + layout.router, base + layout.memory, base + layout.limbic, base + layout.personal,
                         guide, "!" + base + layout.projects]
```

`is_protected` and a helper:

```python
    @staticmethod
    def _rule_matches(rule: str, lowered: str) -> bool:
        return (rule.endswith("/") and lowered.startswith(rule)) or lowered in (rule, rule + ".md")

    def is_protected(self, relative: str) -> bool:
        """Whether a note changes only through an approved SYNAPSE commit.

        Args:
            relative: a vault path.

        Returns:
            True when a protected rule matches (a trailing `/` protects a folder) and no `!` rule
            exempts it, or for the hippocampus, which no exemption reaches.
        """
        lowered = relative.lower()
        rules = [rule.lower() for rule in self.state.get("protected")]
        if any(self._rule_matches(rule[1:], lowered) for rule in rules if rule.startswith("!")):
            return self.is_hippocampus(relative)
        if any(self._rule_matches(rule, lowered) for rule in rules if not rule.startswith("!")):
            return True
        return self.is_hippocampus(relative)
```

- [ ] **Step 7: Move the skeleton brain**

```bash
git mv src/cortex/skeleton/MEMORY src/cortex/skeleton/NEOCORTEX
```

Create `src/cortex/skeleton/THALAMUS.md`:

```markdown
---
tags:
  - memory/core
---
# THALAMUS

The **router**: it tells you where to go, not what to know. It loads with [[CORTEX]].

**Do not read everything.** Identify the task, then read only the relevant instruction file(s).

## Routing Rules
1. Identify the primary intent.
2. Go directly to its instruction file in the table below.
3. State which part of the brain you are using as your first line: `Brain: GENERAL`.
4. Read additional files only when required; follow links one hop, no chains.
5. Prefer existing knowledge over creating duplicates. When creating knowledge, add `[[wikilinks]]` that carry the vault path.

## Routing Table

| Task | Load when the task is about… | Go To |
| --- | --- | --- |
| General | anything; add rows here as you create area files | [[NEOCORTEX/GENERAL\|GENERAL]] |
```

In `src/cortex/skeleton/CORTEX.md`: replace the intro paragraph and `## Routing Rules` section with the text below, and delete the `## Routing Table` section. `## Always-on Rules` and `## Brain Upkeep` stay.

```markdown
This is the **entrypoint**: the rules for every task and how the brain changes. Where each task goes is [[THALAMUS]], the router; the files it links to tell you what to do.

## Conflicts
The human's latest message > project note > area file > this file and THALAMUS. Point out the conflict so it gets fixed.
```

- [ ] **Step 8: Rewrite path examples in source and docs**

```bash
python - <<'EOF'
import re
from pathlib import Path
RULES = [(r"CEREBELLUM/MAP\.md", "LIMBIC/AMYGDALA.md"), (r"CEREBELLUM/CEREBELLUM\.md", "LIMBIC/LIMBIC.md"),
         (r"CEREBELLUM/", "PREFRONTAL/"), (r"\bMEMORY/", "NEOCORTEX/")]
files = [p for p in Path("src/cortex").glob("*.py")] + [Path("README.md"), Path("docs/cheat-sheet.md")]
for p in files:
    text = p.read_bytes().decode("utf-8")
    new = text
    for pattern, repl in RULES:
        new = re.sub(pattern, repl, new)
    if new != text:
        p.write_bytes(new.encode("utf-8"))
        print("rewrote", p.as_posix())
EOF
```

Then by hand:
- `src/cortex/mcp_tools.py` `INSTRUCTIONS`: `The personal layer (CEREBELLUM) is human-owned: cortex_load includes its map; load the sections the map lists for the task's area.` → `cortex_load returns CORTEX.md, the router (THALAMUS) and the personal router (AMYGDALA) with its Always sections; load the PREFRONTAL sections AMYGDALA lists for the task's area.`; `Memory and CEREBELLUM change only through the hippocampus` → `NEOCORTEX and the personal layer (LIMBIC, PREFRONTAL) change only through the hippocampus`; add `Project hubs under PREFRONTAL/PROJECTS/ are written directly with cortex_write.`
- `synapse_queue` `target` description: `a NEOCORTEX area for a global rule ('NEOCORTEX/WRITING › Avoid'), or the personal layer for a personal preference or environment fact ('PREFRONTAL/STYLE#CODING'); pick with the brain's scope ladder in LIMBIC/LIMBIC.md and ask when its tests disagree`.
- `README.md` line 92 row: `` | `LIMBIC/…`, `PREFRONTAL/…` | Your personal layer: AMYGDALA (the personal router) says which PREFRONTAL sections each area loads; PREFRONTAL holds preferences and projects | Only through an approved SYNAPSE commit (protected), except `PREFRONTAL/PROJECTS/`, which is written directly | ``; line 91 `MEMORY` → `NEOCORTEX`; the config table row for `layout.memory, personal, personal_map` becomes `` | `layout.router`, `memory`, `limbic`, `personal_map`, `personal`, `projects` | `THALAMUS.md`, `NEOCORTEX/`, `LIMBIC/`, `LIMBIC/AMYGDALA.md`, `PREFRONTAL/`, `PREFRONTAL/PROJECTS/` | The router, memory areas, personal router and personal layer; with the guide, they seed the protected list (`!` + projects exempts project hubs) | ``; add a sentence under the protected-notes table: `A protected rule starting with ! exempts a path (hippocampus files excepted).`
- `CLAUDE.md` conventions bullet: `The personal layer (\`LIMBIC/\`, \`PREFRONTAL/\`) is human-owned: protected by default and changed only through \`synapse_commit\`; project hubs under \`PREFRONTAL/PROJECTS/\` are exempt (a \`!\` rule).`
- `CHANGELOG.md` › 🚧 Unreleased › Changed: `- The brain layout follows claude-brain's anatomy: memory areas in \`NEOCORTEX/\`, a router \`THALAMUS.md\`, the personal router \`LIMBIC/AMYGDALA.md\` and all personal memory in \`PREFRONTAL/\` (config \`layout.*\`, new keys \`router\`, \`limbic\`, \`projects\`). Operator: after upgrading, set Settings › Protected to the new defaults (see README); a list saved before still names \`MEMORY/\` and \`CEREBELLUM/\`.` and under Added: `- Protected paths accept \`!\` exemptions; project hubs under \`PREFRONTAL/PROJECTS/\` stay writable inside the protected personal layer.`

- [ ] **Step 9: Run all checks**

- Run: `python scripts/python/check.py`
- Expected: ruff, mypy and pytest pass. If a test still names an old path in a string the Step 2 rules missed, fix it to the new layout.

- Run: `grep -rn "CEREBELLUM\|MEMORY/\|MAP\.md" src config README.md docs CLAUDE.md tests --include=*.py --include=*.md --include=*.yaml`
- Expected: no output (CHANGELOG history is excluded on purpose).

- [ ] **Step 10: Commit**

```bash
git add -A config src tests README.md docs/cheat-sheet.md CLAUDE.md
git add CHANGELOG.md
git commit -m "Adopt the NEOCORTEX/LIMBIC/PREFRONTAL layout with ! exemptions

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: Cortex: cortex_load returns the router

**Files:**
- Modify: `src/cortex/brain.py` (`Overview`, `overview`), `src/cortex/mcp_tools.py` (`cortex_load`), `README.md` (commands table row for `use the cortex`), `CHANGELOG.md`
- Test: `tests/test_app.py`

**Interfaces:**
- Consumes: `LayoutConfig.router` (Task 6).
- Produces: `Overview.router_path: str = ""`, `Overview.router: str = ""` (both empty when the brain has no router).

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_app.py` after `test_load_includes_personal_map_and_always_sections`:

```python
def test_load_returns_cortex_then_router_then_personal_router(client: TestClient) -> None:
    key = new_key(client)
    failed, text = call(client, key, "cortex_load")
    assert not failed
    positions = [text.index(f"--- {path} ---") for path in ("CORTEX.md", "THALAMUS.md", "LIMBIC/AMYGDALA.md")]
    assert positions == sorted(positions)
    assert "| Code | [[NEOCORTEX/CODING" in text


def test_load_without_router_says_so(config: Config, brain_dir: Path, logger: Logger, errors: ErrorHandler) -> None:
    (brain_dir / "THALAMUS.md").unlink()
    with build(config, logger, errors) as client:
        key = new_key(client)
        failed, text = call(client, key, "cortex_load")
        assert not failed and "--- CORTEX.md ---" in text
        assert "No router at THALAMUS.md" in text
```

- [ ] **Step 2: Run them to verify they fail**

- Run: `python -m pytest tests/test_app.py -q -k "router"`
- Expected: 2 failed (`ValueError: substring not found` and missing "No router" text).

- [ ] **Step 3: Implement**

`Overview` gains, after `text: str`:

```python
    router_path: str = ""  # empty when the brain has no router file
    router: str = ""
```

In `Brain.overview`, after `map_path = ...`:

```python
        home = self._home(self.cortex_path)
        router_path = self._layout_path(self.config.layout.router, home)
        router = self.vault.read(router_path) if self.vault.exists(router_path) else ""
```

(use `home` in the existing `map_path` line too), change the log line to `self.logger.event(who, "load", " + ".join(part for part in (self.cortex_path, router_path if router else "", map_path if personal_map else "") if part))`, and pass `router_path=router_path if router else "", router=router,` to `Overview(...)`. Update the docstring's first line to `"""The routing files (CORTEX, the router, the personal router with its \`Always\` sections) and hippocampus counts.`.

In `mcp_tools.cortex_load`: docstring becomes `"""Load the user's second brain: returns CORTEX.md (rules), THALAMUS (the router to follow for the rest of the session), plus the personal router AMYGDALA and its Always sections when the brain has one. Call once per session when the user says "use the cortex", "use your brain" or runs /cortex, and again on "reload the brain"."""`; after the `lines = [...]` block add:

```python
        if not overview.router:
            lines.append(f"- No router at {brain.config.layout.router}: route with CORTEX.md alone and mention it so it gets fixed.")
```

change the personal-layer line to `f"- Personal layer: {overview.personal_map_path} (AMYGDALA) is below, already read, with its Always sections. For each task, also load the sections it lists under the task's area: cortex_read('PREFRONTAL/FILE#Section')."`, change `"- The map links to sections"` to `"- AMYGDALA links to sections"` and `"so the map gets fixed"` to `"so AMYGDALA gets fixed"`, and build the text as:

```python
        text = "\n".join(lines) + f"\n\n--- {overview.cortex_path} ---\n" + overview.text
        if overview.router:
            text += f"\n\n--- {overview.router_path} ---\n" + overview.router
        if overview.personal_map:
```

README commands row: `Loads \`CORTEX.md\`, the router \`THALAMUS.md\` and your personal router (\`LIMBIC/AMYGDALA.md\` with its \`Always\` sections) for the session, …`. CHANGELOG Changed: `- \`cortex_load\` returns the router (THALAMUS.md) between CORTEX.md and the personal router, so a session loads all three in one call.`

- [ ] **Step 4: Run the tests to verify they pass**

- Run: `python scripts/python/check.py`
- Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add src/cortex/brain.py src/cortex/mcp_tools.py tests/test_app.py README.md
git add CHANGELOG.md
git commit -m "Return the router with CORTEX in cortex_load

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 8: Cortex: warn when a layout folder isn't protected

**Files:**
- Modify: `src/cortex/brain.py` (`audit`, new `_protection_gaps`), `CHANGELOG.md`
- Test: `tests/test_app.py`

**Interfaces:**
- Consumes: `LayoutConfig.memory`, `.limbic`, `.personal`; `Brain.is_protected` (Task 6).
- Produces: `Brain._protection_gaps() -> list[str]`, lines `warning: <FOLDER> isn't protected: add it to Settings › Protected`.

- [ ] **Step 1: Write the failing test**

```python
def test_check_warns_when_a_layout_folder_is_unprotected(config: Config, logger: Logger, errors: ErrorHandler) -> None:
    # A protected list saved before the layout moved still names MEMORY/ and CEREBELLUM/.
    app = create_app(config, logger, Secrets(config.secrets), errors)
    brain = app.state.brain
    brain.configure("CORTEX.md", protected=["CORTEX.md", "MEMORY/", "CEREBELLUM/"])
    output = brain.audit("test").output
    for folder in ("NEOCORTEX/", "LIMBIC/", "PREFRONTAL/"):
        assert f"warning: {folder} isn't protected" in output
    brain.configure("CORTEX.md")
    assert "isn't protected" not in brain.audit("test").output
```

- [ ] **Step 2: Run it to verify it fails**

- Run: `python -m pytest tests/test_app.py -q -k unprotected`
- Expected: FAIL (`assert 'warning: NEOCORTEX/ isn't protected' in ...`).

- [ ] **Step 3: Implement**

In `Brain.audit`, before the log line:

```python
        gaps = self._protection_gaps()
        if gaps:
            report = dataclasses.replace(report, output="\n".join([report.output, *gaps]))
```

Add `import dataclasses` at the top of `brain.py` if it isn't there (keep the existing `from dataclasses import ...` line). Add the method after `_built_in_audit`:

```python
    def _protection_gaps(self) -> list[str]:
        """Warnings for layout folders no protected rule covers (a list saved before the layout moved)."""
        home = self._home(self.cortex_path)
        layout = self.config.layout
        gaps = []
        for folder in (layout.memory, layout.limbic, layout.personal):
            path = self._layout_path(folder, home)
            if not self.is_protected(path.rstrip("/") + "/probe.md"):
                gaps.append(f"warning: {path} isn't protected: add it to Settings › Protected")
        return gaps
```

A warning never flips `passed`. CHANGELOG Added: `- "check the brain" warns when the memory, LIMBIC or PREFRONTAL folder isn't in the protected list.`

- [ ] **Step 4: Run all checks**

- Run: `python scripts/python/check.py`
- Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add src/cortex/brain.py tests/test_app.py
git add CHANGELOG.md
git commit -m "Warn in check the brain when a layout folder isn't protected

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 9: Ship and verify end to end (human-gated)

**Files:** none new.

- [ ] **Step 1: Ask the human, in one message, for each outward step**: (a) merge `claude-brain` `brain-anatomy` into `main` and push to GitHub (this changes Cortex's template brain `jimmydagher/claude-brain`); (b) merge `cortex` `brain-anatomy`, release 0.3.0 with the repo's release flow (`scripts/python/release.py`; see `docs/cheat-sheet.md`) and deploy with `scripts/ps1/deploy-nas.ps1`; (c) how the NAS brain folder receives the reorganized vault today. Do only what they approve.

- [ ] **Step 2: After the push, run the real-template test**

- Run (in `cortex`): `python -m pytest tests/test_integration.py -m integration -q`
- Expected: pass.

- [ ] **Step 3: After deploy, reset the protected list**

Ask the human to open the Cortex GUI › Settings › Protected and replace the list with exactly these lines (never save it empty: that protects nothing):

```text
CORTEX.md
THALAMUS.md
NEOCORTEX/
LIMBIC/
PREFRONTAL/
HIPPOCAMPUS/HIPPOCAMPUS.md
!PREFRONTAL/PROJECTS/
```

- [ ] **Step 4: Verify through the live MCP server**

Call `cortex_load` (reload): the output shows `--- CORTEX.md ---`, `--- THALAMUS.md ---` and `--- LIMBIC/AMYGDALA.md ---` in that order. Call `cortex_check`: `Passed`, no `isn't protected` warning. Call `cortex_read('NEOCORTEX/CODING')`: header ends with `· protected`. Call `cortex_read('PREFRONTAL/PROJECTS/PROJECTS')`: no `· protected`.

- [ ] **Step 5: Restore the local CODING.md line**

```bash
BACKUP="/c/Users/jdagher/Development/projects/_backup/claude-brain-personal-2026-09-27"
sed 's#MEMORY/CODING.md#NEOCORTEX/CODING.md#g' "$BACKUP/coding-local.patch" | git apply
git diff --stat NEOCORTEX/CODING.md
```

- Expected: `1 file changed, 1 insertion(+)`, left uncommitted as before.

- [ ] **Step 6: Final report**

Report to the human: commits on each branch, check outputs (`check_brain.py`, unittest, `check.py`, `cortex_check`), the backup location, and anything skipped. Suggest removing the backup only after they've confirmed the graph looks right.
