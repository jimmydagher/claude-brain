---
tags:
  - project
---
> How projects are kept. Open the project's hub, then only the sub-note the task needs. · Pairs with: [[NEOCORTEX/PLANNING|PLANNING]], [[NEOCORTEX/KNOWLEDGE|KNOWLEDGE]]

The project list is `PROJECTS/INDEX.md`, a personal file that git doesn't track. Missing? The human has no projects yet: use the template below.

## Rules
1. A project note overrides general area rules for that project ([[CORTEX#Conflicts|CORTEX › Conflicts]]).
2. Changing state lives in the hub (status, decisions, next actions); stable how-to rules live in NEOCORTEX.
3. Log decisions in the hub as `YYYY-MM-DD: decision (why)`, newest last.
4. Code projects: `/sdsi:core` ([[NEOCORTEX/CODING|CODING]] RULE#1).
5. New project: create `PROJECTS/<Name>/<NAME>.md` from the template below, tag it and its sub-notes `project/<name>`, and add a row to `PROJECTS/INDEX.md`.
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
