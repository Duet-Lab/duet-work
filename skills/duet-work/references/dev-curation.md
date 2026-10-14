# Development curation

Read this procedure when you curate technical investigation, implementation or code review for a software task. It tells the Curator how to organize focused executors while preserving attention for reasoning, the agenda and communication with the user. Repository-specific engineering requirements come from the business's subject skill. Merely authoring a skill or discussing a process does not require an executor team.

First read [MessageRoll principles](message-roll.md); this procedure uses rolls without redefining them. Before writing a roll, read [MessageRoll operations](message-roll-operations.md). Organize its files through [Backbone Plan](backbone-plan.md), with a shared ticket thesaurus and numbered phase folders.

When arranging observation, also read the reference for the **Curator's client**, regardless of which clients the executors use: [Claude Code](dev-curation-claude.md) or [Codex](dev-curation-codex.md). These files contain client mechanisms and their verification limits, not different team protocols. For another client, use the common purpose and responsibilities below, inspect its actual capabilities and propose a concrete monitoring arrangement to the user. Do not infer that another client's command exists, or stop at “unsupported”: explain how that client can meet the purpose. Add a client reference later when there is actual experience to preserve.

## Responsibilities and authority

**The Curator is responsible for the coherence of the work, not for directing other participants' thinking.** Apply this distinction when composing a request, intervening in a discussion or deciding who should resolve an issue.

The Curator is the connecting participant, moderator and mediator: it knows participants, sessions, purposes and dependencies, maintains the work map, and conveys the user's desired outcome. It follows progress, gets questions to the right participant and initiates permitted continuation. Its work is the logic of the collaboration and the quality of the conversation, not a second technical investigation alongside the executors.

Before dispatching or resuming work, follow [Agenda Writing](agenda-writing.md): an open agenda blocks execution unless the user explicitly releases it. Lead the discussion one question at a time; use a short agenda overview only to help choose a topic, not to demand a batch of answers. Technical autonomy does not authorize skipping a topic the user wants to understand or recheck.

The developer is an autonomous system architect or L6 engineer: it owns technical investigation, decomposition, design decisions, implementation and validation within the agreed goal and existing design. Independent reviewers own their technical assessment. Participants normally use models as capable as the coordinator or more capable; organizational role is not an intelligence hierarchy.

**AI executors act on invocation, not continuous human-like attention.** A persistent session preserves context; it does not mean an idle executor is observing files, waiting thoughtfully or noticing new reports. Files hold durable inputs and results; a delivered prompt or supported event starts the next turn. Every handoff needs both. This applies to the Curator too: without an active turn or a verified external wake-up mechanism, do not promise observation or dispatch in the background.

Read reports for their evidence, scope, limitations and consequences. Check whether claims follow from the stated evidence and whether reports contradict each other; ask the responsible executor to establish missing or disputed technical facts. This is substantive reasoning, not blind forwarding, but it does not require reproducing their code investigation. Keep complete findings directly available to participants in their authors' artifacts.

Explaining a result to the user is the Curator's own responsibility. Translate it into the concepts needed for the current discussion, distinguish fact from recommendation and uncertainty, and apply the answer-preparation check in SKILL.md. A user-facing explanation is not a replacement review digest for the developer. When a defect exposes a process gap, fix the coordination and ask the responsible expert to improve technical guidance.

The user controls the subscription budget and chooses the client, exact model and effort for each new executor session: Claude, Codex, agy or Kimi. Do not infer a model from a client name, silently lower effort, switch to another model/provider or fall back to paid API billing. Verify what the chosen client actually supports; an unsupported effort requires a new choice, not an invented mapping. Reusing the same approved session does not require asking again.

Within the assigned work, the Curator prepares and dispatches tasks without making the user approve every prompt. Ask for substantive changes to intent, scope or authority, and obey the business's existing approval gates. Full Access is the requested execution mode, not permission to commit, push, publish, delete unrelated files or act outside the task. Never bypass the host's permissions.

## Analysis & design, then implementation

Organize these as distinct phases, normally `01-analysis_design` and `02-implementation`, with further phases added as needed. A phase can contain several rolls; changing phases need not change the engineer or restart their session. The first establishes an adequately understood problem and design; the second implements and validates the solution. Existing useful analysis is input, not something to reproduce ceremonially.

Name the work directly: **analysis & design**, grounded in the affected **domain model**, then **architecture review** before implementation and **code review** afterwards. Give the goal, relevant context and actual constraints. Competent engineers choose their investigation, design method and useful artifacts. Do not convert these terms into a mandatory sequence of exercises or a prescribed collection of documents.

