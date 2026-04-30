#!/usr/bin/env python3
"""
Proton Pass Helper for Hermes/REED Integration

Purpose: Lookup tool metadata from Proton Pass vault
Safety: Never returns passwords, only metadata (vault name, item exists, last verified)

Usage:
    python3 proton_pass_helper.py lookup <tool_name>
    python3 proton_pass_helper.py verify <tool_name>
    python3 proton_pass_helper.py sync <tool_name>
"""

import subprocess
import sys
import json
import re
from datetime import datetime
from typing import Optional, Dict, List

# Workbook path (relative to this script)
WORKBOOK_PATH = "/Users/banirisset/2_Areas/banirisset/ops/Tools Premium.xlsx"


def run_pass_cli(args: List[str]) -> subprocess.CompletedProcess:
    """Run pass-cli command and return result."""
    try:
        result = subprocess.run(
            ["pass-cli"] + args,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(args, 1, "", "Timeout")
    except FileNotFoundError:
        return subprocess.CompletedProcess(args, 127, "", "pass-cli not found in PATH")
    except Exception as e:
        return subprocess.CompletedProcess(args, 1, "", str(e))


def check_cli_available() -> bool:
    """Check if pass-cli is available and user is logged in."""
    result = run_pass_cli(["--version"])
    if result.returncode != 0:
        print(json.dumps({
            "error": "pass-cli not available",
            "detail": result.stderr
        }))
        return False
    
    # Check if logged in by trying to list vaults
    result = run_pass_cli(["vault", "list"])
    if result.returncode != 0:
        stderr_lower = result.stderr.lower()
        if "authenticated" in stderr_lower or "session" in stderr_lower or "logout" in stderr_lower:
            print(json.dumps({
                "status": "CLI ready, login required",
                "action_required": "Run: pass-cli login",
                "detail": "User must login interactively to Proton Pass"
            }))
            return False
        print(json.dumps({
            "error": "CLI error",
            "detail": result.stderr
        }))
        return False
    
    return True


def search_items(query: str) -> List[Dict]:
    """Search for items in Proton Pass matching query."""
    result = run_pass_cli(["item", "list", "--search", query])
    
    if result.returncode != 0:
        return []
    
    # Parse the output - pass-cli outputs items in a table format
    items = []
    lines = result.stdout.strip().split("\n")
    
    # Skip header lines and look for item data
    for line in lines:
        line = line.strip()
        if not line or "─" in line or "ID" in line:
            continue
        
        # Parse item line (format varies by vault/item type)
        # Return raw lines for now - caller can filter
        if line and not line.startswith("╭") and not line.startswith("╰"):
            items.append({"raw": line})
    
    return items


def lookup_tool(tool_name: str) -> Dict:
    """Lookup a tool by name in Proton Pass vaults."""
    if not check_cli_available():
        return {"found": False, "error": "CLI not available"}
    
    # Search for the tool
    items = search_items(tool_name)
    
    if not items:
        return {
            "found": False,
            "tool": tool_name,
            "message": f"'{tool_name}' not found in Proton Pass"
        }
    
    # Get vault list to map vault IDs to names
    vault_result = run_pass_cli(["vault", "list"])
    vaults = {}
    if vault_result.returncode == 0:
        for line in vault_result.stdout.strip().split("\n"):
            if "│" in line:
                parts = line.split("│")
                if len(parts) >= 3:
                    vault_id = parts[1].strip()
                    vault_name = parts[2].strip()
                    vaults[vault_id] = vault_name
    
    # For now, return candidate matches without passwords
    return {
        "found": True,
        "tool": tool_name,
        "candidates": len(items),
        "vaults": list(vaults.values())[:3],  # Return first 3 vault names
        "message": f"Found {len(items)} candidate(s). Use Proton Pass GUI for password retrieval.",
        "timestamp": datetime.now().isoformat()
    }


def verify_tool_exists(tool_name: str) -> Dict:
    """Quick check if tool exists in Proton Pass."""
    result = lookup_tool(tool_name)
    return {
        "tool": tool_name,
        "exists": result.get("found", False),
        "candidates": result.get("candidates", 0),
        "timestamp": datetime.now().isoformat()
    }


def sync_metadata(tool_name: str) -> Dict:
    """Verify and return metadata for workbook sync (no writes yet)."""
    result = lookup_tool(tool_name)
    
    if not result.get("found"):
        return {
            "tool": tool_name,
            "synced": False,
            "password_location": "Proton Pass - Not Found",
            "vault": "N/A",
            "last_verified": datetime.now().strftime("%Y-%m-%d")
        }
    
    return {
        "tool": tool_name,
        "synced": True,
        "password_location": "Proton Pass",
        "vault": result.get("vaults", ["Unknown"])[0],
        "last_verified": datetime.now().strftime("%Y-%m-%d"),
        "candidates": result.get("candidates", 1)
    }


def main():
    if len(sys.argv) < 3:
        print(json.dumps({
            "error": "Usage: proton_pass_helper.py <lookup|verify|sync> <tool_name>"
        }))
        sys.exit(1)
    
    command = sys.argv[1].lower()
    tool_name = sys.argv[2]
    
    if command == "lookup":
        result = lookup_tool(tool_name)
    elif command == "verify":
        result = verify_tool_exists(tool_name)
    elif command == "sync":
        result = sync_metadata(tool_name)
    else:
        print(json.dumps({
            "error": f"Unknown command: {command}",
            "available": ["lookup", "verify", "sync"]
        }))
        sys.exit(1)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
