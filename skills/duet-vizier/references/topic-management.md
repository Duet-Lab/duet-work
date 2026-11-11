# Topic management

Read this before you create, change, move or report on a topic, and whenever a work folder already holds topic folders. A topic is one part of the work with one expected outcome, and topics are the top-level division of a work folder that is organized by subject. The work folder is the memory agents share between sessions, and I read it topic by topic: a conversation drifts across several subjects, and a folder that mixes them is as hard to read as the chat was.

## What a topic is

A topic is one subject with one expected outcome. The outcome is what is on hand when the topic is done and what the topic runs for, so it also says when the topic is closed. Because a topic has one outcome, it is homogeneous: designing something and implementing the design are two topics, not two phases of one. When an outcome seems to need both, split the topic.

A topic's folder is a container for what we know about the topic, not a sign that work on it has started. Create it in the turn the conversation first holds anything about the topic — a remark, a definition, any fact that has to be filed somewhere — because everything I say lands in a file in the same turn (see "Blockers, rolls, reviews and the handoff" below), and the topic's folder is where that file belongs. So an implementation topic gets its folder as soon as anything is said about it, long before the design it follows is ready. Where the work on a topic stands is told by its status (see "The topic folder"), never by whether the folder exists. Write in the folder only what the conversation has established: a topic created this early may not yet have a known outcome or type, and its map says so instead of guessing; fill them in once they are known.

Topics are ordered by how close they are to the purpose of the ticket, not by when they came up. A topic that drifts far from that purpose is a candidate for a ticket of its own; see "Moving topics" below.

## The topic folder

Each topic is a folder `NN_slug` directly in the work folder, with an `INDEX.md` inside. Everything the topic holds lives in that folder, so a reader can take one topic and ignore the rest.

- **Number.** `NN` fixes the order in the folder and serves as a mnemonic; it is not an address. I may ask to reorder topics; renumbering changes the folder name, the number in the H1 of `INDEX.md` and of each document, the order of the "Topics" section in the work's `INDEX.md`, and every path kept current that contains the folder name, such as a line of the notepad's dashboard. Nothing else changes, because a link names a topic by its slug, never by its number, and rolls and other history keep the paths they were written with.
- **Slug.** The slug is the topic's name: unique within the work folder, lowercase Latin letters, digits and underscores, without the order number and with no hyphens, so that a double-click selects it whole and I can paste it into the chat. Keep a new slug at most 12 characters: it is a memory hook, not the meaning, which the title next to it carries; I paste it at the start of a reply, and the dashboard aligns slugs in a column that a long one widens. Existing slugs are not renamed for length. It changes only when I ask to rename the topic; renaming changes the folder name, the `slug` in the frontmatter, the title in the H1 of `INDEX.md` and of each document, the topic's line in the work's `INDEX.md`, and every link and plan step that names the slug, found by searching, as "It leaves the system consistent" in the system prompt requires.
- **Frontmatter.** `INDEX.md` carries `folder-type: topic`, `topic-type` (see "Topic types" below) once it is known, and `slug`, so that a topic can be found with a search and told apart from a work folder (`folder-type: work`).
- **Heading.** The H1 is the ticket number, a hyphen, the topic number, a period and the title: `# ABC001-01. Working in branches`. Each topic is a document of its own, and the files in its folder are the parts of that document.
- **Body.** `**Purpose:**` on one line, then `**Expected outcome:**` in the form described under "Expected outcome" below, then the status, then `**Documents:**` as a list of the topic's documents with one phrase each (a handoff is listed too, marked temporary; reviews are not listed, their folder is found by name), then `**Rolls:**` as a list, one line per roll in the topic's `rolls/` folder: its file name, what it is for, and whether it is live or closed. Take what it is for from the roll's `purpose`, or from its first assignment when it has none, and set `purpose` whenever you open a roll for a topic. A roll is live while the work it was opened for is under way; mark it closed when that work is done and no assignment in it is open, whether or not its participants' sessions go on in other rolls. A live roll also names who works in it now, with their models and any skills their assignment requires, as the roll's latest assignments say. When a state cannot be established, the line says it is unknown. The list is a view of the rolls, not a roster of their participants: identities, sessions and windows stay in each roll's frontmatter, and the list is corrected from the rolls, never the other way round. Then `**Blockers:**` as one line that points to the topic's `blockers/` folder without listing what is in it, the way the work's `INDEX.md` points to its own: a list repeats the folder and drifts from it, while the open blockers are exactly the files lying directly in the folder. Nothing else, apart from the one bold opening line of a moved topic (see "Moving topics"): the map stays short enough to read in seconds.
- **Purpose.** A short phrase naming the topic's share of the ticket's work, such as "design of the rules for working in branches" or "implementation of the rules for working in branches". Why the work is needed at all is the ticket's purpose, stated once in the notepad's dashboard; a topic purpose that restates it adds nothing and makes the topics look alike. The expected outcome says what will be on hand when the topic is done; the purpose says which part of the ticket the topic carries. The dashboard shows the purpose in the progress of the work.
- **Status.** One or two sentences in plain words on where the work stands — not started, under way, paused, moved and the like — and who acts next, with no account of how it got there and no hashes or message IDs. Keep it current and update it in the same turn the state changes, because the folder's existence says nothing about the work; the dashboard shows it under the topic's purpose. How the field is marked up is not settled yet; until it is, write it the way the work folder's other topics already do, as "It fits what is already there" in the system prompt asks.

