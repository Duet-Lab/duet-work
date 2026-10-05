# Duet Work

A library of skills for working with an AI assistant. Some of them belong to [Duet](https://github.com/alatyshau/duet), a human–AI operating environment; the rest work on their own.

Each skill is a folder under `skills/` with a `SKILL.md` in the Anthropic skill format, so it can be loaded by Claude Code, claude.ai and other clients that read that format. The Duet system prompts live under `system-prompts/`.

## Skills

`duet-chat`, `duet-work` and the `duet-workflow` system prompt are alternative conversation formats. Use one per session.

### `duet-chat`

A self-contained conversation skill for browser chats and Claude Code. It guides the assistant to understand requests before acting, offer constructive criticism, and write clear, structured replies. Replies are numbered for easy reference.

### `duet-work`

A conversation skill for Claude Code, tied to a work folder. The skill's argument is the path to the folder: it supplies the context of the work and keeps its results between sessions. Used with the `duet-core` system prompt.

### `duet-tools`

An index of standalone tool scripts, one folder per tool, invoked only on request (never auto-loaded). Currently holds `session_history_converter`, which splits an AI conversation into one markdown file per turn — from a Claude Code or local ChatGPT Code/Work session, a claude.ai, ChatGPT or Gemini export, a Google AI Mode export or saved page, or a DeepSeek export — and can save the whole conversation as a dated, named folder, finding Claude Code sessions by workspace folder and local Codex / ChatGPT Code/Work sessions by title, ID or workspace. Comes with a catalog of the ways those exports are made. Scripts run through `uv` and leave no environment or cache behind next to them.

### `duet-setup-claude`

Know-how for tuning Claude Code and its VS Code extension: where the relevant files live, what can be changed, and what each change risks. Loaded only on request.

### `duet-work-full`

**Deprecated.** Kept as a source to mine; not for use. Described a conversation format with addressable thoughts and two root files of a work folder: `INDEX.md` kept by the agent, `NOTES.md` kept by the human.

## System prompts

Each file under `system-prompts/` is a Claude Code output style. A business gets one as its system prompt through the `system_prompt` field of its `context.json`, and Duet deploys it to Claude Code, Codex and Kimi Code.

### `duet-core`

The foundation of a Duet session: orientation in the business through Duet MCP, the model of contexts, the manifest, alpha paths, the memory policy and the writing rules. It is the Duet platform prompt (`packages/instructions/bootstrapper.md` in Duet), taken as a standalone system prompt.

### `duet-workflow`

The complete Duet session for Claude Code, needing no conversation skill: `duet-core`, the conversation format of `duet-work`, and the turn protocol, in which the Duet server leads the agent through the session and every turn and the agent reports each step with a tool call. In development; the server side of the protocol does not exist yet.
