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
4. Read additional files **only when required**: at most 3 brain files besides CORTEX, THALAMUS and the personal map before answering.
5. Follow links from that file when deeper context is needed: one hop, no chains. Personal layer: if `CEREBELLUM/MAP.md` exists, it loads with CORTEX and THALAMUS; load only the sections it lists for the task's area (and its `Always` ones); they don't count toward the 3-file cap. No map: skip. Rules: [[CEREBELLUM/CEREBELLUM|CEREBELLUM]].
6. Do not load unrelated knowledge. Don't re-read a file already loaded this session unless it changed or the human says "reload the brain".
7. Prefer existing knowledge over creating duplicates.
8. When creating knowledge, add appropriate `[[wikilinks]]`.

## Routing Table

|     | Task (Memory)              | Load when the task is about…                               | Go To                           |
| --- | -------------------------- | ---------------------------------------------------------- | ------------------------------- |
| 💻  | Code \| technical          | writing, fixing, debugging or refactoring code and scripts | [[NEOCORTEX/CODING\|CODING]]       |
| 🧠  | Thinking \| decisions      | choosing between options, trade-offs, "should I…"          | [[NEOCORTEX/THINKING\|THINKING]]   |
| ✍️  | Writing \| communication   | emails, docs, posts, messages, editing prose               | [[NEOCORTEX/WRITING\|WRITING]]     |
| 🔎  | Research \| investigation  | finding, verifying or comparing information and sources    | [[NEOCORTEX/RESEARCH\|RESEARCH]]   |
| 📋  | Planning \| projects       | turning goals into briefs, specs, roadmaps, task lists     | [[NEOCORTEX/PLANNING\|PLANNING]]   |
| 🔄  | Review \| reflection       | critiquing a draft, plan or code; retros; feedback         | [[NEOCORTEX/REVIEW\|REVIEW]]       |
| 📚  | Knowledge \| summarization | summarizing, extracting, filing notes in this vault        | [[NEOCORTEX/KNOWLEDGE\|KNOWLEDGE]] |
| 🌐  | Translation \| language    | translating, localizing, proofreading                      | [[NEOCORTEX/LANGUAGE\|LANGUAGE]]   |
| 📊  | Data \| analysis           | datasets, SQL, metrics, statistics, spreadsheets           | [[NEOCORTEX/ANALYTICS\|ANALYTICS]] |
| 🖼️ | Images \| visual           | image prompts, diagrams, UI/web design, slides, video      | [[NEOCORTEX/VISUAL\|VISUAL]]       |
| 💬  | Conversation \| assistant  | general questions and advice; anything unmatched           | [[NEOCORTEX/ASSISTANT\|ASSISTANT]] |
| 🤖  | Agents \| tools \| MCP     | multi-step autonomous work, tool use, subagents, MCP       | [[NEOCORTEX/AUTOPILOT\|AUTOPILOT]] |
| 🛡️ | Security \| safety         | secrets, permissions, destructive actions, untrusted input | [[NEOCORTEX/SECURITY\|SECURITY]]   |
| 💼  | Business \| marketing      | strategy, marketing copy, sales outreach, product specs    | [[NEOCORTEX/BUSINESS\|BUSINESS]]   |
| 🎓  | Learning \| teaching       | "teach me", tutoring, quizzes, study plans                 | [[NEOCORTEX/LEARNING\|LEARNING]]   |
| 🧩  | Prompts \| skills          | prompts, skills, agents, CLAUDE.md, rules for this brain   | [[NEOCORTEX/PROMPTING\|PROMPTING]] |
| 🔧  | Mechanics \| Markdown      | writing any .md file; how the brain loads, caches, reloads | [[NEOCORTEX/MECHANICS\|MECHANICS]] |
| 📈  | Projects                   | anything tied to a named project                           | [[NEOCORTEX/PROJECTS\|PROJECTS]]   |