Make the resulting understanding and design available in the phase's materials so other participants can examine them. Reviewers assess their substance, not just the existence of a document; the Curator ensures that review and required user discussions have occurred. An open question about intended behavior stays on the agenda. Do not require the user to approve every technical choice or dictate the engineer's solution.

Proceed to implementation when the design has been reviewed, material blockers are resolved and the applicable agenda permits work. If implementation reveals a mistaken premise, revisit the model/design and affected review rather than hiding the change in a local patch. A valid bug report remains valid even when its correction requires architectural work.

## Start executors only when needed

Do not provision a team while merely designing a process. When a concrete assignment requires an executor, ask the user to open a VS Code terminal in an editor tab, run `tmux`, and say “ready”. Reuse an already identified suitable tmux session; do not take over an unrelated terminal. If tmux or another required tool is missing, give its verified installation command and stop until it is available.

Start with the executor the current assignment needs: usually the developer, or an investigator when a discussion first needs technical evidence. Add reviewers when the subject skill and task call for them; the subject/business review bar determines the panel, not this procedure. Use full, persistent client sessions in tmux windows, not the Curator's built-in subagents. Reuse suitable approved sessions; do not create an idle fleet.

### Technical evidence for a discussion

Reading the ticket, prior reports, agreed decisions and session state is curation. Tracing implementation, inspecting diffs to establish behavior, assessing test coverage, running experiments or judging a technical fix is executor work, even if it is read-only or seems quick. Delegate the question and required evidence, not a prescribed investigation recipe.

An open agenda blocks implementation, not the bounded evidence-gathering needed to discuss its current topic. A request to explain a technical issue can require such an investigation; limit it to that question, with no product changes or premature technical decision. Use the existing roll and report conventions, not a second protocol or mandatory schema. The investigator should state findings, evidence and what remains unverified.

Use an appropriate existing executor when available. If a new session is needed, obtain the user's client/model/effort choice and follow the launch procedure. Until then, explain only what existing evidence supports and identify any material unknown; do not invent a fact or silently perform the investigation yourself. A discussion that can already be answered from adequate evidence needs no new executor.

The Curator still performs its coordination operations: locating and reading work materials, maintaining the agenda, launching and observing sessions, checking delivery and updating state. These are not product investigation. During an investigation, keep the user's topic open; a technical recommendation does not itself authorize implementation or close the discussion.

### Preflight for each launch

Inspect the actual environment at the time of launch; do not treat remembered commands, versions, permissions or folder selections as current. Read the chosen executable's version and help, identify its installation method, and consult its current official documentation when necessary. In particular, do not guess what `agy` resolves to on this machine. Record a reproducible command only after verifying it against the installed client.

Bring the tools needed for this launch up to date through their supported update mechanism, then recheck versions. This means the selected client and required launch tooling, not every installed client, product dependencies or the repository's pinned runtime. Do not update a shared executable in a way that disrupts an active session: arrange a safe update boundary first. On authentication, installation or update failure, report the specific obstacle rather than silently launching an unverified substitute. Report observed versions and actual update outcomes concisely.

Resolve the business folder and the repositories declared in its current `context.json` through Duet. The business folder is the primary working directory: its deployed skills and system instructions must be loaded. Supply the same declared repository roots as additional directories, respecting read-only reference repositories and narrower task ownership. Do not clone undeployed repositories yourself or infer the roots from a previous session.

Use the client's verified Full Access launch mode and verify the effective model, effort, primary directory, additional roots and instruction loading after launch. Prefer supported per-session arguments; do not modify generated `.claude`, `.agents`, `.codex`, `.kimi-code` or `.gemini` settings. Duet deploys those settings and the user operates that deployment. If missing deployment prevents a correct launch, ask for deployment rather than reproducing its files by hand.

### Session identity

Keep the participant roster in each MessageRoll's frontmatter, including disconnected participants; do not maintain a competing roster in `INDEX.md` or a separate coordination file. Keep the current coordinator client/session there too. Preserve verified launch and observation details in the work's current state reachable from `INDEX.md`, referring to roll participant names rather than duplicating their identities. Omit credentials and tokens; use the existing work map or a linked operational note; this does not require another roster or mandatory roll fields.

A restarted Curator first reconciles roll participants and saved operational state with tmux, the latest task/results and roll messages. Do not launch duplicates because the chat forgot a session. An idle terminal is not proof of task completion; a surviving tmux pane is not proof of an intact model session. If resumption is impossible, record the interruption and get a model/effort choice for a replacement session.

## Assignments and ownership

