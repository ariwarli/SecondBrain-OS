#!/usr/bin/env python3
"""
ClawHub approval gate for autonomous installs.

Protocol:
- Request install first (creates pending request with TTL)
- Human approves via strict text command:
  APPROVE SKILL <slug> <version>
  APPROVE PLUGIN <slug> <version>
- Installer must consume approval token once.

Hard-stop behavior:
- No valid approval token -> consume fails.
- Expired token -> consume fails.
- Used token -> consume fails.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Tuple


DEFAULT_STORE = os.getenv("OPENCLAW_APPROVAL_STORE", "/home/openclaw/banirisset/state/clawhub_approvals.json")
ALLOWED_KIND = {"skill", "plugin"}
APPROVAL_RE = re.compile(
    r"^APPROVE\s+(SKILL|PLUGIN)\s+([a-z0-9][a-z0-9._/-]{0,120})\s+([A-Za-z0-9][A-Za-z0-9._+:-]{0,80})$"
)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat()


def parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def sanitize_slug(raw: str) -> str:
    slug = raw.strip().lower()
    if not slug or slug.startswith("/") or ".." in slug:
        raise ValueError("invalid slug")
    if not re.match(r"^[a-z0-9][a-z0-9._/-]{0,120}$", slug):
        raise ValueError("invalid slug")
    return slug


def sanitize_version(raw: str) -> str:
    version = raw.strip()
    if not version or len(version) > 81:
        raise ValueError("invalid version")
    if not re.match(r"^[A-Za-z0-9][A-Za-z0-9._+:-]{0,80}$", version):
        raise ValueError("invalid version")
    return version


def parse_approval_text(text: str) -> Tuple[str, str, str]:
    match = APPROVAL_RE.match(text.strip())
    if not match:
        raise ValueError("invalid approval format")
    kind = match.group(1).lower()
    slug = sanitize_slug(match.group(2))
    version = sanitize_version(match.group(3))
    return kind, slug, version


def load_store(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {"requests": [], "grants": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("requests", [])
    data.setdefault("grants", [])
    return data


def save_store(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", delete=False, dir=str(path.parent), encoding="utf-8") as tmp:
        json.dump(data, tmp, ensure_ascii=True, indent=2)
        tmp.flush()
        os.fsync(tmp.fileno())
        temp_name = tmp.name
    os.replace(temp_name, path)


def fail(message: str, code: str = "error") -> None:
    print(json.dumps({"ok": False, "code": code, "message": message}, ensure_ascii=True))
    raise SystemExit(1)


def ok(payload: Dict[str, Any]) -> None:
    out = {"ok": True}
    out.update(payload)
    print(json.dumps(out, ensure_ascii=True))


@dataclass
class RequestSpec:
    kind: str
    slug: str
    version: str
    ttl_minutes: int
    purpose: str


def create_request(path: Path, spec: RequestSpec) -> None:
    if spec.kind not in ALLOWED_KIND:
        fail("kind must be skill or plugin", "invalid_kind")
    now = utc_now()
    expires = now + timedelta(minutes=spec.ttl_minutes)
    data = load_store(path)

    for req in data["requests"]:
        if (
            req.get("kind") == spec.kind
            and req.get("slug") == spec.slug
            and req.get("version") == spec.version
            and req.get("status") in {"pending", "approved"}
            and parse_iso(req["expires_at"]) > now
        ):
            ok(
                {
                    "status": "existing",
                    "request_id": req["request_id"],
                    "kind": req["kind"],
                    "slug": req["slug"],
                    "version": req["version"],
                    "expires_at": req["expires_at"],
                    "approval_command": f"APPROVE {req['kind'].upper()} {req['slug']} {req['version']}",
                }
            )
            return

    request_id = f"req_{secrets.token_hex(8)}"
    record = {
        "request_id": request_id,
        "kind": spec.kind,
        "slug": spec.slug,
        "version": spec.version,
        "purpose": spec.purpose,
        "requested_at": iso(now),
        "expires_at": iso(expires),
        "status": "pending",
    }
    data["requests"].append(record)
    save_store(path, data)
    ok(
        {
            "status": "created",
            "request_id": request_id,
            "kind": spec.kind,
            "slug": spec.slug,
            "version": spec.version,
            "expires_at": record["expires_at"],
            "approval_command": f"APPROVE {spec.kind.upper()} {spec.slug} {spec.version}",
        }
    )


def grant_approval(path: Path, approval_text: str, approver: str, ttl_minutes: int) -> None:
    kind, slug, version = parse_approval_text(approval_text)
    now = utc_now()
    expires = now + timedelta(minutes=ttl_minutes)
    data = load_store(path)

    # Expire old pending requests first
    for req in data["requests"]:
        if req.get("status") == "pending" and parse_iso(req["expires_at"]) <= now:
            req["status"] = "expired"

    pending = None
    for req in reversed(data["requests"]):
        if (
            req.get("kind") == kind
            and req.get("slug") == slug
            and req.get("version") == version
            and req.get("status") == "pending"
            and parse_iso(req["expires_at"]) > now
        ):
            pending = req
            break

    if pending is None:
        fail("no pending request matches approval text", "request_not_found")

    token = secrets.token_urlsafe(24)
    grant = {
        "grant_id": f"grant_{secrets.token_hex(8)}",
        "request_id": pending["request_id"],
        "kind": kind,
        "slug": slug,
        "version": version,
        "token": token,
        "approved_by": approver,
        "approved_at": iso(now),
        "expires_at": iso(expires),
        "used_at": None,
        "used_by": None,
    }
    pending["status"] = "approved"
    pending["approved_at"] = iso(now)
    pending["approved_by"] = approver
    pending["grant_id"] = grant["grant_id"]

    data["grants"].append(grant)
    save_store(path, data)
    ok(
        {
            "status": "granted",
            "grant_id": grant["grant_id"],
            "request_id": grant["request_id"],
            "kind": kind,
            "slug": slug,
            "version": version,
            "expires_at": grant["expires_at"],
            "token": token,
        }
    )


def consume_approval(path: Path, kind: str, slug: str, version: str, token: str, consumer: str) -> None:
    if kind not in ALLOWED_KIND:
        fail("kind must be skill or plugin", "invalid_kind")
    now = utc_now()
    data = load_store(path)

    hit = None
    for grant in data["grants"]:
        if (
            grant.get("kind") == kind
            and grant.get("slug") == slug
            and grant.get("version") == version
            and grant.get("token") == token
        ):
            hit = grant
            break

    if hit is None:
        fail("approval token invalid for requested item/version", "approval_missing")

    if hit.get("used_at"):
        fail("approval token already used", "approval_used")

    if parse_iso(hit["expires_at"]) <= now:
        fail("approval token expired", "approval_expired")

    hit["used_at"] = iso(now)
    hit["used_by"] = consumer

    for req in data["requests"]:
        if req.get("request_id") == hit.get("request_id"):
            req["status"] = "consumed"
            req["consumed_at"] = iso(now)
            req["consumed_by"] = consumer
            break

    save_store(path, data)
    ok(
        {
            "status": "consumed",
            "grant_id": hit["grant_id"],
            "request_id": hit["request_id"],
            "kind": kind,
            "slug": slug,
            "version": version,
            "used_by": consumer,
            "used_at": hit["used_at"],
        }
    )


def show_status(path: Path, include_used: bool) -> None:
    now = utc_now()
    data = load_store(path)

    pending = []
    for req in data["requests"]:
        status = req.get("status")
        if status == "pending" and parse_iso(req["expires_at"]) <= now:
            status = "expired"
        req_view = {
            "request_id": req.get("request_id"),
            "kind": req.get("kind"),
            "slug": req.get("slug"),
            "version": req.get("version"),
            "status": status,
            "expires_at": req.get("expires_at"),
        }
        if status in {"pending", "approved"}:
            pending.append(req_view)

    grants = []
    for grant in data["grants"]:
        used = grant.get("used_at") is not None
        expired = parse_iso(grant["expires_at"]) <= now
        if used and not include_used:
            continue
        grants.append(
            {
                "grant_id": grant.get("grant_id"),
                "request_id": grant.get("request_id"),
                "kind": grant.get("kind"),
                "slug": grant.get("slug"),
                "version": grant.get("version"),
                "approved_by": grant.get("approved_by"),
                "expires_at": grant.get("expires_at"),
                "used_at": grant.get("used_at"),
                "state": "used" if used else ("expired" if expired else "active"),
            }
        )

    ok({"store": str(path), "pending_requests": pending, "grants": grants})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ClawHub install approval gate")
    parser.add_argument("--store", default=DEFAULT_STORE, help="Path to approvals store JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    req = sub.add_parser("request", help="Create install request awaiting approval")
    req.add_argument("--kind", required=True, choices=sorted(ALLOWED_KIND))
    req.add_argument("--slug", required=True)
    req.add_argument("--version", required=True)
    req.add_argument("--ttl-minutes", type=int, default=30)
    req.add_argument("--purpose", default="")

    grant = sub.add_parser("grant", help="Grant approval using strict command text")
    grant.add_argument("--text", required=True, help='Example: "APPROVE SKILL foo/bar 1.2.3"')
    grant.add_argument("--approved-by", default="bani")
    grant.add_argument("--ttl-minutes", type=int, default=10)

    consume = sub.add_parser("consume", help="Consume approval token for installation")
    consume.add_argument("--kind", required=True, choices=sorted(ALLOWED_KIND))
    consume.add_argument("--slug", required=True)
    consume.add_argument("--version", required=True)
    consume.add_argument("--token", required=True)
    consume.add_argument("--consumer", default="reed-installer")

    status = sub.add_parser("status", help="Show pending/active approvals")
    status.add_argument("--include-used", action="store_true")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    store = Path(args.store)

    if args.command == "request":
        try:
            spec = RequestSpec(
                kind=args.kind,
                slug=sanitize_slug(args.slug),
                version=sanitize_version(args.version),
                ttl_minutes=max(1, int(args.ttl_minutes)),
                purpose=(args.purpose or "").strip(),
            )
        except ValueError as exc:
            fail(str(exc), "invalid_request")
        create_request(store, spec)
        return

    if args.command == "grant":
        grant_approval(store, args.text, args.approved_by, max(1, int(args.ttl_minutes)))
        return

    if args.command == "consume":
        try:
            kind = args.kind
            slug = sanitize_slug(args.slug)
            version = sanitize_version(args.version)
        except ValueError as exc:
            fail(str(exc), "invalid_consume")
        consume_approval(store, kind, slug, version, args.token, args.consumer)
        return

    if args.command == "status":
        show_status(store, args.include_used)
        return


if __name__ == "__main__":
    main()
