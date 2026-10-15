# Thesaurus Writing

Read this before creating a ticket's `thesaurus.md` and before editing one: a change to one basic entry reaches every entry that stands on it, and the depth of the check below is chosen by what the change means, not by how many entries it touches. The file holds the structure of an entry, the procedure that produces a thesaurus a reader can rely on, the reviews built into that procedure, a sample entry, and the ways a thesaurus has already gone wrong. SKILL.md says who owns the thesaurus and what it is for; this file says how to build one that works.

Contents: what the result must do · kinds of statements · the entry · a sample entry · the procedure (seven steps) · rubric for the reviewer · how thesauri have gone wrong.

## What the result must do

A thesaurus is the shared vocabulary of a ticket: the user, the Curator, the engineer and the reviewers say the same word and mean the same thing, and assignments, review boards and the PR are written in it. It is read like a dictionary, not like a document: the reader comes for one term, finds it through the file outline, reads its entry and follows its links to other entries. Andrei (2026-10-14): «читатель тезауруса приходит в файл за конкретными терминами и смотрит их через оглавление файла (outline), он прыгает по терминам, которые его интересуют, как в словаре, и читает связи».

The thesaurus has done its job when four things hold:

- the user reads an entry once and does not have to ask what a word in it means, whether two terms are the same thing, or where a claim comes from;
- the engineer can take an assignment written in these terms and know what each one refers to: for a mechanism or a designation, the file and symbol that implement it, and those exist; for an agreement, the decision it rests on;
- a cold reviewer can explain every term back from its entry and the entries it names as prerequisites, and the second pass of the review, which checks the sources, finds that the entry is also true;
- the user has said that the thesaurus is accepted; silence is not acceptance.

The opposite is a file written «для галочки»: it exists, it is linked from INDEX, and the user re-reads it fifteen times and still asks. The KIM001 thesaurus went through exactly that before these rules were written. Andrei: «Надо стараться ради читателя, а не ради того, чтобы закрыть файл для галочки».

## Kinds of statements

A thesaurus mixes statements of different standing, and a reader must see which is which. Before writing an entry, decide what kind of thing the term names and what kind of claims the entry makes:

- **A mechanism** — something the system does: a process, a rule computed by code, a transformation. Its essence explains how it works, and its facts come from the implementation or the official documentation, with a status.
- **A designation** — a name for a part of the world the ticket points at: the first folder of a workspace, the set of folders after it, a configuration file. Its essence says what exactly is designated and what depends on it; «how it works» is not the question.
- **An agreement or a decision** — a meaning the user gave a word, a convention of the ticket, a decided form of a fix. Its essence states the agreed meaning and links the decision; the current code may not implement it yet, and the entry says so.
- **A requirement or a proposal** — something wanted but not decided. It enters the thesaurus only as a term with the status «proposed», never as a fact.

The same distinction governs every claim inside an entry. A claim is marked by where it comes from, in one short form used throughout the file, right after the claim:

- *(исходник: `path`, symbol)* — read in the implementation in this session; the path and the symbol were copied from the open file, not typed from memory; a symbol, not a line number, because line numbers die with the next commit;
- *(документация: page)* — read in the official documentation;
- *(измерено: how)* — observed live, with the command or log line that showed it;
- *(со слов: who)* — asserted by a reviewer, a report or an earlier agent and not yet checked;
- *(выведено: из чего)* — read in a source and applied to a situation the source does not state directly, such as a transformation table read for one side and applied to the other; the entry names the measurement that would confirm it;
- *(не проверено)* — believed, not checked; the entry says what would check it;
- *(решение: where)* — decided by the user; the current implementation may differ.

Why one form: a reader distinguishes measured from derived at a glance, a reviewer knows what to check, and a status is not repeated as a paragraph in three entries. A claim without a status reads as a fact, and a thesaurus that mixes the kinds is one a reviewer cannot trust.

## The entry

Every term is an H3 heading with a unique canonical name in PascalCase, qualified enough to separate it from its neighbours (`KimiWorkingDirectory`, not `WorkingDirectory`, when VS Code and Kimi both have one). The name is a handle for the outline and for references; it does not assert a code symbol of the same name. Under the heading, in this order:

