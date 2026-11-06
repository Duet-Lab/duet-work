# Blockers management

Read this before you create, update, close or report a blocker. A blocker is the most reliable channel to me: the chat may go unread, a blocker does not. So everything that waits on me is recorded as a blocker, not only mentioned in the chat.

## What is a blocker

A blocker is anything in the work that waits on a person: a decision, acceptance of a result, an action only a person can take, the word to take a ready step, or an answer to your proposal. An open question is one kind of blocker.

What follows from what I said or from the files, and changes nothing in my environment, is not a blocker: it is yours to do, and you report it in one line. Everything else that needs a person's word is a blocker, including a question no named step needs yet and a proposal of your own, because left only in the chat it is lost, and I decide when to take it up.

## Files

Each blocker is a file `blockers/<slug>.md` at the root of the work folder, or inside its topic's folder when the work is divided into topics (see `references/topic-management.md`), written in the language of the work folder's files. A blocker is open while its file lies directly in `blockers/`. It moves to `blockers/resolved/` when what it waited for has happened, and to `blockers/canceled/` only on the word of the person it waits on; silence or relabeling never closes a blocker.

The slug is the blocker's permanent address in the map, in other blockers and in the chat, so it never changes, even when the blocker's substance is refined. Write it in lowercase Latin letters with underscores, never hyphens, so that a double-click selects it whole, and repeat it in the frontmatter as `slug: <slug>`, so that the slug stays visible inside the file and can be found by a search.

## Content

The person must grasp a blocker in one reading, at a glance; this matters more than completeness, so leave out every piece of background they do not need in order to answer. The sections, in order, with headings written in the work folder's language:

- a level-1 heading with a plain name of the blocker;
- **Summary:** one or two sentences on what is at stake, then a bold line saying who it waits on and what exactly is needed;
- **Status:** a one- or two-sentence summary of where the discussion stands, kept current;
- a section headed with the person's name, added once they first speak about this blocker: their words about it;
- **Agent's verdict:** what you propose and why, briefly; rewrite it when your proposal changes, so that it never contradicts the status.

## The map

What waits on a person is not listed in the work's `INDEX.md`: it has a section that points to the `blockers/` folders — the root one and, in a work divided into topics, each topic's — so the two cannot drift apart. A topic's own `INDEX.md` lists that topic's open blockers, as `references/topic-management.md` describes.

## Working through blockers

I take one blocker at a time, in any order, and may leave any of them open indefinitely; that is why each lives in its own file. Discuss only the blocker I have taken up.

When you create a blocker, name it once in the reply that ends your turn: its slug together with one plain sentence on what is at stake and what it waits on. When a step I named is ready and waits only on my word, record it as a blocker and name its slug in your reply. Wherever you mention a blocker later, in the chat or in another file, say in the same sentence what it is about, because a slug alone tells the reader nothing. After that first mention, do not push a blocker, remind me of open blockers or list them unless I ask.

When I speak about a blocker, update its status and my section at once; when it is resolved, carry the decision into the decisions in `INDEX.md` and say in the status how it was resolved.
