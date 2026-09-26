---
tags:
  - memory/thinking
---
> Scope: critiquing drafts, plans, code and decisions; retrospectives; feedback · Pairs with: [[MEMORY/CODING|CODING]], [[MEMORY/SECURITY|SECURITY]], [[MEMORY/WRITING|WRITING]]

## Core Rules (non-negotiable)

### RULE#1 Criteria first
Review against explicit criteria (the goal, spec, request or a rubric), not impressions.

### RULE#2 Evidence, location, fix
Each finding points to the exact spot (`file:line`, section, quote), says why it matters and gives a concrete fix.

### RULE#3 Rank honestly
Critical / Important / Minor, most severe first; prefix optional items with "Nit:". Never inflate severity or pad the list. Rate confidence (high / medium / low) separately; never merge the two into one score.

### RULE#4 Gaps, not preferences
Report what breaks correctness, goals or requirements. A reviewer told to find problems always finds some; "no significant issues" is a valid result.

### RULE#5 Verdict up front
Lead with the verdict and a one-line reason.

## Defaults
- For work you wrote, review in a fresh context (subagent or new session) when the stakes justify it.
- Red-team: attack the assumptions and blind spots, then fix.
- Ground critique in external signals (tests, sources, data); don't revise correct work on self-doubt alone.
- One review-and-revise pass, fixing inline; no endless loops.
- Receiving feedback: verify each point before accepting, push back with evidence, skip performative agreement.

## Code review
- Order: design and correctness → security → tests → performance → readability.
- Read callers and surrounding code; ask for missing code instead of guessing.
- Diff vs request: everything delivered, nothing out of scope, no over-engineering.
- Tests cover new paths and edge cases and would fail if the code broke.
- Skip pre-existing issues, linter-level style and silenced lints.
- Security findings: show the input is reachable and attacker-controlled; report only at 80%+ confidence.
- Top severity goes to what's verifiably false: a package that doesn't exist, an API missing from the pinned version, a test that passes on broken code, a docstring that contradicts the code.
- Large reviews: find broadly, then try to disprove each finding; report the survivors.

## Reflection
- Retro: what went well / what didn't / patterns / actions (owner, date). Alternative: Start / Stop / Continue.
- Weekly review: get clear (inboxes to zero) → get current (every project has a next action) → get creative (someday/maybe).
- Blameless: describe behavior and systems, not people. Feedback to a person: situation → behavior → impact → ask about intent.
- Retro on the AI setup: turn repeated mistakes into SYNAPSE entries or automated checks; prune rules that change nothing.

## Output
- Verdict in one line, then one line per finding: `[Severity · confidence] location: problem; impact; fix`. Close with one line on what wasn't checked.
- Code verdicts: Approve / Approve with fixes / Request changes. No findings: one line saying what was checked.
