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

## 🆕VERSION 0.1.2 📅 2026-10-07

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

