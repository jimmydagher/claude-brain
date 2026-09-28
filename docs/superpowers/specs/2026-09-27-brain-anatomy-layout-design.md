---
tags:
  - spec
---
# Brain anatomy layout: design

Status: draft for review · Date: 2026-09-27 · Repos: `claude-brain` (vault), `cortex` (MCP server)

## Goal

Reorganize the vault so each folder plays one anatomical role, the shared brain stays generic and protected, all personal memory lives in one untracked place, and every wikilink resolves. The Cortex server's entrypoint (`CORTEX.md`) does not change.

Success means:
- Each top-level folder has one job and one write rule (protected or freely writable).
- A session loads CORTEX, THALAMUS and AMYGDALA in one `cortex_load` call; a task then reads at most 3 more brain files.
- `check_brain.py` and `cortex_check` report 0 errors, and the graph has no unresolved nodes and no orphans.
- No untracked personal file is lost or left behind.

## Decisions

| # | Decision | Why |
| --- | --- | --- |
| D1 | `CORTEX.md` stays the entrypoint and keeps the highest-level instructions | Cortex finds brains by this file; it is the executive layer |
| D2 | New `THALAMUS.md` holds only routing: routing rules and the routing table | The thalamus is the relay; routing grows without bloating the rules |
| D3 | `MEMORY/` becomes `NEOCORTEX/` | Long-term, shared, protected memory |
| D4 | Lobes are the four existing tag families (Core, Technical, Thinking, Communication); `NEOCORTEX/` stays flat | Changing an area's lobe is a one-tag edit; no link churn |
| D5 | Each area has one home lobe; links to other lobes are ordinary wikilinks (the synapses) | No file is duplicated across lobes |
| D6 | THALAMUS is the only place that lists lobe membership | One source of truth |
| D7 | `NEOCORTEX/PROJECTS.md` is removed; NEOCORTEX never holds project content | Projects are personal, working memory |
| D8 | `CEREBELLUM/` is retired. `LIMBIC/` holds the personal router `AMYGDALA.md` (was `MAP.md`) and its guide | The amygdala tags what matters to this human |
| D9 | `PREFRONTAL/` holds all personal memory: preference topic files and `PROJECTS/` | Working memory: active goals and the human's own context |
| D10 | Project list is `PREFRONTAL/PROJECTS/PROJECTS.md` (was `PROJECTS/INDEX.md`) | Folder-note convention |
| D11 | Preferences change only through SYNAPSE; project hubs are written directly. Server enforces this with a `!` exception in the protected list | Status changes every session; preferences need approval |
| D12 | Every folder gets a guide note named after it; guides link up to their router or process, never down to every file | Folders become visible graph nodes without duplicate edges |
| D13 | Tags stay as they are (`memory/core`, `memory/technical`, `memory/thinking`, `memory/communication`, `memory/personal`, `project`, `project/<name>`, `hippocampus`) | `graph.json` and its checked colors keep working; "memory" names the concept, not the folder |

## Target layout

```text
CORTEX.md                 entrypoint: always-on rules, conflict order, brain upkeep      tracked, protected
THALAMUS.md               router: routing rules + routing table grouped by lobe          tracked, protected
NEOCORTEX/                shared long-term memory                                        tracked, protected
  NEOCORTEX.md            guide: what a lobe is, lobe tags, area-file shape, cross-lobe links
  CODING.md … WRITING.md  17 area files
HIPPOCAMPUS/              intake (unchanged)
  HIPPOCAMPUS.md          guide + templates                                              tracked, protected
  SYNAPSE.md, ENGRAM.md   in transit                                                     untracked, server-managed
LIMBIC/                   personal routing
  LIMBIC.md               guide: ownership, scope ladder, where a lesson goes            tracked, protected
  AMYGDALA.md             personal router: sections to load per area, plus projects      untracked, protected
PREFRONTAL/               all personal memory
  PREFRONTAL.md           guide: topic files, sections, loading, write rules, hub template   tracked, protected
  ENVIRONMENT.md, STYLE.md, PERSONA.md …   preference topic files (created by SYNAPSE)    untracked, protected
  PROJECTS/               project working memory                                         untracked, writable
    PROJECTS.md           project list
    <Name>/<NAME>.md      hubs and sub-notes
```

## File moves

