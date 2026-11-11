# Blockers management

Read this before you create, update, close or report a blocker. A blocker is the most reliable channel to me: the chat may go unread, a blocker does not. So everything that waits on me is recorded as a blocker, not only mentioned in the chat.

## What is a blocker

A blocker is anything in the work that waits on a person: a decision, acceptance of a result, an action only a person can take, the word to take a ready step, or an answer to your proposal. An open question is one kind of blocker.

Which choices go to me at all is set in one place, "It hands back only real decisions" in `SKILL.md`. Whatever passes that test is a blocker, even when no named step needs it yet, because left only in the chat it is lost, and I decide when to take it up; whatever does not pass it is yours to do, reported in one line.

A doubt whether a text suits me is settled the same way. When you or an executor cannot tell from what I have said whether a text written to be used suits me — a skill, a prompt, a product's document — ask me through a blocker, and keep the doubt out of the text itself: do not decorate the text with notes on who approved its wording or on what I have not yet confirmed. Such a note gives the text's reader nothing of value and spoils the text. Attribution and status stay wherever the reader needs them — as evidence, as the subject of the document, or to know what is authorized — and so does the record of accepted and proposed items in a topic's own documents, which `references/topic-management.md` describes.

## Files

Each blocker is a file `blockers/<slug>.md` at the root of the work folder, or inside its topic's folder when the work is divided into topics (see `references/topic-management.md`), written in the language of the work folder's files. A blocker is open while its file lies directly in `blockers/`. It moves to `blockers/resolved/` when what it waited for has happened, and to `blockers/canceled/` only on the word of the person it waits on; silence or relabeling never closes a blocker.

The slug is the blocker's permanent address in the map, in other blockers and in the chat, so it never changes, even when the blocker's substance is refined. Write it in lowercase Latin letters with underscores, never hyphens, so that a double-click selects it whole. Keep a new slug at most 12 characters, as `references/topic-management.md`, "Slug", explains for topics; an existing slug is never renamed for length. Repeat it in the frontmatter as `slug: <slug>`, so that the slug stays visible inside the file and can be found by a search.

## Content

The person must grasp a blocker in one reading, at a glance; this matters more than completeness, so leave out every piece of background they do not need in order to answer. The sections come in the order they are read, with headings written in the work folder's language:

- a level-1 heading that is the question or request to the person, in plain words, so that it reads on its own wherever the blocker is listed, such as in my notepad's dashboard;
- **Status:** one or two sentences, kept current, saying first whether the blocker is ready for the person's answer or is still being prepared by an agent or paused, and then where the discussion stands. Readiness comes first because only a ready blocker is put to them as a question, and a paused one should not be read through before that shows;
- **Summary:** one or two sentences on what is at stake; where the answer is a choice, the options, each with what it changes, one line per option; a bold line saying who it waits on and what exactly is needed only when it adds something to the heading;
- **Agent's verdict:** what you propose and why, briefly, right after the options it chooses among; rewrite it when your proposal changes, so that it never contradicts the status;
- a section headed with the person's name, last, added once they first speak about this blocker: the record of their thoughts about it, written in their best form as "My thoughts in their best form" in `SKILL.md` describes, each decision with the situation and reason it came from, as "Everything needs its reason — always" there describes.

## The map

What waits on a person is listed neither in the work's `INDEX.md` nor in a topic's: each points to its `blockers/` folders instead — the work's `INDEX.md` to the root one and, in a work divided into topics, to each topic's; a topic's `INDEX.md` to its own, as `references/topic-management.md` describes — so a map and its folders cannot drift apart.

## Working through blockers

I take one blocker at a time, in any order, and may leave any of them open indefinitely; that is why each lives in its own file. Discuss only the blocker I have taken up.

When you create a blocker, name it once in the reply that ends your turn: its slug together with one plain sentence on what is at stake and what it waits on. When a step I named is ready and waits only on my word, record it as a blocker and name its slug in your reply. Wherever you mention a blocker later, in the chat or in another file, say in the same sentence what it is about, because a slug alone tells the reader nothing. After that first mention, do not push a blocker, remind me of open blockers or list them unless I ask.

When I speak about a blocker, update its status and my section at once; when it is resolved, carry the decision into the document where it governs the work, update the maps and states it affects, and say in the status how it was resolved.
