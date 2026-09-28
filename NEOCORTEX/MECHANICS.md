---
tags:
  - memory/core
---
> Scope: how the brain loads, caches and reloads; how to write Markdown files · Pairs with: [[NEOCORTEX/PROMPTING|PROMPTING]], [[NEOCORTEX/KNOWLEDGE|KNOWLEDGE]], [[NEOCORTEX/WRITING|WRITING]]

## Core Rules (non-negotiable)

### RULE#1 On request, then cached for the session
The brain is off until the human says "use the cortex" or "use your brain" (or runs `/cortex`). Then read `CORTEX.md` and `THALAMUS.md` once, reply `Brain: on`, and apply it to every task for the rest of the session.

### RULE#2 Read once, reuse from context
A brain file read this session stays in context, and later turns reuse it from the prompt cache. Open area files only when a task needs them, once each; never re-read to "refresh".

### RULE#3 Reload on purpose
Re-read CORTEX, THALAMUS and the area files in use when the human says "reload the brain", when you're told a brain file changed, or after the context was compacted (compaction summarizes files read by tools, so their exact rules are gone).

### RULE#4 No hard wraps in Markdown
One paragraph or list item is one line, however long. Let the editor soft-wrap; never insert line breaks to fit a narrow window.

## Session
- Order: CORTEX first, then area files as tasks need them (plus the PREFRONTAL sections `LIMBIC/AMYGDALA.md` lists for the area), then project notes (a hub's `## Now` first). SYNAPSE only when capturing, reviewing or committing; ENGRAM only by search.
- Per-task announcements follow [[THALAMUS#Routing Rules|THALAMUS › Routing Rules]] (rule 3) (`Brain: CODING + SECURITY`); don't repeat `Brain: on`.
- Always-on setups import CORTEX in CLAUDE.md (`@path`), so it loads at session start, is prompt-cached and survives compaction. If CORTEX is already in context that way, skip the read in RULE#1.

## Markdown
- Line breaks only where structure needs them: between blocks, list items, table rows, lines of code.
- Headings with `#`, in order (no jump from `##` to `####`). Standalone docs (README, specs) get one H1; vault notes use the filename as their title.
- One blank line around headings, lists, tables and code blocks; never two in a row.
- `-` for bullets, `1.` for numbered steps.
- Code in fenced blocks with a language tag (`bash`, `python`, `text`); inline code for names, paths and commands.
- Tables only for real rows and columns; a literal `|` inside a cell is written `\|`.
- Vault links are wikilinks that carry the vault path: `[[NEOCORTEX/CODING|CODING]]`, or `[[NEOCORTEX/CODING\|CODING]]` inside a table. A section link adds `#Heading`: `[[PREFRONTAL/ENVIRONMENT#CODING|ENVIRONMENT › CODING]]`.
- Files meant for GitHub (README) use relative Markdown links, since GitHub doesn't render wikilinks. External links: `[descriptive text](url)`, never "click here" or a bare URL.
- Bold sparingly for key terms, never as a fake heading.
- YAML frontmatter only at the very top; HTML only for comments (`<!-- -->`).
- A Markdown file a script writes (e.g. a CHANGELOG rendered by a release script) takes its format from the script: fix the generator, never hand-edit its output, or the next run undoes the edit.

## Tags
- Every brain note starts with a `tags` property (YAML list); the graph colors come from it (`.obsidian/graph.json`).
- Families: `memory/core` (the brain itself), `memory/technical` (build, operate, secure, data), `memory/thinking` (reason, plan, research, review, learn, file knowledge), `memory/communication` (write, translate, design, sell, converse).
- Project notes: `project/<name>` (lowercase, hyphens); the PROJECTS index: `project`.
- HIPPOCAMPUS notes: `hippocampus`, left uncolored in the graph because they aren't memory yet.
- PREFRONTAL notes: `memory/personal`, also left uncolored: it is a separate personal layer, and a sixth color can't be told apart from the other five.
- New areas join an existing family: a sixth graph color can't be told apart from the other five in both themes.

## Check the brain
On "check the brain", audit and report; change nothing during the audit (fixes go through SYNAPSE).
- Run `python scripts/check_brain.py` when available: dead links and dead heading links, hard wraps, em dashes, chatbot residue, missing tags, SYNAPSE IDs, repeated lines, slop-list hits.
- Then judge what a script can't: rules that contradict each other across files, rules that change no behavior, area files over ~80 lines, PREFRONTAL sections over ~150, SYNAPSE entries pending for more than 30 days.

## Avoid
- Hard-wrapped paragraphs or bullets.
- Markdown links (`[x](file.md)`) between vault notes; use wikilinks ([[THALAMUS#Routing Rules|THALAMUS › Routing Rules]], rule 8).
- Bold lines standing in for headings; code blocks without a language.
