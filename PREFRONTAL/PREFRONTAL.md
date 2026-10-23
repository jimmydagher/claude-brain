---
tags:
  - persona
---
> Scope: the personal layer: the human's own instructions, knowledge and project notes, who owns them and where a lesson goes · Up: [[CORTEX|CORTEX]] · Process: [[CORTEX#Brain Upkeep|CORTEX › Brain Upkeep]]

Everything here except this guide is personal and untracked by git; a fresh clone has none of it. Personal files link up to this guide, and this guide never links down to them, so the public repo names nothing personal.

## Layout
The personal layer mirrors the shared one in NEOCORTEX, area for area. Each person has their own folder, `PREFRONTAL/<user>/`, which the brain shows them as plain `PREFRONTAL/`:

| Mirror | Holds | Loads |
| --- | --- | --- |
| `PREFRONTAL/INSTRUCTIONS/` | your preferences and environment facts, one `##` section per area; `## Now` for your current focus and short-lived constraints, each ending `[expires:: YYYY-MM-DD]` | `## Always` and `## Now` with CORTEX; `## <AREA>` with that area |
| `PREFRONTAL/KNOWLEDGE/` | your own notes and drafts | searched on demand |
| `PREFRONTAL/PROJECTS/<name>/` | your side of a shared project | with that project's hub |

Each mirror folder has an index named like the folder that links up to this guide; its files link up to that index.

## Core Rules (non-negotiable)

### RULE#1 Human-owned
Personal instructions and knowledge change only through SYNAPSE (the `HIPPOCAMPUS` queue), and only their owner approves them. The AI proposes and previews; it never edits them outside a commit the human asked for. Personal project notes are the exception: they're written directly, like a hub's state.

### RULE#2 Narrowest true level
Store each fact at the narrowest level where it is still true:

| Level | Example | Home |
| --- | --- | --- |
| Standard | Every system needs logging | SDSI or the team standard |
| Universal rule | Never game the checks | a NEOCORTEX INSTRUCTIONS area |
| Shared fact | How our NAS deploy works | a NEOCORTEX KNOWLEDGE note |
| One project | This project's stack | the project hub in NEOCORTEX/PROJECTS |
| Me, all projects | My logs are plain text, one line per event | a file in `PREFRONTAL/INSTRUCTIONS/` |
| Me, one project | My review checklist for this project | `PREFRONTAL/PROJECTS/<name>/` |
| One machine | Paths, shell, OS | `PREFRONTAL/INSTRUCTIONS/ENVIRONMENT`, `## MACHINE` |

### RULE#3 Fill gaps, never contradict
A personal entry may fill a gap the protected layer leaves open or choose among options it allows. It overrides an area's Defaults, never its Core Rules, a standard, the Token economy rules or the guardrails in [[CORTEX#Behavior|CORTEX › Behavior]] (rule 14). An entry that would contradict them is refused when it's queued, not settled when it's read.

### RULE#4 Personal stays out of the shared files
No tracked file links to a personal file, names a personal topic or quotes a personal entry. Personal files link up to this guide instead; the sections they hold are the index.

## Where a lesson goes
Run the tests in order. When they disagree, ask the human.
1. **Another-dev test.** Would the rule still be right for a different person using this brain? Yes: NEOCORTEX. No: PREFRONTAL.
2. **What vs how.** A requirement ("logs must exist") is global. A choice among valid options ("plain text, one line per event") is personal.
3. **Violation cost.** Breaking it makes something unsafe, broken or inconsistent for others: global. It only annoys the human: personal.
4. **Portability.** Would the human carry it to a new machine or employer? Taste travels with them; environment facts stay with the machine.
5. **Rule or fact?** A rule goes to INSTRUCTIONS; a fact worth looking up goes to KNOWLEDGE; project state goes to the hub.

The destination goes in the SYNAPSE entry: `→ CODING` for a shared rule, `→ PREFRONTAL/INSTRUCTIONS/ENVIRONMENT#CODING` for a personal one.

## Personal instructions
- Files are named by topic (`ENVIRONMENT`, `STYLE`, `PERSONA`, `MINDSET`), not mirrored from the areas. A file exists only after SYNAPSE has routed an entry to it.
- Every file starts with its link up: `> Up: [[PREFRONTAL/INSTRUCTIONS/INSTRUCTIONS|INSTRUCTIONS]]`.
- One `##` section per area, named exactly like the area file (`## CODING`). New entries append to that section.
- `## Always` holds cross-cutting preferences (persona, mood, mindset); they load with CORTEX every session, so keep them very short.
- Facts shared by many areas live once in a small `## MACHINE` section; an area section that needs them links to it (`[[PREFRONTAL/INSTRUCTIONS/ENVIRONMENT#MACHINE|MACHINE]]`).
- For a task, read the `## <AREA>` section of each file that has one, never a whole file. `cortex_load` lists them by area.
- Section names are the index. Rename them with `rename_heading` so links update; the audit flags dead heading links.
- A section over ~150 lines splits into its own file.
