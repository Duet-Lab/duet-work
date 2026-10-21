# Writing agent instructions

Read this before you create or revise any text that agents work from: a skill (its `SKILL.md`, references, scripts and tests), a system prompt, an agent definition, a command, or similar text written for agents to follow. All of these are instructions, and the rules below apply to each of them. The file is written for whoever does the writing: usually an agent assigned to the task, sometimes the agent coordinating the work.

Before you start, you must load the skill-creation skill that your client's vendor ships and follow it: Anthropic's `skill-creator` in Claude clients, OpenAI's `skill-creator` in Codex. Each vendor's guide describes how its own models read instructions, so use the one that matches the agent doing the work, and load it through the client's skill mechanism. For a skill, follow it in full; for other instructions, apply its guidance on writing instructions wherever it fits. This file adds the rules that `skill-creator` does not cover.

## Write for the agent that will use the instructions

Keep actionable guidance, the reason behind it, and the evidence needed to check it. Leave out authoring history: discarded options, rollout status, migration notes, and dated provenance such as "(my rule, 2026-10-14)" or "these rules come from real sessions". An agent cannot act on where a rule came from, and a stranger cannot check it; that history belongs in the materials of the work that changed the skill.

Organize detail by when the reader needs it. `SKILL.md` says when to read each reference rather than summarizing it, because a summary costs context on every load and drifts from the reference it repeats.

A label or metaphor the user chose is a pointer to a need, not the requirement itself. Read the source in full, headings included, find what the user needs, and write the behavior that meets it. Do not transplant the label into the skill, and do not spend the work evaluating or replacing the label with another one.

Before you rewrite a passage, name the function it serves in the instructions and every need it carries, then check that each one survives the rewrite. Fixing a defect in a passage, such as a reference that cannot be resolved, does not license changing what the passage is for: remove the defect, not the purpose.

## Put each rule in the narrowest place it belongs

A rule for one part of a skill goes into that part's reference; a rule for the whole skill goes into its `SKILL.md`; a rule for a wider audience goes into the shared instructions that audience loads, such as a system prompt. A rule placed too wide starts governing work it was never meant for. Always edit the source of a skill, never a deployed copy.

## Write to open-source standard by default

All instructions are written as if they were going into a public open-source repository, whether or not it is published yet, so that it never needs a separate cleanup before release:

- **Native American English, written rather than translated.** When the source material is in another language, write the passage anew as an American engineer would, instead of translating it: translated text keeps the other language's structure, calques and quotations. Use US spelling and straight quotes.
- **Nothing personal or private.** No personal names, private ticket codes, private skills, paths into private folders, or details of one machine. An example taken from the user's own work is adapted into a generic one that nothing ties to the user, not just stripped of its names; codes and paths use placeholders such as `ABC001` that cannot be mistaken for real items.
- **Other languages only when they are the point**, for example test strings that check Unicode handling.
- **Readable as raw Markdown.** Reference files by backticked paths relative to the root of the skill or repository, never by `[text](link)`: in raw Markdown the caption hides the address.
- **One name per concept**, in prose and in the helper's output alike, so a reader never wonders whether two words mean two things.
- **One line per paragraph and per list item.** Hard wraps split one thought across lines and make diffs noisy.

## Scripts and tests are part of the skill

Helper scripts bundled with a skill are the skill author's work, not a separate product-development assignment. When applying an explicitly agreed change, keep instructions, helpers and tests consistent, and do not defer the Python part merely because it is code. Carrying out an agreed change does not grant permission for other work the change did not include.

Mechanical determinations belong to scripts, not to agents. When a procedure is a mechanical rule — picking the last matching entry in a list, comparing identifiers, choosing a delivery address, applying per-client lookup heuristics — put it in a helper script and keep it out of the instructions an agent must follow. A helper script applies such a rule cheaply and exactly; for an AI it costs attention and invites mistakes. Instructions tell the agent what to do and what to report, and the helper script decides the rest.

Tests read and write files with an explicit UTF-8 encoding, so they pass under a C or POSIX locale as well.

## Check before handing it over

Have the whole of the instructions reviewed — the entire skill or the entire prompt — by a separate agent with a fresh context, not just the diff: defects in long-committed text are as real as new ones. The reviewer reads every file in full, does not edit, and reports numbered findings with file, line, severity, the current text and a replacement. A useful rubric:

- public-repository fitness: names, private codes, paths and skills, machine details;
- language: text in another language without a reason, translated-sounding English, non-US spelling or typography;
- coherence: contradictions, the same rule stated in two places, references to files, sections, tools or fields that do not exist, terms used without definition;
- instructional quality: reasons given, no unexplained rigid rules, references read at the right time, no authoring history;
- formatting: hard line breaks, broken Markdown;
- scripts and tests: they pass, and the references describe what the helper actually does.

For a skill, load it through the client's skill mechanism to confirm that it is found and loads. Fix the findings, then run a second pass that checks each fix and looks for defects the fixes introduced; replacements made by a script or a regex are a common source of new ones. Test the instructions wherever testing fits the change and is simple to set up — run the helper's tests, or a few test prompts against the old and new text as `skill-creator` describes. When meaningful testing would be complex or costly, do not skip it silently and do not build it on your own: ask the user, proposing a concrete test — what to run, on which prompts or cases, and what it would show. Commit according to the repository's own rules.
