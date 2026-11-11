# Duet Work

A library of skills for working with an AI assistant. Some of them belong to [Duet](https://github.com/Duet-Lab/duet), a human–AI operating environment; the rest work on their own.

Each skill is a folder under `skills/` with a `SKILL.md` in the Anthropic skill format, so it can be loaded by Claude Code, claude.ai and other clients that read that format. Experimental system prompts live under `system-prompts/`, and the `duet-vizier` prompt in the folder of its own skill, `skills/duet-vizier/`; the public `duet-core` prompt ships with Duet, not this repository.

## Skills

`duet-chat`, `duet-work` and the `duet-vizier` and `duet-workflow` system prompts are alternative conversation formats. Use one per session.

### `duet-chat`

A self-contained conversation skill for browser chats and Claude Code. It guides the assistant to understand requests before acting, offer constructive criticism, and write clear, structured replies. Replies are numbered for easy reference.

### `duet-work`

A conversation skill for Claude Code, tied to a work folder. The skill's argument is the path to the folder: it supplies the context of the work and keeps its results between sessions. Used with the `duet-core` system prompt, and invoked only by the user.

### `duet-vizier`

The skills of the Duet Vizier, a character set by the system prompt in the same folder: an index of the references and scripts that prompt reads from. It stands on its own and does not use `duet-work`; where the two hold the same reference, each keeps its own copy. A business that sets the prompt declares this skill too, so that Duet deploys the library with it. A session under the prompt loads the skill at its start; no other session loads it. The prompt is described under "System prompts" below.

### `duet-executor`

**Legacy; a candidate for removal.** Retained for observation, not part of the active DuetLab setup. Contains the former Executor instructions for focused execution, engineering discipline, and human review. Explicit invocation only.

### `duet-vizir`

**Legacy; a candidate for removal.** Retained for observation, not part of the active DuetLab setup. Contains the former Vizir instructions for coordination, delegation, plan maintenance, and human approval gates. Explicit invocation only.

### `duet-tools`

An index of standalone tool scripts, one folder per tool, invoked only on request (never auto-loaded). Currently holds `session_history_converter`, which splits an AI conversation into one markdown file per turn — from a Claude Code or local ChatGPT Code/Work session, a claude.ai, ChatGPT or Gemini export, a Google AI Mode export or saved page, or a DeepSeek export — and can save the whole conversation as a dated, named folder, finding Claude Code sessions by workspace folder and local Codex / ChatGPT Code/Work sessions by title, ID or workspace. Comes with a catalog of the ways those exports are made. Scripts run through `uv` and leave no environment or cache behind next to them.

### `duet-setup-claude`

Know-how for tuning Claude Code and its VS Code extension: where the relevant files live, what can be changed, and what each change risks. Loaded only on request.

### `duet-work-full`

**Deprecated.** Kept as a source to mine; not for use. Described a conversation format with addressable thoughts and two root files of a work folder: `INDEX.md` kept by the agent, `NOTES.md` kept by the human.

## System prompts

A system prompt here is a Claude Code output style: `system-prompts/duet-workflow.md`, and `skills/duet-vizier/system-prompt.md`. Two kinds of companion file are never set as a system prompt. A calibration file, named after the prompt file with `-calibration.md` and kept beside it, holds the key and the common reading that Duet's `orientation` returns to a session of that prompt. A specification keeps the reasoning behind a prompt; for `duet-vizier` it is `skills/duet-vizier/docs/system-prompt-spec.md`. A business gets one as its system prompt through the `system_prompt` field of its `context.json`, and Duet deploys it to Claude Code, Codex and Kimi Code, and to Antigravity as a custom agent that a session selects with `agy --agent <name>`.

### Public foundation: `duet-core`

The public foundation is [`packages/instructions/duet-core.md` in Duet](https://github.com/Duet-Lab/duet/blob/main/packages/instructions/duet-core.md). Host installs it as the `duet-core` output style. This repository does not carry it as a prompt of its own; `duet-vizier` includes its body whole.

Use `duet-core` by itself for the standard Duet environment, or invoke the `duet-work` skill on top of it for the experimental work format. The `duet-vizier` system prompt is a character of its own with a skill of its own, and does not use `duet-work`. A business using the standard foundation does not need a `system_prompt` override. While the skills are being stabilized, this repository is private and access is granted personally.

### `duet-vizier`

The Duet Vizier, the faithful version of the Duet assistant, as a business system prompt: `duet-core` whole, a preamble that sets the spirit of the personality, and the personality text in full. Its references and scripts are the `duet-vizier` skill in the same folder, which the business declares under `skills` beside `system_prompt`. Executors in that business are launched with their own prompt, `duet-core` by default. It lives in `skills/duet-vizier/`: the prompt is `system-prompt.md`, and why it is built this way is in `docs/system-prompt-spec.md`. A secular version is planned under the name `duet-assistant`. The prompt is not the legacy `duet-vizir` skill listed above.

### `duet-workflow`

A self-contained work-session prompt with the Duet platform foundation, conversation rules, ticket operations, and work-folder memory. The agent manages the turn, using `turn_report` for its interpretation and `turn_plan` for a multi-step checklist; these tools display the supplied text and state, not a server-managed session. Uses the Backend tool set with `business_tree`. An alternative to `duet-core` plus `duet-work`, not an additional conversation layer.
