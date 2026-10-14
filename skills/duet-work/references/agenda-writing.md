# Agenda Writing

Read this when preparing or leading discussions, maintaining `AGENDA.md`, or checking whether work may proceed. The Curator owns the conversation's order and continuity; the user controls what needs discussion and when a topic is settled.

## What the agenda is

`AGENDA.md` is where the Curator organises discussions with Andrei: their topics, order, current state and outcomes. It stands beside the Backbone Plan in `INDEX.md` (see `references/backbone-plan.md`) and replaces an «Open questions» section there: the plan holds execution steps, the agenda holds what must be discussed. Conversations with Andrei are steps of the plan too, so that he sees the whole picture; a plan step that waits for a conversation names the agenda item's slug.

Topics include Andrei's points of control and rechecking, his curiosity, questions from the agent, and exploration where he leads the formulation of questions. Curiosity is not a lesser category: it may expose concerns, risks or unknown unknowns that change the entire task. A discussion need not begin with a concrete choice or end in an implementation instruction to belong on the agenda.

**An open agenda blocks the work it governs.** Do not start or continue execution while that agenda remains open unless Andrei explicitly releases the work or changes the scope of the gate. Do not decide on his behalf that a topic is merely curiosity, technical, already obvious or independent enough to bypass. Record the waiting discussion in the plan. An engineer's autonomy within an agreed assignment does not remove Andrei's right to discuss its premises or inspect a technical choice before proceeding.

Preparing evidence for the current discussion, recording decisions and applying an explicitly agreed outcome are part of resolving the agenda, not permission to resume the rest of execution. In software curation, use the bounded investigation route in `dev-curation.md` when that evidence needs technical work. During skill authoring an agreed outcome can include instructions, helpers and tests together; Python is not a separate forbidden category.

**An unread objection is still open.** Preserve substantive objections and new proposals from chat even when Andrei has not read the answer. State them as the agent's proposals, not accepted requirements. Do not treat a request for a plan, a change of topic or silence as acceptance. An agenda is not a duplicate task list: add what needs a conversation, not every implementation step or a minor choice within the agent's authority. Do not reopen decisions Andrei has already made.

## Structure

- `AGENDA.md` is the top level: a numbered list of the items of the first level in logical order (the order may change), each with a link and a state.
- A large item gets its own file `agenda/it_<slug>.md`; inside it, every useful piece is a separate item under H3/H4 with the slug `it_X_Y`, `it_X_Y_Z`. The detailed agenda of an item is generated when its turn comes, not in advance.
- States are defined at the top of the file; in the model they were «ждёт», «в ревью», «закрыт» for files and «ждёт», «принят», «отменён», «перенесён» for items. An item moves to a closed state only on Andrei's decision.

Deferring an item at the agent's discretion changes the conversation order, not its unresolved state or any applicable development gate. Moving a question outside the current work clears that gate only when Andrei has explicitly agreed to the changed scope. The Curator cannot close the agenda by relabelling its own proposals.

## How items are discussed in chat

### Orient before choosing, then discuss one question

When Andrei needs a reminder of the agenda, give a brief state overview: 3–5 nearest, most significant topics, or all remaining topics if fewer. For a large agenda, also state its total open count and broad thematic groups. Choose priorities from the current situation and explain them in short, intelligible labels, not bare slugs. Recommend one or two starting points and let him choose which to open in detail.

For example: «В повестке 20 вопросов: границы задачи, проверка результата и публикация. Вот пять ближайших тем: … Предлагаю начать с … или … Какую разберём?» Use real counts and topics; this is an orientation pattern, not a required template for every reply.

The overview is a menu for selecting a discussion, never a request to answer several substantive questions at once. Once a topic is selected, discuss strictly one question at a time so Andrei can concentrate and think. A broad topic may take several turns; do not disguise a batch of questions as one agenda item. Do not repeat the overview when the current question is already clear.

### Explain, explore or decide — follow the current request

Apply the answer-preparation sequence in SKILL.md: start from what Andrei can understand, explain the relevant facts and their limits, then end in the way his request calls for. «Explain this topic» is not yet «ask me to close it». A source retracting a recommendation changes the evidence, not the user's right to discuss it.

Bring independent reasoning rather than rubber-stamping a source or the user. Distinguish his decision, which governs the work, from a factual assertion that needs evidence. If technical verification is needed, obtain it from the responsible executor; do not turn the discussion into the Curator's own product investigation.

When a decision is actually before him, present the reasonable alternatives and consequences, with a recommendation. When he is reviewing wording, show the actual proposed text, ready for use, rather than a label for it. These are forms for those requests, not mandatory endings for every explanation or exploration.

### Move only when the user moves the conversation

Approval of the current item, including «да», authorizes its agreed action, not the next agenda item. Complete that action, record the outcome, then wait without introducing another item or asking whether to continue. Each transition needs an explicit instruction such as «дальше» or a named next topic; an earlier request to continue is not standing permission.

On «дальше», select the next highest-priority question in logical order, respecting the user's stated sequence. Prefer questions whose resolution determines later ones. If the user asks for orientation or wants to choose, show the brief overview instead. Changing the order or deferring a topic does not close it; keep it visible and return to it.

## What the file records

For each item: the claim or question in substance, what was checked, the options with their cost, and — once Andrei has spoken — his decision in his terms and what was done with it (transferred, cancelled, where). The agent's proposals that Andrei has not answered stay marked as the agent's: silence does not close an item.

When the agenda changes, inform the participants in a moderator update, including what is now blocked, released or awaiting discussion when that affects them. Use [MessageRoll principles](message-roll.md) when working through rolls. This keeps participants aligned; it does not require repeating the whole agenda or turning the user's current conversation into another status report.

Live instances: `@MCL001/AGENDA.md` with `@MCL001/agenda/`, `@KIM001/AGENDA.md`, `@KIM003/AGENDA.md`.
