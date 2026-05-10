import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "kb_ingest_promote.py"


def load_module():
    spec = importlib.util.spec_from_file_location("kb_ingest_promote", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class KbIngestPromoteTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp(prefix="kb-promote-test-"))
        self.kb = self.tmpdir / "knowledge-base"
        (self.kb / "wiki").mkdir(parents=True)
        (self.kb / "wiki" / "log.md").write_text("# Wiki Log\n\n", encoding="utf-8")
        (self.kb / "wiki" / "index.md").write_text("# Wiki Index\n\n", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def write_processed(self, content, name="processed.md"):
        path = self.tmpdir / name
        path.write_text(content, encoding="utf-8")
        return path

    def test_research_processed_item_promotes_to_wiki_research_with_source(self):
        module = load_module()
        source = self.write_processed(
            """# [Research] — Obsidian canonical store

**Timestamp:** 2026-04-17 18:20
**Bucket:** Research
**Routed to:** knowledge-base/
**Original:** Obsidian dipakai sebagai canonical knowledge store, bukan LLM.

## Status
- Processed: ✅
- Routed to: knowledge-base/
"""
        )

        result = module.promote_file(source, self.kb)

        self.assertEqual(result.status, "created")
        self.assertEqual(result.plan.folder, "research")
        self.assertTrue(result.plan.raw_path.exists())
        self.assertTrue(result.plan.wiki_path.exists())
        self.assertEqual(
            result.plan.wiki_path,
            self.kb / "wiki" / "research" / "2026-04-17-obsidian-canonical-store.md",
        )
        note = result.plan.wiki_path.read_text(encoding="utf-8")
        self.assertIn("## Source", note)
        self.assertIn(str(source.resolve()), note)
        self.assertIn("Data Classification: Internal", note)

        wiki_index = (self.kb / "wiki" / "index.md").read_text(encoding="utf-8")
        self.assertEqual(wiki_index.count("wiki/research/2026-04-17-obsidian-canonical-store.md"), 1)
        log = (self.kb / "wiki" / "log.md").read_text(encoding="utf-8")
        self.assertEqual(log.count("wiki/research/2026-04-17-obsidian-canonical-store.md"), 1)

    def test_task_item_is_skipped_unless_routed_to_knowledge_base(self):
        module = load_module()
        source = self.write_processed(
            """# [Task] — Buat proposal

**Timestamp:** 2026-04-17 18:25
**Bucket:** Task
**Routed to:** daily.md
**Original:** Buat proposal minggu depan.
"""
        )

        result = module.promote_file(source, self.kb)

        self.assertEqual(result.status, "skipped")
        self.assertIn("not durable knowledge", result.message)
        self.assertFalse((self.kb / "wiki" / "notes").exists())

    def test_project_item_promotes_to_projects_when_routed_to_knowledge_base(self):
        module = load_module()
        source = self.write_processed(
            """# [Project] — SecondBrain Ruben

**Timestamp:** 2026-04-17 18:30
**Bucket:** Project
**Routed to:** knowledge-base/projects/
**Original:** Catat konteks project SecondBrain untuk Ruben.
"""
        )

        result = module.promote_file(source, self.kb)

        self.assertEqual(result.status, "created")
        self.assertEqual(result.plan.folder, "projects")
        self.assertTrue((self.kb / "wiki" / "projects" / "index.md").exists())

    def test_template_item_promotes_to_templates_when_routed_to_templates(self):
        module = load_module()
        source = self.write_processed(
            """# [Template] — Customer response

**Timestamp:** 2026-04-17 19:55
**Bucket:** Template
**Routed to:** knowledge-base/wiki/templates/
**Original:** Template jawaban customer untuk follow-up cepat.
"""
        )

        result = module.promote_file(source, self.kb)

        self.assertEqual(result.status, "created")
        self.assertEqual(result.plan.folder, "templates")
        self.assertEqual(
            result.plan.wiki_path,
            self.kb / "wiki" / "templates" / "2026-04-17-customer-response.md",
        )
        self.assertTrue((self.kb / "wiki" / "templates" / "index.md").exists())

    def test_restricted_personal_item_is_not_promoted(self):
        module = load_module()
        source = self.write_processed(
            """# [Knowledge] — Kondisi personal

**Timestamp:** 2026-04-17 18:35
**Bucket:** Knowledge
**Routed to:** knowledge-base/
**Original:** Catatan health personal dan wellbeing.
"""
        )

        result = module.promote_file(source, self.kb)

        self.assertEqual(result.status, "skipped_restricted")
        self.assertFalse((self.kb / "wiki" / "notes").exists())

    def test_state_prevents_duplicate_even_if_final_note_removed(self):
        module = load_module()
        source = self.write_processed(
            """# [Knowledge] — Durable note

**Timestamp:** 2026-04-17 18:40
**Bucket:** Knowledge
**Routed to:** knowledge-base/
**Original:** Memory final harus idempotent.
"""
        )

        first = module.promote_file(source, self.kb)
        first.plan.wiki_path.unlink()
        second = module.promote_file(source, self.kb)

        self.assertEqual(first.status, "created")
        self.assertEqual(second.status, "skipped")
        self.assertFalse(first.plan.wiki_path.exists())

    def test_cli_pending_processes_processed_directory(self):
        pending_dir = self.tmpdir / "inbox" / "processed"
        pending_dir.mkdir(parents=True)
        self.write_processed(
            """# [Knowledge] — Batch note

**Timestamp:** 2026-04-17 18:45
**Bucket:** Knowledge
**Routed to:** knowledge-base/
**Original:** Batch promotion works.
""",
            name="batch.md",
        ).rename(pending_dir / "batch.md")

        completed = subprocess.run(
            [
                sys.executable,
                str(MODULE_PATH),
                "--kb-root",
                str(self.kb),
                "--pending-dir",
                str(pending_dir),
                "--pending",
            ],
            text=True,
            capture_output=True,
            check=True,
        )

        self.assertIn("batch.md", completed.stdout)
        self.assertIn("status: created", completed.stdout)
        self.assertTrue((self.kb / "wiki" / "notes" / "2026-04-17-batch-note.md").exists())


if __name__ == "__main__":
    unittest.main()
