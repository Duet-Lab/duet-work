"""saving.py and save.py: the folder every source is saved into, and the
generic entry point that gets there from any export convert.py recognizes."""

import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import pytest

from saving import folder_name, save_as_folder
from sources import claude_export
from turns import Atom

CONVERTER_DIR = Path(__file__).resolve().parents[2] / "scripts" / "session_history_converter"
FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_folder_name_is_start_client_name():
    start = datetime(2026, 9, 27, 1, 53, tzinfo=timezone.utc)
    assert folder_name(start, "ClaudeCodeFable", "РаботаНадФормами") == "260927_0153_ClaudeCodeFable_РаботаНадФормами"
    assert folder_name(start, "GoogleAI", "Эталоны", date_only=True) == "260927_GoogleAI_Эталоны"
    assert folder_name(date(2026, 9, 15), "GoogleAI", "Языки") == "260915_GoogleAI_Языки"  # the source knows only the day


def test_folder_name_needs_a_start():
    with pytest.raises(ValueError):
        folder_name(None, "Claude", "x")


def test_save_as_folder_copies_source_and_writes_turns(tmp_path: Path):
    source = FIXTURES_DIR / "claude_export" / "basic" / "input.md"
    atoms = claude_export.load_atoms(source)
    out_dir = save_as_folder(source, atoms, tmp_path / "source", "ClaudeChat", "Столицы")
    assert out_dir == tmp_path / "source" / "260915_1131_ClaudeChat_Столицы"  # first timestamp in the export
    assert sorted(p.name for p in out_dir.iterdir()) == ["01_0915_1131.md", "input.md"]


def test_dialogue_only_drops_tool_calls_and_the_source_copy(tmp_path: Path):
    source = tmp_path / "session.jsonl"
    source.write_text("{}\n", encoding="utf-8")
    t = lambda minute: datetime(2026, 10, 10, 10, minute)
    atoms = [
        Atom("prompt", text="first question", timestamp=t(1)),
        Atom("tool_call", tool_name="exec", tool_input={"input": "cat secret"}),
        Atom("response", text="interim note", timestamp=t(2)),
        Atom("tool_call", tool_name="exec", tool_input={"input": "ls"}),
        # an inline prompt: it follows a tool call, so it stays in turn 1
        Atom("prompt", text="one more thing", timestamp=t(3)),
        Atom("response", text="first answer", timestamp=t(4)),
        Atom("prompt", text="second question", timestamp=t(5)),
        Atom("response", text="second answer", timestamp=t(6)),
    ]
    full = save_as_folder(source, atoms, tmp_path / "full", "Codex", "Sample")
    slim = save_as_folder(source, atoms, tmp_path / "slim", "Codex", "Sample", dialogue_only=True)

    turn_files = ["01_1010_1001.md", "02_1010_1005.md"]
    assert sorted(p.name for p in full.iterdir()) == turn_files + ["session.jsonl"]
    assert sorted(p.name for p in slim.iterdir()) == turn_files  # same turn boundaries, no source copy

    first = (slim / turn_files[0]).read_text(encoding="utf-8")
    assert "Tool_" not in first and "cat secret" not in first
    for kept in ("first question", "interim note", "one more thing", "first answer"):
        assert kept in first
    assert "## Tool_exec:01" in (full / turn_files[0]).read_text(encoding="utf-8")


def _run_save(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(CONVERTER_DIR / "save.py"), *args], capture_output=True, text=True)


def test_save_py_names_the_client_after_the_source(tmp_path: Path):
    source = FIXTURES_DIR / "claude_export" / "basic" / "input.md"
    result = _run_save(str(source), "--dest", str(tmp_path), "--name", "Столицы")
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "260915_1131_ClaudeChat_Столицы" / "01_0915_1131.md").is_file()
    assert result.stdout.strip() == f"1 turns -> {tmp_path / '260915_1131_ClaudeChat_Столицы'}"


@pytest.mark.parametrize(
    "fixture, folder",
    [("gemini_export/basic", "260927_2211_Gemini_Бугор"), ("chatgpt_export/basic", "260927_2154_ChatGPT_Бугор")],
)
def test_save_py_names_the_exporter_family_clients(tmp_path: Path, fixture: str, folder: str):
    result = _run_save(str(FIXTURES_DIR / fixture / "input.md"), "--dest", str(tmp_path), "--name", "Бугор")
    assert result.returncode == 0, result.stderr
    assert (tmp_path / folder / "input.md").is_file()


def test_save_py_refuses_an_undated_source_without_start(tmp_path: Path):
    source = FIXTURES_DIR / "google_export" / "basic" / "input.md"
    result = _run_save(str(source), "--dest", str(tmp_path), "--name", "Эталоны")
    assert result.returncode != 0
    assert "--start" in result.stderr


def test_save_py_names_the_folder_by_day_when_the_page_shows_only_days(tmp_path: Path):
    source = FIXTURES_DIR / "google_saved_page" / "date_labels" / "input.html"
    result = _run_save(str(source), "--dest", str(tmp_path), "--name", "Языки")
    assert result.returncode == 0, result.stderr
    out_dir = tmp_path / "260915_GoogleAI_Языки"
    assert sorted(p.name for p in out_dir.iterdir()) == ["01_0915.md", "02_0915.md", "03_0917.md", "input.html"]


def test_save_py_dates_an_undated_source_from_start(tmp_path: Path):
    source = FIXTURES_DIR / "google_export" / "basic" / "input.md"
    result = _run_save(str(source), "--dest", str(tmp_path), "--name", "Эталоны", "--start", "260926")
    assert result.returncode == 0, result.stderr
    out_dir = tmp_path / "260926_GoogleAI_Эталоны"
    assert sorted(p.name for p in out_dir.iterdir()) == ["01.md", "02.md", "input.md"]
