# Backbone Plan

Read this when organizing a ticket's phases and materials or maintaining its plan in `INDEX.md`. The plan shows the whole path; phase folders hold the work's details without turning the entry file into a report.

## What the plan is for

The plan is the one place that always shows the whole path of the work: what is done, what is in progress, what remains. The reader opens `INDEX.md` and sees the picture without reading anything else. Detail lives elsewhere; the plan only points to it.

## Shape

- **Sections, not a table.** Phases are headings; steps inside a phase are headings one level deeper. A table was rejected: it compresses names and hides the hierarchy.
- **Phases and steps, numbered as `Phase 1`, `Step 1.2`.** Deeper levels are allowed when the work needs them, but each level is a heading, never a bullet list of paragraphs.
- **Self-explanatory names, with no saving on words.** A step name says what is done and to what: «Move the fix onto the current main branch», not «Rebase». A reader who knows nothing of the work must understand the step from the heading alone.
- **One line under a phase** saying why the phase exists. **One line under a step** with its state, and, when relevant, the skill the step runs under and the agenda slug of the conversation it waits for.

## What stays out

The plan is a backbone, not a detail document: no detailed task lists, candidate lists, findings or reports inside a step. Link these materials in the corresponding phase folder. Questions for Andrei live in the root `AGENDA.md`; the plan names their topics and slugs rather than duplicating the discussion.

## Phase folders

Give each phase an ordered folder with a meaningful name, for example `01-analysis_design` and `02-implementation`. Add subsequent phases as the work develops; do not construct a full empty directory tree in advance. A phase is an intentional stage with its own purpose and results, not a ticket or a particular roll.

A phase can hold one or several MessageRolls and the artifacts it needs: analysis, designs, assignments, review files or other results. Their names and grouping follow the actual work. No per-phase INDEX or fixed artifact list is required. Keep product source in its repository; the ticket holds coordination and supporting materials, not a competing product tree.

The ticket's INDEX links phases and shows their state; AGENDA and `thesaurus.md` remain shared at the root. Number phase folders consistently with the plan. If the plan changes, keep navigation coherent and preserve references; do not move active rolls while writers or watchers use them. Existing historical materials need not be relocated merely to demonstrate the new convention.

## Keeping it current

The state line of a step changes in the same turn in which the state changed in fact. Sections «What is done», «What is next» and «Open questions» do not exist beside the plan: done and next are the states of steps, open questions are the agenda. Steps may be added, removed, renamed or reordered as understanding grows; detailing them in place is the violation.

## Example

```
## Backbone Plan

### Phase 4. Bring the fix up to the current code

The main branch moved 358 commits ahead, so the fix must be moved, amended and re-verified.

#### Step 4.1. Settle with Andrei the two open questions about the code itself

State: waiting for the conversation. Agenda: `it_Code`.

#### Step 4.2. Move the fix onto the current main branch

State: not started. Skill: `kimi-vscode-dev`.
```

Existing tickets may retain older detail files. Preserve their useful content and links while organizing new phase work under its own folder; a migration is a deliberate action of the owning Curator, not an automatic side effect of reading this reference.
