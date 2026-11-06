# Topic management

Read this before you create, change, move or report on a topic, and whenever a work folder already holds topic folders. A topic is one part of the work with one expected outcome, and topics are the top-level division of a work folder that is organized by subject. The work folder is the memory agents share between sessions, and I read it topic by topic: a conversation drifts across several subjects, and a folder that mixes them is as hard to read as the chat was.

## What a topic is

A topic is one subject with one expected outcome. The outcome is what is on hand when the topic is done and what the topic runs for, so it also says when the topic is closed. Because a topic has one outcome, it is homogeneous: designing something and implementing the design are two topics, not two phases of one, and the implementation topic opens when the design is ready to hand over. When an outcome seems to need both, split the topic.

Topics are ordered by how close they are to the purpose of the ticket, not by when they came up. A topic that drifts far from that purpose is a candidate for a ticket of its own; see "Moving and duplicating topics" below.

## The topic folder

Each topic is a folder `NN_slug` directly in the work folder, with an `INDEX.md` inside. Everything the topic holds lives in that folder, so a reader can take one topic and ignore the rest.

- **Number.** `NN` fixes the order in the folder and serves as a mnemonic; it is not an address. I may ask to reorder topics; renumbering changes the folder name, the number in the H1 of `INDEX.md` and of each document, and the order of the "Topics" section in the work's `INDEX.md`, and nothing else, because links name a topic by its slug, never by its number.
- **Slug.** The slug is the topic's name: unique within the work folder, lowercase Latin letters, digits and underscores, without the order number and with no hyphens, so that a double-click selects it whole and I can paste it into the chat. It changes only when I ask to rename the topic; renaming changes the folder name, the `slug` in the frontmatter, the title in the H1 of `INDEX.md` and of each document, the topic's line in the work's `INDEX.md`, and every link and plan step that names the slug, found by searching, as "It leaves the system consistent" in `SKILL.md` requires.
- **Frontmatter.** `INDEX.md` carries `folder-type: topic`, `topic-type` (see "Topic types" below) and `slug`, so that a topic can be found with a search and told apart from a work folder (`folder-type: work`).
- **Heading.** The H1 is the ticket number, a hyphen, the topic number, a period and the title: `# ABC001-01. Working in branches`. Each topic is a document of its own, and the files in its folder are the parts of that document.
- **Body.** `**Expected outcome:**` on one line, then `**Documents:**` as a list of the topic's documents with one phrase each (a handoff is listed too, marked temporary; rolls and reviews are not listed, their folders are found by name), then `**Blockers:**` as a list of the topic's open blockers, slug and one phrase each, updated in the same turn a blocker opens or moves. Unlike the work's `INDEX.md`, the topic map lists its blockers, because a reader who takes one topic must see in one place what it waits on. Nothing else, apart from the one bold opening line of a moved or duplicated topic (see "Moving and duplicating topics"): the map stays short enough to read in seconds.

Example:

```markdown
---
folder-type: topic
topic-type: discovery
slug: working_in_branches
---

# ABC001-01. Working in branches

**Expected outcome:** design — the rules for working in branches, ready to hand to an implementer.

**Documents:**

- `01_protocol.md` — the protocol itself.

**Blockers:**

- `merge_push_main` — whether the agent pushes `main` right after the squash merge.
```

## The work's `INDEX.md`

In a work folder divided into topics, the work's `INDEX.md` has a "Topics" section that lists the topics in their order, one line each: the slug, the plain name and the expected outcome, with the state when it is not obvious from the outcome. Details stay in the topic folders. Its section on blockers points to the `blockers/` folders, the root one and those of the topics, without listing them, as `references/blockers-management.md` describes. A step of the Backbone Plan that belongs to a topic names the topic's slug.

## Expected outcome

Write the outcome as "type — subject": `design — the rules for working in branches`, `knowledge — where the git rules are written today`. The type comes first because it is what I need to grasp without thinking; a chain of nouns that hides the type in its first word costs me the effort of parsing it. Keep the line short — about half of what first seems necessary — and leave the details to the topic's documents.

