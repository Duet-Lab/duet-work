# MessageRoll principles

Read this when organizing or joining a shared conversation through files. A **MessageRoll**, or roll, is a Markdown record of messages for a particular purpose, with named participants and a moderator. It preserves the exchange across clients and sessions; it is not itself a task, a phase or a running agent.

## Purpose and participants

The moderator creates a roll for the conversation that is needed and keeps its purpose and participants clear. A ticket may have any number of rolls, and a phase may contain more than one. A design discussion and a round-table exchange can use the same basic format without sharing a development process. The procedure using the roll determines when to create it and what counts as a result.

The user sets intent and authority. The moderator connects participants and mediates the exchange; it does not become the owner of their technical judgment. Participants may use different clients and models. Their roles describe responsibilities, not an intelligence hierarchy.

Clarify ambiguous user wording with the user before handing it to participants. Give them the distilled request, using canonical terms from the shared thesaurus where short forms could mislead, rather than forwarding the whole clarification exchange. This protects their working context without concealing relevant reasoning, constraints or remaining uncertainty. Do not turn a tentative statement into a decision or a clarified goal into instructions for how an engineer must solve it.

Use stable, informative participant names so authorship is understandable: for example `Developer_Gemini_1` or `Reviewer_Codex_Security_1`. Keep everyone who contributed, including disconnected participants. A replacement gets a new name; an interruption must not erase or reassign earlier contributions. The current moderator address can change without rewriting the conversation.

## Messages and artifacts

A message records who said what and has an ID that other messages can refer to. Keep the exchange in ordinary readable Markdown. Corrections and clarifications are new messages rather than silent rewrites of earlier contributions. Refer to a message when answering it, and preserve the distinction between a proposal, a report and an accepted decision.

The roll holds the conversation; substantial results can live in linked artifacts. Save a result before posting its short reference. A brief assignment may be a message; a useful separate assignment file is equally valid, with the message linking to it. Maintain one authoritative text rather than two competing copies. This does not require task fields, assignment versions or a fixed artifact catalog.

Participants read relevant artifacts directly. The moderator need not collect or rewrite their results for other participants to use them. Explaining a result to the user is a separate responsibility, not a replacement for the original evidence. Shared terms come from the ticket's `thesaurus.md`, not a different glossary in every roll.

## Moderator updates

The coordinator and moderator are the same role. Maintain the shared context of the conversation, including its agenda and the ticket's thesaurus. Extract terms from the user's requests and all participants' contributions, and refine them through discussion; do not wait for someone to request glossary maintenance. Preserve the distinction between established meanings and unresolved disputes.

When shared context changes, inform all participants through an ordinary moderator message: say what changed, what it means for the discussion or work, and link the current source. Group related changes into a useful update rather than announcing every edit. Across rolls, reference the same authoritative agenda or thesaurus instead of making local copies. No special message type or metadata field is needed.

Publishing the update and reaching participants are separate responsibilities. Deliver it to current participants through the procedure's verified invocation mechanism; bring returning or replacement participants up to date before they continue. Do not restart disconnected agents just to announce a change. A change affecting ongoing work needs timely delivery, not merely a note waiting for someone to discover it; an update itself is not permission to resume blocked work.

## Persistence is not invocation

AI participants act when invoked; a persistent conversation does not mean they are continuously watching the file. Saving, notifying and acting are distinct events. Use a verified delivery or observation mechanism to start the next turn, then read the durable message and its context. A notice is not proof of completion and does not grant user authority.

After an interruption, reconcile the retained messages, current moderator and actual sessions before continuing. Do not treat silence as agreement or duplicate an action because its notice arrived twice. Specific scheduling, permissions and completion gates belong to the procedure using the roll, not to the meaning of the file.

## Format and operation

Frontmatter identifies `roll-type`, the current `coordinator`, and `participants`. The moderator is stored as `coordinator`; development curation calls that participant the Curator. Messages retain authorship, timestamps and IDs. Keep this record useful independently of a particular workflow: phases, code-review rules and client-specific automation should not become mandatory message semantics.

Before creating, changing metadata or appending, read [MessageRoll operations](message-roll-operations.md). It specifies the current schema, helpers and concurrency/delivery limits. For software work, [Development curation](dev-curation.md) applies these principles to engineers, phases and review; it does not redefine the roll.
