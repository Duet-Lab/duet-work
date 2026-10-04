"""Source: a claude.ai conversation as the site's own API returns it — the
JSON the chat page itself loads (how to get one: the skill's
references/session_history_converter/chrome-exporters.md).

Unlike the Chrome exporter's markdown (claude_export), which keeps only the
names of the tools that were called, this JSON carries every tool call with
its input. A turn can therefore include tool calls, the responses written
between them, and an interrupt where the person stopped a reply.

The JSON holds the whole message tree. Only the thread that ends in
`current_leaf_message_uuid` is rendered — the conversation as the person
last saw it; regenerated replies and edited prompts on side branches stay
in the source file. So do thinking summaries, tool results, citations and
the text of attached files: this converter renders what was said, not how
it was produced, and an attachment or image is a marker line under the
prompt, not its content.
"""

import json
import sys
from pathlib import Path

from turns import Atom
from sources.claude_jsonl import parse_timestamp

CANCELED = "user_canceled"


def load(path: Path) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return data if isinstance(data, dict) else None


def detect(path: Path) -> bool:
    if path.suffix.lower() != ".json":
        return False
    data = load(path)
    return data is not None and isinstance(data.get("chat_messages"), list) and "current_leaf_message_uuid" in data


def main_thread(data: dict) -> list[dict]:
    """The messages from the first prompt down to the current leaf, in order."""
    by_uuid = {m["uuid"]: m for m in data["chat_messages"]}
    thread = []
    message = by_uuid.get(data["current_leaf_message_uuid"])
    while message is not None:
        thread.append(message)
        message = by_uuid.get(message.get("parent_message_uuid"))
    return thread[::-1]


def tool_name(raw: str) -> str:
    """An MCP tool arrives as `<server>:<tool>`; the colon would collide with
    the one in our `Tool_<Name>:NN` heading, so it becomes `__`, the
    separator Claude Code uses for the same thing."""
    return raw.replace(":", "__")


def prompt_text(message: dict) -> str:
    """The person's words, then one marker line per attached file or image.
    The message's own `text` field is empty in this API; the words are in
    its text blocks."""
    words = "\n\n".join(b.get("text", "") for b in message.get("content", []) if b.get("type") == "text").strip("\n")
    markers = [f"[Attachment: {a.get('file_name') or 'unnamed'}]" for a in message.get("attachments", [])]
    for f in message.get("files", []):
        label = "Image" if f.get("file_kind") == "image" else "File"
        markers.append(f"[{label}: {f.get('file_name') or 'unnamed'}]")
    return "\n\n".join(part for part in (words, "\n".join(markers)) if part)


def reply_atoms(message: dict, turn: str | None) -> list[Atom]:
    atoms: list[Atom] = []
    for block in message.get("content", []):
        kind = block.get("type")
        ts = parse_timestamp(block.get("start_timestamp") or message.get("created_at"))
        if kind == "text":
            if block.get("text", "").strip():
                atoms.append(Atom("response", text=block["text"], timestamp=ts, turn_id=turn))
        elif kind == "tool_use":
            data = block.get("input") or {}
            if not isinstance(data, dict):
                data = {"input": data}
            atoms.append(Atom("tool_call", tool_name=tool_name(block.get("name", "?")), tool_input=data, timestamp=ts, turn_id=turn))
        elif kind in ("thinking", "tool_result"):
            continue
        else:
            print(f"warning: unknown content block type {kind!r}, skipped", file=sys.stderr)
    if message.get("stop_reason") == CANCELED:
        atoms.append(Atom("interrupt", timestamp=parse_timestamp(message.get("created_at")), turn_id=turn))
    return atoms


def load_atoms(path: Path) -> list[Atom]:
    """Every atom carries the uuid of the prompt that opened its turn. A
    reply the person stopped before any text was written leaves no response
    behind; without the explicit turn the next prompt would be folded into
    the stopped one, and turn numbers would drift from prompt numbers."""
    atoms: list[Atom] = []
    turn = None
    for message in main_thread(load(path)):
        if message.get("sender") == "human":
            turn = message["uuid"]
            atoms.append(Atom("prompt", text=prompt_text(message), timestamp=parse_timestamp(message.get("created_at")), turn_id=turn))
        else:
            atoms.extend(reply_atoms(message, turn))
    return atoms
