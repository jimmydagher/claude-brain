---
tags:
  - memory/communication
---
> Scope: image prompts, diagrams, UI/web design, slides, video · Pairs with: [[MEMORY/ANALYTICS|ANALYTICS]] (data charts), [[MEMORY/WRITING|WRITING]] (on-image copy), [[MEMORY/BUSINESS|BUSINESS]] (brand)

## Core Rules (non-negotiable)

### RULE#1 Purpose first
Know what it's for, who sees it and where (size, aspect ratio, light or dark background) before designing.

### RULE#2 Concrete beats hype
Describe subject, action, setting, composition, lighting and style. Drop "stunning, 8k, masterpiece".

### RULE#3 Exact text in quotes
Put on-image text in quotes, with font, size, color and placement. Settle the wording before generating.

### RULE#4 Edits change one thing
"Change only X; keep everything else the same." Restate what must not change on every turn.

## Images
- Prompt shape: `[Subject] + [Action] + [Location] + [Composition] + [Style]`, then quoted text and aspect ratio.
- Say what you want ("an empty street"), not what you don't ("no cars"); keep explicit exclusions for artifacts ("no watermark").
- Use camera, lens and lighting terms (low angle, macro, softbox) and counts ("three cats").
- Iterate with one small change per turn.
- Video: also give shot type, camera move, motion and duration.

## Diagrams
- Mermaid in a fenced `mermaid` block; `flowchart TD` or `LR`; short IDs; 12 nodes max, split bigger ones.
- Quote labels that contain symbols: `A["run()"]`. Never use lowercase `end` as an ID.

## UI / web design
- Start from product, audience and purpose. Before code, write a one-line plan for palette, type and layout, plus an ASCII wireframe.
- 1–2 deliberate typefaces (not Inter, Arial or system defaults); 4–6 named colors; tinted neutrals; no gray text on color.
- Body lines under ~80 characters; motion only with purpose (no bounce or elastic easing).
- Check the plan for genericness before building.
- Avoid the AI look: purple-to-blue gradients, an icon tile over every heading, cards inside cards, identical rounded "SaaS cards", letter-spaced ALL-CAPS labels everywhere. Also avoid their stock replacements: cream + serif + terracotta, near-black + acid green.

## Slides
- One idea per slide; the headline states the takeaway.
- .pptx deliverables: use the matching skill if the harness has one.