- **Сущность** — what kind of thing it is, what sets it apart, and, for a mechanism, how it works: what runs where and why. This is a definition by genus and difference, extended for mechanisms to the way they are built. Andrei's rule (2026-10-14): «понятие не введено, если определение не оставляет понимания, как это работает». A sentence that names a recognisable feature («окно, подключённое к удалённому хосту») or the user's steps («установить расширение и подключиться») has not introduced a mechanism; such things go to the operational part. For a designation or an agreement, the essence says what is designated or agreed and what depends on it.
- **Ловушка** — present when a word in the name or next to it reads differently from how the thing is built: `host` in «extension host» is not the remote host; `workspace` in `extensionKind` is a side, not a set of folders; `remote` in «Remote Repositories» is not a remote window. Say what the word suggests, what it actually denotes here, and how to read it. A warning lives in the entry of the term it concerns, because that is where the reader is when it must fire; a separate section that collects all warnings is not read. Andrei: «ты повыносил слова-ловушки в отдельную статью, но так её никто не будет читать».
- **Пограничный случай** — present when the user, a reviewer or the author found a case where the definition's «all», «only», «first» or «always» could be misread: a workspace with all folders virtual except one that is not the first; a workspace file whose own address is remote. The user's «т.е. …?» in conversation is the usual source; record the answer here, not only in the chat. The part is omitted when there is no such boundary: an ordinary fact or a rule of procedure put into this slot to fill it teaches the reader that the slot means nothing.
- **Операционально** — how to find or verify the thing in practice: the API field, the function that computes it, the file it lives in, the command that shows it, the log line that proves it. Every path and symbol is copied from a file opened in this session; a name typed from memory is the main source of the carelessness a reader then takes for fact. An unknown operational rule is marked unresolved, never invented from the name.
- **Употребление** — the short forms allowed and where, the terms it must not be confused with (as their canonical names), and any convention the ticket has settled, such as «always say „папки воркспейса" or „папки чата", never bare „дополнительные папки"».

**How much mechanism belongs in an entry.** Enough for the reader to tell the term from its neighbours and use it correctly: what runs where, what the term depends on, what depends on it. The choice between design variants and the reasons for it belong to the analysis and design artifacts; the thesaurus keeps the name of the chosen variant with a link to the decision. A user guide (which menu, which command) belongs to the operational part at most, and only when the user needs it to recognise the thing.

**Self-sufficiency and splitting.** An entry is self-sufficient when a reader who jumped to it from the outline can use the term after reading it and the entries it names as prerequisites. Prerequisites are named explicitly, as canonical names in parentheses at the first mention in each entry — «работает extension host (ExtensionHost)» — so the reader can tell a defined term from an ordinary word and jump to it; a canonical name is the link, and it must exist as an H3. This holds for the terms the file uses most, not only for the rare ones: a foundation term such as «координатор» or «движок» that appears in every entry gets its name at its first mention in every entry, or is declared once in the head's list of one-meaning words with the entry that defines it; an author who silently treats a frequent term as an ordinary word leaves the reader without the jump exactly where it is needed most. When a part of an entry gets a name of its own, is referred to from another entry, or the entry grows past a screen, that part is a term: give it its own H3, because an outline does not show bold subheadings and the reader cannot find the answer there.

**Two rules of form.** An enumeration — cases, values, kinds, sources, steps — is a list with one full sentence per item, never a paragraph with cases behind semicolons: the reader is looking for one case and must find it without parsing the others (Andrei: «тут надо было сделать список, а не сжимать в один абзац; это общее правило написания тезаурусов»). And words that have one fixed meaning in the file («хост», «сервер», «чат») are listed once in the head of the file, so that entries can use them without redefining.

**The head of the file** is for the reader, not for the author: two or three lines on why to read it and how it is read, what the file does not cover, the legend of the status marks the reader will meet, then the list of one-meaning words. The rules of writing live in this reference, not in every thesaurus; a dated rule with its author's name in the head is the file telling its own story, which SKILL.md forbids for files made for the user. Terms are grouped in sections by domain, foundations first.

## A sample entry

A short entry of the designation kind, with a prerequisite, a trap, a status and a usage convention; a mechanism entry adds «how it works» to the essence and a source to each operational claim.

