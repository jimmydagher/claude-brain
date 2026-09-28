---
tags:
  - memory/personal
---
> Scope: the human's own layer: who owns it, where a lesson goes, and how AMYGDALA routes to it · Storage: [[PREFRONTAL/PREFRONTAL|PREFRONTAL]] · Process: [[CORTEX#Brain Upkeep|CORTEX › Brain Upkeep]]

## Core Rules (non-negotiable)

### RULE#1 Human-owned
Preferences reach PREFRONTAL, and rows reach AMYGDALA, only through SYNAPSE (see [[HIPPOCAMPUS/HIPPOCAMPUS|HIPPOCAMPUS]]), and only the human approves them. The AI proposes and previews; it never edits them outside a commit the human asked for. Project hubs are the exception: their state is written directly ([[PREFRONTAL/PREFRONTAL#Projects|PREFRONTAL › Projects]]).

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
Everything in LIMBIC and PREFRONTAL except their guides is untracked by git, so the public repo stays generic. No tracked file links to a personal file, names a personal topic or quotes a personal entry; AMYGDALA is the only index into PREFRONTAL.

## Where a lesson goes
Run the tests in order. When they disagree, ask the human.
1. **Another-dev test.** Would the rule still be right for a different person using this brain? Yes: NEOCORTEX. No: PREFRONTAL.
2. **What vs how.** A requirement ("logs must exist") is global. A choice among valid options ("plain text, one line per event") is personal.
3. **Violation cost.** Breaking it makes something unsafe, broken or inconsistent for others: global. It only annoys the human: personal.
4. **Portability.** Would the human carry it to a new machine or employer? Taste travels with them; environment facts stay with the machine.

The destination goes in the SYNAPSE entry: `→ CODING` for global, `→ PREFRONTAL/ENVIRONMENT#CODING` for personal.

## AMYGDALA
`LIMBIC/AMYGDALA.md` is the personal router. It loads with CORTEX and THALAMUS, once per session, if it exists; no AMYGDALA (a fresh clone): skip silently.
- One `##` section per area, named exactly like the area file (`## CODING`), each a list of deep links: `- [[PREFRONTAL/ENVIRONMENT#CODING|ENVIRONMENT › CODING]]`. Several areas may point into the same file.
- `## Always` lists cross-cutting sections (persona, mood, mindset) that load with AMYGDALA. Keep them very short: they load every session.
- `## Projects` holds one link, to `PREFRONTAL/PROJECTS/PROJECTS.md`, the project list.
- Load only the sections listed for the task's area; they don't count toward the 3-file cap in [[THALAMUS#Routing Rules|THALAMUS › Routing Rules]].
- A new PREFRONTAL file or section adds its AMYGDALA row in the same commit.

## Avoid
- Secrets or credentials: never, anywhere in the brain.
- A personal choice stored in a NEOCORTEX area file, or a universal rule stored in PREFRONTAL.
- Loading a whole PREFRONTAL file when one section was linked.
- Duplicating a fact across sections instead of linking to `## MACHINE`.
