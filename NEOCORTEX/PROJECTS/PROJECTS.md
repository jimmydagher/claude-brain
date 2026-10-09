---
tags:
  - project
---
> Scope: shared project hubs: how they're named, loaded, written and archived · Up: [[NEOCORTEX/NEOCORTEX|NEOCORTEX]] · Pairs with: `PLANNING`, `KNOWLEDGE`

Project hubs are working memory. Only this guide is tracked by git; the project list (`NEOCORTEX/PROJECTS/HUB.md`) and the hubs live in the brain and stay out of the public repo. Missing list? There are no projects yet: start one from the template below. Your own notes on a project go in the mirror, `PREFRONTAL/PROJECTS/<name>/`.

## Core Rules (non-negotiable)

### RULE#1 State direct, rules gated
A hub's state (`## Now`, decisions, next actions, notes) is written directly. A project's lasting rules (conventions, constraints others must follow) and this guide change only through SYNAPSE.

### RULE#2 Project over general Defaults
A hub's rules override an area's Defaults for that project, never its Core Rules (`CORTEX › Conflicts`).

### RULE#3 Resume from Now
When resuming, read the list, then the hub's `## Now` first. Every hub has a `## Now` (8 lines max): where things stand and the next step; rewrite it on "wrap up".

### RULE#4 Stay in scope
The hub's Context states the project's scope; facts outside it stay out of the project, even when they come up in its sessions.

## Defaults
- Changing state lives in the hub; stable how-to rules live in INSTRUCTIONS.
- Log decisions as `YYYY-MM-DD: decision (why) · who`, newest last. A decision about one subject goes in that subject's note; the hub's `## Decisions` keeps project-wide ones.
- "commit this session": review the session for facts, decisions, status and requirements, filter them (`CORTEX › Brain Upkeep`, step 2), then merge them into the hub and its notes. "wrap up" still rewrites only `## Now`.
- Project notes follow the KNOWLEDGE writing rules: verified facts, frontmatter, links and file names.
- Information that fits none of the project's areas gets a new area, never the closest wrong one (`TEMPLATES.md` › Rules, when the brain has it): create the folder with its index, link it from the hub, and say so in one line.
- Code projects: `/sdsi:core` (`CODING` RULE#1).
- Names: the project folder is all lowercase, words joined with hyphens (`life-dashboard/`), in both `NEOCORTEX/PROJECTS/` and the personal mirror; note files inside are uppercase (`LIFE-DASHBOARD.md`). The list is `HUB.md`.
- New project: when `NEOCORTEX/PROJECTS/TEMPLATES.md` exists, ask which template fits, read only its section, and name it on the hub's header line (`Template: technical`; none means default). Create `NEOCORTEX/PROJECTS/<name>/<NAME>.md` from the hub template below, tag it and its sub-notes `project/<name>`, and add a row to the list. The hub links up to this guide; sub-notes link up to the hub by full path (`[[NEOCORTEX/PROJECTS/<name>/<NOTE>|NOTE]]`).
- Done: set Status to done, move reusable lessons to KNOWLEDGE with "share", leave a pointer in the hub.

## Hub template
```markdown
---
tags:
  - project/name
---
> Up: [[NEOCORTEX/PROJECTS/PROJECTS|PROJECTS]]

# NAME
Goal: one sentence · Status: active | paused | done · Template: default · Updated: YYYY-MM-DD

## Now
Where things stand and the next step (8 lines max; rewritten on "wrap up").

## Context
Who it's for, scope, constraints, stack.

## Decisions
- YYYY-MM-DD: decision (why) · who

## Next actions
- [ ] action · owner · due

## Open questions

## Notes
```