```markdown
### TicketWorkFolder

**Сущность.** Папка одной работы — проекта, программы или рутины — внутри папки бизнеса.
Её имя — номер тикета и короткое название (`DUE007_Name`); от того, на какой полке она
лежит — `work/`, `backlog/` или `archive/`, — зависит состояние работы: в работе, ждёт,
закрыта. Адрес `@DUE007` (AlphaPath) указывает на неё, где бы она ни лежала.

**Ловушка.** Слово «папка» здесь — папка работы, не папка бизнеса и не папка репозитория:
у бизнеса есть `INDEX.md` с `folder-type: business`, у работы — с `folder-type: work`.

**Операционально.** Создаётся только инструментом `new_ticket`, переносится между полками
только `move_ticket` *(документация: duet-core, раздел «Tickets are managed through Duet»)*.
Внутри — `INDEX.md` с целью и планом и, при необходимости, `AGENDA.md` и `thesaurus.md`.

**Употребление.** «папка работы», «тикет» в значении папки; в задании — alpha-адрес.
```

## The procedure

Each step produces something the next step checks. Skipping a review step is how a thesaurus becomes a file nobody can use. The depth of a pass depends on the change: a typo needs a local check; a new meaning, a changed boundary or a corrected source needs the dependent entries re-read and the regression questions re-run; a new thesaurus needs all seven steps.

### 1. Harvest the words

Collect candidate terms from three sources, in this order of authority:

1. The user's own words, verbatim, with the meaning the user gave them; his terms keep his senses and are never silently replaced by a dictionary or a code name.
2. Identifiers in the code and the official documentation of the system under work: field names, function names, settings, scheme names.
3. Words used by reviewers, earlier agents and prior tickets — as candidates only, because their classifications and arguments may rest on an example rather than on the mechanism.

At the same time collect the trap words. The principle: every ordinary word that appears in the ticket's materials with more than one meaning. Search the materials for each candidate and read the hits; the words that turned out ambiguous in one software ticket were host, local, remote, workspace, project, session, server, agent, additional, and any product name that reads like a category, but the list is an example, not the principle. The output of this step is a list of terms with their kind (mechanism, designation, agreement, proposal), a list of trap words, and the list of one-meaning words for the file head, each with where it was found.

### 2. Establish each mechanism from primary sources

For every mechanism, find the code or official text that implements or defines it, open it in this session, read the function that computes it to the end, and copy the path and the symbol from the open file. For every designation, find where it is produced (the API field, the file); for every agreement, find the decision and link it. The source decides the classification: classify things by the mechanism behind them — who answers for an address, which process runs where — never by the examples that happen to appear in a test or a review board. A single example (`vscode-vfs:`) must not become the name of a class («виртуальные схемы»); the class is named by what makes its members alike, and the example is marked as an example.

Three checks belong to this step:

- **Does the source prove this claim?** A function that checks schemes proves a claim about schemes, not a claim about where files are stored; a file service that compares paths proves what that service does, not the whole access policy of every tool. Note the version or the commit the source was read at when it matters.
- **For «always», «only», «never», «if and only if» — look for the counterexample** before writing the word: a network share, a read-only provider, a second configuration, an older engine. If one exists, the claim gets a boundary case or a weaker verb.
- **Measure when measuring is cheap.** If a claim can be checked in minutes — one log line, one command — check it and write *(измерено)*; «derived from source» is for what cannot be measured now, and then the entry names what will measure it later. Five «не проверено» in a file read as an unfinished file.

Mark every claim with its status in the form above, and mark what is current base, inherited change, decided requirement or default configuration when the ticket has several of these at once. Consequences are derived from the defined concept, not from the author's current environment: the question «what would Duet do in a remote window» is answered from what a remote window is, not from where the author's folders happen to be today.

Check every word used in a definition: it is either ordinary, or in the one-meaning list, or itself an entry. A word of a neighbouring domain that the thesaurus does not cover — «повестка», «фаза», «доска ревью» in a thesaurus about rolls — is the usual third case: declare it in the head's list with a pointer to where it is defined, and from then on it counts as ordinary; a word declared nowhere and used in a definition is a defect. The technique that finds these words: go through the definitions and write out every noun the intended reader does not know from ordinary life; each one is then an entry, a declared neighbour, or a replacement by a plain word. If a definition of `FolderUriScheme` needs «authority», then `UriAuthority` is an entry, written before the one that uses it; if an argument rests on a field like `extensionKind`, the field is an entry before the argument is made.

### 3. Write the entries

