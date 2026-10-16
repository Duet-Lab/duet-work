# Development curation in Claude Code

Read this when the Curator runs in Claude Code. Executors may use any client. Team responsibilities are in [dev-curation.md](dev-curation.md); shared principles and file operations are in [MessageRoll](message-roll.md) and [MessageRoll operations](message-roll-operations.md). This reference explains actual observation, not a different team protocol.

## Verify the observation mechanism

Check the available tools and the [official Monitor reference](https://code.claude.com/docs/en/tools-reference#monitor-tool) in the actual curator session. The required mechanism delivers a running command's stdout lines to the curator; confirm its availability, expiry and stop behavior before relying on it. A working local file watcher alone does not establish delivery to the client.

## Normal delivery: append → watch stdout → Monitor

Register your participant entry with `role: Curator`, `client: claude` and your verified session ID. The helper selects the recipient from participants. Before dispatching work, start a Monitor with this command after resolving paths:

```sh
uv run --script "<skill>/scripts/log_append.py" watch \
  --roll "<absolute-roll.md>" --after "<last-handled-message-id>"
```

Omit `--after` on a new roll or when full reconciliation is needed; it replays retained non-moderator messages. For several active rolls, establish coverage for each rather than watching only one ticket-wide file. Store each watch identifier, expiry, stop action and handled-message position in the work's current state. The watch validates whole records, follows atomic replacement of the file, notices metadata changes and emits message IDs, not participant-authored instructions.

An executor saves its result and calls the common `append` operation. It does not invoke Monitor or issue a second client-specific command. The running watch emits a line for a new complete message, which Monitor delivers to the curator. The curator reads durable messages and results, reconciles the assignment and invokes the next executor when appropriate. The watcher does not interpret results or mediate disputes.

The watch polls once per second by default (`--poll-seconds` adjusts this). It emits `message-roll:ready` on attachment, metadata-change notices, and only new non-moderator message notices afterwards. This is near-immediate event observation, not a hard latency guarantee. On attachment/restart, reconcile saved state; duplicate signals must not duplicate dispatch. Do not write a message merely to acknowledge an empty check.

## Health check every five minutes

Check sessions, jobs, blocked prompts, missed messages and observation health every five minutes while the agreed work remains active. Claude chooses a suitable verified mechanism; this requirement does not prescribe `/loop`. The bundled watch emits a `message-roll:health-check` stdout line every 300 seconds while alive (`--health-seconds` adjusts it), which can supply ordinary health prompts through Monitor.

A watch cannot report its own disappearance after the client exits. Account for Monitor expiry/failure using the client's actual completion notice or a separate periodic mechanism. Check availability and limits in the official reference before launch; renew and reconcile on expiry while the purpose remains active. Do not pretend the helper checks agent health itself: its tick only asks the curator to perform that inspection.

If a separate scheduler is appropriate, consult the client's current [scheduled-task instructions](https://code.claude.com/docs/en/scheduled-tasks); select and verify the mechanism rather than requiring `/loop`. Keep only one effective cadence per work when several rolls emit health ticks: coalesce checks already performed recently instead of repeating a full inspection for each roll. Five minutes is the intended cadence, not a strict response deadline when the client is busy.

## Failure, first use and shutdown

The CLI operation `watch --once` validates the roll and prints pending notices without starting a background process. A corrupt roll or absent `--after` ID fails explicitly. The helper's sidecar lock prevents metadata/message write races; manual edits require stopped writers. A saved Claude conversation does not preserve a running watch: re-establish it after restart.

Before relying on Monitor, test an authorized harmless roll message in the real session and confirm that it invokes the same curator without a user ping. Also check duplicate delivery, a blocked executor and the all-reviewers-finished gate. Monitor can deliver a line without the curator completing the resulting work; handled-message state is separate.

If Monitor is unavailable, propose verified periodic checking with its delivery delay, not imaginary background Bash wake-up. Stop only this work's watches/schedules when the purpose ends or the user stops it; do not kill unrelated processes. Do not modify generated client settings to force tool availability.
