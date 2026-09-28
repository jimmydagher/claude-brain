---
tags:
  - memory/core
---
> Scope: long-term shared memory: what a lobe is and the shape area files share · Index: [[THALAMUS#Routing Table|THALAMUS › Routing Table]] · Process: [[CORTEX#Brain Upkeep|CORTEX › Brain Upkeep]]

## Lobes
- A lobe is a family of areas that serve the same kind of task. It is a tag, not a folder: every area file sits directly in `NEOCORTEX/`, so moving an area to another lobe is a one-tag edit and no link breaks.
- Membership is listed in one place only: THALAMUS's routing table.
- Each area has one home lobe, the one whose tasks it serves most often. Never copy a file into a second lobe.
- Cross-lobe connections are the `Pairs with` wikilinks in each area's scope line: the synapses between lobes. An area that often works with another adds it there.
- A new area joins an existing lobe: a new lobe would need a sixth graph color, which can't be told apart from the other five in both themes.

| Lobe | Tag | Covers | Graph color |
| --- | --- | --- | --- |
| Core | `memory/core` | the brain itself: loading, Markdown, prompts and rules | blue `#2a78d6` |
| Technical | `memory/technical` | build, operate, secure, data | green `#008300` |
| Thinking | `memory/thinking` | reason, plan, research, review, learn, file knowledge | aqua `#1baf7a` |
| Communication | `memory/communication` | write, translate, design, sell, converse | gold `#c98500` |

## Area file shape
- `tags` frontmatter with the area's lobe tag.
- A scope line: `> Scope: … · Pairs with: [[NEOCORTEX/X|X]], …`.
- `## Core Rules (non-negotiable)` with `### RULE#n` headings, then `## Defaults` (PREFRONTAL preferences may override these), `## Avoid` and `## Output`. Reference areas such as MECHANICS may replace Defaults and Output with their own sections.
- Under ~80 lines. Corrections don't pile up as add-ons: committing one rewrites the rule it changes.
