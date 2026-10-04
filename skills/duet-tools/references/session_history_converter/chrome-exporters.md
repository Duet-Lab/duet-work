# Exporting web AI chats from Chrome

A running catalog of ways to get a chat out of an AI provider's web UI
into a file. Primary use: someone asks how to export a chat from Claude,
ChatGPT, Gemini, Google AI Mode, or DeepSeek — answer from the list below:
for Google AI Mode that is Chrome's own Save Page As, for the others the
actual extension for that provider, by name and store link. Grown as new
ways turn up — this isn't meant to be exhaustive on day one.

Secondary use, for work on this tool itself: each entry also gives the
export's output signature (so a file can be recognized even without knowing
which extension made it) and, where confirmed, which `sources/*.py` module
already parses that output.

For local ChatGPT Code/Work sessions, use [codex-sessions.md](codex-sessions.md)
instead; this catalog concerns web exports, not local rollout logs.

## Google AI Mode: Save Page As — Web Page, Complete

No extension. In Chrome, on the AI Mode thread: **Save Page As → Web Page,
Complete**. This is the better export for AI Mode: it keeps when each
prompt was asked (the time, or for older prompts only the day), every turn
up to the moment of saving, and the formulas — all
of which the extension below drops. `sources/google_saved_page.py` parses
the saved page; the page is large (~18 MB with its `_files` folder), so it
goes through a slim step first — see [google-ai-mode.md](google-ai-mode.md).

**Save Page As → Webpage, HTML Only** does not work: it saves the server's
first HTML, before any turn has been rendered.

## AI Chat Exporter

[Chrome Web Store](https://chromewebstore.google.com/detail/ai-chat-exporter/gnplifnbchmpeggocmkejocgldkahgnc)

Signs its output with a footer line, the last line of the file:

```
---
Exported by AI Chat Exporter on 9/17/2026, 11:55:57 PM from Google AI conversation
```

Confirmed to cover **Google Search AI Mode** — this is the actual source of
the `### AI Mode reply for ...` export format handled by
`sources/google_export.py` in this tool (confirmed against two real exports
that carry this exact footer). For AI Mode it is the fallback, not the
first choice: it drops the prompt times and the formulas, which the saved
page above keeps. Which other
AI services it supports isn't recorded here yet.

## AI Chat Exporter: Save Claude as PDF, MD and more

[Chrome Web Store](https://chromewebstore.google.com/detail/ai-chat-exporter-save-cla/elhmfakncmnghlnabnolalcjkdpfjnin)

A different extension from the one above, despite the similar name — each
extension exports a different provider's chats, not one extension covering
several. This one is specifically for **claude.ai**. Signs its output with:

```
Powered by Claude Exporter (https://www.ai-chat-exporter.net)
```

This is the actual source of the `## User:` / `## Assistant:` export format
handled by `sources/claude_export.py` (confirmed against a real export that
carries this exact signature).

## claude.ai: the conversation JSON the page itself loads

No extension. Reach for it when the tool calls of a claude.ai chat matter —
reports sent through an MCP tool, searches, commands. The exporter above
keeps only the names of the tools a reply called, not what was passed to
them; Save Page As keeps only the messages on screen at that moment, with
every tool block collapsed. The chat page loads the whole conversation from
the site's own API in one response, and that response is the export:

```
https://claude.ai/api/organizations
https://claude.ai/api/organizations/<uuid>/chat_conversations/<chat-id>?tree=True&rendering_mode=messages&render_all_tools=true
```

The first address lists the account's organizations, each with a `uuid`;
`<chat-id>` is the tail of the chat's own address.

This is not cross-platform: the agent needs a plugin that drives the
person's own browser, where they are signed in to claude.ai, and each agent
has its own. A plain web request, `curl`, or an automated browser with a
fresh profile cannot do it: none of them carries the person's sign-in, and
the sign-in is never copied out of the browser to give it to them.

**Claude Code** — checked 2026-10-04 in the VS Code extension, with the
Claude in Chrome extension installed in the browser.

1. The browser tools (`mcp__claude-in-chrome__*`) are not in the session
   until the person types `@browser` in the chat, for example
   `@browser:new_tab claude.ai`. The agent cannot switch them on itself. An
   agent that lacks them asks the person for exactly that line and offers
   nothing else in its place.
2. Open the chat's address in a tab of the agent's own.
3. With the JavaScript tool, request both addresses from inside the page.
   Keep the response in a page variable and return only counts — messages,
   tool calls. The body is too large for a tool result, and the extension
   blocks a result that looks like cookie or query-string data.
4. Ask the person for a yes to the download, naming the file and its size,
   then save the response from the page as a `.json` file; it lands in the
   browser's download folder.
5. Convert it with `save.py` and close the tab.

**Other agents** (Codex, Gemini, Kimi) — not checked. The same job needs
that agent's own browser plugin; which one, and how the person switches it
on, is not recorded here yet. Add it as its own entry when it is checked.

**No browser plugin at all** — the person opens the two addresses
themselves and saves the second response as a `.json` file.

The API is internal and undocumented: it answered this way on 2026-10-04
and may change.

Recognized by its top-level `chat_messages` and `current_leaf_message_uuid`;
handled by `sources/claude_chat_json.py` (confirmed against a real
conversation of 94 prompts and 96 tool calls, 2026-10-04, compared prompt by
prompt with the extension's export of the same chat). The JSON also holds
what the turn files leave out: thinking summaries, tool results, the text of
attached files, and the side branches of regenerated replies. Images are
not in it.

## ChatGPT Exporter - ChatGPT to PDF, MD, and more

[Chrome Web Store](https://chromewebstore.google.com/detail/chatgpt-exporter-chatgpt/ilmdofdhpnhffldihboadndccenlnfll)

For **ChatGPT**. Signs its output with a rule and a line, the last two of
the file:

```
---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)
```

Its markdown has `## Prompt:` / `## Response:` sections, a date line such
as `9/27/2026, 9:54:58 PM · gpt-6-pro` under each marker (the model only on
responses), and the model's reasoning as a quote block ending in
`> Worked for 33s`. Handled by `sources/chatgpt_export.py` (confirmed
against a real export, 2026-09-29, that carries this exact signature).

## AI Chat Exporter: Gemini to PDF, MD and more

[Chrome Web Store](https://chromewebstore.google.com/detail/ai-chat-exporter-gemini-t/jfepajhaapfonhhfjmamediilplchakk)

For **Gemini** (the chat product, not Google Search AI Mode — a different
extension above already covers that one). Same publisher family as the
first two entries, one extension per provider again.

A real Gemini export in markdown (2026-09-29) was handled by
`sources/gemini_export.py`, but it carries no signature, so which extension
made it isn't confirmed. What it does carry: a `**Exported:**` /
`**Link:** https://gemini.google.com/app/...` header, `## User:` /
`## Gemini:` sections with a `> 2026/9/27 22:11:36` date line under each
marker — the same date line as the Claude export above — and the model's
reasoning as a quote block opening with `> **Thinking steps**`.

## DeepSeek Chat Exporter

[Chrome Web Store](https://chromewebstore.google.com/detail/deepseek-chat-exporter/cohbpcihoiahgokbjkgkecodljploimg)

For **DeepSeek**. `sources/deepseek_export.py` already exists in this tool
and expects `### User` / `### DeepSeek AI` markers, but that module was
ported from an older tool and — as its own docstring says — has never been
checked against a real DeepSeek export in this project. No signature or
example from this specific extension is on hand yet either, so whether its
output actually matches what `deepseek_export.py` expects is still an open
question, not a confirmed link like the first two entries above.
