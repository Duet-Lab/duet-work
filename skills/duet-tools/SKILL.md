---
name: duet-tools
description: The Duet tool scripts, one folder per tool, with the references that say how to run them.
disable-model-invocation: true
---

# Duet Tools

One tool, one folder under `scripts/`, always run as

```bash
uv run --script scripts/<tool>/<entry>.py ...
```

so that nothing gets installed next to the script on the synced drive. If `uv` is missing, tell the user the install command for their OS (`brew install uv` on macOS; the others are in `references/writing-a-tool.md`) and stop rather than working around it.

A reference may also be read by path without loading this skill, when another skill's instructions name it; Duet deploys this folder beside the other skills of a business that declares it.

## Tools

### Session History Converter — `scripts/session_history_converter/`

Turns an AI conversation into one markdown file per human turn, in our own format, and can file it as a `<YYMMDD>_<HHMM>_<Client>_<Name>/` folder under whatever directory the person names — where chats are kept is their choice, not the tool's. Sources: local Claude Code sessions (by workspace) and Codex / ChatGPT Code/Work sessions (by title, session ID or workspace), claude.ai, ChatGPT and Gemini exports, Google AI Mode exports and saved pages, DeepSeek exports.

Reach for it when someone wants a conversation kept or converted, asks how to export a chat, or hands over such a file. Read `references/session_history_converter.md` first: it lists the entry points with their flags and says which deeper guide to open for exporters, Google saved pages, new sources, or math that won't render.

### MessageRoll — `scripts/message_roll/`

A MessageRoll, or roll, is a Markdown file that keeps a conversation among named participants — people and AI sessions in any client — and the helper `scripts/message_roll/log_append.py` creates a roll, registers participants, appends messages under a file lock, notifies the Curator and finds a participant's tmux window.

Read `references/message_roll.md` when organizing or joining a conversation through a roll, and `references/message_roll/operations.md` before creating a roll, registering in one or appending to it.

## Adding or changing a script

Read `references/writing-a-tool.md` before writing: the script header `uv` needs, why no cache or environment may appear beside a script, the one line a multi-file tool must have before importing its siblings, and where tests go.
