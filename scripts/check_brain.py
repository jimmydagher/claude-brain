#!/usr/bin/env python3
"""Read-only checks for the claude-brain vault (standard library only).

python scripts/check_brain.py           whole vault
python scripts/check_brain.py FILE...   only these files
python scripts/check_brain.py --hook    Claude Code PostToolUse hook: checks the file just written

Errors: dead wikilinks and heading links, ambiguous bare-name links, tracked notes linking to personal notes, hard wraps, em dashes, chatbot residue, missing tags, SYNAPSE IDs.
Warnings: slop-list hits (they mark a passage to test, not a verdict), repeated long lines, links that leave the tree, orphan notes, personal sections over the size cap, two notes on one subject (the same name in one scope), knowledge notes without sources, and active project hubs not updated for a month.
Exit: 0 no errors, 1 errors, 2 errors in --hook mode (Claude Code shows them to Claude).
"""
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".obsidian", ".trash", ".git", ".claude", ".remember", "scripts", "docs", "meta"}
UNTAGGED_OK = {"README.md"}
HIPPOCAMPUS = ("HIPPOCAMPUS/SYNAPSE.md", "HIPPOCAMPUS/ENGRAM.md")
# Notes git doesn't track (.gitignore): the personal layer, shared knowledge notes and project hubs; only their guides are tracked.
UNTRACKED = ("prefrontal/", "neocortex/knowledge/", "neocortex/projects/")
GUIDES = {"prefrontal/prefrontal", "neocortex/knowledge/knowledge", "neocortex/projects/projects"}
PERSONAL_ROOT = "prefrontal/"
MOUNT = re.compile(r"prefrontal/([^/]+)/")  # a user's folder, which the brain shows them as plain PREFRONTAL/
TOP = "cortex"  # the note every folder index hangs from
ROOTS = {TOP, "readme"}
# Links allowed to leave the tree on purpose: ENGRAM shows where committed memory lands.
TREE_EXCEPTIONS = {("hippocampus/engram", "neocortex/neocortex")}
HEADING = re.compile(r"#{1,6}\s+(.*)")
BLOCK = re.compile(r"\s*([#>|*+-]|\d+\.\s|<!--)")
LINK = re.compile(r"\[\[([^\]|#\\]+)(?:#([^\]|\\]+))?")
SECTION_CAP = 150
CODE_SPAN = re.compile(r"`[^`]*`")
QUOTED = re.compile("\"[^\"]*\"|“[^”]*”")
RESIDUE = re.compile(r"oaicite|contentReference\[|utm_source=chatgpt\.com|\[cite:\s*\d+\]|\[Your Name\]|lorem ipsum", re.I)
STALE_DAYS = 30
PROJECT = re.compile(r"(?:neocortex|prefrontal/[^/]+)/projects/([^/]+)/")  # a note inside one project's folder
HUB_STATUS = re.compile(r"Status:\s*active\b", re.I)
HUB_UPDATED = re.compile(r"Updated:\s*(\d{4}-\d{2}-\d{2})")
HX = re.compile(r"\bHX(\d{4})\b")
ENTRY = re.compile(r"\s*- \[[ xX-]\] HX(\d{4})\b")


def is_note(path):
    return path.suffix == ".md" and path.is_relative_to(ROOT) and not SKIP_DIRS & set(path.relative_to(ROOT).parts)


def rel(path):
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.name


def is_untracked(key):
    """Whether a lowercase vault key (path without .md) is a note git doesn't track."""
    return key.startswith(UNTRACKED) and key not in GUIDES


def resolve_path(key, own, paths):
    """A full-path link target as a vault key: as written, or, from inside a user's personal folder,
    the way the brain shows it to them (`PREFRONTAL/INSTRUCTIONS/X` means `PREFRONTAL/<user>/INSTRUCTIONS/X`)."""
    if key in paths:
        return key
    mount = MOUNT.match(own)
    if mount and key.startswith(PERSONAL_ROOT):
        mapped = mount.group(0) + key[len(PERSONAL_ROOT):]
        if mapped in paths:
            return mapped
    return None


def parent(key, paths):
    """The note a note hangs from: its folder's index (the note named like the folder), up to CORTEX."""
    folders = key.split("/")[:-1]
    if folders and key.rsplit("/", 1)[-1] == folders[-1]:
        folders = folders[:-1]  # a folder's own index hangs from the folder above
    while folders:
        index = "/".join([*folders, folders[-1]])
        if index in paths:
            return index
        folders = folders[:-1]
    return None if key == TOP else TOP


def in_tree(source, target, paths):
    """Whether a link follows the tree: to the note's index, a note it indexes, or a neighbour inside a region."""
    up, down = parent(source, paths), parent(target, paths)
    return target == up or source == down or (up == down and up != TOP) or (source, target) in TREE_EXCEPTIONS