| Old | New | Notes |
| --- | --- | --- |
| `MEMORY/*.md` (17 areas) | `NEOCORTEX/*.md` | `git mv`; content changes limited to link and name updates |
| `MEMORY/PROJECTS.md` | removed | Rules and hub template move into `PREFRONTAL/PREFRONTAL.md` |
| routing rules and table in `CORTEX.md` | `THALAMUS.md` | CORTEX keeps the rest |
| `CEREBELLUM/CEREBELLUM.md` | split into `LIMBIC/LIMBIC.md` and `PREFRONTAL/PREFRONTAL.md` | Ownership and scope ladder go to LIMBIC; file and section conventions go to PREFRONTAL |
| `CEREBELLUM/MAP.md` | `LIMBIC/AMYGDALA.md` | Untracked; link targets change from `CEREBELLUM/` to `PREFRONTAL/` |
| `CEREBELLUM/<topic>.md` (none exist today) | `PREFRONTAL/<topic>.md` | Nothing to move now |
| `PROJECTS/INDEX.md` | `PREFRONTAL/PROJECTS/PROJECTS.md` | Untracked |
| `PROJECTS/<Name>/…` | `PREFRONTAL/PROJECTS/<Name>/…` | Untracked |
| (new) | `NEOCORTEX/NEOCORTEX.md` | Tracked guide |

## Note contents

### CORTEX.md
- Opening: what the file is, "load once per session" (link to MECHANICS), and that loading also brings THALAMUS and, when present, AMYGDALA.
- `## Conflicts` (was routing rule 9): the human's latest message > project note > PREFRONTAL > area file > CORTEX and THALAMUS; Token economy exception unchanged.
- `## Always-on Rules`: Token economy 1-7 and Behavior 8-16 unchanged in wording, except rule 14 names NEOCORTEX, PREFRONTAL and project hubs as instruction sources.
- `## Brain Upkeep`: unchanged process; destinations become `→ CODING` (global) or `→ PREFRONTAL/ENVIRONMENT#CODING` (personal); the scope ladder link points to LIMBIC; rule 4's "adds its row to MAP" becomes "adds its row to AMYGDALA".
- Links: THALAMUS, `NEOCORTEX/MECHANICS`, `NEOCORTEX/SECURITY`, `NEOCORTEX/WRITING`, `LIMBIC/LIMBIC`, `HIPPOCAMPUS/HIPPOCAMPUS`.

### THALAMUS.md
- `## Routing Rules`: today's rules 1-8, with rule 5 rewritten: AMYGDALA, when it exists, loads with CORTEX; load only the sections it lists for the task's area and its `Always` ones; THALAMUS, AMYGDALA and those sections don't count toward the 3-file cap.
- `## Routing Table`: one `###` section per lobe (Core, Technical, Thinking, Communication), each a table with the same columns as today. The section opens with a link to `NEOCORTEX/NEOCORTEX` for what a lobe is.
- `## Outside the neocortex`: Projects row → `PREFRONTAL/PREFRONTAL` (the guide; a named project's hub is found through AMYGDALA's `## Projects` section); personal-layer row → `LIMBIC/LIMBIC`.
- THALAMUS never links to an untracked file.

### NEOCORTEX/NEOCORTEX.md
- What a lobe is (a tag family, not a folder), the four families and their colors, how to pick an area's home lobe, and that cross-lobe connections are `Pairs with` wikilinks.
- The area-file shape: tags, scope line, Core Rules, Defaults, Avoid, Output; under ~80 lines.
- It does not list members (D6).

### LIMBIC/LIMBIC.md
- Rules 1-3 from today's CEREBELLUM guide (human-owned, narrowest true level, fill gaps never contradict), with the level table's personal rows pointing to PREFRONTAL.
- `## Where a lesson goes`: the four tests, unchanged.
- `## AMYGDALA`: format: one `##` per area named like the area file, `## Always` for cross-cutting sections, `## Projects` with one link to `PREFRONTAL/PROJECTS/PROJECTS`. Rows are deep links: `- [[PREFRONTAL/ENVIRONMENT#CODING|ENVIRONMENT › CODING]]`.
- Rule 5 becomes: nothing tracked links to an untracked personal file or quotes a personal entry; AMYGDALA is the only index into PREFRONTAL.

### LIMBIC/AMYGDALA.md (untracked)
Today's MAP content with paths updated, plus a `## Projects` section. It links up to `LIMBIC/LIMBIC`.