Write every entry in the structure above, foundations first, with the status marks in place. Write the head of the file last, when the one-meaning words are known from the entries. Keep the thesaurus about language: how the system is designed and why belongs to analysis and design artifacts, which refer to these terms.

### 4. Review it yourself as a cold reader

After writing, and after every later series of edits, read the whole file from the top as someone who knows none of its facts. This is a separate pass, not something done while editing: entries written one per question, each correct in itself, produce a file whose words contradict each other and whose traps are unmarked. Check:

- Every word in every definition is ordinary, in the one-meaning list, or an entry.
- No example stands as the name of a class; every «и подобные» is replaced by the class and its mechanism.
- Every enumeration is a list; every list item is a sentence. A cold eye misses these, so search mechanically: a semicolon inside a paragraph, «для X — …; для Y — …», and «A, B и C» after a colon are enumerations hiding in prose.
- Every term mentioned in another entry carries its canonical name at first mention and that entry exists as an H3. Check in both directions: that every name in parentheses has its H3, and, for every H3, that its plain word and the short forms from its Употребление are found in every other entry with the name at the first mention; the second direction is the one authors skip.
- Each word that has two meanings anywhere in the file has its trap recorded in the entry where the reader meets it.
- Each claim has its status; derived claims are not written as measured ones; every path and symbol was copied from an open file.
- Each entry is self-sufficient for a reader who jumped straight to it from the outline, and no entry hides a named part that should be its own term.
- The same word means the same thing in every entry.

Then run the regression questions of step 5 if any exist from an earlier round: read each question and answer it from the text alone. Fix by rewriting the entry, not by appending a clarifying sentence: a thesaurus grown by patches reads as patches. A change to a basic entry is followed by re-reading the entries that name it.

### 5. Review by the user, through questions

Hand the file to the user and treat every question about a term inside the promised scope as a defect report on an entry, not as a question to answer in chat. «Что такое authority?» means the entry that used the word did not define it. «Разве это не одно и то же?» means two entries name neighbouring things without saying what makes them alike and what separates them. «Где написано, может ли Kimi читать?» means the entry promised a rule and did not state it. «Т.е. если …?» is a boundary case to record. Answer the question in the chat and fix the entry in the same turn; then re-read the entry and ask whether it would have answered the question on its own.

A question outside the promised scope — about a neighbouring system, about a design choice the thesaurus only names — is first judged: if the term belongs in the thesaurus, it is harvested; if not, the answer stays in the chat and the scope line in the head says what the file does not cover.

Keep the user's questions, verbatim, as a test list in a file for agents, never in the user's thesaurus: `thesaurus-questions.md` in the ticket root, linked from INDEX; a review phase that uses the list links to it rather than keeping a copy. They are the regression tests for every later revision, because the next reader will ask the same things; before step 6 the author runs them once more against the text.

### 6. Independent review

Give the thesaurus to a reviewer who has not seen the conversation — another model, or a session with a cold context — with the question list from step 5 and the rubric below. The review has two passes, because explaining a mechanism back and checking that it is true are different work:

1. **Cold reading.** The reviewer reads the file alone, without the sources, and records for each entry whether it can explain the mechanism back, which words it found undefined, which classification rests on an example, which question from the list the text does not answer.
2. **Verification against sources.** The reviewer opens every path and symbol the file names and reports each one that does not exist or is named wrong; checks for each sourced claim whether that source proves that claim, at which version and under which conditions; and for every absolute claim looks for a counterexample. A claim without a status is reported as such.

The reviewer reports on a review board in the conventions of the business, in the form the rubric prescribes. Fix what the review found, re-read the file as in step 4, and send the changed entries and the entries that depend on them back for a second pass. The ticket's review bar decides how many reviewers and which models; the subject skill, if any, decides where the board lives.

### 7. Accept, use, maintain

The thesaurus is accepted when the substantive findings are closed, the regression questions are answered from the text, and the user has said so; the user's silence, fatigue or a postponed reading are not acceptance. From then on, assignments, review boards and the PR use its terms, and the Curator maintains it: a term that emerges in a conversation gets an entry when it is settled; a real disagreement is marked «disputed» with a link to the open agenda item rather than settled by editing; a correction from the user is applied by rewriting the entry, re-reading the entries that depend on it and re-running the questions. A thesaurus that is maintained by appending sentences at the point of each question returns to the state this procedure exists to prevent.

