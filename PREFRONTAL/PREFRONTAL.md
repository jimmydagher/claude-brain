---
tags:
  - persona
---
> Scope: working memory: the human's own preferences and active projects, who owns them and where a lesson goes · Up: [[CORTEX|CORTEX]] · Process: [[CORTEX#Brain Upkeep|CORTEX › Brain Upkeep]]

Everything here except this guide is personal and untracked by git; a fresh clone has none of it. Personal files link up to this guide, and this guide never links down to them, so the public repo names nothing personal.

## Core Rules (non-negotiable)

### RULE#1 Human-owned
Preferences change only through SYNAPSE (the `HIPPOCAMPUS` queue), and only the human approves them. The AI proposes and previews; it never edits them outside a commit the human asked for. Project hubs are the exception: their state is written directly (see Projects below).

### RULE#2 Narrowest true level
Store each fact at the narrowest level where it is still true:

| Level | Example | Home |
| --- | --- | --- |
| Standard | Every system needs logging | SDSI or the team standard |
| Universal rule | Never game the checks | a NEOCORTEX area file |
| Me, all projects | My logs are plain text, one line per event | a PREFRONTAL topic file |
| One project | This project's stack | the project hub in PREFRONTAL/PROJECTS |
| One machine | Paths, shell, OS | PREFRONTAL, environment file |

### RULE#3 Fill gaps, never contradict
A PREFRONTAL entry may fill a gap a standard leaves open or choose among options it allows. It overrides an area file's Defaults, never its Core Rules, a standard, the Token economy rules or the guardrails in [[CORTEX#Behavior|CORTEX › Behavior]] (rule 14).

### RULE#4 Personal stays out of the shared files
No tracked file links to a personal file, names a personal topic or quotes a personal entry. Personal files link up to this guide instead; the sections they hold are the index.

## Where a lesson goes
Run the tests in order. When they disagree, ask the human.
1. **Another-dev test.** Would the rule still be right for a different person using this brain? Yes: NEOCORTEX. No: PREFRONTAL.
2. **What vs how.** A requirement ("logs must exist") is global. A choice among valid options ("plain text, one line per event") is personal.
3. **Violation cost.** Breaking it makes something unsafe, broken or inconsistent for others: global. It only annoys the human: personal.
4. **Portability.** Would the human carry it to a new machine or employer? Taste travels with them; environment facts stay with the machine.

The destination goes in the SYNAPSE entry: `→ CODING` for global, `→ PREFRONTAL/ENVIRONMENT#CODING` for personal.

## Preferences
- Files are named by topic (`ENVIRONMENT`, `STYLE`, `PERSONA`, `MINDSET`), not mirrored from the areas. A file exists only after SYNAPSE has routed an entry to it.
- Every file starts with its link up: `> Up: [[PREFRONTAL/PREFRONTAL|PREFRONTAL]]`.
- One `##` section per area, named exactly like the area file (`## CODING`). New entries append to that section.
- `## Always` holds cross-cutting preferences (persona, mood, mindset); they load with CORTEX every session, so keep them very short.
- Facts shared by many areas live once in a small `## MACHINE` section; an area section that needs them links to it (`[[PREFRONTAL/ENVIRONMENT#MACHINE|MACHINE]]`).
- For a task, read the `## <AREA>` section of each file that has one, never a whole file. `cortex_load` lists them by area; on disk, find them with a heading scan (`grep "^## " PREFRONTAL/*.md`).
- Section names are the index. Rename them in Obsidian or with `rename_heading` so links update; the audit flags dead heading links.
- A section over ~150 lines splits into its own file.

## Projects
Project hubs are working memory: written directly, not through SYNAPSE. The project list is `PREFRONTAL/PROJECTS/PROJECTS.md`: it links up to this guide and down to each hub. Missing? The human has no projects yet: use the template below. Pairs with: `PLANNING`, `KNOWLEDGE`
1. A project note overrides general area rules for that project ([[CORTEX#Conflicts|CORTEX › Conflicts]]).
2. Changing state lives in the hub (status, decisions, next actions); stable how-to rules live in NEOCORTEX.
3. Log decisions in the hub as `YYYY-MM-DD: decision (why)`, newest last.
4. Code projects: `/sdsi:core` (`CODING` RULE#1).
5. New project: create `PREFRONTAL/PROJECTS/<Name>/<NAME>.md` from the template below, tag it and its sub-notes `project/<name>`, and add a row to the project list. Link sub-notes by full path (`[[PREFRONTAL/PROJECTS/<Name>/<NOTE>|NOTE]]`).
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

## Avoid
- Secrets or credentials: never, anywhere in the brain.
- A personal choice stored in a NEOCORTEX area file, or a universal rule stored in PREFRONTAL.
- Loading a whole PREFRONTAL file when one section applies.
- Duplicating a fact across sections instead of linking to `## MACHINE`.