### PREFRONTAL/PREFRONTAL.md
- `## Preferences`: topic files (`ENVIRONMENT`, `STYLE`, `PERSONA`, `MINDSET`), one `##` per area, `## MACHINE` for shared facts, ~150-line section cap, load the linked section only, change only through SYNAPSE.
- `## Projects`: today's `MEMORY/PROJECTS.md` rules and hub template, with paths under `PREFRONTAL/PROJECTS/` and the list file named `PROJECTS.md`. Hubs are written directly (not through SYNAPSE).
- Links up to `LIMBIC/LIMBIC` and `CORTEX#Brain Upkeep`.

### PREFRONTAL/PROJECTS/PROJECTS.md (untracked)
Today's INDEX table with hub links rewritten to `PREFRONTAL/PROJECTS/<Name>/<NAME>`; the header links to `PREFRONTAL/PREFRONTAL`.

### Other tracked notes
- `NEOCORTEX/MECHANICS.md`: session order (CORTEX + THALAMUS + AMYGDALA, then areas, then PREFRONTAL sections, then hubs); link examples use `NEOCORTEX/`; the Tags section describes lobes and personal tags with the new folder names.
- `NEOCORTEX/PLANNING.md`, `KNOWLEDGE.md`, `BUSINESS.md`: `Pairs with` links to `MEMORY/PROJECTS` become `PREFRONTAL/PREFRONTAL`.
- `HIPPOCAMPUS/HIPPOCAMPUS.md`: template comments use `NEOCORTEX/FILE` and `PREFRONTAL/FILE#Section`.
- `README.md`: diagram, folder list, graph-colors table, gitignore note, "Make it yours".
- Numbered cross-file references become heading links the checker can verify: "CORTEX rule 14" → `[[CORTEX#Behavior|CORTEX › Behavior]]` (rule 14), "CORTEX rule 3" and "rule 8" → `[[THALAMUS#Routing Rules|THALAMUS › Routing Rules]]`, "CORTEX rule 9" → `[[CORTEX#Conflicts|CORTEX › Conflicts]]`, "CORTEX's 3-file cap" → THALAMUS link.

## Lobes

Membership is today's tag families; THALAMUS lists it.

| Lobe | Tag | Areas |
| --- | --- | --- |
| Core | `memory/core` | MECHANICS, PROMPTING (plus CORTEX and THALAMUS for color) |
| Technical | `memory/technical` | CODING, AUTOPILOT, SECURITY, ANALYTICS |
| Thinking | `memory/thinking` | THINKING, PLANNING, RESEARCH, REVIEW, KNOWLEDGE, LEARNING |
| Communication | `memory/communication` | WRITING, LANGUAGE, VISUAL, BUSINESS, ASSISTANT |

Every area already links to at least one area in another lobe through its `Pairs with` line (checked 2026-09-27), so no new cross-lobe links are required. New notes take tags: the NEOCORTEX guide `memory/core`; the LIMBIC and PREFRONTAL guides, AMYGDALA and preference files `memory/personal`, so the personal layer stays uncolored as it is today.

## Load sequence

1. "use the cortex": `cortex_load` returns CORTEX, THALAMUS, AMYGDALA (if present) and AMYGDALA's `Always` sections.
2. Per task: THALAMUS picks the area file(s), at most 3; AMYGDALA's section for that area loads its PREFRONTAL sections.
3. Named project: AMYGDALA `## Projects` → PROJECTS.md → the hub's `## Now` first.

## Protection and tracking

| Path | Git | Server write rule |
| --- | --- | --- |
| `CORTEX.md`, `THALAMUS.md` | tracked | protected |
| `NEOCORTEX/` | tracked | protected |
| `HIPPOCAMPUS/HIPPOCAMPUS.md` | tracked | protected |
| `HIPPOCAMPUS/SYNAPSE.md`, `ENGRAM.md` | ignored | synapse tools only |
| `LIMBIC/LIMBIC.md` | tracked | protected |
| `LIMBIC/AMYGDALA.md` | ignored | protected |
| `PREFRONTAL/PREFRONTAL.md` | tracked | protected |
| `PREFRONTAL/<topic>.md` | ignored | protected |
| `PREFRONTAL/PROJECTS/` | ignored | writable (`!` exception) |

`.gitignore` replaces the CEREBELLUM and PROJECTS rules with:

```text
LIMBIC/*
!LIMBIC/LIMBIC.md
PREFRONTAL/*
!PREFRONTAL/PREFRONTAL.md
```

## Cortex server changes