Keep assignments brief and about **what**, never the Curator's prescription of **how**. Usually the ticket link and existing design-document link suffice; otherwise give the goal and one sentence asking for the action. The developer discovers details and chooses the engineering approach. Do not turn dispatch into a Curator-authored implementation plan, file-by-file checklist or test recipe.

If a design document already exists, reference it rather than paraphrasing it into a new specification. Preserve actual user constraints by pointing to their source; do not manufacture restrictions to compensate for assumed executor weakness. A conflict or missing substantive decision is raised explicitly, not silently settled by the Curator's technical prescription. Use backticked alpha paths, resolved through Duet, for references.

Reviewer requests may be longer when the review scope requires it, but brevity remains the default: identify the changes, review purpose or panel lens, and relevant sources. Reviewers choose how to investigate. Role-specific skills and existing process rules supply standing requirements; do not repeat them as a detailed assignment checklist.

Publish the brief request in the phase's roll or link a separate assignment file when useful, then invoke the participant with that reference. Keep one authoritative assignment, not copies in both places. Clarifications are new messages referring to the prior request. File-based assignments need not become a task-management schema or an excuse for detailed instructions about how to engineer the solution.

Do not require a formal acknowledgement for every message. A substantive reply clearly addressing the request already establishes that the participant received it; silence and queue acceptance do not. When conditions of ongoing work materially change, explicitly reach the participant and establish that it understood the change. Editing a linked file alone neither invokes nor interrupts an agent.

Duet's system instructions load automatically in properly configured sessions. Verify this rather than pasting them into assignments. The assignment selects the executor's role and subject skill; do not invoke `duet-work` for an executor as if it were another Curator of the ticket.

A shared working tree has one product-code writer at a time. Reviewers write their own findings, not changes to the reviewed material. Name the exact review snapshot: a commit or saved diff plus untracked-file contents for code, and saved copies or hashes for design artifacts. Once handed over, reviewed files remain unchanged until all assigned reviewers finish; this is mandatory. Discussion may continue, but corrections wait. Never reset or discard user work to arrange a review.

A changed design or code snapshot requires reassessment of the affected conclusions. This is distinct from changing the assignment text; neither a revision number nor a majority vote substitutes for resolving a blocking finding.

## Using MessageRolls

Use [MessageRoll principles](message-roll.md) for the shared conversation and participant model, and [MessageRoll operations](message-roll-operations.md) for metadata, append and delivery. Create each roll for a clear purpose inside its phase; the phase may contain several rolls. Both analysis/design and implementation can use `roll-type: dev-curation`: the type names this procedure, not a phase or task state.

Reuse the phase's existing roll when its purpose still fits. Separate a new discussion when it has its own focus or participants, not merely because another message arrived. Link relevant artifacts instead of copying them; an engineer can continue across phases without restarting their session. Record current coordinator and participant identities in the rolls, not a parallel registry.

### Dispatch and reports

Substantive instructions and results stay in durable Markdown. Send a short prompt with the exact relevant path/message to the verified client session; do not paste the whole conversation or use “Continue” unless the next action is already unambiguous. Verify that a tmux pane belongs to the intended client and is awaiting appropriate input, not a shell or another process. A roll append notifies its coordinator, not every participant; the curator still invokes the next executor explicitly.

For moderator updates, follow the same delivery distinction: publish the change to shared context and send current participants a short reference through their verified session mechanisms. Include pending updates when a participant returns. When a change affects an ongoing assignment, establish that the participant understood it before relying on further dependent results; do not infer this from a successful append or demand ritual acknowledgments for every notice. Updating terminology communicates the discussion's outcome, not a new technical design imposed by the Curator.

Executor reports state checks performed, outcomes, unperformed checks, limitations and unresolved questions. Use the business's review-board convention. A standalone report may carry `model-created` with the verified model/effort; never add this to product code or a conflicting established schema. The curator checks that required evidence exists and refers technical disputes to responsible executors rather than reviewing code personally.

## Observe, continue, stop

### Observation is a concrete arrangement

Before dispatching work, establish what invokes the Curator again: a scheduled prompt, a native monitor, a verified event-to-session delivery path, or an active turn that waits and checks. Select and verify it through the matching client reference. Keep observation details and handled-message positions per roll in the work's current state reachable from `INDEX.md`, without a second participant roster. Do not launch duplicate observers on resume. Manual user pings are not the assumed architecture; propose them only as an explicit fallback when actual client constraints require them.

The observation targets are the active rolls and their known participant sessions, not the code diff. A notification is a hint to inspect durable state, not a verdict or an instruction with user authority. Re-read complete messages and their linked artifacts; a file-change event, quiet terminal, process exit or elapsed time alone proves neither delivery nor success.

