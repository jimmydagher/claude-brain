---
tags:
  - memory/core
---
The **area index** of long-term memory: it tells you where to go, not what to know; the area files tell you what to do. It loads with [[CORTEX|CORTEX]], once per session.

**Do not read everything.** Identify the task, then read **only the relevant instruction file(s)**.

## Routing Rules
1. Identify the **primary intent**.
2. Go directly to its instruction file.
3. Inform the human which part of the brain (memory) you are using, as your first line: `Brain: CODING + SECURITY`. Multiple sections is ok to use **if required by the intent**.
4. Read additional files **only when required**: at most 3 brain files besides CORTEX and this index before answering.
5. Follow links from that file when deeper context is needed: one hop, no chains. Personal layer: for the task's area, also read the `## <AREA>` section of each PREFRONTAL file that has one (the `## Always` ones load with CORTEX); they don't count toward the 3-file cap. No PREFRONTAL files: skip. Rules: `PREFRONTAL`.
6. Do not load unrelated knowledge. Don't re-read a file already loaded this session unless it changed or the human says "reload the brain".
7. Prefer existing knowledge over creating duplicates.
8. When creating knowledge, add wikilinks that follow the tree (`MECHANICS` › Markdown).

## Routing Table
Projects and personal preferences aren't areas: they live in PREFRONTAL, which CORTEX routes to.

### Core lobe
|     | Task (Memory)         | Load when the task is about…                               | Go To                              |
| --- | --------------------- | ---------------------------------------------------------- | ---------------------------------- |
| 🧩  | Prompts \| skills     | prompts, skills, agents, CLAUDE.md, rules for this brain   | [[NEOCORTEX/PROMPTING\|PROMPTING]] |
| 🔧  | Mechanics \| Markdown | writing any .md file; how the brain loads, caches, reloads | [[NEOCORTEX/MECHANICS\|MECHANICS]] |

### Technical lobe
|     | Task (Memory)          | Load when the task is about…                               | Go To                              |
| --- | ---------------------- | ---------------------------------------------------------- | ---------------------------------- |
| 💻  | Code \| technical      | writing, fixing, debugging or refactoring code and scripts | [[NEOCORTEX/CODING\|CODING]]       |
| 🤖  | Agents \| tools \| MCP | multi-step autonomous work, tool use, subagents, MCP       | [[NEOCORTEX/AUTOPILOT\|AUTOPILOT]] |
| 🛡️ | Security \| safety     | secrets, permissions, destructive actions, untrusted input | [[NEOCORTEX/SECURITY\|SECURITY]]   |
| 📊  | Data \| analysis       | datasets, SQL, metrics, statistics, spreadsheets           | [[NEOCORTEX/ANALYTICS\|ANALYTICS]] |

### Thinking lobe
|     | Task (Memory)              | Load when the task is about…                            | Go To                              |
| --- | -------------------------- | ------------------------------------------------------- | ---------------------------------- |
| 🧠  | Thinking \| decisions      | choosing between options, trade-offs, "should I…"       | [[NEOCORTEX/THINKING\|THINKING]]   |
| 📋  | Planning \| projects       | turning goals into briefs, specs, roadmaps, task lists  | [[NEOCORTEX/PLANNING\|PLANNING]]   |
| 🔎  | Research \| investigation  | finding, verifying or comparing information and sources | [[NEOCORTEX/RESEARCH\|RESEARCH]]   |
| 🔄  | Review \| reflection       | critiquing a draft, plan or code; retros; feedback      | [[NEOCORTEX/REVIEW\|REVIEW]]       |
| 📚  | Knowledge \| summarization | summarizing, extracting, filing notes in this vault     | [[NEOCORTEX/KNOWLEDGE\|KNOWLEDGE]] |
| 🎓  | Learning \| teaching       | "teach me", tutoring, quizzes, study plans              | [[NEOCORTEX/LEARNING\|LEARNING]]   |

### Communication lobe
|     | Task (Memory)             | Load when the task is about…                            | Go To                              |
| --- | ------------------------- | ------------------------------------------------------- | ---------------------------------- |
| ✍️  | Writing \| communication  | emails, docs, posts, messages, editing prose            | [[NEOCORTEX/WRITING\|WRITING]]     |
| 🌐  | Translation \| language   | translating, localizing, proofreading                   | [[NEOCORTEX/LANGUAGE\|LANGUAGE]]   |
| 🖼️ | Images \| visual          | image prompts, diagrams, UI/web design, slides, video   | [[NEOCORTEX/VISUAL\|VISUAL]]       |
| 💼  | Business \| marketing     | strategy, marketing copy, sales outreach, product specs | [[NEOCORTEX/BUSINESS\|BUSINESS]]   |
| 💬  | Conversation \| assistant | general questions and advice; anything unmatched        | [[NEOCORTEX/ASSISTANT\|ASSISTANT]] |

## Lobes
- A lobe is a family of areas that serve the same kind of task. It is a tag, not a folder: every area file sits directly in `NEOCORTEX/`, so moving an area to another lobe is a one-tag edit and no link breaks.
- Membership is listed in one place only: the routing table above.
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