def frontmatter(lines):
    if lines[:1] == ["---"]:
        for i, line in enumerate(lines[1:], 1):
            if line == "---":
                return lines[1:i]
    return None


def body(lines):
    """Yield (line number, text without inline code, current heading) outside frontmatter and code fences."""
    front = frontmatter(lines)
    start = len(front) + 2 if front is not None else 0
    fence, section = False, ""
    for n, line in enumerate(lines[start:], start + 1):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        heading = HEADING.match(line)
        if heading:
            section = heading.group(1)
        yield n, CODE_SPAN.sub("", line), section


def slop_pattern():
    """Build a matcher from WRITING.md's slop list, so the list lives in one place."""
    words, phrases = [], []
    writing = ROOT / "NEOCORTEX" / "INSTRUCTIONS" / "WRITING.md"
    if writing.exists():
        for line in writing.read_text(encoding="utf-8").splitlines():
            if line.startswith("- Words:"):
                words = [w.strip(" .") for w in line[len("- Words:"):].split(",") if w.strip() and "(" not in w]
            elif line.startswith("- Phrases:"):
                phrases = [(a or b).strip("!.… ") for a, b in re.findall("\"([^\"]+)\"|“([^”]+)”", line)]
    terms = [t for t in words + phrases if t]
    return re.compile(r"\b(" + "|".join(map(re.escape, terms)) + r")\b", re.I) if terms else None


def build_index():
    """Return note paths, a name-to-paths map and each note's lowercase headings (for #Heading links)."""
    paths, names, heads = set(), {}, {}
    for p in ROOT.rglob("*.md"):
        if not is_note(p):
            continue
        key = p.relative_to(ROOT).as_posix()[:-3].lower()
        paths.add(key)
        names.setdefault(key.rsplit("/", 1)[-1], []).append(key)
        found = (HEADING.match(line) for line in p.read_text(encoding="utf-8").splitlines())
        heads[key] = {m.group(1).strip().lower() for m in found if m}
    return paths, names, heads


def check_note(path, slop, index, errors, warnings, linked):
    name = rel(path)
    lines = path.read_text(encoding="utf-8").splitlines()
    front = frontmatter(lines)
    if name not in UNTAGGED_OK and not (front and any(line.startswith("tags:") for line in front)):
        errors.append(f"{name}:1: missing tags frontmatter")
    paths, names, heads = index
    own = name[:-3].lower()
    tracked = not is_untracked(own) and name not in HIPPOCAMPUS
    prev_plain = False
    for n, text, section in body(lines):
        plain = bool(text.strip()) and not BLOCK.match(text)
        if plain and prev_plain:
            errors.append(f"{name}:{n}: hard wrap: join this line with the one above")
        prev_plain = plain
        for target, heading in LINK.findall(text):
            key = target.strip().lower().removesuffix(".md")
            if "/" in key:
                resolved = resolve_path(key, own, paths)
                found = [resolved] if resolved else []
            else:
                found = names.get(key, [])
            if not found:
                errors.append(f"{name}:{n}: dead link [[{target.strip()}]]")
                continue
            if "/" not in key and len(found) > 1:
                errors.append(f"{name}:{n}: ambiguous link [[{target.strip()}]] matches {', '.join(sorted(found))}: use the full path")
            if tracked and any(is_untracked(f) for f in found):
                errors.append(f"{name}:{n}: tracked note links to untracked note [[{target.strip()}]]: untracked notes link up to their guide instead")
            if len(found) == 1 and found[0] != own and not in_tree(own, found[0], paths):
                warnings.append(f"{name}:{n}: link [[{target.strip()}]] leaves the tree: write it as a plain name in backticks")
            others = [f for f in found if f != own]
            if others:
                linked.update([own, *others])  # a graph edge: neither end is an orphan
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


def check_ids(errors):
    owner, next_id = {}, None
    for name in HIPPOCAMPUS:
        path = ROOT / name
        if not path.exists():
            continue
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith("Next ID:"):
                found = HX.search(line)
                next_id = int(found.group(1)) if found else None
            entry = ENTRY.match(line)
            if entry:
                num = int(entry.group(1))
                if num in owner:
                    errors.append(f"{name}:{n}: HX{num:04d} already used at {owner[num]}")
                owner.setdefault(num, f"{name}:{n}")
    if owner and (next_id is None or next_id <= max(owner)):
        errors.append(f"HIPPOCAMPUS/SYNAPSE.md: 'Next ID' must be above HX{max(owner):04d}")


