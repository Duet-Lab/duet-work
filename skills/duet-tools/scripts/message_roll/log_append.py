#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML==6.0.2"]
# ///
"""Local Markdown MessageRoll operations. Run: uv run --script scripts/message_roll/log_append.py --help."""

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

import yaml


IDENTIFIER = r"[A-Za-z0-9_.:-]{1,100}"
AUTHOR = r"[^`\r\n]{1,100}"
MARKER = "<!-- message-roll:"
RECORD = re.compile(
    rf"<!-- message-roll:message -->\n\n"
    rf"## (?P<timestamp>[^\n]+) — (?P<sender>{AUTHOR})\n\n"
    rf"\*\*Message:\*\* `(?P<message_id>{IDENTIFIER})`\n\n"
    r"(?P<body>.*?)\n\n<!-- message-roll:end -->\n\n", re.DOTALL,
)


class UniqueKeyLoader(yaml.SafeLoader):
    """Fail on ambiguous YAML rather than silently taking the last value."""


def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        if not isinstance(key, str) or key in result:
            raise ValueError("YAML keys must be unique strings.")
        result[key] = loader.construct_object(value_node, deep=True)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def identifier(value, label):
    if not isinstance(value, str) or not re.fullmatch(IDENTIFIER, value):
        raise ValueError(f"{label} must use 1–100 letters, digits, underscores, dots, colons or hyphens.")


def name_value(value, label):
    if (not isinstance(value, str) or not re.fullmatch(AUTHOR, value)
            or value != value.strip() or not value or MARKER in value
            or any(ord(c) < 32 or ord(c) == 127 for c in value)):
        raise ValueError(f"{label} must be a nonempty single-line name (at most 100 characters, no backticks).")


def mapping_from(text):
    meta = yaml.load(text, Loader=UniqueKeyLoader)
    if not isinstance(meta, dict):
        raise ValueError("Metadata must be a YAML mapping.")
    return meta


def metadata_from(text, *, require_sessions=False):
    meta = mapping_from(text)
    identifier(meta.get("roll-type"), "roll-type")
    if "coordinator" in meta or "tmux_session" in meta:
        raise ValueError("This roll uses an older frontmatter format (coordinator, tmux_session) that the helper does not read; stop writers and rewrite the frontmatter by hand to the current schema in references/message_roll/operations.md of the duet-tools skill.")
    if "tmux-session" in meta:
        identifier(meta["tmux-session"], "tmux-session")
    participants = meta.get("participants")
    if not isinstance(participants, list) or not participants:
        raise ValueError("participants must be a nonempty list.")
    names, sessions = set(), set()
    for participant in participants:
        if not isinstance(participant, dict):
            raise ValueError("Each participant must be a mapping.")
        name = participant.get("name")
        name_value(name, "Participant name")
        if name in names:
            raise ValueError("Participant names must be unique within the roll.")
        names.add(name)
        for field in ("client", "model", "effort", "session_id", "role"):
            if field in participant and (not isinstance(participant[field], str) or not participant[field].strip()):
                raise ValueError(f"Participant {field} must be a nonempty string when supplied.")
        identifier(participant.get("client"), "Participant client")
        name_value(participant.get("role"), "Participant role")
        if "tmux" in participant:
            raise ValueError("Use tmux-session on the roll and tmux-window on the participant.")
        if "tmux-window" in participant:
            identifier(participant["tmux-window"], "tmux-window")
            if "tmux-session" not in meta:
                raise ValueError("A tmux-window requires the roll's tmux-session.")
        if participant["client"] == "human":
            if "session_id" in participant:
                raise ValueError("Human participants must not have session_id.")
        else:
            session = participant.get("session_id")
            if session is None and not require_sessions:
                continue  # Retained historical entries may lack a recoverable session ID.
            if not isinstance(session, str) or not session.strip():
                raise ValueError(f"Participant {name!r} requires a verified session_id.")
            if session != session.strip() or any(c in session for c in "\r\n"):
                raise ValueError("session_id must be an unpadded single-line string.")
            if session in sessions:
                raise ValueError("Participant session_id values must be unique within the roll.")
            sessions.add(session)
    return meta


