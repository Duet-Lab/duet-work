# MessageRoll operations

Read MessageRoll principles (`references/message-roll.md`) before using these operations. This describes the bundled local helper, not the definition of a development workflow.

The bundled `scripts/log_append.py` implements `init`, `register`, `metadata`, `append` and `watch` on macOS/Linux. Use `uv run --script`; its pinned YAML dependency lives in uv's cache, never in the business folder. If uv is missing, stop and give `brew install uv` on macOS with Homebrew, or verify the installation command for the actual platform. Client notifications still require a reachable real Curator; local tests are not proof of live delivery.

Use a distinct readable name for each roll and make it reachable from the work's `INDEX.md` through its owning phase. For example, `01-analysis_design/rolls/<purpose>.md` is a phase-local path, not a fixed ticket-wide channel or an assignment versioning scheme. The helper assumes that the Curator and all writers run on one machine. Reading a synchronized copy elsewhere is fine; cloud-drive synchronization is not a distributed write lock.

## Frontmatter

Prepare YAML input without the enclosing `---` lines. The helper writes those delimiters to the roll. Example values below are placeholders, not model recommendations:

```yaml
roll-type: discussion
tmux-session: abc001  # optional; shared by this roll's tmux participants
participants:
  - name: Alex  # use the user name returned by Duet orientation
    role: User
    client: human
  - name: Curator_Codex_1
    role: Curator
    client: codex
    session_id: "<verified current session ID>"
    model: "<actual model>"
  - name: Participant_Gemini_1
    role: Investigator
    client: gemini
    session_id: "<verified participant session ID>"
    model: "<actual model>"
    effort: "<only if actually selected>"
    tmux-window: investigator
```

Every participant has an explicit `role` and `client`; names do not determine roles. Roles are open-ended. Every newly registered AI participant must have a verified `session_id`, unique within the roll even across clients. Human participants use `client: human`, with no session ID; get the person's name from Duet `orientation`, whose default is `Human`. Do not use `User` as a placeholder for that name. Model and effort record actual choices, not defaults invented for the roster.

Keep existing participant entries unchanged and in order, including disconnected ones. Resuming the same session keeps the same entry; a new session requires a new participant name and entry. A handoff registers the new Curator instead of editing an old address. The helper determines notification routing and suppresses self-notification; there is no separate `coordinator` field. Agents do not compute that routing rule or test whether the roll still points to themselves. A roll may have no Curator: messages are saved without notification or delivery error.

The optional roll-level `tmux-session` and participant-level `tmux-window` describe terminal placement, not AI identity. A window requires the session field. Once set, the roll's tmux session cannot be changed through ordinary metadata updates because that would change retained participants' addresses.

No transport selector, task state or assignment revision is required by the file format. Extra descriptive YAML fields are allowed, but do not introduce fields without a present use. Existing participant entries are immutable through the helper; correcting erroneous historical metadata requires stopped writers and an explicit repair, not disguising a replacement as a correction.

## Create a roll and update its metadata

Resolve the helper, roll and input paths before invoking commands. The parent directory must exist. Metadata input is the complete proposed frontmatter, not a patch. Prefer `register` to add one participant atomically. For a full metadata update, start from the current frontmatter; stale input that drops or reorders someone is rejected.

```sh
uv run --script "<skill>/scripts/log_append.py" init \
  --roll "<absolute-roll.md>" --metadata "<absolute-metadata.yaml>"

uv run --script "<skill>/scripts/log_append.py" metadata \
  --roll "<absolute-roll.md>" --metadata "<absolute-metadata.yaml>"
```

`init` never overwrites an existing file. `metadata` preserves published message bytes, refuses removing/changing existing participants and refuses changing `roll-type`. It normalizes YAML formatting; do not store essential information only in YAML comments. Prepare input files outside the synchronized business folder when they are merely temporary transport, and remove them afterwards.

## Register your session before answering

