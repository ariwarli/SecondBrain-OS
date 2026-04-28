import importlib.util
import logging
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPTS_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SCRIPTS_DIR.parent.parent


def load_module(name: str, path: Path):
    script_dir = str(path.parent)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class InboxMonitorTopicsTest(unittest.TestCase):
    def test_production_topic_registry_matches_forum_threads(self):
        with mock.patch("os.makedirs"), mock.patch(
            "logging.FileHandler", side_effect=lambda *args, **kwargs: logging.NullHandler()
        ):
            module = load_module("inbox_monitor_v2", SCRIPTS_DIR / "inbox_monitor_v2.py")

        expected = {
            "inbox": 11,
            "tasks": 10,
            "personal-crm": 9,
            "content": 3,
            "ops": 27,
            "knowledge-base": 16,
            "research": 16,
            "updates": 13,
            "archives": 12,
            "scheduler": 99,
            "wellbeing": 19,
        }

        self.assertEqual(module.TOPICS, expected)

    def test_research_intent_routes_to_research_bucket(self):
        with mock.patch("os.makedirs"), mock.patch(
            "logging.FileHandler", side_effect=lambda *args, **kwargs: logging.NullHandler()
        ):
            module = load_module("inbox_monitor_v2_research", SCRIPTS_DIR / "inbox_monitor_v2.py")

        result = module.fast_path_classify("Tolong riset competitor dan analisis benchmark untuk tool ini")
        self.assertEqual(result["bucket"], "Research")
        self.assertGreaterEqual(result["confidence"], 70)

    def test_all_primary_routing_buckets_match_representative_inputs(self):
        with mock.patch("os.makedirs"), mock.patch(
            "logging.FileHandler", side_effect=lambda *args, **kwargs: logging.NullHandler()
        ):
            module = load_module("inbox_monitor_v2_all_routes", SCRIPTS_DIR / "inbox_monitor_v2.py")

        cases = [
            ("archive ini saja, project sudah selesai", "Archives"),
            ("server VPS error, tolong restart gateway sekarang", "Ops"),
            ("ingatkan gw besok pagi jam 8 follow up klien", "Reminder"),
            ("Dede minta revisi brief STOP TB besok", "Project"),
            ("follow-up Mas Dede belum jawab proposal 2 minggu", "CRM"),
            ("bikin thread linkedin dari ide ini", "Content"),
            ("tolong review dan rapihin task ini hari ini", "Task"),
            ("tolong riset competitor dan analisis benchmark tool ini", "Research"),
            ("simpan link tutorial ini sebagai referensi nanti dibaca https://example.com", "Knowledge"),
        ]

        for text, expected_bucket in cases:
            with self.subTest(text=text, expected_bucket=expected_bucket):
                result = module.fast_path_classify(text)
                self.assertEqual(result["bucket"], expected_bucket)
                self.assertGreaterEqual(result["confidence"], 70)

    def test_conversational_prompt_is_not_treated_as_inbox_item(self):
        with mock.patch("os.makedirs"), mock.patch(
            "logging.FileHandler", side_effect=lambda *args, **kwargs: logging.NullHandler()
        ):
            module = load_module("inbox_monitor_v2_conversational", SCRIPTS_DIR / "inbox_monitor_v2.py")

        self.assertTrue(module.is_conversational("gimana cara pakai ini?"))
        self.assertTrue(module.is_conversational("hai reed"))
        self.assertFalse(module.is_conversational("tolong bikin draft proposal untuk NIRVA"))

    def test_manual_triage_choice_maps_short_reply(self):
        with mock.patch("os.makedirs"), mock.patch(
            "logging.FileHandler", side_effect=lambda *args, **kwargs: logging.NullHandler()
        ):
            module = load_module("inbox_monitor_v2_manual_triage", SCRIPTS_DIR / "inbox_monitor_v2.py")

        self.assertEqual(module.parse_manual_triage_choice("Task"), "Task")
        self.assertEqual(module.parse_manual_triage_choice("project"), "Project")
        self.assertIsNone(module.parse_manual_triage_choice("hai"))

    def test_classify_uses_llm_for_ambiguous_message(self):
        with mock.patch("os.makedirs"), mock.patch(
            "logging.FileHandler", side_effect=lambda *args, **kwargs: logging.NullHandler()
        ):
            module = load_module("inbox_monitor_v2_llm", SCRIPTS_DIR / "inbox_monitor_v2.py")

        with mock.patch.object(
            module,
            "call_llm_classifier",
            return_value={
                "bucket": "Project",
                "confidence": 82,
                "reasoning_short": "Pesan membahas pekerjaan project untuk Ruben.",
                "source": "llm",
            },
        ) as mock_llm:
            result = module.classify("cek second brain project untuk ruben")

        mock_llm.assert_called_once()
        self.assertEqual(result["bucket"], "Project")
        self.assertEqual(result["confidence"], 82)
        self.assertEqual(result["source"], "llm")

    def test_parse_classifier_response_recovers_from_wrapped_json(self):
        with mock.patch("os.makedirs"), mock.patch(
            "logging.FileHandler", side_effect=lambda *args, **kwargs: logging.NullHandler()
        ):
            module = load_module("inbox_monitor_v2_parse_json", SCRIPTS_DIR / "inbox_monitor_v2.py")

        parsed = module.parse_classifier_response(
            '```json\n{"bucket":"Project","confidence":81,"reasoning_short":"Pesan membahas pekerjaan project."}\n```'
        )
        self.assertEqual(parsed["bucket"], "Project")
        self.assertEqual(parsed["confidence"], 81)

    def test_classify_falls_back_when_llm_errors(self):
        with mock.patch("os.makedirs"), mock.patch(
            "logging.FileHandler", side_effect=lambda *args, **kwargs: logging.NullHandler()
        ):
            module = load_module("inbox_monitor_v2_llm_error", SCRIPTS_DIR / "inbox_monitor_v2.py")

        with mock.patch.object(
            module,
            "fast_path_classify",
            return_value={
                "bucket": "Task",
                "confidence": 72,
                "reasoning_short": "Fast-path masih lemah.",
                "source": "fast_path",
                "scores": {"Task": 2},
            },
        ), mock.patch.object(module, "call_llm_classifier", side_effect=RuntimeError("boom")):
            result = module.classify("tolong review dan rapihin task ini hari ini")

        self.assertEqual(result["bucket"], "Task")
        self.assertEqual(result["source"], "fast_path_fallback")
        self.assertIn("LLM fallback error", result["reasoning_short"])

    def test_task_borderline_with_content_signal_not_misrouted_to_task(self):
        with mock.patch("os.makedirs"), mock.patch(
            "logging.FileHandler", side_effect=lambda *args, **kwargs: logging.NullHandler()
        ):
            module = load_module("inbox_monitor_v2_task_content_ambig", SCRIPTS_DIR / "inbox_monitor_v2.py")

        result = module.classify("tolong cek ide konten ini, nanti kita eksekusi kalau oke")
        self.assertNotEqual(result["bucket"], "Task")
        self.assertIn(result["bucket"], {"Content", "Project", "Knowledge"})

    def test_process_inbox_keeps_low_confidence_in_unsorted(self):
        with mock.patch("os.makedirs"), mock.patch(
            "logging.FileHandler", side_effect=lambda *args, **kwargs: logging.NullHandler()
        ):
            module = load_module("inbox_monitor_v2_low_conf", SCRIPTS_DIR / "inbox_monitor_v2.py")

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            module.WORKSPACE = str(tmp_path)
            module.STATE_FILE = str(tmp_path / "inbox" / ".monitor_v2_state.json")
            module.PROCESSED_DIR = str(tmp_path / "inbox" / "processed")
            module.SESSIONS_JSON = str(tmp_path / "sessions.json")

            with mock.patch.object(module, "get_inbox_session_file", return_value="session.jsonl"), \
                 mock.patch.object(
                     module,
                     "parse_session_messages",
                     return_value=[{"message_id": "2001", "text": "mungkin ini penting nanti", "timestamp": "2026-04-17T03:23:07Z"}],
                 ), \
                 mock.patch.object(module, "write_unsorted_file", return_value=str(tmp_path / "inbox" / "unsorted" / "2001.md")), \
                 mock.patch.object(
                     module,
                     "classify",
                     return_value={
                         "bucket": "Task",
                         "confidence": 65,
                         "reasoning_short": "Masih ambigu.",
                         "source": "llm",
                     },
                 ), \
                 mock.patch.object(module, "send_message") as mock_send:
                processed = module.process_inbox()

            self.assertEqual(processed, 1)
            mock_send.assert_called_once()
            state = module.load_state()
            self.assertEqual(len(state["pending_triage"]), 1)

    def test_process_inbox_resolves_pending_triage_from_short_reply(self):
        with mock.patch("os.makedirs"), mock.patch(
            "logging.FileHandler", side_effect=lambda *args, **kwargs: logging.NullHandler()
        ):
            module = load_module("inbox_monitor_v2_resolve_triage", SCRIPTS_DIR / "inbox_monitor_v2.py")

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            module.WORKSPACE = str(tmp_path)
            module.STATE_FILE = str(tmp_path / "inbox" / ".monitor_v2_state.json")
            module.PROCESSED_DIR = str(tmp_path / "inbox" / "processed")
            module.SESSIONS_JSON = str(tmp_path / "sessions.json")

            unsorted_dir = tmp_path / "inbox" / "unsorted"
            unsorted_dir.mkdir(parents=True, exist_ok=True)
            unsorted_file = unsorted_dir / "2026-04-17_10-22-06_1680.md"
            unsorted_file.write_text(
                "# [Unsorted] — cek second brain project untuk ruben\n\n"
                "**Timestamp:** 2026-04-17 10:22\n"
                "**Source message id:** 1680\n"
                "**Status:** pending-triage\n"
                "**Original:** cek second brain project untuk ruben\n",
                encoding="utf-8",
            )

            state = {
                "processed_message_ids": [],
                "pending_triage": [
                    {
                        "source_message_id": "1680",
                        "unsorted_path": str(unsorted_file),
                        "original_text": "cek second brain project untuk ruben",
                        "created_at": "2026-04-17 10:22:07",
                        "status": "pending",
                        "awaiting_choice": True,
                    }
                ],
            }
            module.save_state(state)

            with mock.patch.object(module, "get_inbox_session_file", return_value="session.jsonl"), \
                 mock.patch.object(
                     module,
                     "parse_session_messages",
                     return_value=[{"message_id": "1682", "text": "Task", "timestamp": "2026-04-17T03:23:07Z"}],
                 ), \
                 mock.patch.object(module, "copy_message") as mock_copy, \
                 mock.patch.object(module, "send_message") as mock_send:
                processed = module.process_inbox()

            self.assertEqual(processed, 1)
            mock_copy.assert_called_once_with(1680, module.TOPICS["tasks"])
            mock_send.assert_not_called()

            updated_state = module.load_state()
            self.assertEqual(updated_state["pending_triage"], [])
            self.assertIn("1682", updated_state["processed_message_ids"])

            updated_unsorted = unsorted_file.read_text(encoding="utf-8")
            self.assertIn("**Status:** resolved-task", updated_unsorted)
            self.assertIn("**Resolved to:** Task", updated_unsorted)