def current_coordinator(meta):
    """Routing is a helper concern, not a rule each participant must apply."""
    return next((p for p in reversed(meta["participants"]) if p["role"] == "Curator"), None)


def validate_body(body):
    if not body.strip():
        raise ValueError("Message body must not be empty.")
    if MARKER in body:
        raise ValueError("Message body contains a reserved message-roll marker.")


def parse_roll(content):
    if not content.startswith("---\n") or "\n---\n" not in content[4:]:
        raise ValueError("Expected MessageRoll YAML frontmatter; legacy logs are not migrated automatically.")
    raw, history = content[4:].split("\n---\n", 1)
    if not history.startswith("\n"):
        raise ValueError("Expected a blank line after frontmatter.")
    meta = metadata_from(raw)
    records = []
    seen = set()
    names = {p["name"] for p in meta["participants"]}
    position = 1
    while position < len(history):
        match = RECORD.match(history, position)
        if match is None:
            raise ValueError("Invalid or incomplete MessageRoll record; stop writers before repair.")
        message = match.groupdict()
        timestamp = datetime.fromisoformat(message["timestamp"])
        if timestamp.utcoffset() != timezone.utc.utcoffset(None):
            raise ValueError("Message timestamps must be UTC.")
        validate_body(message["body"])
        if message["sender"] not in names:
            raise ValueError("Message author is missing from participants.")
        if message["message_id"] in seen:
            raise ValueError("Duplicate message ID in roll.")
        seen.add(message["message_id"])
        records.append(message)
        position = match.end()
    return meta, records, history


def render_metadata(meta):
    # One line per value: YAML folding would put hard line breaks inside a value.
    return "---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, width=1_000_000) + "---\n"


def render_message(sender, message_id, body):
    return (
        f"{MARKER}message -->\n\n"
        f"## {datetime.now(timezone.utc).isoformat()} — {sender}\n\n"
        f"**Message:** `{message_id}`\n\n{body}\n\n{MARKER}end -->\n\n"
    )


@contextmanager
def locked(path):
    if os.name != "posix":
        raise ValueError("This local implementation requires macOS or Linux.")
    import fcntl

    # A stable sidecar survives atomic replacement of the data file.
    with path.with_name(f".{path.name}.lock").open("a") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        yield