## Rubric for the reviewer

For each entry, answer the seven questions; write one line per entry when all seven pass, and for a failed question write the finding in full — place, evidence, proposal — because a table of a hundred answers is not read, and a reviewer who answers selectively and calls it a pass has not reviewed:

1. For a mechanism: from the Сущность alone, can you explain how the thing works — what runs where and why? If you can only recognise it, the concept is not introduced. For a designation or an agreement: is it stated what exactly is designated or agreed and what depends on it?
2. Is every word in the definition ordinary, in the one-meaning list, or defined in this file?
3. Is anything named by an example where a class is meant, or by a class where one product is meant?
4. Does every claim carry its status, and does the named source prove this claim? Did you open every named file and find every named symbol? A missing one is a finding.
5. Does the entry warn about the misleading word you stumbled on, in this entry and not somewhere else?
6. Can you construct a boundary case or a counterexample that the entry's «all», «only», «first» or «always» does not settle?
7. For a mechanism or a designation: could an engineer take an assignment written with this term and find the thing in the code? For an agreement or a decision: is the decision linked, and is it visible whether the current implementation follows it?

For the file as a whole: does any word mean two things in two entries; does the head name the one-meaning words you needed; can you reach foundations from any entry by following canonical names; does every question from the regression list get its answer from the text.

## How thesauri have gone wrong

Each failure below happened in a real session; each is caught by a step above. Read them to recognise the pattern, not to memorise the case.

- **Written from the facts, not from the reader.** Entries composed one per question, each true, with no pass over the whole; the user re-read the file many times and kept asking. Caught by step 4.
- **A classification borrowed from an example.** A test used `vscode-vfs:` as a sample virtual folder; the thesaurus turned it into the name of all virtual file systems, and the user built a wrong model on it. Caught by step 2: classify by mechanism, mark examples as examples.
- **A source that proves a different claim.** A function that classifies folders by scheme was cited as proof that virtual folders have no disk anywhere; a file service that compares paths was cited as the whole access boundary of the agent; an internal computed kind of extension host was cited as a third value of the manifest field. All sources were real and all claims were wrong. Caught by step 2's first check and by the verification pass of step 6.
- **A correction that broke a neighbour.** Fixing four wrong code references in one pass dropped a true condition («неархивных») from a neighbouring sentence and pointed another claim at a file that does something else. Caught by re-reading the dependent entries after a change and by the second pass of the review.
- **Paths and symbols from memory.** Four entries named a function, a file and an environment variable that did not exist under those names; each read as a verified fact. Caught by the copy-from-open-file rule of step 2 and rubric question 4.
- **An argument carried over with its form.** A reviewer's correct argument rested on `extensionKind: ["workspace"]`; the thesaurus repeated the argument four times without ever introducing the field. Caught by step 2's word check.
- **Essence written as a symptom.** «A window connected to a remote host» — recognisable, but it does not say what runs where; the user could not tell what would change for his own tool in that window. Caught by rubric question 1.
- **An absolute without a counterexample.** «Two folders with the same scheme and authority lie on the same machine» — a network share is a folder with scheme `file:` on another machine. Caught by step 2's second check and rubric question 6.
- **Warnings collected in one place.** The trap words were gathered into a dedicated section, which the user said nobody would read; moved into the entries. Caught by step 4 and rubric question 5.
- **Cases compressed into a paragraph.** Three schemes and four reading rules in one paragraph; the user asked for lists and named it a general rule of thesaurus writing. Caught by step 4.
- **A consequence derived from the environment.** Asked what a remote window would mean for his tool, the author reasoned from where the folders lay on the current machine instead of from the definition. Caught by step 2.
- **A fact asserted without status.** A claim that folder schemes could be seen in a saved workspace file was written as fact; the source showed the opposite. Caught by the status rule and rubric question 4.
- **A decision read as a description of the code.** The decided form of a fix was written in the operational part as if the code did it; the code in the clone did something else. Caught by the kinds of statements and rubric question 7.
- **Patching instead of rewriting.** Each question added a sentence to the entry it concerned; the entries grew inconsistent. Caught by steps 4 and 7.
- **An entry that swallowed its neighbours.** One entry grew to sixty lines with bold subsections that the outline does not show, so the answer to a user's question could not be found by jumping. Caught by the splitting rule and step 4.
