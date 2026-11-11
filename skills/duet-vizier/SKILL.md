---
name: duet-vizier
description: Used only with the system prompt duet-vizier.
---

# Duet Vizier

This skill is the pair of the system prompt `duet-vizier`: a session under that prompt loads it at the start, and no other session loads it. If your system prompt is not `duet-vizier`, do not load this skill and do not work by it; a reference in this folder is yours to read only when your assignment names it.

The Duet Vizier is a character set by that system prompt, `system-prompt.md` in this folder. Its skills live here: the references and scripts the prompt reads from. This file lists them. The prompt says when each reference is read, under "Which reference, when": read a reference by its path when its context comes up, not when this skill is loaded.

## References

- `references/topic-management.md`: a work folder divided into topics.
- `references/blockers-management.md`: blockers, the files for what waits on a person.
- `references/notepad-management.md`: the user's notepad and its dashboard.
- `references/requirements-voice.md`: requirements for work that another agent implements.
- `references/dev-curation.md`: software investigation, implementation, code review and the writing of a skill, done by executors. `references/dev-curation-claude.md` and `references/dev-curation-codex.md` describe, for each client, how the Curator observes its executors.
- `references/instruction-authoring.md`: writing instructions for agents; it is given to the executor who writes them.
- `references/message-roll.md` and `references/message-roll-operations.md`: file-based conversations, their principles and the helper's operations.
- `references/thesaurus-writing.md`: a ticket's thesaurus.
- `references/business-curation.md`: the procedure of the `business-curation` routine.

## Scripts

- `scripts/log_append.py`: the MessageRoll helper. `references/message-roll-operations.md` describes its commands; run it as `uv run --script scripts/log_append.py`, so that nothing is installed beside it on a synced drive. Its tests are `tests/test_vizier_log_append.py`.

## The system prompt's own files

`system-prompt.md`, its companion `system-prompt-calibration.md` and the folder `docs/` belong to the system prompt and are not part of the library. A business sets the prompt through the `system_prompt` field of its manifest and declares this skill in `skills`, so that Duet deploys the library with it.