Separate release (0.3.0) in the `cortex` repo, on its own branch, started only after the in-progress GUI work there is committed by the human.
- `layout` config: `router: THALAMUS.md`, `memory: NEOCORTEX/`, `limbic: LIMBIC/`, `personal: PREFRONTAL/`, `personal_map: LIMBIC/AMYGDALA.md`, `projects: PREFRONTAL/PROJECTS/`.
- Default protected list: CORTEX, router, memory, limbic, personal, hippocampus guide, and `!` + projects.
- `is_protected`: a rule starting with `!` exempts a path; an exemption wins over a matching protection.
- `overview` / `cortex_load`: also returns the router's path and text. A missing router is reported, not fatal.
- `cortex_check`: warns when a layout folder (memory, limbic, personal) is not covered by a protected rule, so a stale protected list is visible.
- Text updates: `INSTRUCTIONS` in `mcp_tools.py`, SYNAPSE/ENGRAM template comments in `synapse.py`, docstring examples, `README.md`, `docs/cheat-sheet.md`, skeleton brain (`skeleton/MEMORY/GENERAL.md` → `skeleton/NEOCORTEX/GENERAL.md`, plus a skeleton `THALAMUS.md`).
- Tests: update fixtures to the new layout; add tests for the `!` exemption, the router in `overview`, and the unprotected-layout warning.
- After deploy: reset the protected list to the new defaults (re-run setup or save settings with an empty list) and confirm via `status()`.

## Link integrity

`check_brain.py` changes:
- Paths: `MEMORY` → `NEOCORTEX` (slop list, repeat check); section cap applies to `PREFRONTAL/*.md` except the guide.
- New error: a bare-name link (`[[BUSINESS]]`) that matches more than one note.
- New error: a tracked note linking to an untracked personal path (`LIMBIC/` or `PREFRONTAL/` except their guides).
- New warning: an orphan note (no incoming wikilinks), excluding the roots `CORTEX.md` and `LIMBIC/AMYGDALA.md` (tracked notes may not link to it), `README.md`, specs and HIPPOCAMPUS's in-transit files.
- `docs/` is skipped as a vault note folder and added to Obsidian's excluded files, so specs stay out of the graph.

Verification after each step: `python scripts/check_brain.py` shows 0 errors; a grep for `MEMORY/`, `CEREBELLUM`, `MAP.md` and `INDEX.md` finds nothing outside ENGRAM (history is left as written). After the server release: `cortex_check` clean and `cortex_load` returns all three routers. Final: Obsidian "Reload app without saving", graph shows no unresolved nodes and no orphans.

## Rollout

Each step is one commit in `claude-brain`, verified before the next.
0. Safety: copy `PROJECTS/`, `CEREBELLUM/` and `HIPPOCAMPUS/` (untracked files) to a dated backup outside the vault; close Obsidian during moves.
1. `MEMORY/` → `NEOCORTEX/`; rewrite links; numbered references → heading links.
2. Split CORTEX into CORTEX + THALAMUS.
3. Personal layer: create LIMBIC and PREFRONTAL guides from CEREBELLUM's guide and `MEMORY/PROJECTS.md`; move MAP → AMYGDALA and PROJECTS → `PREFRONTAL/PROJECTS/` (INDEX → PROJECTS.md); update `.gitignore`; remove CEREBELLUM and `NEOCORTEX/PROJECTS.md`.
4. Lobes: `NEOCORTEX/NEOCORTEX.md`; THALAMUS table grouped by lobe; MECHANICS Tags section.
5. `check_brain.py` upgrades, README, Obsidian exclusion for `docs/`.
6. Cortex server 0.3.0, deploy, reset protected list, verify.

Between step 3 and step 6 the deployed server still looks for `CEREBELLUM/MAP.md` (it skips a missing map silently) and still protects `MEMORY/` (which no longer exists), so NEOCORTEX is unprotected on the server until step 6. Steps 1-6 run in one session to keep that window short.

## Out of scope

- Renaming tags or changing graph colors.
- Changing any area file's rules beyond links and names.
- New areas, merging areas, or moving an area to a different lobe.
- Rewriting ENGRAM's history.

## Risks

| Risk | Mitigation |
| --- | --- |
| Untracked personal files lost in a move | Step 0 backup; compare file counts after step 3 |
| Server protection lapses after the rename | Step 6 in the same session; `cortex_check` warns on unprotected layout folders |
| Numbered rule references silently wrong | Replaced by heading links the checker verifies |
| Obsidian rewrites links during an external move | Obsidian closed during moves |
| Name collisions on bare links (`BUSINESS` in NEOCORTEX and a project) | New ambiguous-link error; project links use full paths |
