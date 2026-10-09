# Changelog

All notable changes, newest first. See `VERSION` for the current release.

## 🚧 Unreleased

### Added or New Features
(none)

### Removed
(none)

### Changed
(none)

### Bug/Issues/Fixes
(none)

## 🆕VERSION 0.1.3 📅 2026-10-09

### Added or New Features
- NEOCORTEX is now a hub over three shared areas: `INSTRUCTIONS/` (the 16 area files and their routing index), `KNOWLEDGE/` (shared reference notes, searched on demand; guide: `NEOCORTEX/KNOWLEDGE/KNOWLEDGE.md`) and `PROJECTS/` (shared project hubs in lowercase folders such as `life-dashboard/`, and the `HUB.md` list; guide and hub template: `NEOCORTEX/PROJECTS/PROJECTS.md`). Knowledge notes and project hubs are gitignored; only the guides are tracked.
- PREFRONTAL mirrors the three areas per user: `PREFRONTAL/<user>/INSTRUCTIONS/`, `KNOWLEDGE/` and `PROJECTS/`, each with an index that links up to the PREFRONTAL guide.
- `check_brain.py` resolves a personal note's `PREFRONTAL/…` links the way Cortex shows them (inside the user's own folder), treats knowledge notes and project hubs as untracked, and caps personal sections in `PREFRONTAL/<user>/INSTRUCTIONS/`.
- "check the brain" warns on two notes with one name in the same scope (knowledge names are unique across the brain, project note names within their project), knowledge notes without `sources`, and active project hubs not updated for 30 days.
- CORTEX › Brain Upkeep: **Undo** with a correcting SYNAPSE entry (`corrects: HX0012`) that restores the old values from ENGRAM.
- SECURITY RULE#6 (no tax IDs, bank or card numbers or personal contact details in any note) and RULE#7 (a refused write means stop, never route around it); a Default that identity never comes from the chat.
- INSTRUCTIONS routing rules 9 (memory vs source: follow the note, report the conflict) and 10 (cite the notes an answer used, in one closing line).
- KNOWLEDGE guide: RULE#5 Verified facts only and RULE#6 One subject, one note, plus writing rules for Claude (frontmatter `aliases`, `status`, `updated`, `sources`; links; file names). Project notes follow them.
- PROJECTS guide: RULE#4 Stay in scope, decisions name who decided, "commit this session", a new area for information that fits none of a project's areas, and project templates from `NEOCORTEX/PROJECTS/TEMPLATES.md` when the brain has one (Cortex installs it; the hub names its template on its header line).

### Removed
- The `KNOWLEDGE` instruction area. Its summarizing rules moved to `WRITING` (RULE#5 Faithful to the source, summary and extraction formats); its filing rules moved to the new KNOWLEDGE guide.

### Changed
- Area files moved from `NEOCORTEX/` to `NEOCORTEX/INSTRUCTIONS/`, and every link to them now carries the new path. Links written as `[[NEOCORTEX/CODING|…]]` outside this vault need the same change.
- The routing table and lobes moved from `NEOCORTEX/NEOCORTEX.md` to `NEOCORTEX/INSTRUCTIONS/INSTRUCTIONS.md`, which is what loads with CORTEX. Cortex 0.3+ loads it by default; an older Cortex still loads `NEOCORTEX/NEOCORTEX.md`, now only the hub.
- CORTEX › Conflicts is now an ordered list: protected Core Rules win over everything personal or project-level, and a personal entry that contradicts them is refused when it's queued. Rule 14 names knowledge notes as data, not instructions.
- Projects moved from `PREFRONTAL/<user>/PROJECTS/` to the shared `NEOCORTEX/PROJECTS/`, tagged `project/<name>` instead of `persona/project/<name>`; the graph's magenta group now matches `tag:#project`. After pulling, run Obsidian's **Reload app without saving** before opening the graph.
- One status line per session, naming the brain: `Cortex brain: connected to <brain>` (replaces `Cortex brain: connected`, `Using the [area] part of the brain` and `Brain: on`); each task still names its areas with `Brain: CODING + SECURITY`.
- Commits follow the caller's role in the brain: a brain admin's are written at once and reported, a member's personal ones are previewed and written on "yes", and a member's "share" waits for an admin. This replaces the old Preview step.
- A commit merges into current memory: create when nothing is there, otherwise add, update or delete in place and update every other place that states the old value; stop and ask on a conflict. ENGRAM is the only history, and its committed lines record old → new.
- CORTEX › Filter leaves out off-topic, unresolved, unconfirmed, temporary, no-change and sensitive items and says why; the human's plain statement counts as verified.
- The project hub template has a `Template:` field, decisions with `· who`, and an `## Open questions` section.

### Bug/Issues/Fixes
(none)

## 🟨VERSION 0.1.2 📅 2026-10-07

### Added or New Features
(none)

### Removed
(none)

### Changed
- Changes were applied to CODING.md

### Bug/Issues/Fixes
(none)

## 🟧VERSION 0.1.1 📅 2026-10-06

### Added or New Features
(none)

### Removed
(none)

### Changed
- Response-shaping rules adapted from the i-have-adhd skill (HX0010–HX0018): CORTEX rules 5, 6, 12 and 13 (side issues last, first/last-line test, one small next step, show what now works); AUTOPILOT turn status line; PLANNING concrete estimates; CODING error format; ASSISTANT list cap of 5 per group (WRITING defers to it in chat); WRITING slop list adds figurative idioms.

### Bug/Issues/Fixes
(none)

## 🟥VERSION 0.1.0 📅 2026-10-04

### Added or New Features
- Versioning and release chain: `meta/VERSION`, this changelog, and git hooks (`scripts/git/`, `scripts/python/release.py`) that bump the version, promote these notes and close referenced `meta/TODO.md` items on every commit to `main`. Operator: after cloning, run the two `git config` commands in README › Releases; the hooks need Python 3.9+ on `PATH`.

### Removed
(none)

### Changed
- `TODO.md` moved to `meta/TODO.md`.
- `README.md` shows the current version under the title, kept in sync by the release hooks.
- `scripts/check_brain.py` skips `meta/`: project records, not brain notes.

### Bug/Issues/Fixes
(none)

