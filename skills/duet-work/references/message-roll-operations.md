# MessageRoll operations

Read [MessageRoll principles](message-roll.md) before using these operations. This is the current local file/notification implementation, not the definition of a development workflow.

The bundled `scripts/log_append.py` implements `init`, `metadata`, `append` and `watch` on macOS/Linux. Use `uv run --script`; its pinned YAML dependency lives in uv's cache, never in the business folder. If uv is missing, stop and give `brew install uv` on macOS with Homebrew, or verify the installation command for the actual platform. Client notifications still require a reachable real coordinator; local tests are not proof of live delivery.

Use a distinct readable name for each roll and make it reachable from the work's `INDEX.md` through its owning phase. For example, `01-analysis_design/rolls/<purpose>.md` is a phase-local path, not a fixed ticket-wide channel or an assignment versioning scheme. The initial implementation has one machine for the coordinator and all writers. Reading a synchronized copy elsewhere is fine; Google Drive synchronization is not a distributed write lock.

### Frontmatter

Prepare YAML input without the enclosing `---` lines. The helper writes those delimiters to the roll. Example values below are placeholders, not model recommendations:

```yaml
roll-type: discussion
coordinator:
  name: Moderator_Codex_1
  client: codex
  session_id: "<verified current session ID>"
participants:
  - name: User
  - name: Moderator_Codex_1
    client: codex
    model: "<actual model>"
  - name: Participant_Gemini_1
    client: gemini
    model: "<actual model>"
    effort: "<only if actually selected>"
```

`coordinator.name` refers to its roster entry; it identifies authored moderator messages and prevents self-notification loops. The user can be a named author without client/model fields. Record actual agent launch choices, omitting unsupported or unspecified fields. Keep all prior participant entries unchanged; add a new name for a replacement. To resume the coordinator, update its current `session_id`; when a different moderator instance takes over, add its name and point `coordinator.name` to it. Do not rewrite previous authorship.

No transport selector, task state or assignment revision is required by the file format. Extra descriptive YAML fields are allowed, but do not introduce fields without a present use. Existing participant entries are immutable through the helper; correcting erroneous historical metadata requires stopped writers and an explicit repair, not disguising a replacement as a correction.

### Create a roll and update its metadata

Resolve the helper, roll and input paths before invoking commands. The parent directory must exist. Metadata input is the complete proposed frontmatter, not a patch. Start from the current frontmatter when adding a participant or changing the coordinator; a stale input that drops someone is rejected.

```sh
uv run --script "<skill>/scripts/log_append.py" init \
  --roll "<absolute-roll.md>" --metadata "<absolute-metadata.yaml>"

uv run --script "<skill>/scripts/log_append.py" metadata \
  --roll "<absolute-roll.md>" --metadata "<absolute-metadata.yaml>"
```

`init` never overwrites an existing file. `metadata` preserves published message bytes, refuses removing/changing existing participants and refuses changing `roll-type`. It normalizes YAML formatting; do not store essential information only in YAML comments. Prepare input files outside the synchronized business folder when they are merely temporary transport, and remove them afterwards.

### Append a message

Save the detailed result first when a message points to it. Then use one operation for saving the message and notifying the coordinator:

```sh
uv run --script "<skill>/scripts/log_append.py" append \
  --roll "<absolute-roll.md>" --roll-ref '@ABC001/01-analysis_design/rolls/discussion.md' \
  --message-id contribution-1 --sender Participant_Gemini_1 \
  --body "<absolute-body.md>"
```

`--roll-ref` must identify the same file as `--roll`; Duet resolution is the caller's responsibility, not something the local helper can infer. Register the author first. A readable generated message contains a UTC timestamp, author, message ID and Markdown body. There are no mandatory `task` or `kind` fields. Headings, code fences, lists and alpha links remain ordinary text. The prefix `<!-- message-roll:` is reserved for complete-record boundaries.

Message IDs are unique within a roll. Identical retries retain the original timestamp and bytes but retry notification; conflicting reuse fails. Send corrections as new messages. A completion statement is a participant's report, not automatic acceptance or permission for further action. Secret values and raw terminal dumps do not belong in a roll.

### Saving, delivery and failures

All mutations share a stable hidden `.filename.lock` sidecar and replace the data file atomically after flushing it. This protects concurrent message and frontmatter updates on one machine. Never delete the lock while writers or watchers run. Do not mix helper writes with manual editor saves; stop writers before manual repair. Old channel files are rejected, not silently migrated or truncated.

For `coordinator.client: codex`, append invokes the installed `codex queue` after saving and releasing the file lock. Its default timeout is 20 seconds (`--notify-timeout` adjusts it). For `claude`, append leaves the event to an already running Monitor watch. Other clients retain the message but report an unsupported notification route; agree and verify a concrete adapter rather than inventing success. Moderator messages do not notify themselves.

Exit 0 means the operation succeeded, not that a coordinator acted. Exit 3 means the message is saved but notification is unconfirmed; retry the identical command after resolving the delivery issue. Other errors stop the operation; after any uncertain interruption, retry the same ID rather than inventing another. Queue acceptance can be duplicated on retry, so the curator deduplicates handling per roll/message ID. A coordinator change during delivery is reconciled on the next check; a retry reads its latest address.

## Read notifications with watch

For a client that observes command output, `watch` emits notices for complete messages rather than executing their contents:

```sh
uv run --script "<skill>/scripts/log_append.py" watch \
  --roll "<absolute-roll.md>" --after "<last-handled-message-id>"
```

Omit `--after` to replay retained non-moderator messages. `--once` prints pending notices and exits; otherwise polling defaults to one second and a health-check notice to 300 seconds (`--poll-seconds` and `--health-seconds`). A tick is not an agent-health test. Reconcile the message and saved state before acting; repeated notices must not duplicate work.

The development coordinator's verified observation arrangements are described in [Claude](dev-curation-claude.md) and [Codex](dev-curation-codex.md). Other uses need their own observation arrangement; saving a message does not establish one.
