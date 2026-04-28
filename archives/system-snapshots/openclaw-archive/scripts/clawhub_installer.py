#!/usr/bin/env python3
"""
ClawHub autonomous installer for skills and plugins.

Workflow:
1. Fetch metadata from ClawHub.
2. Risk analysis (capabilities check).
3. Propose install and wait for Human Approval (Batch 1 gate).
4. Install to staging, run smoke test, then promote.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# Constants
DEFAULT_APPROVAL_SCRIPT = os.getenv("OPENCLAW_APPROVAL_SCRIPT", "/home/openclaw/banirisset/openclaw/scripts/clawhub_approval.py")
DEFAULT_STAGING_DIR = os.getenv("OPENCLAW_STAGING_DIR", "/home/openclaw/banirisset/openclaw/staging")
DEFAULT_PRODUCTION_DIR = os.getenv("OPENCLAW_PRODUCTION_DIR", "/home/openclaw/.openclaw")
DEFAULT_BACKUP_DIR = os.getenv("OPENCLAW_BACKUP_DIR", "/home/openclaw/banirisset/openclaw/backups")
CLAW_HUB_URL = "https://clawhub.ai"
DEFAULT_APPROVAL_STORE = os.getenv("OPENCLAW_APPROVAL_STORE", "/home/openclaw/banirisset/state/clawhub_approvals.json")
DEFAULT_AUDIT_LOG = os.getenv("OPENCLAW_INSTALL_LOG", "/home/openclaw/banirisset/ops/clawhub_installs.log")

class InstallerError(Exception):
    def __init__(self, message: str, code: str = "error"):
        super().__init__(message)
        self.code = code

def log_audit(event: Dict[str, Any]) -> None:
    """Append structured log to audit file."""
    log_path = Path(DEFAULT_AUDIT_LOG)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    event["timestamp"] = datetime.now(timezone.utc).isoformat()
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

def check_dependencies(metadata: Dict[str, Any]) -> None:
    """Verify system dependencies are met."""
    deps = metadata.get("dependencies", [])
    for dep in deps:
        if dep == "jq":
            if subprocess.run(["which", "jq"], capture_output=True).returncode != 0:
                raise InstallerError("Missing required dependency: jq", "missing_dependency")
        # Add more dependency checks as needed

def run_command(args: List[str], capture: bool = True) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(args, capture_output=capture, text=True, check=True)
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        raise InstallerError(f"Command failed: {' '.join(args)} - {error_msg}", "command_failed")

def analyze_risk(metadata: Dict[str, Any]) -> str:
    """Classify risk level based on capabilities."""
    caps = metadata.get("capabilities", [])
    high_risk = {"exec", "network", "filesystem_root"}
    med_risk = {"filesystem_workspace", "environment_read"}
    
    if any(c in high_risk for c in caps):
        return "HIGH"
    if any(c in med_risk for c in caps):
        return "MEDIUM"
    return "LOW"

def validate_metadata(metadata: Dict[str, Any]) -> None:
    """Strictly validate source and version before proceeding."""
    source = metadata.get("source", "")
    if not source.startswith(CLAW_HUB_URL):
        raise InstallerError(f"Unauthorized source: {source}. Only {CLAW_HUB_URL} allowed.", "unauthorized_source")
    
    version = metadata.get("version", "")
    if not re.match(r"^\d+\.\d+\.\d+(-[a-z0-9.]+)?$", version):
        raise InstallerError(f"Invalid version pinning: {version}. Must follow semver format (e.g. 1.2.3).", "invalid_version")

def fetch_catalog(slug: str) -> Dict[str, Any]:
    """
    Mock fetcher for ClawHub catalog.
    In real usage, this would be a curl to clawhub.ai/api/v1/item/<slug>
    """
    if slug == "team/example-skill":
        return {
            "slug": "team/example-skill",
            "kind": "skill",
            "version": "1.0.0",
            "capabilities": ["filesystem_workspace"],
            "dependencies": ["jq"],
            "description": "Example skill for testing Batch 2",
            "source": f"{CLAW_HUB_URL}/dist/example-skill-1.0.0.tar.gz",
            "checksum": "sha256:1234567890abcdef"
        }
    elif slug == "team/high-risk-plugin":
        return {
            "slug": "team/high-risk-plugin",
            "kind": "plugin",
            "version": "0.1.0",
            "capabilities": ["exec", "network"],
            "dependencies": [],
            "description": "Powerful plugin that needs extra confirmation",
            "source": f"{CLAW_HUB_URL}/dist/high-risk-0.1.0.tar.gz",
            "checksum": "sha256:deadbeef"
        }
    elif slug == "team/untrusted-plugin":
        return {
            "slug": "team/untrusted-plugin",
            "kind": "plugin",
            "version": "1.0.0",
            "capabilities": [],
            "dependencies": [],
            "description": "Untrusted source test",
            "source": "https://malicious.ai/plugin.tar.gz",
            "checksum": "sha256:bad"
        }
    raise InstallerError(f"Item not found in ClawHub catalog: {slug}", "not_found")

def request_approval(kind: str, slug: str, version: str, risk: str) -> str:
    """Request approval via Batch 1 script."""
    purpose = f"Autonomous install of {risk} risk {kind} {slug}@{version}"
    args = [
        sys.executable, DEFAULT_APPROVAL_SCRIPT, "request",
        "--kind", kind, "--slug", slug, "--version", version,
        "--purpose", purpose
    ]
    proc = run_command(args)
    data = json.loads(proc.stdout)
    if not data.get("ok"):
        raise InstallerError(f"Failed to create approval request: {data.get('message')}")
    return data["approval_command"]

def verify_approval(kind: str, slug: str, version: str, token: str) -> bool:
    """Consume approval token via Batch 1 script."""
    args = [
        sys.executable, DEFAULT_APPROVAL_SCRIPT, "consume",
        "--kind", kind, "--slug", slug, "--version", version,
        "--token", token, "--consumer", "clawhub-installer"
    ]
    try:
        proc = run_command(args)
        data = json.loads(proc.stdout)
        return data.get("ok", False)
    except InstallerError as e:
        print(f"Approval verification failed: {e}", file=sys.stderr)
        return False

def staging_install(metadata: Dict[str, Any]) -> Path:
    """Download and extract to staging area."""
    slug = metadata["slug"]
    version = metadata["version"]
    staging_path = Path(DEFAULT_STAGING_DIR) / f"{slug.replace('/', '_')}-{version}"
    staging_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Staging {slug} at {staging_path}...", file=sys.stderr)
    # Mock download/extract
    (staging_path / "metadata.json").write_text(json.dumps(metadata, indent=2))
    (staging_path / "smoke_test.py").write_text("print('Smoke test OK')")
    
    return staging_path

def smoke_test(staging_path: Path) -> bool:
    """Run smoke test on staged artifact."""
    test_script = staging_path / "smoke_test.py"
    if not test_script.exists():
        print("No smoke test found, skipping.", file=sys.stderr)
        return True
    
    try:
        run_command([sys.executable, str(test_script)])
        print("Smoke test PASSED.", file=sys.stderr)
        return True
    except Exception as e:
        print(f"Smoke test FAILED: {e}", file=sys.stderr)
        return False

def promote_install(staging_path: Path) -> Path:
    """Move staged artifact to production directory with rollback support."""
    meta_file = staging_path / "metadata.json"
    if not meta_file.exists():
        raise InstallerError("Metadata missing in staging area.", "corrupt_staging")
    
    meta = json.loads(meta_file.read_text())
    kind = meta["kind"]
    slug = meta["slug"]
    
    dest_base = Path(DEFAULT_PRODUCTION_DIR)
    if kind == "skill":
        dest = dest_base / "skills" / slug.split("/")[-1]
    elif kind == "plugin":
        dest = dest_base / "plugins" / slug.split("/")[-1]
    else:
        raise InstallerError(f"Unsupported kind for promotion: {kind}")

    print(f"Promoting {slug} to {dest}...", file=sys.stderr)
    dest.parent.mkdir(parents=True, exist_ok=True)
    
    # Create backup if exists
    backup_path = None
    if dest.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        backup_path = Path(DEFAULT_BACKUP_DIR) / f"{slug.replace('/', '_')}-{stamp}.bak"
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Backing up existing version to {backup_path}...", file=sys.stderr)
        shutil.copytree(dest, backup_path)

    try:
        # Remove old version if it exists (using shutil for safety)
        if dest.exists():
            if dest.is_dir():
                shutil.rmtree(dest)
            else:
                dest.unlink()
                
        # Move staging to production (use copytree + rmtree for cross-filesystem)
        shutil.copytree(str(staging_path), str(dest))
        shutil.rmtree(staging_path)
        
        # Cleanup backup after successful promotion
        if backup_path and backup_path.exists():
            shutil.rmtree(backup_path)
            
        return dest
    except Exception as e:
        print(f"Promotion failed: {e}. Attempting rollback...", file=sys.stderr)
        if backup_path and backup_path.exists():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(str(backup_path), str(dest))
            shutil.rmtree(backup_path)
            print("Rollback successful.", file=sys.stderr)
        raise InstallerError(f"Promotion failed and rollback attempted: {e}", "promotion_failed")

def main():
    parser = argparse.ArgumentParser(description="ClawHub Autonomous Installer")
    sub = parser.add_subparsers(dest="command", required=True)
    
    # Propose install
    prop = sub.add_parser("propose", help="Analyze and propose installation")
    prop.add_argument("--slug", required=True)
    
    # Execute install
    exec_inst = sub.add_parser("install", help="Execute installation with approval token")
    exec_inst.add_argument("--slug", required=True)
    exec_inst.add_argument("--token", required=True)
    exec_inst.add_argument("--confirm-high-risk", action="store_true", help="Explicit confirmation for HIGH risk items")
    
    # Promote
    prom = sub.add_parser("promote", help="Promote staged installation to production")
    prom.add_argument("--staging-path", required=True)

    args = parser.parse_args()
    
    try:
        if args.command == "propose":
            meta = fetch_catalog(args.slug)
            validate_metadata(meta)
            risk = analyze_risk(meta)
            cmd = request_approval(meta["kind"], meta["slug"], meta["version"], risk)
            
            print(json.dumps({
                "ok": True,
                "proposal": {
                    "slug": meta["slug"],
                    "kind": meta["kind"],
                    "version": meta["version"],
                    "risk_level": risk,
                    "capabilities": meta["capabilities"],
                    "dependencies": meta.get("dependencies", []),
                    "description": meta["description"],
                    "approval_required": cmd
                }
            }, indent=2))
            
        elif args.command == "install":
            meta = fetch_catalog(args.slug)
            validate_metadata(meta)
            check_dependencies(meta)
            risk = analyze_risk(meta)
            
            if risk == "HIGH" and not args.confirm_high_risk:
                raise InstallerError("High risk item detected. Explicit confirmation required: use --confirm-high-risk flag.", "high_risk_escalation")

            if not verify_approval(meta["kind"], meta["slug"], meta["version"], args.token):
                raise InstallerError("Valid approval token required to proceed.", "unauthorized")
            
            staging_path = staging_install(meta)
            if not smoke_test(staging_path):
                # Cleanup staging
                print(f"Cleaning up failed installation at {staging_path}")
                raise InstallerError("Smoke test failed, installation aborted.", "smoke_test_failed")
            
            print(json.dumps({
                "ok": True,
                "status": "installed_to_staging",
                "staging_path": str(staging_path),
                "message": f"Successfully installed {meta['slug']}@{meta['version']} to staging. Run promote to finalize."
            }, indent=2))

        elif args.command == "promote":
            staging_path = Path(args.staging_path)
            if not staging_path.exists():
                raise InstallerError(f"Staging path not found: {staging_path}", "staging_not_found")
            
            meta = json.loads((staging_path / "metadata.json").read_text())
            risk = analyze_risk(meta)
            
            dest_path = promote_install(staging_path)
            
            log_audit({
                "action": "promote",
                "slug": meta["slug"],
                "version": meta["version"],
                "kind": meta["kind"],
                "risk_level": risk,
                "dest_path": str(dest_path)
            })
            
            print(json.dumps({
                "ok": True,
                "status": "promoted",
                "dest_path": str(dest_path),
                "message": f"Successfully promoted {meta['slug']} to production."
            }, indent=2))
            
    except InstallerError as e:
        print(json.dumps({"ok": False, "code": e.code, "message": str(e)}, indent=2))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"ok": False, "code": "system_error", "message": str(e)}, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()