def check_repeats(warnings):
    seen = {}
    shared = sorted(p for p in (ROOT / "NEOCORTEX").rglob("*.md") if not is_untracked(rel(p)[:-3].lower()))
    for path in [ROOT / "CORTEX.md", *shared]:
        for n, text, _ in body(path.read_text(encoding="utf-8").splitlines()):
            key = re.sub(r"\s+", " ", re.sub(r"^[\s>*+-]*(\d+\.\s*)?", "", text)).strip().lower()
            if len(key.split()) >= 12:
                seen.setdefault(key, []).append(f"{rel(path)}:{n}")
    for places in seen.values():
        if len({p.split(":")[0] for p in places}) > 1:
            warnings.append(f"{places[0]}: line repeated in {', '.join(places[1:])}: give it one home")


def check_orphans(files, linked, warnings):
    """Warn about notes with no link in or out, as Obsidian's graph counts orphans (roots excepted)."""
    for path in files:
        key = rel(path)[:-3].lower()
        if key not in linked and key not in ROOTS:
            warnings.append(f"{rel(path)}: orphan: no link in or out")


def check_prefrontal(warnings):
    """Warn when a personal instruction section outgrows the cap: it splits into its own file."""
    personal = ROOT / "PREFRONTAL"
    for path in sorted([*personal.glob("INSTRUCTIONS/*.md"), *personal.glob("*/INSTRUCTIONS/*.md")]):
        if path.name == "INSTRUCTIONS.md":
            continue
        title, count = None, 0
        for line in path.read_text(encoding="utf-8").splitlines() + ["## "]:
            if line.startswith("## "):
                if title and count > SECTION_CAP:
                    warnings.append(f"{rel(path)}: section '{title}' has {count} lines (cap {SECTION_CAP}): split it into its own file")
                title, count = line[3:].strip(), 0
            else:
                count += 1


def is_index(key):
    """Whether a note is its folder's index (named like the folder), which every folder repeats by design."""
    parts = key.split("/")
    return len(parts) > 1 and parts[-1] == parts[-2]


def is_knowledge(key):
    """A knowledge note, shared or personal (not a folder index)."""
    return (key.startswith("neocortex/knowledge/") or re.match(r"prefrontal/([^/]+/)?knowledge/", key)) and not is_index(key)


def check_health(files, warnings, today=None):
    """Warn on two notes about one subject, knowledge notes without sources, and stale active project hubs."""
    today = today or datetime.date.today()
    scopes = {}
    for path in files:
        key = rel(path)[:-3].lower()
        if is_index(key) or key in ROOTS:
            continue
        project = PROJECT.match(key)
        scopes.setdefault((project.group(0) if project else "", key.rsplit("/", 1)[-1]), []).append(rel(path))
    for (scope, _), places in sorted(scopes.items()):
        if len(places) > 1:
            where = f"in {scope.rstrip('/')}" if scope else "across the brain"
            warnings.append(f"{places[0]}: same note name {where} as {', '.join(places[1:])}: one subject, one note")
    for path in files:
        key = rel(path)[:-3].lower()
        lines = path.read_text(encoding="utf-8").splitlines()
        if is_knowledge(key) and not any(line.startswith("sources:") for line in frontmatter(lines) or []):
            warnings.append(f"{rel(path)}: knowledge note without sources in its frontmatter")
        project = PROJECT.match(key)
        if project and key.startswith("neocortex/") and key == project.group(0) + project.group(1):
            header = next((line for line in lines if HUB_STATUS.search(line)), None)
            if header:
                updated = HUB_UPDATED.search(header)
                age = (today - datetime.date.fromisoformat(updated.group(1))).days if updated else None
                if age is None or age > STALE_DAYS:
                    since = f"for {age} days" if age is not None else "(no Updated date)"
                    warnings.append(f"{rel(path)}: active project hub not updated {since}: refresh ## Now or change its Status")


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    hook = "--hook" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--hook"]
    if hook:
        try:
            target = Path(json.load(sys.stdin)["tool_input"]["file_path"]).resolve()
        except (ValueError, KeyError, TypeError):
            return 0
        if not (target.is_file() and is_note(target)):
            return 0
        files = [target]
    else:
        files = [Path(a).resolve() for a in args] or sorted(p for p in ROOT.rglob("*.md") if is_note(p))
    errors, warnings, linked = [], [], set()
    slop, index = slop_pattern(), build_index()
    for path in files:
        check_note(path, slop, index, errors, warnings, linked)
    if not hook or rel(files[0]) in HIPPOCAMPUS:
        check_ids(errors)
    if not hook and not args:
        check_repeats(warnings)
        check_orphans(files, linked, warnings)
        check_prefrontal(warnings)
        check_health(files, warnings)
    out = sys.stderr if hook else sys.stdout
    for line in errors + warnings:
        print(line, file=out)
    if not hook:
        print(f"{len(errors)} errors, {len(warnings)} warnings")
    return (2 if hook else 1) if errors else 0


if __name__ == "__main__":
    sys.exit(main())