Example; its status line is an illustration, not a settled format:

```markdown
---
folder-type: topic
topic-type: discovery
slug: branch_rules
---

# ABC001-01. Working in branches

**Purpose:** design of the rules for working in branches.

**Expected outcome:** design — the rules for working in branches, ready to hand to an implementer.

**Status:** design under way; waits on my answer about one worktree per ticket.

**Documents:**

- `01_protocol.md` — the protocol itself.

**Rolls:** none yet.

**Blockers:** in this topic's `blockers/` folder; open ones lie directly in it, resolved and canceled ones in its `resolved/` and `canceled/`.
```

## The work's `INDEX.md`

In a work folder divided into topics, the work's `INDEX.md` has a "Topics" section that lists the topics in their order, one line each: the slug, the plain name and the expected outcome, with the topic's status when it is not obvious from the outcome. Details stay in the topic folders. Its section on blockers points to the `blockers/` folders, the root one and those of the topics, without listing them, as `references/blockers-management.md` describes. A step of the Backbone Plan that belongs to a topic names the topic's slug.

## Expected outcome

Write the outcome with its type first and its subject after it: `design — the rules for working in branches`, `knowledge — where the git rules are written today`. The type comes first because it is what I need to grasp without thinking; a chain of nouns that hides the type in its first word costs me the effort of parsing it. Keep the wording short — about half of what first seems necessary — and leave the details to the topic's documents.

Types that have served so far: **design** (what something will be), **knowledge** (how something is now), **decision** (a chosen option with its reason), **answer** (the answer to a question of mine), **change** (work done in a product), **understanding** (what I learned and can retell). Reuse one of these words when it fits, so that outcomes stay comparable across topics; when none fits, name the type in one plain word that says what the topic delivers.

For a change, name the form of the change rather than files: which parts of the system change and how — a new tool, a changed one, a new reference — without file names or details, which belong to the topic's documents. When several parts change, put the type first and list the parts under it, a few words each. When a topic's outcome is the same as the ticket's expected results, write the same words in both places and say so next to the label, such as "(same as the ticket)"; when they match only in part, the note says which part.

## Topic types

`topic-type` says what the topic runs for. For discovery, delivery and study it follows from the outcome type and from who consumes the outcome, so it is never a separate decision; a debug topic is recognized by what prompts it.

- **discovery** — find out what to do; outcomes: design, knowledge, decision, answer, consumed by later work.
- **delivery** — do it: implementation by executors and reviewers, driven by a design from a discovery topic; outcome: change. It is the topic that normally holds rolls and reviews.
- **study** — knowledge for its own sake; outcomes: knowledge or understanding, with me as the only consumer. A study becomes discovery when its knowledge gets a consumer.
- **debug** — correcting the agent itself and the way we work together, prompted by my remarks on its behavior. A debug topic has no prescribed outcome: write the one the conversation has established.