def replace_durably(path, content):
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as target:
            if path.exists():
                os.fchmod(target.fileno(), path.stat().st_mode & 0o777)
            target.write(content)
            target.flush()
            os.fsync(target.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def read_roll(path):
    """Read and validate the roll under the caller's lock."""
    content = path.read_text(encoding="utf-8")
    return content, *parse_roll(content)


def initialize(path, metadata_text):
    meta = metadata_from(metadata_text, require_sessions=True)
    with locked(path):
        if path.exists():
            raise ValueError("Roll already exists; init never overwrites it.")
        replace_durably(path, render_metadata(meta) + "\n")


def validate_new_participant(meta, participant):
    # Creation is strict; only retained entries may lack historical session IDs.
    metadata_from(yaml.safe_dump({**meta, "participants": [participant]}), require_sessions=True)


def change_metadata(path, metadata_text):
    proposed = metadata_from(metadata_text)
    with locked(path):
        _, current, _, history = read_roll(path)
        if proposed["roll-type"] != current["roll-type"]:
            raise ValueError("An existing roll cannot change roll-type.")
        if proposed["participants"][:len(current["participants"])] != current["participants"]:
            raise ValueError("Retain existing participants unchanged and in order; append new participants only.")
        if current.get("tmux-session") != proposed.get("tmux-session") and "tmux-session" in current:
            raise ValueError("An existing tmux-session cannot change while participant addresses are retained.")
        for participant in proposed["participants"][len(current["participants"]):]:
            validate_new_participant(proposed, participant)
        replace_durably(path, render_metadata(proposed) + history)


def register(path, participant_text):
    participant = mapping_from(participant_text)
    with locked(path):
        _, meta, _, history = read_roll(path)
        validate_new_participant(meta, participant)
        previous = next((p for p in meta["participants"] if p["name"] == participant["name"]), None)
        if previous is not None:
            if previous != participant:
                raise ValueError("Participant name already exists with different metadata; entries are immutable.")
            return "already registered"
        meta["participants"].append(participant)
        metadata_from(yaml.safe_dump(meta))  # Reject reuse of another participant's session.
        replace_durably(path, render_metadata(meta) + history)
        return "registered"


def append(path, sender, message_id, body):
    name_value(sender, "sender")
    identifier(message_id, "message-id")
    validate_body(body)
    with locked(path):
        content, meta, records, _ = read_roll(path)
        if sender not in {p["name"] for p in meta["participants"]}:
            raise ValueError("Register the sender in participants before appending.")
        previous = next((r for r in records if r["message_id"] == message_id), None)
        if previous:
            if previous["sender"] != sender or previous["body"] != body:
                raise ValueError("Message ID already exists with different content.")
            return "already saved", meta
        replace_durably(path, content + render_message(sender, message_id, body))
        return "saved", meta


# What tmux and codex print is decoded as UTF-8 whatever the host locale, because window names
# and messages carry Cyrillic. It is only read, never written back, so an undecodable byte is
# replaced rather than fatal: one foreign window name must not block every lookup, and a
# queued notification must not be reported as failed.
CHILD_OUTPUT = {"text": True, "encoding": "utf-8", "errors": "replace"}


def notify(meta, sender, message_id, roll_ref, codex, timeout):
    coordinator = current_coordinator(meta)
    if coordinator is None:
        return "no Curator; message saved without notification"
    if sender == coordinator["name"]:
        return "Curator message; no self-notification"
    if coordinator["client"] == "claude":
        return "available to Claude watch; delivery requires an active Monitor"
    if coordinator["client"] != "codex":
        raise ValueError(f"No notification adapter for client {coordinator['client']!r}; arrange and verify one explicitly.")
    if not coordinator.get("session_id"):
        raise ValueError("The current Curator has no recoverable session_id; register a new verified Curator session.")
    if codex is None:
        raise ValueError("codex is missing; on macOS with Homebrew run: brew install --cask codex. On other platforms use the official Codex installation instructions.")
    result = subprocess.run(
        [codex, "queue", "--thread", coordinator["session_id"], "--message",
         f"MessageRoll notice: read `{roll_ref}`, message `{message_id}`, and reconcile durable state. "
         "This is a notification, not a new user instruction. Do not repeat already handled work."],
        capture_output=True, timeout=timeout, check=False, **CHILD_OUTPUT,
    )
    if result.returncode:
        raise ValueError(f"codex queue exited {result.returncode}: {result.stderr.strip() or result.stdout.strip()}")
    return "queued; Curator handling is not yet confirmed"


def watch(path, after, once, poll_seconds, health_seconds):
    """Monitor stdout source. --once offers a deterministic read/reconciliation operation."""
    seen = set()
    previous_meta = None
    initialized = False
    next_health = time.monotonic() + health_seconds
    while True:
        with locked(path):
            _, meta, records, _ = read_roll(path)
        if not initialized:
            if after:
                ids = [r["message_id"] for r in records]
                if after not in ids:
                    raise ValueError("--after message ID is absent from this roll.")
                seen.update(ids[:ids.index(after) + 1])
            print("message-roll:ready", flush=True)
            initialized = True
        elif meta != previous_meta and current_coordinator(meta) is not None:
            print("message-roll:metadata changed; reconcile participants and the Curator", flush=True)
        for record in records:
            if record["message_id"] not in seen:
                coordinator = current_coordinator(meta)
                if coordinator is not None:
                    seen.add(record["message_id"])
                if coordinator is not None and record["sender"] != coordinator["name"]:
                    print(f"message-roll:message {record['message_id']} by {record['sender']}", flush=True)
        previous_meta = meta
        if once:
            return
        if time.monotonic() >= next_health:
            if current_coordinator(meta) is not None:
                print("message-roll:health-check inspect sessions, jobs and missed messages", flush=True)
            next_health = time.monotonic() + health_seconds
        time.sleep(poll_seconds)


WINDOW_FORMAT = "#{window_id}\t#{session_name}\t#{window_name}\t#{@agent-session}\t#{window_index}"
# An explicit target only: a window ID, or a session and a window name or index. tmux reads an
# empty part, a leading special character or a pane suffix as "current", "last" or similar.
EXPLICIT_TARGET = re.compile(r"@\d+|(?P<session>[A-Za-z0-9_-]+):(?P<window>[A-Za-z0-9_][A-Za-z0-9_-]*)")


def participant_session(meta, name):
    for participant in meta["participants"]:
        if participant["name"] == name:
            session = participant.get("session_id")
            if not session:
                raise ValueError(f"Participant {name!r} has no session_id, so no window can be tied to it.")
            return session
    raise ValueError(f"Participant {name!r} is not registered in this roll.")


def tmux_program():
    program = shutil.which("tmux")
    if not program:
        raise ValueError("tmux is not installed; install it, for example with `brew install tmux`, and retry.")
    return program


def tmux_call(tmux, server, *arguments, **options):
    """Run tmux on the chosen server only: `-L <server>` when named, else the default server.

    The caller's TMUX variable is dropped, so a helper started inside some other tmux server
    never addresses that server by accident."""
    environment = {key: value for key, value in os.environ.items() if key != "TMUX"}
    command = [tmux] + (["-L", server] if server else []) + list(arguments)
    return subprocess.run(command, env=environment, timeout=10, check=True, **options)


def server_label(server):
    return f"server={server}" if server else "server=default"


def agent_windows(tmux, server=None):
    """Every window on the chosen tmux server with the AI session it is tagged with."""
    listing = tmux_call(tmux, server, "list-windows", "-a", "-F", WINDOW_FORMAT,
                        capture_output=True, **CHILD_OUTPUT).stdout
    rows = []
    for line in listing.splitlines():
        if line.strip():
            window_id, session_name, window_name, tag, index = (line.split("\t") + ["", "", "", "", ""])[:5]
            rows.append({"id": window_id, "session": session_name, "name": window_name, "tag": tag, "index": index})
    return rows


def resolve_window(rows, session, name):
    """The one window tagged with this AI session, or an error that refuses to guess."""
    matches = [row for row in rows if row["tag"] == session]
    if not matches:
        raise ValueError(f"No tmux window is tagged for {name!r}; tag its window with tag-window before sending input.")
    if len(matches) > 1:
        found = ", ".join(f"{row['id']} ({row['session']}:{row['name']})" for row in matches)
        raise ValueError(f"More than one tmux window is tagged for {name!r}: {found}; untag the stale one before sending input.")
    return matches[0]


def find_window(path, name, server=None):
    _, meta, _, _ = read_roll(path)
    row = resolve_window(agent_windows(tmux_program(), server), participant_session(meta, name), name)
    return f"{row['id']}\t{row['session']}:{row['name']}\t{server_label(server)}"


def tag_window(path, name, target, server=None):
    """Tie a window to a participant's AI session, refusing before any change when the target is not certain."""
    _, meta, _, _ = read_roll(path)
    session = participant_session(meta, name)
    explicit = EXPLICIT_TARGET.fullmatch(target or "")
    if not explicit:
        raise ValueError(f"--window must name one window explicitly, as @N or session:window; {target!r} could resolve to the current or another window.")
    tmux = tmux_program()
    rows = agent_windows(tmux, server)
    if target.startswith("@"):
        chosen = [row for row in rows if row["id"] == target]
    else:
        chosen = [row for row in rows if row["session"] == explicit["session"]
                  and explicit["window"] in (row["name"], row["index"])]
    if len(chosen) != 1:
        raise ValueError(f"{target!r} matches {len(chosen)} windows; name exactly one window, preferably by its @N id.")
    window = chosen[0]
    if window["tag"] and window["tag"] != session:
        raise ValueError(f"Window {window['id']} ({window['session']}:{window['name']}) is already tagged for another agent's session; untag it there first.")
    others = [row for row in rows if row["tag"] == session and row["id"] != window["id"]]
    if others:
        raise ValueError(f"{name!r} is already tagged on window {others[0]['id']}; untag it there first.")
    for option, value in (("@agent-session", session), ("@agent", name)):
        tmux_call(tmux, server, "set-option", "-w", "-t", window["id"], option, value)
    return f"{window['id']}: tagged for {name} ({server_label(server)})"


def absolute_path(value):
    path = Path(value)
    if not path.is_absolute():
        raise argparse.ArgumentTypeError("Resolve alpha paths to absolute local paths first.")
    return path.resolve()


def positive_seconds(value):
    seconds = float(value)
    if not 0 < seconds <= 86400:
        raise argparse.ArgumentTypeError("Expected seconds greater than zero and at most 86400.")
    return seconds


def main():
    # Roll names and participant names are Unicode, regardless of the host locale.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "metadata", "append", "watch", "register", "window", "tag-window"):
        command = commands.add_parser(name)
        command.add_argument("--roll", type=absolute_path, required=True)
        if name in ("init", "metadata"):
            command.add_argument("--metadata", type=absolute_path, required=True, help="Complete proposed frontmatter as YAML, without --- delimiters")
        elif name == "register":
            command.add_argument("--participant", type=absolute_path, required=True, help="One new participant as YAML")
        elif name in ("window", "tag-window"):
            command.add_argument("--participant", required=True, help="Participant name as the roll records it")
            command.add_argument("--tmux-server", help="tmux socket name (tmux -L); omit for the default server")
            if name == "tag-window":
                command.add_argument("--window", required=True, help="tmux target of the window to tag")
        elif name == "append":
            command.add_argument("--message-id", required=True)
            command.add_argument("--sender", required=True)
            command.add_argument("--body", type=absolute_path, required=True)
            command.add_argument("--roll-ref", required=True, help="Alpha path used in the Curator notification")
            command.add_argument("--notify-timeout", type=positive_seconds, default=20)
        else:
            command.add_argument("--after", help="Last handled message ID; default replays existing messages")
            command.add_argument("--once", action="store_true")
            command.add_argument("--poll-seconds", type=positive_seconds, default=1)
            command.add_argument("--health-seconds", type=positive_seconds, default=300)
    args = parser.parse_args()
    # Discover the external program up front; a missing notifier must not erase a message.
    codex = shutil.which("codex") if args.command == "append" else None
    try:
        if args.command == "init":
            initialize(args.roll, args.metadata.read_text(encoding="utf-8"))
        elif args.command == "metadata":
            change_metadata(args.roll, args.metadata.read_text(encoding="utf-8"))
        elif args.command == "register":
            print(register(args.roll, args.participant.read_text(encoding="utf-8")))
        elif args.command in ("window", "tag-window") and args.tmux_server is not None and not re.fullmatch(IDENTIFIER, args.tmux_server):
            raise ValueError("--tmux-server must name a server (letters, digits, underscores, dots, colons or hyphens); omit it to use the default server.")
        elif args.command == "window":
            print(find_window(args.roll, args.participant, args.tmux_server))
        elif args.command == "tag-window":
            print(tag_window(args.roll, args.participant, args.window, args.tmux_server))
        elif args.command == "watch":
            watch(args.roll, args.after, args.once, args.poll_seconds, args.health_seconds)
        else:
            if not re.fullmatch(r"@[^/`\r\n]+/[^`\r\n]+", args.roll_ref):
                raise ValueError("--roll-ref must be an alpha path to this roll.")
            outcome, meta = append(args.roll, args.sender, args.message_id, args.body.read_text(encoding="utf-8"))
            print(f"{args.message_id}: {outcome}", flush=True)
            try:
                print(notify(meta, args.sender, args.message_id, args.roll_ref, codex, args.notify_timeout))
            except (OSError, ValueError, subprocess.TimeoutExpired) as error:
                parser.exit(3, f"log_append: message saved, notification not confirmed: {error}\nRetry the identical append to retry delivery; do not invent a new message ID.\n")
    except (OSError, ValueError, yaml.YAMLError, subprocess.SubprocessError) as error:
        parser.exit(1, f"log_append: {error}\n")
    except KeyboardInterrupt:
        parser.exit(130, "log_append: stopped\n")


if __name__ == "__main__":
    main()
