---
tags:
  - project
---
> Index of projects. Open the project's hub, then only the sub-note the task needs. · Pairs with: [[MEMORY/PLANNING|PLANNING]], [[MEMORY/KNOWLEDGE|KNOWLEDGE]]

| Project        | Hub                                                        | What it is                                  |
| -------------- | ---------------------------------------------------------- | ------------------------------------------- |
| Cornerstone    | [[PROJECTS/Cornerstone/CORNERSTONE\|CORNERSTONE]]          | ARIEL, a middleware/integration service     |
| Flammeau       | [[PROJECTS/Flammeau/FLAMMEAU\|FLAMMEAU]]                   | Website (Django) and the business behind it |
| Life-Dashboard | [[PROJECTS/Life-Dashboard/LIFE-DASHBOARD\|LIFE-DASHBOARD]] | _add a one-line description_                |

## Rules
1. A project note overrides general area rules for that project (CORTEX rule 9).
2. Changing state lives in the hub (status, decisions, next actions); stable how-to rules live in MEMORY.
3. Log decisions in the hub as `YYYY-MM-DD: decision (why)`, newest last.
4. Code projects: `/sdsi:core` ([[MEMORY/CODING|CODING]] RULE#1).
5. New project: create `PROJECTS/<Name>/<NAME>.md` from the template below, tag it and its sub-notes `project/<name>`, and add a row above.
6. Every hub has a `## Now` section (8 lines max): where things stand and the next step. Read it first when resuming; rewrite it on "wrap up".

## Hub template
```markdown
---
tags:
  - project/name
---
# NAME
Goal: one sentence · Status: active | paused | done · Updated: YYYY-MM-DD

## Now
Where things stand and the next step (8 lines max; rewritten on "wrap up").

## Context
Who it's for, constraints, stack.

## Decisions
- YYYY-MM-DD: decision (why)

## Next actions
- [ ] action · owner · due

## Notes
[[sub-note]]
```
