# Notepad management

Read this before you create or edit my notepad, the `notepad.md` file in a work folder. The notepad is my personal file: it is neither the work map nor a report. I return to it from other work to remember what this work is about and to decide where my attention should go next. Every rule below follows from that use. The notepad must let me get back into the work within seconds and choose what to read, and it must keep my own thinking separate from what agents write.

`INDEX.md` remains the map an agent uses to pick up the work cold. The notepad is for me, so it holds only what I use.

## Structure

```markdown
# <TICKET> · <short name> · Notepad

## T1_<Mnemo> — <Topic>

### User notes

<my text>

### Purpose and status

**Purpose:** <why this topic exists: the outcome it serves and for whom, in one sentence>

**Status:** <where it stands now, in one or two sentences>

**References:**
- <only what is critical beyond the rolls, such as the artifact awaiting my decision>

### Agents in tmux

Roll `<alpha path of the roll>` — <what the roll is for, in a few words>:

- `<window>` — <client, model, effort>, <role> — <working on … | idle>

### Q1_1_<Mnemo> — <A question for me, phrased as a question?>

<only what I need in order to decide>
```

**Each topic gets its own H2.** A topic is a distinct thread of the work, and it usually has its own roll with its own set of agents. Topics are what I switch between, so they form the top level.

**`User notes` comes first in every topic, and it belongs to me.** I write whatever I find useful there. Read it, since it is often the best evidence of what I care about, but never change it: do not fix my typos, reorder my lines or add answers or "done" marks under my items. Answer my notes in the chat. When agents write under my lines, I can no longer tell my thinking from theirs, and separating them later takes forensic work.

**`Purpose and status` comes second, is always there and stays current.** These are the two fields I reread most often: when I come back from other work, they tell me what the topic is and where it stands. Write one sentence for each, two at most for the status, in plain words, with no hashes, no message IDs and no account of how the status came about. Update the status in the same turn in which it changes. Never remove these fields during a cleanup just because an agent wrote them: what matters is that I use them, not who wrote them.

**Purpose follows the standard form of a purpose statement.** It answers "why": the outcome the topic serves and for whom. It does not say what is being done, by what means or where the files are. "Bring the docs to American English" describes an activity, and "Roll `…/check_lang.md`" describes a location, while "Maintainers read the fix as natural American English and judge the contribution on its merits, not its language" is a purpose. To test a purpose, swap out the agents, the roll and the method: if the sentence is still true, it is a purpose.

**References come after the status and list only what is critical**, such as an artifact awaiting my decision or a key index file. A roll belongs in `Agents in tmux`, as the heading over its agents, because the roll is their conversation. That is where I look for it, and giving each reference one place keeps the notepad short. When nothing else is critical, leave the block out rather than writing an empty one.

**You choose any further H3s** based on what I need to know right now: the agents of the topic, a question for me, a risk I should see. Remove an H3 once it no longer needs me, for example after I have answered its question.

## One H3 is one unit of attention

An H3 is what I can take in at one sitting: within seconds I read it and decide whether to look closer and work on it. The heading itself must therefore say what the section is about, such as "Do you agree with the PR title?" rather than "Question 3", and the body holds only what that decision needs. Never group several items under one H3, because a list of seven questions hides six of them. Twelve questions for me mean twelve H3 sections, which I will read when I choose to.

## Slugs

I refer to topics and questions in the chat, and copying a whole heading is clumsy. Each topic and each question therefore starts its heading with a slug I can copy with a double-click: `## T3_PR — PR quality`, `### Q3_1_Comment — Accept the new comment text?`. A topic slug is `T<n>_<Mnemo>`. A question slug is `Q<topic n>_<n>_<Mnemo>`, numbered within its topic. A slug is at most 12 characters long and uses only letters, digits and underscores, because a hyphen or a space breaks double-click selection. The mnemonic is a short memory hook, not the meaning; the heading after the dash carries the meaning. The other H3s (`User notes`, `Purpose and status` and `Agents in tmux`) need no slug.

A slug is an address, so it must stay stable. When a question is answered and removed, its number is never reused and the remaining questions keep their numbers; the next question takes the next free number. Because a removed number no longer appears in the notepad, keep the next free number for each topic in the work's `INDEX.md`, in a short notepad line or section, and update it whenever you add a question. In the chat, give the slug together with its topic in words, for example "`Q3_3_Title` — the PR title", because I may be reading the chat without the notepad open.

## Only what is worth my time

The results, reviews and reasoning of executors live in their rolls and review boards, and answers to my notes live in the chat. The notepad does not repeat them. When a question needs evidence, give the one fact or text I must see, such as the proposed wording of a comment, and a path to the rest. A notepad that shows off diligence instead of serving me is one I stop reading.

## Agents in tmux

Each topic lists the agents actually running for it, grouped under the roll they talk in: first the roll's alpha path with a few words on its purpose, then for each agent its tmux window, client, model and effort, role and whether it is working or idle. Take this from `tmux` at the time of writing, not from the roll's participant list or an earlier map: a recorded participant may be gone, and a pane may be running something else. An agent that has finished but still holds a window is shown as finished, along with a question about whether to close it. This is a live snapshot for me, not a roster: participant identities stay in the roll's frontmatter.

## Starting and migrating

Two defaults apply until I decide otherwise. The Curator opens a new H2 when a new topic starts, usually together with its roll, and leaves an empty `User notes` for me. A topic whose work is done stays in the notepad, with its status saying so, until I remove it or ask you to, because my notes live there.

When a notepad predates this structure, move my lines verbatim into the `User notes` of the topics they belong to. Do this once; it is the only time my text is moved. Decide which lines are mine from evidence, not from style: a line is mine when no agent's edit to the file ever produced it, and session transcripts record every agent edit. Text I pasted from an agent's reply in the chat is not my own writing; tell me what you removed and where it can be recovered.
