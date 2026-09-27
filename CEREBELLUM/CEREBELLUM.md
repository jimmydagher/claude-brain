---
tags:
  - memory/personal
---
> Scope: the human's own layer of the brain: personal preferences, environment facts, style and mindset · Load: to decide where a lesson goes; the rest of CEREBELLUM loads through `CEREBELLUM/MAP.md` · Process: [[CORTEX#Brain Upkeep|CORTEX › Brain Upkeep]]

## Core Rules (non-negotiable)

### RULE#1 Human-owned
Entries reach CEREBELLUM only through SYNAPSE (see [[HIPPOCAMPUS/HIPPOCAMPUS|HIPPOCAMPUS]]), and only the human approves them. The AI proposes and previews; it never edits CEREBELLUM outside a commit the human asked for.

### RULE#2 Narrowest true level
Store each fact at the narrowest level where it is still true:

| Level | Example | Home |
| --- | --- | --- |
| Standard | Every system needs logging | SDSI or the team standard |
| Universal rule | Never game the checks | a MEMORY area file |
| Me, all projects | My logs are plain text, one line per event | CEREBELLUM |
| One project | This project's stack | the PROJECTS hub |
| One machine | Paths, shell, OS | CEREBELLUM, environment file |

### RULE#3 Fill gaps, never contradict
A CEREBELLUM entry may fill a gap a standard leaves open or choose among options it allows. It overrides an area file's Defaults, never its Core Rules, a standard, the Token economy rules or the guardrails in CORTEX rule 14.

### RULE#4 Load the linked section only
Read the section `MAP.md` lists for the task's area, not the whole file. It doesn't count toward CORTEX's 3-file cap.

### RULE#5 Personal stays out of the shared files
Everything in CEREBELLUM except this guide is untracked by git, so the public repo stays generic. No tracked file links to a personal file, names a personal topic or quotes a personal entry; only `MAP.md` points into CEREBELLUM.

## Where a lesson goes
Run the tests in order. When they disagree, ask the human.
1. **Another-dev test.** Would the rule still be right for a different person using this brain? Yes: MEMORY. No: CEREBELLUM.
2. **What vs how.** A requirement ("logs must exist") is global. A choice among valid options ("plain text, one line per event") is personal.
3. **Violation cost.** Breaking it makes something unsafe, broken or inconsistent for others: global. It only annoys the human: personal.
4. **Portability.** Would the human carry it to a new machine or employer? Taste travels with them; environment facts stay with the machine.

The destination goes in the SYNAPSE entry: `→ CODING` for global, `→ CEREBELLUM/ENVIRONMENT#CODING` for personal.

## Files and links
- Files are named by topic (`ENVIRONMENT`, `STYLE`, `PERSONA`, `MINDSET`), not mirrored from the areas. A file exists only after SYNAPSE has routed an entry to it.
- One `##` section per area inside a file, named exactly like the area (`## CODING`). New entries append to that section.
- `CEREBELLUM/MAP.md` is the only index. CORTEX reads it once per session, if it exists, and loads from it only the sections listed for the task's area. No map or no CEREBELLUM folder (a fresh clone): skip silently.
- MAP has one `##` section per area (`## CODING`), each a list of deep links: `- [[CEREBELLUM/ENVIRONMENT#CODING|ENVIRONMENT › CODING]]`. Several areas may point into the same file.
- **Cross-cutting** files (persona, mood, mindset) apply to every task, so MAP lists them under `## Always`, loaded with the map. Keep them very short: they load every session.
- Facts shared by many areas live once in a small `## MACHINE` section, not repeated.
- Creating a file or section also adds its row to MAP in the same commit; no tracked file changes.- Section names are part of the link contract. Rename them in Obsidian or with `rename_heading` so links update; the audit flags dead heading links.
- A section over ~150 lines splits into its own file; only the link target changes.

## Avoid
- Secrets or credentials: never, anywhere in the brain.
- A personal choice stored in a MEMORY area file, or a universal rule stored here.
- Loading a whole CEREBELLUM file when one section was linked.
- Duplicating a fact across sections instead of linking to `## MACHINE`.
