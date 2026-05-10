import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "kb_lint.py"


def load_module():
    spec = importlib.util.spec_from_file_location("kb_lint", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class KbLintTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp(prefix="kb-lint-test-"))
        self.kb = self.tmpdir / "knowledge-base"
        (self.kb / "wiki" / "notes").mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def write_note(self, name, content):
        path = self.kb / "wiki" / "notes" / name
        path.write_text(content, encoding="utf-8")
        return path

    def test_valid_final_note_has_no_findings(self):
        module = load_module()
        self.write_note(
            "valid.md",
            """# Valid Note

## Summary

Isi ringkas.

## Source

- Source file: inbox/processed/example.md
- Data Classification: Internal
""",
        )

        findings = module.lint_kb(self.kb)

        self.assertEqual(findings, [])

    def test_missing_source_and_classification_are_findings(self):
        module = load_module()
        self.write_note(
            "bad.md",
            """# Bad Note

## Summary

Tanpa metadata.
""",
        )

        findings = module.lint_kb(self.kb)

        messages = "\n".join(f.message for f in findings)
        self.assertIn("missing Source section", messages)
        self.assertIn("missing Data Classification", messages)

    def test_secret_like_text_is_finding(self):
        module = load_module()
        self.write_note(
            "secret.md",
            """# Secret Note

## Source

- Source file: inbox/processed/example.md
- Data Classification: Internal

TELEGRAM_BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi
""",
        )

        findings = module.lint_kb(self.kb)

        self.assertTrue(any("possible secret" in finding.message for finding in findings))

    def test_templates_are_linted_as_final_notes(self):
        module = load_module()
        template_dir = self.kb / "wiki" / "templates"
        template_dir.mkdir(parents=True)
        (template_dir / "customer-response.md").write_text(
            """# Customer Response

## Summary

Reusable template tanpa metadata source.
""",
            encoding="utf-8",
        )

        findings = module.lint_kb(self.kb)

        self.assertTrue(
            any(
                finding.path.name == "customer-response.md"
                and finding.message == "missing Source section"
                for finding in findings
            )
        )

    def test_cli_exits_nonzero_when_findings_exist(self):
        self.write_note("bad.md", "# Bad\n")

        completed = subprocess.run(
            [sys.executable, str(MODULE_PATH), "--kb-root", str(self.kb)],
            text=True,
            capture_output=True,
        )

        self.assertEqual(completed.returncode, 1)
        self.assertIn("missing Source section", completed.stdout)


if __name__ == "__main__":
    unittest.main()