Use the list as it stands and raise a blocker when a topic fits none of the four.

## The parts of a topic

### Documents

A document is a file `NN_slug.md` in the topic folder, numbered like topics, and it holds the topic's state. It is never a log: it says what we found and decided as of now, and when the understanding changes, the text is rewritten in place.

Each document answers one kind of question. Text types: need, design, plan, rules, knowledge, investigation, questions and answers. The ticket's `thesaurus.md` stays at the root of the work folder, as the system prompt requires; a topic document does not replace it.

Inside a document, the topic's H1 is repeated, then `## NN.` followed by the file's subject, then H3 for the file's own structure. Add frontmatter with `slug` when the file is referred to by slug from a blocker, a roll or the chat, so that the address can be found by a search; otherwise none.

Where a document records what is settled and what is only proposed, mark each item **accepted** or **proposed**, with the blocker that waits on it, so that a proposal is never read as a decision.

### Blockers, rolls, reviews and the handoff

- **Blockers** of a topic live in `blockers/` inside the topic folder, kept as `references/blockers-management.md` describes, so that a reader who takes one topic sees what it waits on. Resolved and canceled ones move to `resolved/` and `canceled/` there. A blocker about the ticket as a whole stays in `blockers/` at the root of the work folder. A blocker's slug stays unique across the whole work folder, topics included, because it is the blocker's address in the plan, the notepad and the chat. The Invocation section of the system prompt has them read at the start of a chat together with the root ones.
- **Executors** belong to one topic each and work only within it. An executor may know about other topics and pass something to a neighboring one — an implementation topic takes input from its design topic and gives feedback back — but only through the Curator. A topic may have several rolls, though one usually suffices.
- **Rolls and reviews** live in `rolls/` and `reviews/` inside the topic folder of the work they serve, whatever its type. They are history, appended and never rewritten, and documents are state, which is why the two never share a folder.
- **A handoff**, `handoff.md` at the root of a topic, is a temporary file written only when a session ends before the topic's documents hold what the conversation established. It collects my decisions, my words verbatim where the wording matters, the agent's proposals with their blockers, facts found on disk, and where to continue — gathered from the transcript turn by turn, not from memory of the themes, because memory drops the remarks that no blocker captured. It opens with a line saying it is temporary and is deleted when the topic's documents hold its content.

Everything I say lands in a file in the same turn, broken into its parts: an idea goes to a document or a blocker, a rule to a document, a question to a questions-and-answers document together with its answer, or to a blocker while it has none. What stays only in the chat may never reach me again and is not the state a new session starts from.

## Moving topics

When a topic outgrows its ticket, propose a ticket of its own; on my word, create it with `new_ticket`, as "One chat may work on any number of tickets" in the system prompt describes, and the topic moves there and gets a number there. In the parent ticket its folder stays as it was at the moment of the move, blockers included, with two changes: its status says that the topic has moved, and the first line of its `INDEX.md` body says, in bold, that the topic has moved to `@ABC002`, named in words, and is not developed here. Its blockers are not read as open in the parent, because that line says where the live ones are, and the start-of-chat reading of open blockers skips a moved topic. The frozen copy lets a new session in the parent restore the context without leaving, and the status keeps anyone from working on the stale copy.

A link between tickets points at the ticket, `@ABC002` with the ticket's plain name, and names the topic in words, because the ticket number never changes while a topic's number and slug may.

## Reporting on topics in chat

Name a topic by its slug and say in the same sentence what it is about. When the changes matter to me now, name the topic and the files under `### Work Folder Updates`, one line each, as the Response Protocol in the system prompt allows, and do not retell their content: the reply still carries the substance my current question needs, as "Files vs chat" in the system prompt requires, and the rest I read in the folder. When a topic's outcome or type changes, say so explicitly, because it changes what I expect from the topic.
