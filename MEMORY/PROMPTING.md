---
tags:
  - memory/core
---
> Scope: prompts, skills, agents, system prompts, CLAUDE.md/AGENTS.md, rules for this brain · Pairs with: [[MEMORY/AUTOPILOT|AUTOPILOT]], [[MEMORY/KNOWLEDGE|KNOWLEDGE]], [[MEMORY/REVIEW|REVIEW]], [[MEMORY/MECHANICS|MECHANICS]] (Markdown format)

## Core Rules (non-negotiable)

### RULE#1 Only what the model lacks
Assume the model is smart. Keep a line only if removing it would cause a mistake.

### RULE#2 One rule, one place
Link instead of copying; one term per concept; no contradictions between files.

### RULE#3 Explain why, skip the caps
A short reason beats CRITICAL or MUST. Save emphasis for rules the model is seen ignoring.

### RULE#4 Positive and checkable
State the behavior you want, not only what to avoid; every step ends in a checkable "done".

### RULE#5 Test it
Try 3+ realistic prompts with and without the instruction; refine from what actually happened.

## Defaults
- Descriptions (skills, agents, routing rows) say what it does and when to use it, trigger words first.
- Keep main files short (brain area files under ~80 lines, skills under 500); move case-specific detail to linked files one level deep.
- Show concrete input → output examples; use rigid templates only for rigid formats.
- Be exact for fragile steps (exact commands), loose for open-ended ones.
- Leave out facts that go stale or that config and `--help` already state.
- Prompt skeleton: goal → context → task → constraints → output format → examples.
- Brain area files: `tags` property (family, see [[MEMORY/MECHANICS|MECHANICS]]) → Scope line → Core Rules → Defaults → Avoid → Output.
- Skills: `name` up to 64 chars, lowercase with hyphens; `description` up to 1,024 chars; steps first, reference after.

## Avoid
- Vague names or descriptions ("helper", "helps with documents").
- Explaining what the model already knows.
- References nested more than one level; bloated files; stale rules piling up.
- A menu of options with no default; unexplained magic numbers.
- Overfitting to the test examples.

## Output
- The prompt in a code block, then up to 3 lines on key choices and how to test it.
