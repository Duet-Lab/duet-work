#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML==6.0.2"]
# ///
"""MessageRoll contract: real CLI, temporary files and concurrent processes.
Only the external Codex executable is substituted; no live model sessions are used.
Run: uv run --script scripts/test_log_append.py
"""

from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import selectors
import subprocess
import sys
import tempfile
import unittest

import yaml

SCRIPT = Path(__file__).with_name("log_append.py")


class RollTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.roll = self.root / "discussion.md"
        self.body = self.root / "body.md"
        # Non-ASCII on purpose: the roll must round-trip UTF-8 bodies byte for byte.
        self.body.write_text("## Результат\n\nМнение и `@ABC001/report.md`.\n```python\nprint('да')\n```\n", encoding="utf-8")
        self.environment = dict(os.environ)
        self.environment.update(PATH=str(self.root), ROLL=str(self.roll), CAPTURE=str(self.root / "queue.json"))
        self.codex = self.root / "codex"
        self.codex.write_text(
            f"#!{sys.executable}\n"
            "import json, os, pathlib, sys\n"
            "roll = pathlib.Path(os.environ['ROLL']).read_text(encoding='utf-8')\n"
            "assert '<!-- message-roll:end -->' in roll, 'notification preceded durable message'\n"
            "pathlib.Path(os.environ['CAPTURE']).write_text(json.dumps(sys.argv[1:]), encoding='utf-8')\n"
            "if 'QUEUE_OUTPUT' in os.environ:\n"
            "    output = pathlib.Path(os.environ['QUEUE_OUTPUT']).read_bytes()\n"
            "    sys.stdout.buffer.write(output); sys.stderr.buffer.write(output)\n"
            "sys.exit(int(os.environ.get('QUEUE_EXIT', '0')))\n", encoding="utf-8")
        self.codex.chmod(0o700)

    def c_locale(self, **extra):
        """The host environment forced to the C locale with ASCII stdio, plus any extra variables."""
        return {**self.environment, "LC_ALL": "C", "PYTHONUTF8": "0",
                "PYTHONCOERCECLOCALE": "0", "PYTHONIOENCODING": "ascii", **extra}

    def metadata(self, client="claude"):
        return {
            "roll-type": "dev-curation",
            "participants": [
                {"name": "Curator_1", "client": client, "role": "Curator", "session_id": "session-one"},
                {"name": "Developer_Gemini_1", "client": "gemini", "role": "Developer", "session_id": "developer-one", "model": "test-model", "effort": "test-effort"},
                {"name": "Alex", "client": "human", "role": "User"},
            ],
        }

    def command(self, action, *arguments, roll=None, environment=None):
        return subprocess.run(
            [sys.executable, str(SCRIPT), action, "--roll", str(roll or self.roll), *arguments],
            capture_output=True, text=True, encoding="utf-8", timeout=20, env=environment or self.environment,
        )

    def save_metadata_input(self, meta, name="metadata.yaml"):
        path = self.root / name
        path.write_text(yaml.safe_dump(meta, allow_unicode=True, sort_keys=False), encoding="utf-8")
        return path

    def initialize(self, meta=None, roll=None):
        result = self.command("init", "--metadata", str(self.save_metadata_input(meta or self.metadata())), roll=roll)
        self.assertEqual(result.returncode, 0, result.stderr)

    def send(self, message_id="m1", sender="Developer_Gemini_1", **options):
        return self.command("append", "--message-id", message_id, "--sender", sender,
                            "--body", str(self.body), "--roll-ref", "@ABC001/rolls/discussion.md", **options)

    def register(self, participant, **options):
        return self.command("register", "--participant", str(self.save_metadata_input(participant, "participant.yaml")), **options)

    def legacy(self):
        meta = self.metadata()
        meta["coordinator"] = {"name": "Curator_1", "client": "claude", "session_id": "session-one"}
        for p in meta["participants"]:
            p.pop("role")
            p.pop("session_id", None)
        meta["participants"][-1].pop("client")
        meta["tmux_session"] = "abc001"
        meta["participants"][1]["tmux"] = "2:developer"
        self.roll.write_text("---\n" + yaml.safe_dump(meta, sort_keys=False) + "---\n\n", encoding="utf-8")
        return meta

    def read_metadata(self):
        return yaml.safe_load(self.roll.read_text(encoding="utf-8").split("---\n")[1])

    def test_append_preserves_readable_markdown_without_development_fields(self):
        meta = self.metadata()
        meta["roll-type"] = "round-table"
        self.initialize(meta)
        result = self.send()
        self.assertEqual(result.returncode, 0, result.stderr)
        content = self.roll.read_text(encoding="utf-8")
        self.assertIn(self.body.read_text(encoding="utf-8"), content)
        self.assertIn(" — Developer_Gemini_1\n", content)
        self.assertNotIn("**Task:**", content)

    def test_long_frontmatter_values_stay_on_one_line(self):
        meta = self.metadata()
        meta["purpose"] = ", ".join(["Очень длинное назначение ролла"] * 8)
        self.initialize(meta)
        header = self.roll.read_text(encoding="utf-8").split("---\n")[1]
        self.assertIn("\npurpose: " + meta["purpose"] + "\n", header)

    def test_init_refuses_to_overwrite_existing_roll(self):
        self.initialize()
        before = self.roll.read_bytes()
        result = self.command("init", "--metadata", str(self.save_metadata_input(self.metadata())))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.roll.read_bytes(), before)

    def test_missing_cli_arguments_are_distinct_from_delivery_failure(self):
        result = self.command("append")
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.roll.exists())
        self.assertNotIn("message saved", result.stderr)

    def test_duplicate_yaml_keys_are_rejected(self):
        path = self.save_metadata_input(self.metadata())
        path.write_text(path.read_text(encoding="utf-8") + "roll-type: surprise\n", encoding="utf-8")
        result = self.command("init", "--metadata", str(path))
        self.assertEqual(result.returncode, 1)
        self.assertFalse(self.roll.exists())

    def test_duplicate_participant_names_are_rejected(self):
        meta = self.metadata()
        meta["participants"].append(meta["participants"][1].copy())
        result = self.command("init", "--metadata", str(self.save_metadata_input(meta)))
        self.assertEqual(result.returncode, 1)
        self.assertIn("unique", result.stderr)

    def test_legacy_coordinator_is_rejected_on_init(self):
        meta = self.metadata()
        meta["coordinator"] = {"name": ["not-a-name"]}
        result = self.command("init", "--metadata", str(self.save_metadata_input(meta)))
        self.assertEqual(result.returncode, 1)
        self.assertIn("older frontmatter format", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_identical_retry_preserves_file_bytes(self):
        self.initialize()
        self.assertEqual(self.send().returncode, 0)
        before = self.roll.read_bytes()
        result = self.send()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.roll.read_bytes(), before)

    def test_conflicting_retry_does_not_overwrite_message(self):
        self.initialize()
        self.send()
        before = self.roll.read_bytes()
        self.body.write_text("Changed reply", encoding="utf-8")
        result = self.send()
        self.assertEqual(result.returncode, 1)
        self.assertIn("different content", result.stderr)
        self.assertEqual(self.roll.read_bytes(), before)

    def test_unregistered_sender_is_rejected_without_mutation(self):
        self.initialize()
        before = self.roll.read_bytes()
        result = self.send(sender="Stranger")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.roll.read_bytes(), before)

    def test_user_can_author_a_message(self):
        self.initialize()
        result = self.send(sender="Alex")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(" — Alex\n", self.roll.read_text(encoding="utf-8"))

    def test_invalid_message_body_is_rejected(self):
        self.initialize()
        before = self.roll.read_bytes()
        for body in ("  \n", "<!-- message-roll:end -->"):
            with self.subTest(body=body):
                self.body.write_text(body, encoding="utf-8")
                self.assertEqual(self.send().returncode, 1)
                self.assertEqual(self.roll.read_bytes(), before)

    def test_corrupt_record_blocks_append_without_truncation(self):
        self.initialize()
        self.send()
        self.roll.write_bytes(self.roll.read_bytes()[:-10])
        before = self.roll.read_bytes()
        result = self.send("m2")
        self.assertEqual(result.returncode, 1)
        self.assertIn("incomplete", result.stderr)
        self.assertEqual(self.roll.read_bytes(), before)

    def test_missing_boundary_between_messages_blocks_append(self):
        self.initialize()
        self.send("m1")
        self.send("m2")
        self.roll.write_text(self.roll.read_text(encoding="utf-8").replace("<!-- message-roll:end -->", "", 1), encoding="utf-8")
        before = self.roll.read_bytes()
        self.assertEqual(self.send("m3").returncode, 1)
        self.assertEqual(self.roll.read_bytes(), before)

    def test_metadata_update_preserves_published_messages_exactly(self):
        self.initialize()
        self.send()
        history = self.roll.read_text(encoding="utf-8").split("\n---\n", 1)[1]
        meta = self.metadata()
        meta["participants"].append({"name": "Curator_2", "client": "codex", "role": "Curator", "session_id": "session-two"})
        meta["participants"].append({"name": "Reviewer_Codex_Security_1", "client": "codex", "role": "Reviewer", "session_id": "reviewer-one"})
        result = self.command("metadata", "--metadata", str(self.save_metadata_input(meta)))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.roll.read_text(encoding="utf-8").split("\n---\n", 1)[1], history)
        self.assertIn("session-one", self.roll.read_text(encoding="utf-8"))
        self.assertEqual(self.send("m2", sender="Reviewer_Codex_Security_1").returncode, 0)

    def test_metadata_refuses_to_remove_disconnected_participant(self):
        self.initialize()
        before = self.roll.read_bytes()
        meta = self.metadata()
        meta["participants"].pop(1)
        result = self.command("metadata", "--metadata", str(self.save_metadata_input(meta)))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.roll.read_bytes(), before)

    def test_metadata_refuses_to_rewrite_participant_identity(self):
        self.initialize()
        meta = self.metadata()
        meta["participants"][1]["model"] = "replacement-model"
        result = self.command("metadata", "--metadata", str(self.save_metadata_input(meta)))
        self.assertEqual(result.returncode, 1)
        self.assertIn("Retain existing participants", result.stderr)

    def test_simultaneous_metadata_and_messages_do_not_lose_history(self):
        self.initialize()
        meta = self.metadata()
        meta["participants"].append({"name": "Developer_Gemini_2", "client": "gemini", "role": "Developer", "session_id": "developer-two"})
        path = self.save_metadata_input(meta, "replacement.yaml")
        with ThreadPoolExecutor(max_workers=8) as pool:
            futures = [pool.submit(self.send, f"m{i}") for i in range(16)]
            futures += [pool.submit(self.send, f"m{i}") for i in range(16)]
            futures.append(pool.submit(self.command, "metadata", "--metadata", str(path)))
            results = [f.result() for f in futures]
        for result in results:
            self.assertEqual(result.returncode, 0, result.stderr)
        content = self.roll.read_text(encoding="utf-8")
        self.assertEqual(content.count("<!-- message-roll:end -->"), 16)
        self.assertIn("Developer_Gemini_2", content)
        for i in range(16):
            self.assertEqual(content.count(f"**Message:** `m{i}`"), 1)

    def test_codex_notification_uses_current_session_after_message_is_saved(self):
        self.initialize(self.metadata("codex"))
        meta = self.metadata("codex")
        meta["participants"].append({"name": "Curator_2", "client": "codex", "role": "Curator", "session_id": "session-two"})
        self.command("metadata", "--metadata", str(self.save_metadata_input(meta)))
        result = self.send()
        self.assertEqual(result.returncode, 0, result.stderr)
        args = json.loads((self.root / "queue.json").read_text(encoding="utf-8"))
        self.assertEqual(args[:3], ["queue", "--thread", "session-two"])
        self.assertIn("@ABC001/rolls/discussion.md", args[4])
        self.assertIn("`m1`", args[4])

    def test_queue_failure_keeps_message_and_identical_retry_redelivers(self):
        self.initialize(self.metadata("codex"))
        result = self.send(environment=dict(self.environment, QUEUE_EXIT="7"))
        self.assertEqual(result.returncode, 3)
        self.assertIn("message saved", result.stderr)
        before = self.roll.read_bytes()
        (self.root / "queue.json").unlink()
        retry = self.send()
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual(self.roll.read_bytes(), before)
        self.assertTrue((self.root / "queue.json").exists())

    def test_notifier_utf8_output_is_read_under_c_locale(self):
        self.initialize(self.metadata("codex"))
        output = self.root / "queue-output.txt"
        output.write_bytes("Уведомление поставлено в очередь\n".encode("utf-8"))
        queued = self.send(environment=self.c_locale(QUEUE_OUTPUT=str(output)))
        self.assertEqual(queued.returncode, 0, queued.stderr)
        self.assertIn("queued; Curator handling is not yet confirmed", queued.stdout)
        output.write_bytes("Очередь недоступна\n".encode("utf-8"))
        failed = self.send("m2", environment=self.c_locale(QUEUE_OUTPUT=str(output), QUEUE_EXIT="7"))
        self.assertEqual(failed.returncode, 3)
        self.assertIn("message saved", failed.stderr)
        self.assertIn("codex queue exited 7: Очередь недоступна", failed.stderr)
        self.assertNotIn("Traceback", failed.stderr)

    def test_missing_codex_reports_installation_without_losing_message(self):
        self.initialize(self.metadata("codex"))
        self.codex.unlink()
        result = self.send()
        self.assertEqual(result.returncode, 3)
        self.assertIn("brew install --cask codex", result.stderr)
        self.assertIn("**Message:** `m1`", self.roll.read_text(encoding="utf-8"))

    def test_queue_timeout_preserves_the_saved_message(self):
        self.initialize(self.metadata("codex"))
        self.codex.write_text(f"#!{sys.executable}\nwhile True: pass\n", encoding="utf-8")
        result = self.command("append", "--message-id", "m1", "--sender", "Developer_Gemini_1",
                              "--body", str(self.body), "--roll-ref", "@ABC001/rolls/discussion.md",
                              "--notify-timeout", "0.2")
        self.assertEqual(result.returncode, 3)
        self.assertIn("timed out", result.stderr)
        self.assertIn("**Message:** `m1`", self.roll.read_text(encoding="utf-8"))

    def test_retry_after_coordinator_replacement_uses_new_address(self):
        self.initialize(self.metadata("codex"))
        self.send(environment=dict(self.environment, QUEUE_EXIT="7"))
        meta = self.metadata("codex")
        meta["participants"].append({"name": "Curator_2", "client": "codex", "role": "Curator", "session_id": "session-two"})
        self.command("metadata", "--metadata", str(self.save_metadata_input(meta)))
        self.assertEqual(self.send().returncode, 0)
        args = json.loads((self.root / "queue.json").read_text(encoding="utf-8"))
        self.assertEqual(args[:3], ["queue", "--thread", "session-two"])
        self.assertEqual(self.roll.read_text(encoding="utf-8").count("**Message:** `m1`"), 1)

    def test_coordinator_does_not_notify_itself(self):
        self.initialize(self.metadata("codex"))
        result = self.send(sender="Curator_1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.root / "queue.json").exists())

    def test_unknown_client_retains_message_but_reports_missing_adapter(self):
        self.initialize(self.metadata("another-client"))
        result = self.send()
        self.assertEqual(result.returncode, 3)
        self.assertIn("No notification adapter", result.stderr)
        self.assertIn("**Message:** `m1`", self.roll.read_text(encoding="utf-8"))

    def test_watch_once_emits_only_messages_after_cursor(self):
        self.initialize()
        self.send("m1")
        self.send("m2")
        result = self.command("watch", "--once", "--after", "m1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("message-roll:message m2", result.stdout)
        self.assertNotIn("message-roll:message m1", result.stdout)

    def test_watch_rejects_an_unknown_cursor(self):
        self.initialize()
        result = self.command("watch", "--once", "--after", "absent")
        self.assertEqual(result.returncode, 1)
        self.assertIn("absent", result.stderr)

    def test_watch_does_not_echo_coordinator_messages(self):
        self.initialize()
        self.send(sender="Curator_1")
        result = self.command("watch", "--once")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("message-roll:message", result.stdout)

    def test_live_watch_observes_atomic_replacement(self):
        self.initialize()
        process = subprocess.Popen(
            [sys.executable, str(SCRIPT), "watch", "--roll", str(self.roll)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", env=self.environment,
        )
        try:
            with selectors.DefaultSelector() as selector:
                selector.register(process.stdout, selectors.EVENT_READ)
                self.assertTrue(selector.select(10), "watch did not become ready")
                self.assertEqual(process.stdout.readline().strip(), "message-roll:ready")
                self.assertEqual(self.send().returncode, 0)
                self.assertTrue(selector.select(10), "watch did not report saved message")
                self.assertIn("message-roll:message m1", process.stdout.readline())
        finally:
            process.terminate()
            process.communicate(timeout=10)

    def test_rolls_have_independent_message_namespaces(self):
        self.initialize()
        second = self.root / "second.md"
        self.initialize(roll=second)
        self.assertEqual(self.send().returncode, 0)
        self.assertEqual(self.send(roll=second).returncode, 0)
        self.assertIn("**Message:** `m1`", second.read_text(encoding="utf-8"))

    def test_symlink_alias_preserves_the_same_roll(self):
        self.initialize()
        alias = self.root / "alias.md"
        alias.symlink_to(self.roll)
        result = self.send(roll=alias)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(alias.is_symlink())
        self.assertIn("**Message:** `m1`", self.roll.read_text(encoding="utf-8"))

    def test_legacy_log_is_not_silently_reinterpreted(self):
        self.roll.write_text("<!-- duet-channel:message -->\n", encoding="utf-8")
        before = self.roll.read_bytes()
        result = self.send()
        self.assertEqual(result.returncode, 1)
        self.assertIn("not migrated automatically", result.stderr)
        self.assertEqual(self.roll.read_bytes(), before)

    def test_new_ai_requires_session_and_human_forbids_it(self):
        for client, session in (("codex", None), ("human", "unexpected")):
            meta = self.metadata()
            p = meta["participants"][0]
            p["client"] = client
            p.pop("session_id")
            if session:
                p["session_id"] = session
            result = self.command("init", "--metadata", str(self.save_metadata_input(meta)))
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertFalse(self.roll.exists())

    def test_duplicate_session_rejected_even_across_clients(self):
        meta = self.metadata()
        meta["participants"][1]["session_id"] = "session-one"
        result = self.command("init", "--metadata", str(self.save_metadata_input(meta)))
        self.assertEqual(result.returncode, 1)
        self.assertIn("unique", result.stderr)

    def test_register_is_idempotent_and_never_reuses_name_or_session(self):
        self.initialize()
        participant = {"name": "Architect_1", "role": "Architect", "client": "codex", "session_id": "new-session"}
        self.assertEqual(self.register(participant).returncode, 0)
        before = self.roll.read_bytes()
        self.assertIn("already registered", self.register(participant).stdout)
        for patch in ({"session_id": "changed"}, {"name": "Architect_2"}, {"role": "Curator"}):
            self.assertEqual(self.register({**participant, **patch}).returncode, 1)
            self.assertEqual(self.roll.read_bytes(), before)

    def test_metadata_cannot_reorder_and_new_entry_requires_session(self):
        self.initialize()
        before = self.roll.read_bytes()
        for mutate in (lambda ps: ps.reverse(), lambda ps: ps.append({"name": "Old_1", "role": "Reviewer", "client": "codex"})):
            meta = self.metadata()
            mutate(meta["participants"])
            result = self.command("metadata", "--metadata", str(self.save_metadata_input(meta)))
            self.assertEqual(result.returncode, 1)
            self.assertEqual(self.roll.read_bytes(), before)

    def test_unicode_human_author_and_custom_role(self):
        meta = self.metadata()
        meta["participants"][-1].update(name="Иван Петров", role="Sponsor")
        self.initialize(meta)
        result = self.send(sender="Иван Петров")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(" — Иван Петров\n", self.roll.read_text(encoding="utf-8"))
        for label, environment in (("inherited", self.environment), ("C", self.c_locale())):
            with self.subTest(locale=label):
                result = self.command("watch", "--once", environment=environment)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("message-roll:message m1 by Иван Петров\n", result.stdout)

    def test_unicode_cli_error_under_c_locale(self):
        self.initialize()
        environment = self.c_locale()
        participant = {"name": "Рецензент", "role": "Reviewer", "client": "codex"}
        before = self.roll.read_bytes()
        result = self.register(participant, environment=environment)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Participant 'Рецензент' requires a verified session_id.", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(self.roll.read_bytes(), before)

    def test_no_curator_saves_without_adapter_and_watch_emits_no_message(self):
        meta = self.metadata()
        meta["participants"][0]["role"] = "Observer"
        self.initialize(meta)
        self.codex.unlink()
        result = self.send()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no Curator", result.stdout)
        self.assertNotIn("message-roll:message", self.command("watch", "--once").stdout)
        # Registering a Curator exposes retained messages rather than losing them.
        self.assertEqual(self.register({"name": "NewCurator", "role": "Curator", "client": "claude", "session_id": "new"}).returncode, 0)
        self.assertIn("message-roll:message m1", self.command("watch", "--once").stdout)

    def test_last_curator_not_last_participant_routes(self):
        self.initialize(self.metadata("codex"))
        self.assertEqual(self.register({"name": "NewCurator", "role": "Curator", "client": "codex", "session_id": "new"}).returncode, 0)
        self.assertEqual(self.register({"name": "Last", "role": "Observer", "client": "human"}).returncode, 0)
        self.assertEqual(self.send(sender="Curator_1").returncode, 0)
        args = json.loads((self.root / "queue.json").read_text(encoding="utf-8"))
        self.assertEqual(args[:3], ["queue", "--thread", "new"])
        (self.root / "queue.json").unlink()
        self.assertEqual(self.send("m2", sender="NewCurator").returncode, 0)
        self.assertFalse((self.root / "queue.json").exists())

    def test_concurrent_registration_does_not_drop_any_participant(self):
        self.initialize()
        inputs = [self.save_metadata_input({"name": f"Architect_{i}", "role": "Architect", "client": "codex", "session_id": f"unique-{i}"}, f"participant-{i}.yaml") for i in range(10)]
        with ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(lambda path: self.command("register", "--participant", str(path)), inputs))
        self.assertTrue(all(r.returncode == 0 for r in results), [r.stderr for r in results])
        meta = self.read_metadata()
        self.assertEqual(meta["participants"][:3], self.metadata()["participants"])
        self.assertEqual({p["name"] for p in meta["participants"][3:]}, {f"Architect_{i}" for i in range(10)})

    def test_legacy_missing_codex_target_reports_saved_not_traceback(self):
        self.initialize(self.metadata("codex"))
        # A retained legacy entry is readable, but not a usable delivery address.
        meta = self.read_metadata()
        meta["participants"][0].pop("session_id")
        self.roll.write_text("---\n" + yaml.safe_dump(meta, sort_keys=False) + "---\n\n", encoding="utf-8")
        result = self.send()
        self.assertEqual(result.returncode, 3)
        self.assertIn("no recoverable session_id", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("**Message:** `m1`", self.roll.read_text(encoding="utf-8"))

    def test_tmux_window_requires_session_and_session_cannot_change(self):
        meta = self.metadata()
        meta["participants"][1]["tmux-window"] = "developer"
        result = self.command("init", "--metadata", str(self.save_metadata_input(meta)))
        self.assertEqual(result.returncode, 1)
        meta["tmux-session"] = "abc001"
        self.initialize(meta)
        before = self.roll.read_bytes()
        meta["tmux-session"] = "other"
        self.assertEqual(self.command("metadata", "--metadata", str(self.save_metadata_input(meta))).returncode, 1)
        self.assertEqual(self.roll.read_bytes(), before)

    def test_no_curator_watch_never_emits_health_ticks(self):
        meta = self.metadata()
        meta["participants"][0]["role"] = "Observer"
        self.initialize(meta)
        self.assertEqual(self.send().returncode, 0)
        process = subprocess.Popen(
            [sys.executable, str(SCRIPT), "watch", "--roll", str(self.roll), "--poll-seconds", "0.02", "--health-seconds", "0.05"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", env=self.environment,
        )
        try:
            with self.assertRaises(subprocess.TimeoutExpired):
                process.communicate(timeout=0.4)
        finally:
            process.terminate()
            stdout, stderr = process.communicate(timeout=10)
        self.assertEqual(stdout.strip(), "message-roll:ready", stderr)

    def test_legacy_coordinator_roll_is_rejected_unchanged_by_every_command(self):
        self.legacy()
        before = self.roll.read_bytes()
        participant = self.save_metadata_input({"name": "New", "role": "Reviewer", "client": "codex", "session_id": "new"}, "participant.yaml")
        for arguments in (("append", "--message-id", "m1", "--sender", "Developer_Gemini_1", "--body", str(self.body), "--roll-ref", "@ABC001/roll.md"),
                          ("register", "--participant", str(participant)),
                          ("metadata", "--metadata", str(self.save_metadata_input(self.metadata()))),
                          ("watch", "--once")):
            with self.subTest(command=arguments[0]):
                result = self.command(*arguments)
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("older frontmatter format", result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(self.roll.read_bytes(), before)


class WindowTests(unittest.TestCase):
    """Window lookup and tagging against a fake tmux that serves a fixed window list."""

    metadata = RollTests.metadata
    c_locale = RollTests.c_locale
    command = RollTests.command
    save_metadata_input = RollTests.save_metadata_input
    initialize = RollTests.initialize

    def setUp(self):
        RollTests.setUp(self)
        self.calls = self.root / "tmux-calls.json"
        self.listing = self.root / "tmux-windows.txt"
        self.listing.write_bytes(b"")
        self.environment.update(TMUX_CALLS=str(self.calls), TMUX_WINDOWS=str(self.listing))
        tmux = self.root / "tmux"
        tmux.write_text(
            f"#!{sys.executable}\n"
            "import json, os, pathlib, sys\n"
            "calls = pathlib.Path(os.environ['TMUX_CALLS'])\n"
            "log = json.loads(calls.read_text(encoding='utf-8')) if calls.exists() else []\n"
            "log.append(sys.argv[1:] + (['TMUX=' + os.environ['TMUX']] if 'TMUX' in os.environ else []))\n"
            "calls.write_text(json.dumps(log), encoding='utf-8')\n"
            "args = sys.argv[3:] if sys.argv[1] == '-L' else sys.argv[1:]\n"
            "if args[0] == 'list-windows':\n"
            "    sys.stdout.buffer.write(pathlib.Path(os.environ['TMUX_WINDOWS']).read_bytes())\n"
            "", encoding="utf-8")
        tmux.chmod(0o700)
        self.initialize()

    def windows(self, *rows):
        """Serve these rows as tmux's window list; a bytes row is written as it is."""
        lines = [row if isinstance(row, bytes) else "\t".join(row).encode("utf-8") for row in rows]
        self.listing.write_bytes(b"".join(line + b"\n" for line in lines))

    def test_window_resolves_the_one_window_tagged_with_the_session(self):
        self.windows(("@1", "abc001", "1abc_cur", "session-one"), ("@3", "abc001", "2wib_dev", "developer-one"))
        result = self.command("window", "--participant", "Developer_Gemini_1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "@3\tabc001:2wib_dev\tserver=default")

    def test_window_reads_utf8_and_undecodable_names_under_c_locale(self):
        self.windows(("@3", "abc001", "2wib_dev", "developer-one", "2"),
                     ("@4", "other", "Заметки", "", "3"),
                     b"@5\tother\tbad\xff\t\t4")
        for label, environment in (("inherited", self.environment), ("C", self.c_locale())):
            with self.subTest(locale=label):
                result = self.command("window", "--participant", "Developer_Gemini_1", environment=environment)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.strip(), "@3\tabc001:2wib_dev\tserver=default")

    def test_window_still_refuses_two_tagged_windows_under_c_locale(self):
        self.windows(("@3", "abc001", "2wib_dev", "developer-one", "2"),
                     ("@4", "other", "Заметки", "developer-one", "3"))
        result = self.command("window", "--participant", "Developer_Gemini_1", environment=self.c_locale())
        self.assertEqual(result.returncode, 1)
        self.assertIn("More than one tmux window is tagged", result.stderr)
        self.assertIn("other:Заметки", result.stderr)

    def test_window_refuses_when_no_window_is_tagged(self):
        self.windows(("@1", "abc001", "1abc_cur", "session-one"))
        result = self.command("window", "--participant", "Developer_Gemini_1")
        self.assertEqual(result.returncode, 1)
        self.assertIn("No tmux window is tagged", result.stderr)

    def test_window_refuses_when_two_windows_carry_the_same_tag(self):
        self.windows(("@3", "abc001", "2wib_dev", "developer-one"), ("@9", "abc001", "old_dev", "developer-one"))
        result = self.command("window", "--participant", "Developer_Gemini_1")
        self.assertEqual(result.returncode, 1)
        self.assertIn("More than one tmux window", result.stderr)

    def test_same_name_in_another_roll_does_not_match_a_different_session(self):
        # Names repeat across rolls; the tag is the AI session, which does not.
        self.windows(("@4", "abc001", "1abc_dev", "another-roll-session"))
        result = self.command("window", "--participant", "Developer_Gemini_1")
        self.assertEqual(result.returncode, 1)
        self.assertIn("No tmux window is tagged", result.stderr)

    def test_window_refuses_a_participant_without_session(self):
        result = self.command("window", "--participant", "Alex")
        self.assertEqual(result.returncode, 1)
        self.assertIn("has no session_id", result.stderr)

    def test_tag_window_sets_both_options_on_the_resolved_window(self):
        self.windows(("@7", "abc001", "2wib_dev", "", "2"))
        result = self.command("tag-window", "--participant", "Developer_Gemini_1", "--window", "abc001:2wib_dev")
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = json.loads(self.calls.read_text(encoding="utf-8"))
        self.assertIn(["set-option", "-w", "-t", "@7", "@agent-session", "developer-one"], calls)
        self.assertIn(["set-option", "-w", "-t", "@7", "@agent", "Developer_Gemini_1"], calls)

    def test_window_uses_the_named_server_and_reports_it(self):
        self.windows(("@3", "abc001", "2wib_dev", "developer-one", "2"))
        result = self.command("window", "--participant", "Developer_Gemini_1", "--tmux-server", "agents")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.strip().endswith("\tserver=agents"))
        calls = json.loads(self.calls.read_text(encoding="utf-8"))
        self.assertTrue(all(call[:2] == ["-L", "agents"] for call in calls), calls)

    def test_tag_window_keeps_the_named_server_for_every_call(self):
        self.windows(("@7", "abc001", "2wib_dev", "", "2"))
        result = self.command("tag-window", "--participant", "Developer_Gemini_1", "--window", "@7", "--tmux-server", "agents")
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = json.loads(self.calls.read_text(encoding="utf-8"))
        self.assertTrue(calls and all(call[:2] == ["-L", "agents"] for call in calls), calls)

    def test_an_empty_server_name_is_refused_before_any_tmux_call(self):
        self.windows(("@7", "abc001", "2wib_dev", "", "2"))
        for action, extra in (("tag-window", ["--window", "@7"]), ("window", [])):
            result = self.command(action, "--participant", "Developer_Gemini_1", *extra, "--tmux-server", "")
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("--tmux-server must name a server", result.stderr)
        self.assertFalse(self.calls.exists())

    def test_default_server_ignores_the_callers_tmux_variable(self):
        # A helper started inside another tmux server must not address that server by accident.
        self.environment["TMUX"] = "/tmp/tmux-test/other,1,0"
        self.windows(("@3", "abc001", "2wib_dev", "developer-one", "2"))
        result = self.command("window", "--participant", "Developer_Gemini_1")
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = json.loads(self.calls.read_text(encoding="utf-8"))
        self.assertFalse(any(arg.startswith("TMUX=") for call in calls for arg in call), calls)
        self.assertFalse(any("-L" in call for call in calls), calls)

    def assert_tag_refused(self, target, message):
        result = self.command("tag-window", "--participant", "Developer_Gemini_1", "--window", target)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn(message, result.stderr)
        calls = json.loads(self.calls.read_text(encoding="utf-8")) if self.calls.exists() else []
        self.assertFalse(any(call[0] == "set-option" for call in calls), calls)

    def test_tag_window_refuses_an_empty_target(self):
        self.windows(("@7", "abc001", "2wib_dev", "", "2"))
        self.assert_tag_refused("", "must name one window explicitly")

    def test_tag_window_refuses_a_target_with_an_empty_window_part(self):
        self.windows(("@7", "abc001", "2wib_dev", "", "2"))
        self.assert_tag_refused("abc001:", "must name one window explicitly")

    def test_tag_window_refuses_special_and_pane_targets(self):
        self.windows(("@7", "abc001", "2wib_dev", "", "2"))
        for target in ("abc001:!", "abc001:{last}", "abc001:2wib_dev.1", ":2wib_dev", "2wib_dev"):
            self.assert_tag_refused(target, "must name one window explicitly")

    def test_tag_window_refuses_a_name_that_matches_no_window_exactly(self):
        # tmux would match a prefix of a window name; the helper demands an exact name.
        self.windows(("@7", "abc001", "2wib_dev", "", "2"))
        self.assert_tag_refused("abc001:2wib", "matches 0 windows")

    def test_tag_window_refuses_a_window_tagged_for_another_agent(self):
        self.windows(("@7", "abc001", "2wib_dev", "session-one", "2"))
        self.assert_tag_refused("@7", "already tagged for another agent's session")

    def test_tag_window_retags_its_own_window_idempotently(self):
        self.windows(("@7", "abc001", "2wib_dev", "developer-one", "2"))
        result = self.command("tag-window", "--participant", "Developer_Gemini_1", "--window", "abc001:2")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_tag_window_refuses_when_the_session_is_tagged_elsewhere(self):
        self.windows(("@2", "abc001", "old_dev", "developer-one", "1"), ("@7", "abc001", "2wib_dev", "", "2"))
        result = self.command("tag-window", "--participant", "Developer_Gemini_1", "--window", "abc001:2wib_dev")
        self.assertEqual(result.returncode, 1)
        self.assertIn("already tagged on window @2", result.stderr)
        calls = json.loads(self.calls.read_text(encoding="utf-8"))
        self.assertFalse(any(call[0] == "set-option" for call in calls))


if __name__ == "__main__":
    unittest.main()
