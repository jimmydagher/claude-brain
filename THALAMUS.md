---
tags:
  - memory/core
---
# THALAMUS

The **router**: it tells you where to go, not what to know. The linked files tell you what to do. It loads with [[CORTEX|CORTEX]], once per session.

**Do not read everything.** Identify the task, then read **only the relevant instruction file(s)**.

## Routing Rules
1. Identify the **primary intent**.
2. Go directly to its instruction file.
3. Inform the human which part of the brain (memory) you are using, as your first line: `Brain: CODING + SECURITY`. Multiple sections is ok to use **if required by the intent**.
4. Read additional files **only when required**: at most 3 brain files besides CORTEX, THALAMUS and AMYGDALA before answering.
5. Follow links from that file when deeper context is needed: one hop, no chains. Personal layer: if `LIMBIC/AMYGDALA.md` exists, it loads with CORTEX and THALAMUS; load only the sections it lists for the task's area (and its `Always` ones); they don't count toward the 3-file cap. No AMYGDALA: skip. Rules: [[LIMBIC/LIMBIC|LIMBIC]].
6. Do not load unrelated knowledge. Don't re-read a file already loaded this session unless it changed or the human says "reload the brain".
7. Prefer existing knowledge over creating duplicates.
8. When creating knowledge, add appropriate `[[wikilinks]]`.

## Routing Table
Areas live in [[NEOCORTEX/NEOCORTEX|NEOCORTEX]], grouped into lobes; a lobe is a tag family, not a folder.

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

## Outside the neocortex
|     | Task           | Load when the task is about…                     | Go To                                                                                |
| --- | -------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------ |
| 📈  | Projects       | anything tied to a named project                 | [[PREFRONTAL/PREFRONTAL\|PREFRONTAL]], then the hub through AMYGDALA's `## Projects` |
| 👤  | Personal layer | where a lesson goes; the human's own preferences | [[LIMBIC/LIMBIC\|LIMBIC]]                                                            |
