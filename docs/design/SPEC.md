# SPEC

Behavior of the brain and its checker. Only what TTD003 changes is new; the rest of the brain is described by its own notes.

## TTD003: lessons from Caveman

Source: https://github.com/juliusbrussee/caveman (a terse-output skill plus input-shrinking tools for coding agents). The brain already has its Token economy rules (`CORTEX › Always-on Rules`); Caveman adds four ideas the brain lacks. Each becomes a small, checkable change. No compression of notes, no proxy, no hooks: Caveman's own numbers for those are unmeasured or preliminary.

### 1. Strict mode gets levels (CORTEX rule 7)
- `terse`, `concise mode`, `optimize` keep today's meaning: level 1.
- New `ultra terse`: level 2. Fragments, no articles, abbreviations and symbols allowed (`→`, `w/`), one line per item.
- `normal` or `full sentences` ends strict mode.
- At every level these stay exact and verbatim: code, commands, paths, numbers, errors, negations.
- At every level these switch to full sentences: security warnings, irreversible actions, and a human who is confused or repeats a question.

### 2. No narration between tool calls (AUTOPILOT)
- Between tool calls, no filler ("Now let me…", "I'll check…"). Speak only to report a result, a blocker or a decision.
- The human's own prompts are never rewritten or "improved" without being asked.

### 3. Read less (CORTEX, INSTRUCTIONS index)
- Reading cost is a budget, separate from reply length. Already-loaded files are not read again; a section (`FILE#Heading`) is read instead of a whole note when one section answers.
- `scripts/check_brain.py` reports the approximate token size (characters / 4) of what loads every session (CORTEX, the instructions index, each area file) and warns when the always-loaded total or any single area file exceeds a cap held as constants at the top of the script.
- The warning is advisory, like the other checker warnings: it never fails the check.

### 4. Knowledge note
- Shared knowledge notes are untracked and change only through SYNAPSE, so this repo does not carry the note. It is proposed to the owner (summary in the task report) instead. The note would cover: what it does, the measured figures with their caveats (a plain "be concise" instruction is the honest baseline; the rules themselves cost input tokens), and which ideas the brain adopted or declined. It carries a `sources:` line, as the checker requires.

### Declined (and why)
- Classical-Chinese or other exotic output modes: unreadable for the owner.
- Note compression with backups, the proxy, `shrink`, `browse`, blocks, `mem`: no measured gain on a Markdown vault of ~1,200 lines; revisit if the load report shows the brain outgrowing its cap.
