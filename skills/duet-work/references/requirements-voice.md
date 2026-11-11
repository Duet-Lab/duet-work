# Requirements voice

Read this when you clarify requirements — business, functional or non-functional — for work that another agent implements, and before you write any of them down. It says what such requirements may contain, how they are worded and when you ask me, because the executor reads every line of them as what I want.

## What goes into the requirements

Record my thoughts and what follows directly from them, and nothing beyond that. A requirement binds the executor: it takes each line as what I want and builds to it. A guess of yours about what the work should do or how it should be done therefore narrows the executor's solution to your framing, and when the guess is wrong the work is built on something I never asked for. The executor must not be confined by your guesses, either about what the work does or about how it is done. This bounds what you record, not what you say to me: when a thought of mine looks wrong to you, tell me so with your reason, and record what I decide. Record each requirement with the situation and reason it came from, as "Everything needs its reason — always" in `SKILL.md` describes.

When I say how something should be done — which mechanism to use, which library to rely on, where a value comes from — that is my requirement, not a proposal of yours, and it goes in like any other. Keep how settled I am: an option I am only considering is recorded as an option I am considering, because writing it down as decided would add a decision I have not made.

A direct consequence is what my words already commit to, so that anyone who accepts them has to accept it too: if I say a setting is kept per user, one global value does not meet it. When getting from my words to a statement takes a choice between options, the statement is not a direct consequence but your addition.

Anything beyond that — more about what the work does, or a way of doing it that I did not state, such as names of fields, parameters or filters, lists of files, methods or tests, a transition period, or the side on which a check runs — enters the requirements only once I knowingly agree to it. By default it stays out, and the executor settles it. If you think such an addition belongs in the requirements, put it to me as a blocker, stated as your proposal (`references/blockers-management.md`), and carry it in only once I accept it. Where a document holds both accepted and proposed items, mark each one as `references/topic-management.md` describes, so that a proposal is never read as a decision.

## How to word it

Word each requirement as "My thoughts in their best form" in `SKILL.md` describes.

## When to ask

Open a blocker only for a choice that my words and their direct consequences leave open; a word of mine whose purpose you cannot tell leaves such a choice, as "Every part carries equal weight, and every word is deliberate" in `SKILL.md` describes. Do not turn your own reading of a single word into a question: when you understand what I meant by it, write the requirement on that reading. A question asks for my attention, and what you can settle from my words is yours to settle; the general boundary for what goes to me is "It hands back only real decisions" in `SKILL.md`.
