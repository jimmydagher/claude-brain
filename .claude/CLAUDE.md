# memory

- On your first response in every session address me as Mr. Dagher.
- Always use my Cortex brain: at the start of every conversation, before your first reply, call the Cortex 		connector's cortex_load with brain='dagher' and follow what it returns for the whole conversation. Pass brain='dagher' on every Cortex call, this repository is connected to the `claude-brain` project, memory and information will be saved into this project section of the brain. If Cortex can't be reached, tell me and stop. If it says a brain is off, carry on without it.

# SDSI profile

- Language: Python 3.14 (repo tooling in `scripts/`); the product is the Markdown vault
- Project type: other: Markdown second brain (Obsidian vault) with Python checker tooling
- Upkeep: versioning
- Deviation: brain notes (`CORTEX.md`, `NEOCORTEX/`, …) are the product, so `scripts/git/release.json` narrows docs-only commits to `README.md`, `.claude/CLAUDE.md`, `meta/*.md` and `docs/*`; a note change is a release.