Before dispatch, confirm that the roll still names this coordinator session. An old queued notice may arrive after ownership changed; in that case stop acting as coordinator for that roll and reconcile the handoff instead of overwriting the new address to reclaim it.

**Normal progress is event-driven; the health check runs every five minutes.** An executor saves its result and appends a roll reference through the common operation. The notification route is selected by coordinator client: the helper calls `codex queue` for a reachable Codex session, or the append is observed by Claude's Monitor. Real-session delivery must be verified before relying on it. Do not delay normal handoffs until the next health check. The five-minute check is insurance for silent failure, missed delivery, blocked prompts and expired observation. Client scheduling may delay a check while a turn is busy, so this is a cadence, not a hard response-time guarantee.

### What each observation does

Read each roll's messages since its last handled event and reconcile them with assignments and participants in its frontmatter. On a question or blockage, route the issue to the responsible participant, mediate the exchange, or ask the user for a decision within their authority. On completion, verify that the result exists and corresponds to the assignment actually received; then initiate the next permitted step. During review, wait for all assigned results before invoking the developer to process them directly. Do not collect or rewrite their findings.

Use the client's verified delivery mechanism to send the next short prompt to the intended session, with substantive instructions still in files. Save the resulting state so repeated notifications do not cause duplicate dispatch; after interruption, reconcile what was actually received and performed before resending. When nothing changed, do not write another roll message merely to announce an empty check: that would wake the observer again without advancing the work.

Stop or suspend observation when the agreed work is finished, the user stops it, the next step genuinely waits on the user, or the session/budget limit prevents continuation. Record why and who acts next. Renew a limited watch only while its authorized purpose remains active. Never promise background observation after the turn or client exits unless the actual delivery mechanism was verified to survive that boundary.

Do not automatically retry indefinitely, switch models, or spawn replacement sessions on errors. Record the obstacle and resume the existing session when possible. A new model, effort, provider or replacement session requires the user's choice. On user cancellation, signal the assigned task and stop only the relevant work; do not kill unrelated panes or destroy the user's tmux session. Close useful persistent executor sessions only when their work is finished and continuation is no longer needed.

## Review and completion

The subject skill supplies the review requirements and any `review-curation.md`; this file supplies the common session and communication machinery. Give independent reviewers the agreed scope and artifact snapshot. Do not replace independent review with the author's own check.

### Direct exchange of findings

Reviewers publish their complete results in the assigned files and post a short reference in the relevant roll. On its next invocation, the developer reads all results directly; the Curator does not collect, rewrite or forward findings as an intermediary. Merely writing a roll message does not invoke the developer unless a tested delivery mechanism actually does so. The short continuation prompt starts the next turn; it does not replace direct access to the files or require a Curator-written digest.

Keep review artifacts in the owning phase, preserving established boards and history. A suitable default is `<phase>/reviews/review-<participant-id>.md`. Keep later passes and responses for that review together, identifying the design or code snapshot. Give findings stable IDs and serialize edits to shared files. The roll carries short references, not copies of full reports; the developer reads each author's findings directly.

The pass assignment names its reviewers and result paths. In an active turn, the Curator checks that every assigned reviewer has delivered, then invokes the developer with a short continuation prompt pointing to the pass and its existing results. Checking completion and initiating the next turn are coordination, not collecting or rewriting findings. Do not assign an idle developer the job of monitoring missing reports. Missing or interrupted review is not completion; the Curator handles stalled sessions or changes to review scope through the observation and wake-up arrangements described above.

### Developer judgment and resolution

The developer exercises L6-level engineering judgment: understand what a finding protects, test its premise against the code and task, and apply changes that are warranted and useful. A review comment is not an instruction to implement mechanically. Challenge mistaken, inapplicable or unnecessarily costly recommendations with reasons and evidence; do not make a worse change merely to obtain agreement.

After the pass finishes, the developer applies accepted corrections and records, against each finding on its review board, the change and relevant checks or the reason for disputing it. The reviewer assesses that response and the changed code directly. The Curator ensures that independent follow-up review happens and keeps the work map current, but does not arbitrate code behavior by doing another technical review. A developer's disagreement alone does not close a blocking finding: unresolved substantive disagreement goes to the user with the competing reasons visible. No majority vote or silent omission substitutes for resolution.

Keep who acts next, unfinished questions, active sessions and accepted results reachable from the work's `INDEX.md`. A handover names unverified assumptions and waiting user choices. No commit, push, PR publication, settings deployment or claimed completion is implied by an executor's success message; apply the work's actual authority and acceptance rules.
