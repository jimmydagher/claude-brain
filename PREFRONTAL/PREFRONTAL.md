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
