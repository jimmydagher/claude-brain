---
tags:
  - memory/technical
---
> Scope: writing, fixing, debugging and refactoring code · Pairs with: [[NEOCORTEX/REVIEW|REVIEW]] (code review), [[NEOCORTEX/SECURITY|SECURITY]], [[NEOCORTEX/AUTOPILOT|AUTOPILOT]]

## Core Rules (non-negotiable)

### RULE#1 Use the skill `/sdsi:core`
for both projects that are starting new and existing one.
- SDSI owns the standards: naming, structure, config, secrets, logging, errors, testing, dependencies, docs, versioning, workflow. Don't restate or override them here.
- Skill not available in this harness? Apply its core anyway: no over-engineering, no silent assumptions, every changed line traces to the request, plan before code, verify against a test, build or run and show the evidence.

### RULE#2 Debug by reproduction
1. Reproduce first: a failing test or exact command that fails for the right reason.
2. Change one thing at a time; fix the root cause, not the symptom.
3. After two failed fixes, stop and rethink the approach. After three, report what you tried.

### RULE#3 Never game the checks
Never weaken, skip or delete tests, hard-code expected values, swallow errors or bypass hooks (`--no-verify`) to get green. If a check itself is wrong, say so and ask.

### RULE#4 Use `Graphify` Context First (if available, otherwise skip)
1. BEFORE scanning, reading, or indexing raw source files in this repository, always consult the contents of `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.json`.
2. Use this cached data to understand the project architecture, virtual environments, package structures, module dependencies, and database schemas.
3. Prioritize using the `Graphify` index to locate specific functions, classes, or variables instead of blindly reading multiple large files. This minimizes token consumption.

## Defaults
- Never invent APIs, flags or versions; check the installed packages or current docs.
- Request looks wrong, or a simpler path exists? Say so in one sentence, then do as asked unless it's risky.
- The human is describing a problem or thinking aloud: give your assessment; edit only when asked.
- Scale verification to risk: a syntax check for trivial edits, a trace for logic, written scenarios for state or concurrency.
- New test? Prove it catches the bug: break the code, watch the test fail, restore.
- Delete what your change replaces and any temp files you made. Flag unrelated dead code; don't remove it.
- Search (graph, grep, symbols) before opening files; read only the ranges you need.
- Log files are traditional plain text: one line per event (timestamp, level, message), rotated by size. Never JSON or JSONL log files; this sets the file format SDSI's logging standard leaves open. Keep them in a dedicated `logs/` folder, never inside config or data folders.

## Avoid
- "Should work now" without a fresh run.
- Shotgun debugging: several changes at once, "try X and see".
- Drive-by reformatting, renames or refactors.
- Shims for removed code: `_unused` renames, re-exports, `// removed` comments.
- Reverting changes you didn't make; `reset --hard` or `checkout --` without being asked.
- Pasting whole files into the reply.

## Output
- First sentence: the outcome. Then what changed, where (`file:line`) and why.
- Evidence: the command you ran and the output lines that prove it, never full logs. Name anything unverified, skipped or still failing.
