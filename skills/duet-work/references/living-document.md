# Living Document

Read this when the user asks to continue a conversation as one document they will read and react to, rather than as a chain of replies. It is a special mode of work the user requests; nothing switches it on by itself. Before creating the roll, read MessageRoll principles (`references/message-roll.md`) and operations (`references/message-roll-operations.md`); the rules here govern what the document and the cycle are, not how a roll is stored.

## What the mode is for

The user's questions are the expression of their interest: every new question either lands in an existing topic or extends the list of topics, and the document's structure follows them, not what the agents need to learn from the user. Do not interview the user about their interests when the topics and their questions already show them. The user reads a document, not the chat, and does it slowly, like someone who reads a little at a time and asks questions as they go. Never assume they have read the whole document or any particular version of it. Files that record a dialogue, such as one file per reply with the user's message, comments on each paragraph and numbered claims, read as a log; this mode replaces them with one organized text that grows and improves from the user's reactions. The value is that the user can stop anywhere, come back days later, and refer to any section by a stable address.

## The trio

Three participants do the work; roles are responsibilities, not a ranking of models. The user chooses each client, model and effort.

- **Writer** is at the keyboard: improves and extends the document and reports in the roll what changed.
- **Reviewer** is the second pair of eyes, as in pair programming: checks what Writer put in and writes findings, but never edits the document.
- **Curator** is the moderator and defender of the user's interests: turns the user's thoughts into requests, checks the result against what the user actually asked before reporting, and reports. The Curator does not write the document or argue its substance with the agents — the check is about fidelity to the user's intent and readability for a slow reader, not a third technical review.

The defender step exists because Reviewer checks Writer's text, not whether the user was understood; without it nobody compares the result with the user's request.

## The cycle

1. The user writes to the Curator in the chat, usually naming section slugs. Sometimes the meaning needs a short clarification in the chat first; sometimes it is obvious and goes straight out. Learn the measure from the conversation instead of always asking or never asking.
2. The Curator publishes the request in the roll as a message of whatever length the meaning needs — not a compressed brief — and invokes Writer. The roll keeps the whole history so the user can trace how the document developed.
3. Writer edits the document and posts in the roll what changed, which slugs were touched, how each part of the request was handled and what remains unclear. That message ends Writer's turn: the document stays unchanged until Writer is invoked again, because Reviewer reviews exactly that version. Name the snapshot (a hash prefix is enough) in the review request.
4. Reviewer writes findings to a file in the phase's `reviews/` folder and posts a short reference in the roll.
5. Writer processes the findings: fixes what it accepts and argues with reasons against what it does not, answering by finding number in the same file.
6. At most two Writer–Reviewer rounds per request. A disagreement left after the second round goes to the user with both positions, instead of a third round.
7. The Curator checks the result against the user's request and readability; if the request was misread or not fulfilled, the work goes back to Writer.
8. The Curator reports to the user: which sections changed (by slug) and what waits for the user's decision — not what the sections say. The user reads the document; a retelling in the chat duplicates it as a less precise copy and spends the attention the document is meant to save. Because the user reads slowly, the slugs are how they find what to re-read without keeping the edit history in mind. When a correction overturns something the user already read in earlier materials, say so explicitly.

When the user clarifies a request while Writer is working, publish the clarification in the roll and deliver it into Writer's current turn; otherwise Writer finishes in the old form and a round is wasted.

## The document

- **A document, not a log.** No user prompts, no history of replies; it is organized by topic. Off-topic matters that were settled stay outside it, in the work's own files.
- **Every section stands on its own.** It does not assume the rest was read; it restates in a phrase what it relies on and points to other sections by slug. Repetition of a short definition is acceptable; "as mentioned above" is not.
- **Questions for the user live in the document, inside the topics they belong to**: each at the end of its topic's section, with its own slug, so the user meets it while reading that topic. Do not gather the agents' questions at the top: a section's place signals priority, and questions placed first read as a precondition for everything after them, which they almost never are.
- **Checkable claims about the world get sources**: a date, a number, a specification, which platforms a product runs on — however minor, because an agent may need to verify or trace exactly that claim, and a label in the text costs the reader almost nothing. Practical advice (where to find a laptop's model name), explanations of how a mechanism works and the Writer's own estimates need no source; explanations are still checked for correctness, and estimates are marked as estimates. Nothing useful is removed from the document merely because no source was found for it: a claim without one is kept and marked as unconfirmed. The user rarely opens sources; they exist so that agents understand each other and so that, in the rare case it matters, one can trace where a claim comes from.
- **Sources stand at the end of their section**, as a list:

  ```
  References:
  - ref1 Apple https://developer.apple.com/documentation/apple-silicon/porting-your-macos-apps-to-apple-silicon
  - ref2 …
  ```

  The text refers to them by the label `ref1`; a reference to another section's source is `SC_Tiers/ref2`, which is rarely needed. One source may cover a coherent paragraph.
- **The thesaurus is the language the document is written in.** The document introduces and explains the subject-matter concepts the user reads it for, and they stay there with their explanations. The work's `thesaurus.md` holds the working concepts: words the document and the conversation about it are written in that are not themselves the subject, such as a word the participants have used in two senses. When a sense has an established industry word, use it rather than one that grates on a professional's ear, and give a second sense of an industry word a name of its own instead of overloading the word. Making a thesaurus never thins the document by moving its content out.
- **No Markdown links anywhere.** The user reads raw Markdown, where `[Apple](https://…)` puts a caption where the address should be. Always show the URL itself as text.

## Slugs

Every section and subsection has a slug at the end of its heading, in backticks: a short document prefix, an underscore, and one or two English words in CamelCase — for example `SC_Principle`, `SC_WeakPc` for a document about Stack Choice. The prefix keeps a slug from being confused with an ordinary English word, and because a slug uses only letters, digits and `_`, a double-click selects all of it, so the user can copy it into the chat. Choose the prefix with the user when the document is started and record it in the work's entry file.

A slug belongs to its meaning permanently: it survives renaming and rewriting of the section, and the slug of a removed section is never reused. This is what keeps the user's question about `SC_WeakPc` meaningful after the section has been rewritten three times.

## Starting the mode

Record in the work's entry file that the work runs in this mode, with a pointer to this reference, the document's path, its slug prefix and where the roll lives; keep only what is specific to this work there, not a copy of these rules. Create the roll in a phase folder (for example `01-document/rolls/document.md`) with the user and the Curator; Writer and Reviewer register themselves on their first reply. Launch executors in tmux sessions as `references/dev-curation.md` describes for its persistent sessions and observation, and send nothing to them until the Curator has confirmed with the user what they expect, because the first request sets the pattern for everything that follows.

When the document is built from earlier files that record the dialogue, the first request asks Writer to collect their knowledge by topic without losing anything valuable, to give corrected statements in their latest form, and to move open questions into the document. Expect the first review to find errors inherited from the earlier answers: being written before does not make a statement checked.
