# PLAN

## ⛏️ In progress

TTD003 · Learn from the Caveman skill (spec: SPEC › TTD003)

- [x] 1. Baseline: run `scripts/check_brain.py`; record current always-loaded size in characters / 4 so step 4 has a number to compare to.
- [x] 2. CORTEX rule 7: add the `ultra terse` level, the `normal` exit and the full-sentence exceptions. Edit the rule in place; keep CORTEX near its current length.
- [x] 3. AUTOPILOT: add the no-filler-between-tool-calls rule and the never-rewrite-the-human's-prompt rule, once, in the area's Core Rules; no duplicate elsewhere.
- [x] 4. `scripts/check_brain.py`: add the load-size report and the advisory warnings (constants for the two caps, set just above today's baseline so they catch growth). Add tests in `scripts/test_check_brain.py` for under-cap, over-cap and missing-file cases.
- [x] 5. KNOWLEDGE: not written here: shared knowledge is untracked and goes through SYNAPSE; proposed in the report.
- [x] 6. Run the checker and tests; confirm no new errors. Add `meta/CHANGELOG.md` bullets under Unreleased (`TTD003`).
- [x] 7. Review the diff for duplicated rules, then commit.

## Backlog
(none)

## Done
(none)
