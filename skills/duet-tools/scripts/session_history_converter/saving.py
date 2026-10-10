"""Saving a conversation as a folder of its own in our layout — the part that
is the same for every source, so it lives here and not in any one entry
script:

    <dest>/<YYMMDD>_<HHMM>_<Client>_<Name>/
        <the source file, copied in as it was>
        01_MMDD_HHMM.md, 02_..., one turn file per human prompt

With `dialogue_only` the folder holds the turn files alone, and they carry
prompts and responses without tool calls.

`<YYMMDD>_<HHMM>` is when the conversation started, `<Client>` names what
answered (ClaudeCodeFable, Codex, ClaudeChat, ChatGPT, Gemini, GoogleAI, DeepSeek), `<Name>` is the
person's own title for it; `<dest>`, where the folder goes, is the
person's choice too. A source that carries no timestamps gets only
`<YYMMDD>` in the folder name, and the person has to supply that date; one
that knows only the day of its first prompt gets `<YYMMDD>` from it.
"""

import shutil
from datetime import datetime
from pathlib import Path

from turns import Atom, render_turn, split_turns, turn_filename


def folder_name(start: datetime | None, client: str, name: str, date_only: bool = False) -> str:
    if start is None:
        raise ValueError("a start time is needed to name the folder")
    date_only = date_only or not isinstance(start, datetime)  # a bare date has no hour to show
    stamp = f"{start:%y%m%d}" if date_only else f"{start:%y%m%d_%H%M}"
    return f"{stamp}_{client}_{name}"


def first_timestamp(atoms: list[Atom]) -> datetime | None:
    return next((a.timestamp for a in atoms if a.timestamp), None)


def dialogue_only_turn(turn_atoms: list[Atom]) -> list[Atom]:
    """A turn without its tool calls: prompts, responses and interrupts stay.
    Applied to a turn that is already split, never to the whole conversation:
    split_turns reads turn boundaries from what precedes a prompt, so dropping
    tool calls first would move those boundaries."""
    return [a for a in turn_atoms if a.kind != "tool_call"]


def save_as_folder(source_path: Path, atoms: list[Atom], dest: Path, client: str, name: str, start: datetime | None = None, date_only: bool = False, dialogue_only: bool = False) -> Path:
    """Creates the folder, copies the source in, writes the turn files.
    `start` defaults to the first timestamp in the conversation. An existing
    folder is reused, so re-running after more turns arrived refreshes the
    same place; turn files from an earlier, longer run are not deleted.

    `dialogue_only` keeps only what was said: tool calls are left out of the
    turn files and the source is not copied in, because a raw session holds
    the same tool calls together with their results. A source copy already in
    the folder from an earlier full save is left alone."""
    start = start or first_timestamp(atoms)
    out_dir = dest / folder_name(start, client, name, date_only)
    out_dir.mkdir(parents=True, exist_ok=True)
    copied = out_dir / source_path.name
    if not dialogue_only and source_path.resolve() != copied.resolve():
        shutil.copyfile(source_path, copied)
    for n, turn_atoms in enumerate(split_turns(atoms), start=1):
        shown = dialogue_only_turn(turn_atoms) if dialogue_only else turn_atoms
        (out_dir / turn_filename(n, turn_atoms)).write_text(render_turn(n, shown), encoding="utf-8")
    return out_dir
