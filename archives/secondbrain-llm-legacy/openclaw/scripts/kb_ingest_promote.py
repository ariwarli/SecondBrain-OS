#!/usr/bin/env python3
"""
Promote processed inbox markdown into the Obsidian-compatible knowledge base.

This script is intentionally separate from inbox routing. The router decides
where a message belongs; this promoter turns durable processed items into final
wiki notes with provenance.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable, NamedTuple


JAKARTA = timezone(timedelta(hours=7))
DEFAULT_CLASSIFICATION = "Internal"
WORKSPACE = Path("/home/openclaw/banirisset")
DEFAULT_KB_ROOT = WORKSPACE / "knowledge-base"
DEFAULT_PENDING_DIR = WORKSPACE / "inbox" / "processed"


class ProcessedItem(NamedTuple):
    source_path: Path
    title: str
    bucket: str
    timestamp: str
    routed_to: str
    original: str


class PromotionPlan(NamedTuple):
    kb_root: Path
    item: ProcessedItem
    slug: str
    raw_path: Path
    wiki_path: Path
    folder: str
    classification: str


class PromotionResult(NamedTuple):
    status: str
    plan: PromotionPlan
    message: str


DURABLE_BUCKETS = {
    "content": "notes",
    "decision": "decisions",
    "decisions": "decisions",
    "knowledge": "notes",
    "knowledge-base": "notes",
    "meeting": "meetings",
    "meetings": "meetings",
    "note": "notes",
    "notes": "notes",
    "project": "projects",
    "projects": "projects",
    "reference": "references",
    "references": "references",
    "research": "research",
    "template": "templates",
    "templates": "templates",
}

SENSITIVE_RE = re.compile(
    r"\b(client|clients|klien|crm|deal|negosiasi|pricing|invoice|rab|budget)\b",
    re.IGNORECASE,
)
RESTRICTED_RE = re.compile(
    r"\b(wellbeing|mental|health|sehat|sakit|therapy|terapi|personal|private|privat)\b",
    re.IGNORECASE,
)


def normalize_slug(value: str) -> str:
    lowered = value.strip().lower()
    lowered = re.sub(r"[^a-z0-9]+", "-", lowered)
    lowered = re.sub(r"-{2,}", "-", lowered).strip("-")
    return lowered or "untitled"


def parse_heading(text: str) -> tuple[str, str]:
    first_line = next((line.strip() for line in text.splitlines() if line.strip()), "")
    match = re.match(r"^#\s*\[([^\]]+)\]\s*[—-]\s*(.+)$", first_line)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    plain = re.sub(r"^#+\s*", "", first_line).strip()
    return "Knowledge", plain or "Untitled"


def extract_field(text: str, field: str, default: str = "") -> str:
    pattern = rf"^\*\*{re.escape(field)}:\*\*\s*(.+?)\s*$"
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1).strip() if match else default


def parse_processed_file(source_path: Path) -> ProcessedItem:
    source_path = source_path.resolve()
    text = source_path.read_text(encoding="utf-8")
    heading_bucket, heading_title = parse_heading(text)
    timestamp = extract_field(text, "Timestamp", "")
    if not timestamp:
        timestamp = datetime.fromtimestamp(source_path.stat().st_mtime, JAKARTA).strftime("%Y-%m-%d %H:%M")
    return ProcessedItem(
        source_path=source_path,
        title=heading_title or "Untitled",
        bucket=extract_field(text, "Bucket", heading_bucket),
        timestamp=timestamp,
        routed_to=extract_field(text, "Routed to", ""),
        original=extract_field(text, "Original", ""),
    )


def parse_date(timestamp: str) -> str:
    match = re.search(r"\d{4}-\d{2}-\d{2}", timestamp)
    if match:
        return match.group(0)
    return datetime.now(JAKARTA).strftime("%Y-%m-%d")


def classify_item(item: ProcessedItem) -> str:
    haystack = f"{item.bucket}\n{item.title}\n{item.routed_to}\n{item.original}"
    if RESTRICTED_RE.search(haystack):
        return "Restricted"
    if SENSITIVE_RE.search(haystack):
        return "Sensitive"
    return DEFAULT_CLASSIFICATION


def routed_to_kb(item: ProcessedItem) -> bool:
    routed = item.routed_to.strip().lower()
    if not routed:
        return False
    return "knowledge-base" in routed or routed.startswith("wiki/")


def route_folder(item: ProcessedItem) -> str | None:
    bucket = item.bucket.strip().lower()
    folder = DURABLE_BUCKETS.get(bucket)
    if not folder:
        return None
    if bucket in {"project", "projects"} and not routed_to_kb(item):
        return None
    if bucket in {"content"} and not routed_to_kb(item):
        return None
    return folder


def build_plan(kb_root: Path, item: ProcessedItem) -> PromotionPlan:
    date = parse_date(item.timestamp)
    slug = f"{date}-{normalize_slug(item.title)}"
    classification = classify_item(item)
    folder = route_folder(item) or "notes"
    return PromotionPlan(
        kb_root=kb_root,
        item=item,
        slug=slug,
        raw_path=kb_root / "raw" / date / f"{slug}.md",
        wiki_path=kb_root / "wiki" / folder / f"{slug}.md",
        folder=folder,
        classification=classification,
    )


def rel_path(kb_root: Path, path: Path) -> str:
    return path.relative_to(kb_root).as_posix()


def validate_item(item: ProcessedItem) -> list[str]:
    missing = []
    if not item.title.strip() or item.title == "Untitled":
        missing.append("title")
    if not item.bucket.strip():
        missing.append("Bucket")
    if not item.timestamp.strip():
        missing.append("Timestamp")
    if not item.original.strip():
        missing.append("Original")
    return missing


def state_path(kb_root: Path) -> Path:
    return kb_root / "state" / "kb-ingest-promote-state.json"


def load_state(kb_root: Path) -> dict:
    path = state_path(kb_root)
    if not path.exists():
        return {"version": 1, "items": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def source_key(path: Path) -> str:
    return str(path.resolve())


def has_promoted(plan: PromotionPlan) -> bool:
    return source_key(plan.item.source_path) in load_state(plan.kb_root).get("items", {})


def record_promotion(plan: PromotionPlan) -> None:
    path = state_path(plan.kb_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    state = load_state(plan.kb_root)
    state.setdefault("items", {})[source_key(plan.item.source_path)] = {
        "source": str(plan.item.source_path),
        "raw": rel_path(plan.kb_root, plan.raw_path),
        "final": rel_path(plan.kb_root, plan.wiki_path),
        "classification": plan.classification,
        "promoted_at": datetime.now(JAKARTA).isoformat(timespec="seconds"),
    }
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_unique_line(path: Path, line: str) -> bool:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if line in existing:
        return False
    with path.open("a", encoding="utf-8") as file_obj:
        if existing and not existing.endswith("\n"):
            file_obj.write("\n")
        file_obj.write(line + "\n")
    return True


def build_raw_content(item: ProcessedItem) -> str:
    return "\n".join(
        [
            f"# Raw Capture: {item.title}",
            "",
            f"**Timestamp:** {item.timestamp}",
            f"**Bucket:** {item.bucket}",
            f"**Routed to:** {item.routed_to}",
            f"**Source file:** {item.source_path}",
            "",
            "## Original",
            "",
            item.original,
            "",
        ]
    )


def build_final_note(plan: PromotionPlan) -> str:
    item = plan.item
    return "\n".join(
        [
            f"# {item.title}",
            "",
            "## Summary",
            "",
            item.original,
            "",
            "## Facts",
            "",
            f"- Bucket: {item.bucket}",
            f"- Routed to: {item.routed_to or 'knowledge-base/wiki/' + plan.folder + '/'}",
            "",
            "## Decisions",
            "",
            "- Belum ada keputusan eksplisit yang disintesis otomatis.",
            "",
            "## Implications",
            "",
            "- Belum ada implikasi tambahan yang disintesis otomatis.",
            "",
            "## Next Actions",
            "",
            "- [ ] Review manual jika note ini akan dipakai jangka panjang.",
            "",
            "## Source",
            "",
            f"- Source file: {item.source_path}",
            f"- Raw copy: {rel_path(plan.kb_root, plan.raw_path)}",
            f"- Timestamp: {item.timestamp}",
            f"- Data Classification: {plan.classification}",
            "",
        ]
    )


def ensure_folder_index(plan: PromotionPlan) -> None:
    path = plan.kb_root / "wiki" / plan.folder / "index.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        title = plan.folder.replace("-", " ").title()
        path.write_text(f"# {title} Index\n\n", encoding="utf-8")
    append_unique_line(path, f"- [[{plan.slug}|{plan.item.title}]] - {plan.classification}")


def write_wiki_index_entry(plan: PromotionPlan) -> None:
    index_path = plan.kb_root / "wiki" / "index.md"
    if not index_path.exists():
        index_path.write_text("# Wiki Index\n\n", encoding="utf-8")
    line = f"- `{rel_path(plan.kb_root, plan.wiki_path)}` - {plan.item.title} ({plan.classification})"
    append_unique_line(index_path, line)


def write_log_entry(plan: PromotionPlan) -> None:
    log_path = plan.kb_root / "wiki" / "log.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if not log_path.exists():
        log_path.write_text("# Wiki Log\n\n", encoding="utf-8")
    stable = (
        f"| ingest | {rel_path(plan.kb_root, plan.wiki_path)} | "
        f"source={plan.item.source_path} | classification={plan.classification}"
    )
    if stable in log_path.read_text(encoding="utf-8"):
        return
    timestamp = datetime.now(JAKARTA).isoformat(timespec="seconds")
    append_unique_line(log_path, f"- {timestamp} {stable}")


def promote_file(source_path: Path, kb_root: Path, dry_run: bool = False) -> PromotionResult:
    kb_root = kb_root.resolve()
    item = parse_processed_file(source_path)
    plan = build_plan(kb_root, item)
    missing = validate_item(item)
    if missing:
        return PromotionResult("invalid", plan, f"missing required field(s): {', '.join(missing)}")
    if plan.classification == "Restricted":
        return PromotionResult("skipped_restricted", plan, "restricted data requires explicit approval")
    if route_folder(item) is None:
        return PromotionResult("skipped", plan, "not durable knowledge")
    if has_promoted(plan):
        return PromotionResult("skipped", plan, "source file already promoted")
    if plan.wiki_path.exists():
        return PromotionResult("skipped", plan, "final note already exists")
    if dry_run:
        return PromotionResult("dry_run", plan, "dry-run only; no files written")

    plan.raw_path.parent.mkdir(parents=True, exist_ok=True)
    plan.wiki_path.parent.mkdir(parents=True, exist_ok=True)
    plan.raw_path.write_text(build_raw_content(item), encoding="utf-8")
    plan.wiki_path.write_text(build_final_note(plan), encoding="utf-8")
    ensure_folder_index(plan)
    write_wiki_index_entry(plan)
    write_log_entry(plan)
    record_promotion(plan)
    return PromotionResult("created", plan, "promotion complete")


def pending_files(pending_dir: Path) -> Iterable[Path]:
    if not pending_dir.exists():
        return []
    return sorted(path for path in pending_dir.glob("*.md") if path.is_file())


def print_result(result: PromotionResult) -> None:
    plan = result.plan
    print(f"status: {result.status}")
    print(f"message: {result.message}")
    print(f"raw: {rel_path(plan.kb_root, plan.raw_path)}")
    print(f"final: {rel_path(plan.kb_root, plan.wiki_path)}")
    print(f"classification: {plan.classification}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote processed inbox markdown into knowledge-base/wiki")
    parser.add_argument("source", nargs="?", help="Processed markdown file to promote")
    parser.add_argument("--kb-root", default=str(DEFAULT_KB_ROOT), help="Knowledge-base root path")
    parser.add_argument("--pending", action="store_true", help="Promote every .md file in the pending directory")
    parser.add_argument("--pending-dir", default=str(DEFAULT_PENDING_DIR), help="Processed inbox directory")
    parser.add_argument("--dry-run", action="store_true", help="Show target paths without writing")
    args = parser.parse_args()

    kb_root = Path(args.kb_root).resolve()
    if args.pending:
        files = list(pending_files(Path(args.pending_dir).resolve()))
        if not files:
            print(f"no pending files in {args.pending_dir}")
            return 0
        for source_path in files:
            print(f"== {source_path} ==")
            print_result(promote_file(source_path, kb_root, dry_run=args.dry_run))
        return 0

    if not args.source:
        parser.error("provide a source file or use --pending")
    print_result(promote_file(Path(args.source), kb_root, dry_run=args.dry_run))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
