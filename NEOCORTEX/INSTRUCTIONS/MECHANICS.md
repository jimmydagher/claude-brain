---
tags:
  - memory/core
---
> Scope: how the brain loads, caches and reloads; how to write Markdown files · Pairs with: [[NEOCORTEX/INSTRUCTIONS/PROMPTING|PROMPTING]], `KNOWLEDGE`, [[NEOCORTEX/INSTRUCTIONS/WRITING|WRITING]]

## Core Rules (non-negotiable)

### RULE#1 On request, then cached for the session
The brain is off until the human says "use the cortex" or "use your brain" (or runs `/cortex`). Then read `CORTEX.md` and the instructions index (`NEOCORTEX/INSTRUCTIONS/INSTRUCTIONS.md`) once, open the first reply with the status line from `CORTEX › Session start` (`Cortex brain: connected to **<brain>**`), and apply it to every task for the rest of the session.

### RULE#2 Read once, reuse from context
A brain file read this session stays in context, and later turns reuse it from the prompt cache. Open area files only when a task needs them, once each; never re-read to "refresh".

### RULE#3 Reload on purpose
Re-read CORTEX, the INSTRUCTIONS index and the area files in use when the human says "reload the brain", when you're told a brain file changed, or after the context was compacted (compaction summarizes files read by tools, so their exact rules are gone).

### RULE#4 No hard wraps in Markdown
One paragraph or list item is one line, however long. Let the editor soft-wrap; never insert line breaks to fit a narrow window.

## Session
- Order: CORTEX, the INSTRUCTIONS index and the personal `## Always` sections first (one `cortex_load`), then area files as tasks need them plus each personal `## <AREA>` section for the area, then project notes (the project list, a hub's `## Now`, then your own notes on it). Knowledge only by search, when a stored note may answer the task. SYNAPSE only when capturing, reviewing or committing; ENGRAM only by search.
- Per-task announcements follow [[NEOCORTEX/INSTRUCTIONS/INSTRUCTIONS#Routing Rules|INSTRUCTIONS › Routing Rules]] (rule 3) (`Using the **CODING | SECURITY** nodes`); the status line comes once per session, never again.
- Always-on setups import CORTEX in CLAUDE.md (`@path`), so it loads at session start, is prompt-cached and survives compaction. If CORTEX is already in context that way, skip the read in RULE#1.

## Markdown
- Line breaks only where structure needs them: between blocks, list items, table rows, lines of code.
- Headings with `#`, in order (no jump from `##` to `####`). Standalone docs (README, specs) get one H1; vault notes use the filename as their title.
- One blank line around headings, lists, tables and code blocks; never two in a row.
- `-` for bullets, `1.` for numbered steps.
- Code in fenced blocks with a language tag (`bash`, `python`, `text`); inline code for names, paths and commands.
- Tables only for real rows and columns; a literal `|` inside a cell is written `\|`.
- Vault links are wikilinks that carry the vault path: `[[NEOCORTEX/INSTRUCTIONS/CODING|CODING]]`, or `[[NEOCORTEX/INSTRUCTIONS/CODING\|CODING]]` inside a table. A section link adds `#Heading`: `[[PREFRONTAL/INSTRUCTIONS/ENVIRONMENT#CODING|ENVIRONMENT › CODING]]`.
- Links follow the tree, so the graph shows the brain's structure: a note links to its folder's index (the note named like the folder; CORTEX at the top), the notes it indexes, or neighbours in its own region. Any other reference is a plain name in backticks (`SECURITY`, `CORTEX › Brain Upkeep`). The one exception is ENGRAM → NEOCORTEX, which shows where committed memory lands; `check_brain.py` warns on the rest.
- Files meant for GitHub (README) use relative Markdown links, since GitHub doesn't render wikilinks. External links: `[descriptive text](url)`, never "click here" or a bare URL.
- Bold sparingly for key terms, never as a fake heading.
- YAML frontmatter only at the very top; HTML only for comments (`<!-- -->`).
- A Markdown file a script writes (e.g. a CHANGELOG rendered by a release script) takes its format from the script: fix the generator, never hand-edit its output, or the next run undoes the edit.

## Tags
- Every brain note starts with a `tags` property (YAML list); the graph colors come from it (`.obsidian/graph.json`).
- Lobes, their tags and what each covers: [[NEOCORTEX/INSTRUCTIONS/INSTRUCTIONS#Lobes|INSTRUCTIONS › Lobes]]. The NEOCORTEX hub and the INSTRUCTIONS index take `memory/core`. CORTEX takes `memory/core/entry`: it still counts as core, but its own color group (first in the list, so it wins) paints the entry point red.
- Project hubs and their sub-notes: `project/<name>` (lowercase, hyphens); the PROJECTS guide and the project list: `project`. The KNOWLEDGE guide and knowledge notes: `knowledge`.
- HIPPOCAMPUS notes: `hippocampus`, purple in the graph.
- PREFRONTAL notes: `persona`, salmon: the separate personal layer. Knowledge notes: `knowledge`, cyan.
- Graph colors are checked as a set (light and dark themes, color-blind vision) before one is added, so new areas join an existing lobe.

## Check the brain
On "check the brain", audit and report; change nothing during the audit (fixes go through SYNAPSE).
- Run `python scripts/check_brain.py` when available: dead links and dead heading links, ambiguous links, links that leave the tree, orphan notes, hard wraps, em dashes, chatbot residue, missing tags, SYNAPSE IDs, repeated lines, slop-list hits, two notes with one name in the same scope, knowledge notes without `sources`, active project hubs not updated for 30 days.
- Then judge what a script can't: one subject spread over notes with different names, rules that contradict each other across files, rules that change no behavior, area files over ~80 lines, PREFRONTAL sections over ~150, SYNAPSE entries pending for more than 30 days.

## Avoid
- Hard-wrapped paragraphs or bullets.
- Markdown links (`[x](file.md)`) between vault notes; use wikilinks ([[NEOCORTEX/INSTRUCTIONS/INSTRUCTIONS#Routing Rules|INSTRUCTIONS › Routing Rules]], rule 8).
- Bold lines standing in for headings; code blocks without a language.
