# Notepad management

Read this before you read or edit my notepad, the `notepad.md` file in a work folder, because the first rule below limits what of it you may read at all. The notepad is my personal file, and one section of it, the dashboard, is yours to keep. I run many works at once and switch between them, and getting back into one costs me effort. The dashboard is where I start: a mind map of the work, from which I decide what to do now. From it I see in seconds what the work is for, where it stands, what waits on me and who acts next, and it points me to the file to open rather than retelling it: that is why it shows the top three blockers, not all of them, and leaves each blocker's recommendation in its file. It is the first place I read, while the chat is where I write to you and is not built for reading, so it is built for a live person to read.

## Your part and mine

**The dashboard is the section headed `## DASHBOARD`, from that heading to the next H2 heading or separator comment.** It is the only part of the notepad you read or change. Everything else in the file is mine: my own notes, written for me. Do not read them, answer them, edit them or move them, and do not treat them as instructions or as evidence of what I want. What I want you to know I say in the chat. My notes are not part of our exchange, and reading them would turn a private file into an input I never gave you.

**I add the dashboard; you keep it.** When a notepad has no dashboard section, do not create one, and leave the file alone. When I add an empty one and ask you to fill it, fill it as "The skeleton" below shows.

**Read only the dashboard, whenever you look at the notepad and again right before every edit, and change it with targeted edits.** Find the dashboard's heading, read the range up to its end, and edit inside that range; never write the whole file anew. I edit the notepad at any moment, so a version you read earlier in the turn may already be stale, and a full rewrite from it erases what I added since. Reading only the dashboard also keeps my notes out of your context.

## The layout is mine

The dashboard's layout is set by me and changes when I change it: its parts, their order, headings and capitalization, the blank lines and separators, the set of marks, and fixed lines such as the blocker count. Preserve the layout; update the entries within it as the work changes. Adding a topic's subsection, moving it between the active and inactive groups, and changing its mark, status, agents and counts is keeping the dashboard, not reshaping it. What you do not change is the layout itself: you do not add, merge or rename groups, move a topic's blockers out of its subsection, or rearrange a line I placed inside a topic's subsection, which belongs to my design there, not to a draft for you to tidy. When the layout cannot show something the work needs to show, propose a change as a blocker, as `references/blockers-management.md` describes, instead of reshaping the dashboard yourself.

Take the layout from the dashboard in front of you, not from this reference: a copy here would drift from it as soon as I change it. The skeleton below is a reference for filling a dashboard I have added, not a layout to impose: where my dashboard differs from it, mine wins. What follows the skeleton is what each part of my layout does, so that you fill it with understanding rather than by pattern.

## The skeleton

Write the headings in the words my notepads already use, in the dashboard's language, and call a topic by my word for it in that language, the same word throughout.

```
## DASHBOARD

### PURPOSE OF THE TICKET

<why the ticket exists: the outcome it serves and for whom, in one or two sentences>

Expected results:

- <result>


### PROGRESS OF THE WORK

- <the topics that serve the ticket's purpose>:
  - <mark> `<NN_slug>` — <the topic's purpose, compressed>.
    - Status: <where it stands and who acts next>.
- <side topics>:
  - <mark> `<NN_slug>` — <purpose, compressed>.
    - Status: <…>.


### ACTIVE TOPICS

#### <mark> <slug> — <plain name>

* **<Role>** (<model>), window `<window>`
  * Status: <what it works on, or what it waits for and from whom>.

Total blockers: <n>. Top 3, the rest in `<NN_slug>/blockers/`:

1. `<slug>` — <the question its file's title asks>
2. …

Being prepared: `<slug>` — <what it is about>.


### INACTIVE TOPICS

#### <mark> <slug> — <plain name>

<agents, or a line saying there are none>

Total blockers: <n>, in `<NN_slug>/blockers/`:

1. `<slug>` — <the question>


### OTHER BLOCKERS

<only what belongs to no topic>
```

## What each part does

### The purpose of the ticket

Why the ticket exists and its expected results, in one or two sentences and a short list. It returns me to the goal after time away, so it is written from the ticket's `INDEX.md` and changes only when the goal does.

Its first sentence is the ticket's purpose: why the ticket exists, the outcome it serves and for whom — not what is done, by what means or where the files are. To test one, swap out the agents, the topics and the method: if the sentence is still true, it is a purpose. Write each expected result as described under "Expected outcome" in `references/topic-management.md`; when the results are of several types, group them by type.

### The progress of the work

Every topic of the ticket, the topics that serve the ticket's purpose apart from the side ones. It is the overview: one glance shows what exists, what each topic is for and which topics need me. Each topic takes two lines. The first is its mark, its folder name and its purpose compressed to a few words, taken from its map. The second is a sub-item, "Status:", one sentence on where the work stands and who acts next, taken from the status in its map; for a topic marked ❗ it names the blocker that waits on me by its slug. Neither line carries a path, and each fits the editor's width without wrapping, so that the slugs stay aligned in a column.

### Active and inactive topics

