from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from agent_os.engine import intake_goal
from agent_os.store import Store
from agent_os.worker import run_once


class ClosedLoopTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp(prefix="agent-os-test-"))
        (self.tmpdir / "artifacts").mkdir()
        (self.tmpdir / "memory").mkdir()
        (self.tmpdir / "runs").mkdir()
        self.store = Store(self.tmpdir)
        self.store.init()

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir)

    def test_goal_task_execution_verification_and_memory(self) -> None:
        goal_id, task_id = intake_goal(
            self.tmpdir,
            "Create test artifact",
            {
                "description": "Write a test artifact",
                "task_type": "write_file",
                "payload": {
                    "path": "artifacts/out.txt",
                    "content": "hello agent os\n",
                },
                "verification_spec": {
                    "type": "file_contains",
                    "path": "artifacts/out.txt",
                    "contains": "agent os",
                },
            },
        )

        result = run_once(self.tmpdir)
        self.assertEqual(result["task_id"], task_id)
        self.assertTrue(result["verification"]["ok"])
        self.assertTrue((self.tmpdir / "artifacts" / "out.txt").exists())
        self.assertIn("agent os", (self.tmpdir / "artifacts" / "out.txt").read_text(encoding="utf-8"))
        task = self.store.get_task(task_id)
        self.assertEqual(task.status, "verified")
        metrics = self.store.metrics()
        self.assertEqual(metrics["goals_total"], 1)
        self.assertEqual(metrics["tasks_verified"], 1)
        memory_files = list((self.tmpdir / "memory").glob("*.md"))
        self.assertEqual(len(memory_files), 1)
        self.assertIn(f"goal {goal_id}", memory_files[0].read_text(encoding="utf-8").lower())

    def test_shell_task_requires_approval_then_runs_after_approval(self) -> None:
        _, task_id = intake_goal(
            self.tmpdir,
            "Run safe shell command",
            {
                "description": "Print current directory",
                "task_type": "shell_command",
                "payload": {
                    "command": "pwd",
                },
                "verification_spec": {
                    "type": "stdout_contains",
                    "contains": str(self.tmpdir),
                },
                "risk_level": "medium",
                "budget_limit": 3,
            },
        )

        idle = run_once(self.tmpdir)
        self.assertEqual(idle["status"], "idle")
        task = self.store.get_task(task_id)
        self.assertEqual(task.approval_status, "pending")
        approvals = self.store.list_pending_approvals()
        self.assertEqual(len(approvals), 1)

        self.store.set_approval_status(task_id, "approved", "test approval")
        result = run_once(self.tmpdir)
        self.assertEqual(result["task_id"], task_id)
        self.assertTrue(result["verification"]["ok"])
        task = self.store.get_task(task_id)
        self.assertEqual(task.status, "verified")
        self.assertEqual(task.budget_used, 1)


if __name__ == "__main__":
    unittest.main()
