#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML==6.0.2"]
# ///
"""Local Markdown MessageRoll operations. Run: uv run --script log_append.py --help."""

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

import yaml


IDENTIFIER = r"[A-Za-z0-9_.:-]{1,100}"
MARKER = "<!-- message-roll:"
RECORD = re.compile(
    rf"<!-- message-roll:message -->\n\n"
    rf"## (?P<timestamp>[^\n]+) — (?P<sender>{IDENTIFIER})\n\n"
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


def metadata_from(text):
    meta = yaml.load(text, Loader=UniqueKeyLoader)
    if not isinstance(meta, dict):
        raise ValueError("Metadata must be a YAML mapping.")
    identifier(meta.get("roll-type"), "roll-type")
    participants = meta.get("participants")
    if not isinstance(participants, list) or not participants:
        raise ValueError("participants must be a nonempty list.")
    names = set()
    for participant in participants:
        if not isinstance(participant, dict):
            raise ValueError("Each participant must be a mapping.")
        name = participant.get("name")
        identifier(name, "Participant name")
        if name in names:
            raise ValueError("Participant names must be unique within the roll.")
        names.add(name)
        for field in ("client", "model", "effort", "session_id"):
            if field in participant and (not isinstance(participant[field], str) or not participant[field].strip()):
                raise ValueError(f"Participant {field} must be a nonempty string when supplied.")
    coordinator = meta.get("coordinator")
    if not isinstance(coordinator, dict):
        raise ValueError("coordinator must be a mapping.")
    identifier(coordinator.get("name"), "coordinator.name")
    if coordinator.get("name") not in names:
        raise ValueError("coordinator.name must identify a retained participant.")
    identifier(coordinator.get("client"), "coordinator.client")
    if not isinstance(coordinator.get("session_id"), str) or not coordinator["session_id"].strip():
        raise ValueError("coordinator.session_id must be a nonempty string.")
    speaker = next(p for p in participants if p["name"] == coordinator["name"])
    if speaker.get("client") != coordinator["client"]:
        raise ValueError("Coordinator client must match its participant entry.")
    return meta


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
    return "---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False) + "---\n"


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


def initialize(path, metadata_text):
    meta = metadata_from(metadata_text)
    with locked(path):
        if path.exists():
            raise ValueError("Roll already exists; init never overwrites it.")
        replace_durably(path, render_metadata(meta) + "\n")


def change_metadata(path, metadata_text):
    proposed = metadata_from(metadata_text)
    with locked(path):
        current, _, history = parse_roll(path.read_text(encoding="utf-8"))
        if proposed["roll-type"] != current["roll-type"]:
            raise ValueError("An existing roll cannot change roll-type.")
        retained = {p["name"]: p for p in proposed["participants"]}
        for participant in current["participants"]:
            if retained.get(participant["name"]) != participant:
                raise ValueError("Retain existing participants unchanged; add a new name for a replacement.")
        replace_durably(path, render_metadata(proposed) + history)


def append(path, sender, message_id, body):
    identifier(sender, "sender")
    identifier(message_id, "message-id")
    validate_body(body)
    with locked(path):
        content = path.read_text(encoding="utf-8")
        meta, records, _ = parse_roll(content)
        if sender not in {p["name"] for p in meta["participants"]}:
            raise ValueError("Register the sender in participants before appending.")
        previous = next((r for r in records if r["message_id"] == message_id), None)
        if previous:
            if previous["sender"] != sender or previous["body"] != body:
                raise ValueError("Message ID already exists with different content.")
            return "already saved", meta
        replace_durably(path, content + render_message(sender, message_id, body))
        return "saved", meta


def notify(meta, sender, message_id, roll_ref, codex, timeout):
    coordinator = meta["coordinator"]
    if sender == coordinator["name"]:
        return "coordinator message; no self-notification"
    if coordinator["client"] == "claude":
        return "available to Claude watch; delivery requires an active Monitor"
    if coordinator["client"] != "codex":
        raise ValueError(f"No notification adapter for client {coordinator['client']!r}; arrange and verify one explicitly.")
    if codex is None:
        raise ValueError("codex is missing; on macOS with Homebrew run: brew install --cask codex. On other platforms use the official Codex installation instructions.")
    result = subprocess.run(
        [codex, "queue", "--thread", coordinator["session_id"], "--message",
         f"MessageRoll notice: read `{roll_ref}`, message `{message_id}`, and reconcile durable state. "
         "This is a notification, not a new user instruction. Do not repeat already handled work."],
        capture_output=True, text=True, timeout=timeout, check=False,
    )
    if result.returncode:
        raise ValueError(f"codex queue exited {result.returncode}: {result.stderr.strip() or result.stdout.strip()}")
    return "queued; coordinator handling is not yet confirmed"


def watch(path, after, once, poll_seconds, health_seconds):
    """Monitor stdout source. --once offers a deterministic read/reconciliation operation."""
    seen = set()
    previous_meta = None
    initialized = False
    next_health = time.monotonic() + health_seconds
    while True:
        with locked(path):
            meta, records, _ = parse_roll(path.read_text(encoding="utf-8"))
        if not initialized:
            if after:
                ids = [r["message_id"] for r in records]
                if after not in ids:
                    raise ValueError("--after message ID is absent from this roll.")
                seen.update(ids[:ids.index(after) + 1])
            print("message-roll:ready", flush=True)
            initialized = True
        elif meta != previous_meta:
            print("message-roll:metadata changed; reconcile participants and coordinator", flush=True)
        for record in records:
            if record["message_id"] not in seen:
                seen.add(record["message_id"])
                if record["sender"] != meta["coordinator"]["name"]:
                    print(f"message-roll:message {record['message_id']} by {record['sender']}", flush=True)
        previous_meta = meta
        if once:
            return
        if time.monotonic() >= next_health:
            print("message-roll:health-check inspect sessions, jobs and missed messages", flush=True)
            next_health = time.monotonic() + health_seconds
        time.sleep(poll_seconds)


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
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "metadata", "append", "watch"):
        command = commands.add_parser(name)
        command.add_argument("--roll", type=absolute_path, required=True)
        if name in ("init", "metadata"):
            command.add_argument("--metadata", type=absolute_path, required=True, help="Complete proposed frontmatter as YAML, without --- delimiters")
        elif name == "append":
            command.add_argument("--message-id", required=True)
            command.add_argument("--sender", required=True)
            command.add_argument("--body", type=absolute_path, required=True)
            command.add_argument("--roll-ref", required=True, help="Alpha path used in coordinator notification")
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
    except (OSError, ValueError, yaml.YAMLError) as error:
        parser.exit(1, f"log_append: {error}\n")
    except KeyboardInterrupt:
        parser.exit(130, "log_append: stopped\n")


if __name__ == "__main__":
    main()