Two sections with the same layout, one subsection per topic however many rolls it has. A topic goes into a group by the state of its work, not by its mark: it is active while its work is under way or cannot go on until I act, even with no agents yet, and inactive when its work has not started, is done or has moved; a moved topic says where its blockers are now kept. A question to me does not move a finished topic back into the active group: the question shows in the topic's own subsection, and the topic's line in the progress of the work carries ❗. An active topic's mark is also in its heading; an inactive topic's heading keeps its own mark.

### Agents

A topic's subsection lists all its agents, a blank line between them for breathing room.

- **The role** in bold, named by the work the agent does — developer, reviewer, designer — in a word I recognize, not taken from the agent's name in its roll. Do not label an agent "author"; use the role that names its actual work.
- **The model** in parentheses, then the agent's tmux window under its current name, as the helper's `window` command in `references/message-roll-operations.md` finds it, or "no window" when no live window carries its tag.
- **The status** as a sub-item, saying what the agent works on, or what it waits for and from whom, so that I see who acts next. An agent with no assignment left reads "finished, no assignments", not a bare "waiting"; when it still holds a window, the status adds that the window can be closed. That is a status line, never a blocker: I decide when windows close.
- **A consultant outside tmux**, such as a model I talk to in a browser chat, is listed the same way, with "no window, browser chat" in place of the window, and a status saying whether it has an assignment and, if so, what to send it and what to bring back.

A topic without agents says so and, when one is needed, who must be created: role, model, why and when.

### Blockers

After the agents comes the count of all the topic's open blockers, naming the topic's blocker folder once, and then the top three, numbered. A blocker is shown as a numbered question to me only when it is ready for my answer: its slug and the question its file's title asks, shortened if needed. No blocker line repeats a path, because the slug is unique within the work folder and leads to the file, and none carries your recommendation, which waits in the file next to what each answer changes. A blocker the agents are still preparing, or one on pause, is never a numbered item, because a number reads as "waits on you": it goes on its own unnumbered line after the top, as in "Being prepared: `<slug>` — …". The count still includes it.

### Other blockers

Only what belongs to no topic, such as the blockers of the ticket as a whole, with a top for each kind. A finished topic shows its blockers in its own section, so they do not repeat here, and a kind with nothing in it is not written: each thing has one place.

### Marks and raw Markdown

**Marks.** 🔴 under way, ❗ waiting for my decision or action, ⏳ later, ✅ done, ➡️ moved. Only 🔴 and ❗ draw attention, and they are of one color family; the rest stay calm, so that my eye goes only where something is happening or waits on me. The mark follows whether the work is blocked: a topic whose agents are working and are not blocked waiting on me gets 🔴, even with open blockers; ❗ means the work stands waiting on me. The dashboard has no legend line: it is visual noise and costs more than it explains. ❗ goes on topics, in the progress list and in the headings of active topics, never on blocker lines: every blocker in a top three already waits on me, so a ❗ there tells nothing apart.

**Raw Markdown.** I read the file raw, so the layout is built for that: lists rather than tables, which grow too wide to read; slugs aligned in columns; blank lines and separators that set the parts apart; a line that wraps in the editor breaks the column, so keep paths out of topic lines.

## Where the content comes from

The dashboard shows the state of the work; it keeps no state of its own. Everything that waits on me is a blocker file in a `blockers/` folder, and the dashboard only displays those folders. A topic's lines and mark come from the purpose and status in its map (see `references/topic-management.md`), the agents from the rolls and the live tmux windows, the blockers from the folders. When no reliable source says what the state is, the line says it is unknown rather than guessing.

## Quality

**Your main job here is to lower my cognitive load.** Every line is checked by what I get from it without effort: what needs doing and where to read more are visible at once, with no filler. A ❗ line says what exactly waits on me and names the blocker by its slug, so that I can open it; a line that only says "waits on you" sends me to dig.

**Never regenerate the dashboard; touch a line only for a reason.** A line is touched when the state it shows has changed, or when the rereading below finds it failing, and then only as far as that reason needs; every other line keeps its wording, whoever wrote it, because regenerating rewrites wording I may have chosen. The layout itself is never touched.

**Keep what a line names.** Before you rewrite a phrase, establish what it names and which relations, counts and caveats it states, and keep them. Do not replace a precise term with a more familiar one, such as the ticket's own jargon, for habit or uniformity: two terms that look alike may name different things.

## When it is updated

At the end of every turn, in the closing steps of the turn plan that `SKILL.md` describes: first apply this reference to the dashboard by its purpose, which covers what the turn changed but is not limited to it, touching a line only for a reason as above; then reread it whole, as a live person will read it, and fix whatever fails. The rereading checks that the dashboard is intact, coherent and readable: each count matches the live `blockers/` folder it counts — a moved topic's blockers counted where they now live, not in the frozen copy — and every blocker shown belongs to that count, with the folder named so that I can reach the rest; nothing unready is shown as a question to me; no line contradicts another, every topic and blocker is named with what it is about, and every ❗ says what to do and where to read.

Check that the dashboard alone answers three questions: what the ticket is for, what waits on me and where it lies, and who acts next in each active topic.

## Older notepads

A notepad in an older layout, with a section per topic, is left as it is. You do not maintain those sections and you do not migrate them; the dashboard is your only part of a notepad, and only where I have added one.