class SessionCheckpointWorkerTest(unittest.TestCase):
    def test_write_checkpoint_ignores_heartbeat_noise_in_active_context(self):
        module = load_module(
            "session_checkpoint_worker",
            SCRIPTS_DIR / "session_checkpoint_worker.py",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            module.SESSIONS_OUT = tmp_path / "sessions"
            module.SESSIONS_OUT.mkdir()
            module.LOG_PATH = tmp_path / "log.md"
            module.LOG_PATH.write_text("# Wiki Log\n", encoding="utf-8")

            meta = module.SessionMeta(
                agent_id="reed-archivist",
                session_key="agent:reed-archivist:main",
                session_id="session-1",
                jsonl_path=tmp_path / "session.jsonl",
            )

            chunk = [
                (
                    "2026-04-16T04:13:00+00:00",
                    "Read HEARTBEAT.md if it exists (workspace context). "
                    "Follow it strictly. If nothing needs attention, reply HEARTBEAT_OK.",
                ),
                (
                    "2026-04-16T04:14:00+00:00",
                    "Tolong sync knowledge base wiki dan update index.md setelah arsip beres.",
                ),
            ]

            module.write_checkpoint(meta, 1, chunk)

            active_path = module.SESSIONS_OUT / "reed-archivist-agent-reed-archivist-main-active.md"
            active_text = active_path.read_text(encoding="utf-8")

            self.assertIn("Tolong sync knowledge base wiki", active_text)
            self.assertNotIn("Read HEARTBEAT.md", active_text)
            self.assertNotIn("HEARTBEAT_OK", active_text)


class InboxWriterTest(unittest.TestCase):
    def test_write_pending_item_creates_expected_markdown(self):
        module = load_module("inbox_writer_pending", SCRIPTS_DIR / "inbox_writer.py")

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            module.WORKSPACE = str(tmp_path)
            module.PENDING_DIR = str(tmp_path / "inbox" / "pending")
            module.PROCESSED_DIR = str(tmp_path / "inbox" / "processed")
            module.UNSORTED_DIR = str(tmp_path / "inbox" / "unsorted")

            filepath = module.write_pending_item(
                "pesan penting dari user",
                source="telegram",
                timestamp="2026-04-17 09:46",
                filename="manual.md",
            )

            content = Path(filepath).read_text(encoding="utf-8")
            self.assertTrue(filepath.endswith("manual.md"))
            self.assertIn("**Source:** telegram", content)
            self.assertIn("**Original:** pesan penting dari user", content)

    def test_write_unsorted_item_marks_triage_status(self):
        module = load_module("inbox_writer_unsorted", SCRIPTS_DIR / "inbox_writer.py")

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            module.WORKSPACE = str(tmp_path)
            module.PENDING_DIR = str(tmp_path / "inbox" / "pending")
            module.PROCESSED_DIR = str(tmp_path / "inbox" / "processed")
            module.UNSORTED_DIR = str(tmp_path / "inbox" / "unsorted")

            filepath = module.write_unsorted_item(
                "isi belum jelas",
                tg_msg_id="1667",
                timestamp="2026-04-17 09:46",
                filename="unsorted.md",
            )

            content = Path(filepath).read_text(encoding="utf-8")
            self.assertIn("**Status:** pending-triage", content)
            self.assertIn("**Source message id:** 1667", content)


class InboxRecoveryTest(unittest.TestCase):
    def test_collect_failed_pending_writes_detects_missing_file(self):
        module = load_module(
            "recover_inbox_failed_writes",
            SCRIPTS_DIR / "recover_inbox_failed_writes.py",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            workspace = tmp_path / "workspace"
            session_path = tmp_path / "session.jsonl"
            pending_dir = workspace / "inbox" / "pending"
            pending_dir.mkdir(parents=True)

            module.WORKSPACE = str(workspace)
            module.PENDING_DIR = str(pending_dir)

            session_path.write_text(
                '\n'.join([
                    '{"type":"message","timestamp":"2026-04-17T02:47:01.292Z","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_1","name":"write","arguments":{"content":"# INBOX: unanswered audio\\n","path":"inbox/pending/2026-04-17_0946_unanswered_audio.md"}}]}}',
                    '{"type":"message","message":{"role":"toolResult","toolCallId":"call_1","details":{"status":"error","tool":"write","error":"sandbox pinned mutation helper requires python3 or python"}}}',
                ]),
                encoding="utf-8",
            )

            items = module.collect_failed_pending_writes(str(session_path))
            self.assertEqual(len(items), 1)
            self.assertEqual(items[0].relative_path, "inbox/pending/2026-04-17_0946_unanswered_audio.md")


if __name__ == "__main__":
    unittest.main()
