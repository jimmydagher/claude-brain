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

## 🆕VERSION 0.1.0 📅 2026-10-04

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