Outcome types: **design** (what something will be), **knowledge** (how something is now), **decision** (a chosen option with its reason), **answer** (the answer to a question of mine), **change** (work done in a product), **understanding** (what I learned and can retell), **agent rule** (corrected agent behavior, written into a skill's source). Use these words rather than coining new ones, so that outcomes stay comparable across topics; when none fits, say so in a blocker rather than inventing one silently.

## Topic types

`topic-type` says what the topic runs for; it follows from the outcome type and from who consumes the outcome, so it is never a separate decision.

- **discovery** — find out what to do; outcomes: design, knowledge, decision, answer, consumed by later work.
- **delivery** — do it: implementation by executors and reviewers, driven by a design from a discovery topic; outcome: change. It is the topic that normally holds rolls and reviews.
- **study** — knowledge for its own sake; outcomes: knowledge or understanding, with me as the only consumer. A study becomes discovery when its knowledge gets a consumer.
- **debug** — correcting the agent itself and the way we work together, prompted by my remarks on its behavior; outcome: agent rule. The outcome counts only when the rule is written into the source of the skill the agent will read next time, because a correction kept in the chat dies with the session.

Use the list as it stands and raise a blocker when a topic fits none of the four.

## The parts of a topic

### Documents

A document is a file `NN_slug.md` in the topic folder, numbered like topics, and it holds the topic's state. It is never a log: it says what we found and decided as of now, and when the understanding changes, the text is rewritten in place.

Each document answers one kind of question. Text types: need, design, plan, rules, knowledge, investigation, questions and answers. The ticket's `thesaurus.md` stays at the root of the work folder, as `SKILL.md` requires; a topic document does not replace it.

Inside a document, the topic's H1 is repeated, then `## NN.` followed by the file's subject, then H3 for the file's own structure. Add frontmatter with `slug` when the file is referred to by slug from a blocker, a roll or the chat, so that the address can be found by a search; otherwise none.

Where a document records what is settled and what is only proposed, mark each item **accepted** or **proposed**, with the blocker that waits on it, so that a proposal is never read as a decision.

### Blockers, rolls, reviews and the handoff

- **Blockers** of a topic live in `blockers/` inside the topic folder, kept as `references/blockers-management.md` describes, so that a reader who takes one topic sees what it waits on. Resolved and canceled ones move to `resolved/` and `canceled/` there. A blocker about the ticket as a whole stays in `blockers/` at the root of the work folder. A blocker's slug stays unique across the whole work folder, topics included, because it is the blocker's address in the plan, the notepad and the chat. The Invocation section of `SKILL.md` has them read at the start of a chat together with the root ones.
- **Rolls and reviews** live in `rolls/` and `reviews/` inside the topic folder of the work they serve, whatever its type. They are history, appended and never rewritten, and documents are state, which is why the two never share a folder.
- **A handoff**, `handoff.md` at the root of a topic, is a temporary file written only when a session ends before the topic's documents hold what the conversation established. It collects my decisions, my words verbatim where the wording matters, the agent's proposals with their blockers, facts found on disk, and where to continue — gathered from the transcript turn by turn, not from memory of the themes, because memory drops the remarks that no blocker captured. It opens with a line saying it is temporary and is deleted when the topic's documents hold its content.

Everything I say lands in a file in the same turn, broken into its parts: an idea goes to a document or a blocker, a rule to a document, a question to a questions-and-answers document together with its answer, or to a blocker while it has none. Assume the chat is not read; a thing that exists only there is lost.

## Moving and duplicating topics

When a topic outgrows its ticket, propose a ticket of its own; on my word, create it with `new_ticket`, as "One chat may work on any number of tickets" in `SKILL.md` describes, and the topic moves there and gets a number there. In the parent ticket its folder stays as it was at the moment of the move, blockers included, with one change: the first line of its `INDEX.md` body says, in bold, that the topic has moved to `@ABC002`, named in words, and is not developed here. Its blockers are not read as open in the parent, because that line says where the live ones are, and the start-of-chat reading of open blockers skips a moved topic. The frozen copy lets a new session in the parent restore the context without leaving, and the status keeps anyone from working on the stale copy.

When it is not yet clear where a topic will be resolved, copy the topic whole into both tickets; its blockers stay in the ticket where the resolution is likelier, and the first line of each copy's `INDEX.md` body says, in bold, that the other copy exists and where the blockers are. Say so in each ticket's `INDEX.md` as well.

A link between tickets points at the ticket, `@ABC002` with the ticket's plain name, and names the topic in words, because the ticket number never changes while a topic's number and slug may.

## Reporting on topics in chat

Name a topic by its slug and say in the same sentence what it is about. When the changes matter to me now, name the topic and the files under `### Work Folder Updates`, one line each, as the Response Protocol in `SKILL.md` allows, and do not retell their content: the reply still carries the substance my current question needs, as "Files vs chat" in `SKILL.md` requires, and the rest I read in the folder. When a topic's outcome or type changes, say so explicitly, because it changes what I expect from the topic.