The assignment names the participant and role. First discover your own actual session ID through the client's verified session mechanism; never substitute a process ID, tmux window or guessed UUID. Then prepare one YAML mapping containing your name, role, client, session ID and actual launch choices, and register yourself:

```sh
uv run --script "<skill>/scripts/log_append.py" register \
  --roll "<absolute-roll.md>" --participant "<absolute-participant.yaml>"
```

This appends one participant under the same lock as message writes, without replacing the roster. Identical registration is an idempotent retry; reuse of a name with changed metadata or of another participant's session ID fails. For an already registered resumed session, keep the retained entry. If the ID is unavailable, establish it before registering a new AI participant; do not publish a placeholder. The Curator registers itself in the same way or includes its verified entry during `init`.

## Append a message

Save the detailed result first when a message points to it. Then use one operation for saving the message and notifying the Curator (the helper's code calls the Curator the coordinator):

```sh
uv run --script "<skill>/scripts/log_append.py" append \
  --roll "<absolute-roll.md>" --roll-ref '@ABC001/01-analysis_design/rolls/discussion.md' \
  --message-id contribution-1 --sender Participant_Gemini_1 \
  --body "<absolute-body.md>"
```

`--roll-ref` is the alpha path of the same file as `--roll`; the helper checks only its form, so resolving it through Duet is the caller's job. Register the author first. A readable generated message contains a UTC timestamp, author, message ID and Markdown body. There are no mandatory `task` or `kind` fields. Headings, code fences, lists and alpha links remain ordinary text. The prefix `<!-- message-roll:` is reserved for complete-record boundaries.

Message IDs are unique within a roll. Identical retries retain the original timestamp and bytes but retry notification; conflicting reuse fails. Send corrections as new messages. A completion statement is a participant's report, not automatic acceptance or permission for further action. Secret values and raw terminal dumps do not belong in a roll.

## Saving, delivery and failures

All mutations share a stable hidden `.filename.lock` sidecar and replace the data file atomically after flushing it. This protects concurrent message and frontmatter updates on one machine. Never delete the lock while writers or watchers run. Do not mix helper writes with manual editor saves; stop writers before manual repair. The helper rejects a file that is not a valid roll, including older formats with a `coordinator` block, without changing it. An existing participant entry may lack a session ID, for example after a manual repair; that entry stays readable, but every new AI entry needs one.

For a current Curator with `client: codex`, append invokes the installed `codex queue` after saving and releasing the file lock. Its default timeout is 20 seconds (`--notify-timeout` adjusts it). For `claude`, append leaves the event to an already running Monitor watch. Other clients retain the message but report an unsupported notification route; agree and verify a concrete adapter rather than inventing success. Curator messages do not notify themselves.

Exit 0 means the operation succeeded, not that a Curator acted. Exit 3 means the message is saved but notification is unconfirmed; retry the identical command after resolving the delivery issue. Other errors stop the operation; after any uncertain interruption, retry the same ID rather than inventing another. Queue acceptance can be duplicated on retry, so the Curator deduplicates handling per roll/message ID. A Curator handoff during delivery is reconciled on the next check; a retry reads its latest address.

## Read notifications with watch

For a client that observes command output, `watch` emits notices for complete messages rather than executing their contents:

```sh
uv run --script "<skill>/scripts/log_append.py" watch \
  --roll "<absolute-roll.md>" --after "<last-handled-message-id>"
```

Omit `--after` to replay retained non-Curator messages. `--once` prints pending notices and exits; otherwise polling defaults to one second and a health-check notice to 300 seconds (`--poll-seconds` and `--health-seconds`). Without a Curator, watch emits no message, metadata-change or health-check notices after its initial ready line; retained messages become available when a Curator registers. A tick is not an agent-health test. Reconcile the message and saved state before acting; repeated notices must not duplicate work.

The Curator's verified observation arrangements for development work are described in `references/dev-curation-claude.md` and `references/dev-curation-codex.md`. Other uses need their own observation arrangement; saving a message does not establish one.
