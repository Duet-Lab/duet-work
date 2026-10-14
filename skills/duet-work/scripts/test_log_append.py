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
        self.body.write_text("## Результат\n\nМнение и `@ABC001/report.md`.\n```python\nprint('да')\n```\n", encoding="utf-8")
        self.environment = dict(os.environ)
        self.environment.update(PATH=str(self.root), ROLL=str(self.roll), CAPTURE=str(self.root / "queue.json"))
        self.codex = self.root / "codex"
        self.codex.write_text(
            f"#!{sys.executable}\n"
            "import json, os, pathlib, sys\n"
            "roll = pathlib.Path(os.environ['ROLL']).read_text()\n"
            "assert '<!-- message-roll:end -->' in roll, 'notification preceded durable message'\n"
            "pathlib.Path(os.environ['CAPTURE']).write_text(json.dumps(sys.argv[1:]))\n"
            "sys.exit(int(os.environ.get('QUEUE_EXIT', '0')))\n", encoding="utf-8")
        self.codex.chmod(0o700)

    def metadata(self, client="claude"):
        return {
            "roll-type": "dev-curation",
            "coordinator": {"name": "Moderator_1", "client": client, "session_id": "session-one"},
            "participants": [
                {"name": "Moderator_1", "client": client},
                {"name": "Developer_Gemini_1", "client": "gemini", "model": "test-model", "effort": "test-effort"},
                {"name": "User"},
            ],
        }

    def command(self, action, *arguments, roll=None, environment=None):
        return subprocess.run(
            [sys.executable, str(SCRIPT), action, "--roll", str(roll or self.roll), *arguments],
            capture_output=True, text=True, timeout=20, env=environment or self.environment,
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

    def test_append_preserves_readable_markdown_without_development_fields(self):
        meta = self.metadata()
        meta["roll-type"] = "round-table"
        self.initialize(meta)
        result = self.send()
        self.assertEqual(result.returncode, 0, result.stderr)
        content = self.roll.read_text()
        self.assertIn(self.body.read_text(), content)
        self.assertIn(" — Developer_Gemini_1\n", content)
        self.assertNotIn("**Task:**", content)

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
        path.write_text(path.read_text() + "roll-type: surprise\n")
        result = self.command("init", "--metadata", str(path))
        self.assertEqual(result.returncode, 1)
        self.assertFalse(self.roll.exists())

    def test_duplicate_participant_names_are_rejected(self):
        meta = self.metadata()
        meta["participants"].append(meta["participants"][1].copy())
        result = self.command("init", "--metadata", str(self.save_metadata_input(meta)))
        self.assertEqual(result.returncode, 1)
        self.assertIn("unique", result.stderr)

    def test_invalid_coordinator_name_has_a_clear_validation_error(self):
        meta = self.metadata()
        meta["coordinator"]["name"] = ["not-a-name"]
        result = self.command("init", "--metadata", str(self.save_metadata_input(meta)))
        self.assertEqual(result.returncode, 1)
        self.assertIn("coordinator.name", result.stderr)
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
        self.body.write_text("Изменённый ответ")
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
        result = self.send(sender="User")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(" — User\n", self.roll.read_text())

    def test_invalid_message_body_is_rejected(self):
        self.initialize()
        before = self.roll.read_bytes()
        for body in ("  \n", "<!-- message-roll:end -->"):
            with self.subTest(body=body):
                self.body.write_text(body)
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
        self.roll.write_text(self.roll.read_text().replace("<!-- message-roll:end -->", "", 1))
        before = self.roll.read_bytes()
        self.assertEqual(self.send("m3").returncode, 1)
        self.assertEqual(self.roll.read_bytes(), before)

    def test_metadata_update_preserves_published_messages_exactly(self):
        self.initialize()
        self.send()
        history = self.roll.read_text().split("\n---\n", 1)[1]
        meta = self.metadata()
        meta["coordinator"]["session_id"] = "session-two"
        meta["participants"].append({"name": "Reviewer_Codex_Security_1", "client": "codex"})
        result = self.command("metadata", "--metadata", str(self.save_metadata_input(meta)))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.roll.read_text().split("\n---\n", 1)[1], history)
        self.assertNotIn("session-one", self.roll.read_text())
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
        meta["participants"].append({"name": "Developer_Gemini_2", "client": "gemini"})
        path = self.save_metadata_input(meta, "replacement.yaml")
        with ThreadPoolExecutor(max_workers=8) as pool:
            futures = [pool.submit(self.send, f"m{i}") for i in range(16)]
            futures += [pool.submit(self.send, f"m{i}") for i in range(16)]
            futures.append(pool.submit(self.command, "metadata", "--metadata", str(path)))
            results = [f.result() for f in futures]
        for result in results:
            self.assertEqual(result.returncode, 0, result.stderr)
        content = self.roll.read_text()
        self.assertEqual(content.count("<!-- message-roll:end -->"), 16)
        self.assertIn("Developer_Gemini_2", content)
        for i in range(16):
            self.assertEqual(content.count(f"**Message:** `m{i}`"), 1)

    def test_codex_notification_uses_current_session_after_message_is_saved(self):
        self.initialize(self.metadata("codex"))
        meta = self.metadata("codex")
        meta["coordinator"]["session_id"] = "session-two"
        self.command("metadata", "--metadata", str(self.save_metadata_input(meta)))
        result = self.send()
        self.assertEqual(result.returncode, 0, result.stderr)
        args = json.loads((self.root / "queue.json").read_text())
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

    def test_missing_codex_reports_installation_without_losing_message(self):
        self.initialize(self.metadata("codex"))
        self.codex.unlink()
        result = self.send()
        self.assertEqual(result.returncode, 3)
        self.assertIn("brew install --cask codex", result.stderr)
        self.assertIn("**Message:** `m1`", self.roll.read_text())

    def test_queue_timeout_preserves_the_saved_message(self):
        self.initialize(self.metadata("codex"))
        self.codex.write_text(f"#!{sys.executable}\nwhile True: pass\n")
        result = self.command("append", "--message-id", "m1", "--sender", "Developer_Gemini_1",
                              "--body", str(self.body), "--roll-ref", "@ABC001/rolls/discussion.md",
                              "--notify-timeout", "0.2")
        self.assertEqual(result.returncode, 3)
        self.assertIn("timed out", result.stderr)
        self.assertIn("**Message:** `m1`", self.roll.read_text())

    def test_retry_after_coordinator_replacement_uses_new_address(self):
        self.initialize(self.metadata("codex"))
        self.send(environment=dict(self.environment, QUEUE_EXIT="7"))
        meta = self.metadata("codex")
        meta["participants"].append({"name": "Moderator_2", "client": "codex"})
        meta["coordinator"] = {"name": "Moderator_2", "client": "codex", "session_id": "session-two"}
        self.command("metadata", "--metadata", str(self.save_metadata_input(meta)))
        self.assertEqual(self.send().returncode, 0)
        args = json.loads((self.root / "queue.json").read_text())
        self.assertEqual(args[:3], ["queue", "--thread", "session-two"])
        self.assertEqual(self.roll.read_text().count("**Message:** `m1`"), 1)

    def test_coordinator_does_not_notify_itself(self):
        self.initialize(self.metadata("codex"))
        result = self.send(sender="Moderator_1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.root / "queue.json").exists())

    def test_unknown_client_retains_message_but_reports_missing_adapter(self):
        self.initialize(self.metadata("another-client"))
        result = self.send()
        self.assertEqual(result.returncode, 3)
        self.assertIn("No notification adapter", result.stderr)
        self.assertIn("**Message:** `m1`", self.roll.read_text())

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
        self.send(sender="Moderator_1")
        result = self.command("watch", "--once")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("message-roll:message", result.stdout)

    def test_live_watch_observes_atomic_replacement(self):
        self.initialize()
        process = subprocess.Popen(
            [sys.executable, str(SCRIPT), "watch", "--roll", str(self.roll)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=self.environment,
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
        self.assertIn("**Message:** `m1`", second.read_text())

    def test_symlink_alias_preserves_the_same_roll(self):
        self.initialize()
        alias = self.root / "alias.md"
        alias.symlink_to(self.roll)
        result = self.send(roll=alias)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(alias.is_symlink())
        self.assertIn("**Message:** `m1`", self.roll.read_text())

    def test_legacy_log_is_not_silently_reinterpreted(self):
        self.roll.write_text("<!-- duet-channel:message -->\n")
        before = self.roll.read_bytes()
        result = self.send()
        self.assertEqual(result.returncode, 1)
        self.assertIn("not migrated automatically", result.stderr)
        self.assertEqual(self.roll.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
