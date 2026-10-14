# Development curation in Codex

Read this when the Curator runs in the **Codex VS Code extension or Codex in a terminal**. Team responsibilities are in [dev-curation.md](dev-curation.md); shared principles and file operations are in [MessageRoll](message-roll.md) and [MessageRoll operations](message-roll-operations.md). Do not require the desktop app or move the curator there to obtain scheduling.

## Verify the notification route

Inspect the installed `codex queue --help` and the [official command reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli#codex-queue). Prefer the target session's verified UUID over a potentially ambiguous name. CLI availability alone does not establish reachability of a VS Code extension session or its server; verify the exact route before relying on it.

## Normal delivery: append saves, then invokes queue

Set `coordinator.client: codex` and the current session ID in the roll. The common `append` command saves the message and then invokes:

```sh
codex queue --thread "<current-coordinator-session-id>" \
  --message '<notice naming the roll alpha path and message ID>'
```

This is the helper's underlying command, not a mandatory second executor action. Any executor client can invoke the same append helper. It uses the locally installed CLI and existing authentication, without selecting another model or changing permissions. A separate watcher is not required for ordinary result notifications. There is no `notify_via` field and no free-form command taken from YAML.

If queue is missing, exits unsuccessfully or times out, the message remains saved and append exits 3 with an explicit delivery problem. Resolve the problem and repeat the identical append command; its message ID prevents another file entry, but the queue notice may repeat. The curator deduplicates handling by roll/message ID and reads durable state rather than treating notification text as a new user instruction.

Moderator-authored messages do not queue back to the same moderator. A resumed coordinator gets its current address through the `metadata` operation. In-flight delivery might still reach the former address; the next health check or identical retry reconciles the durable message. Queue acceptance is not proof that the curator completed a turn.

## Establish reachability before dispatch

For both terminal and VS Code, verify the exact target session/server and send one authorized harmless test message before starting executors. Check the idle and busy cases, model/effort/workspace preservation and stop behavior. The helper currently uses the CLI's default local server connection; if the target needs an explicit `--remote` connection, report that limitation and establish a supported route before claiming delivery works. Do not silently switch API billing, start a duplicate curator or alter generated settings.

## Health check every five minutes

Normal progress is driven by append notifications; independently inspect sessions, jobs, permission/authentication prompts and missed messages about every five minutes. The initial concrete option is an active curator turn using its available interruptible sleep/wait tool between checks. Check durable rolls and live session state, then wait up to 300 seconds; on incoming notifications, handle them and reconcile the check cadence.

Use tools actually exposed by that session. With shell/process waiting, `sleep 300` plus the process-wait tool can keep the active turn waiting; prefer an interruptible sleep tool when available. The model does not need to reason continuously during sleep, but subsequent checks consume model work. A final reply, interruption or client exit ends this arrangement. Do not claim background observation survives those boundaries.

If a verified client-native scheduler exists, it can replace active waiting. A detached timer repeatedly calling queue is not bundled or required: adding one would also require bounded outstanding ticks, handling acknowledgements and lifecycle control. Do not manufacture that infrastructure merely to satisfy the cadence on paper. If neither active waiting nor a verified scheduler meets the user's needed lifetime, explain the limitation and propose a concrete alternative before dispatch.

## Fallback, reconciliation and shutdown

If queue cannot reach the target session, active-turn checking can still notice new roll messages at the next check. That is a degraded, up-to-five-minute delivery path; propose it explicitly rather than calling it the event-driven happy path. Do not assume manual user pings are the architecture. Never create a Goal without an explicit user request just to keep the session active.

Keep observation ownership, handled-message positions per roll, last health check and stop action in the existing work map or a linked operational note. Participant identities remain in roll frontmatter, not another roster. Reconcile before resuming so there are not two dispatchers. A surviving pane and unchanged output alone prove neither a healthy model session nor completed work.

Stop only this work's observation when finished, stopped or waiting on a substantive user decision. Preserve unfinished messages and who acts next. Live first-use validation must include duplicate delivery, an interrupted executor and the rule that all assigned reviewers finish before the developer edits reviewed files.
