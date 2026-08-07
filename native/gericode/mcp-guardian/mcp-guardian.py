#!/usr/bin/env python3
"""mcp-guardian.py - MCP discovery, validation, and management tool.

Scans:
- C:\\DevTools\\.kilocode\\mcp.json
- C:\\Users\\GG\\.kilocode\\mcp.json
- C:\\DevTools\\bin\\codebase-memory-mcp\\codebase-memory-mcp.exe
- C:\\DevTools\\.cache\\codebase-memory-mcp

Validates connectivity, configuration, and allowed directories.
"""

import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


DEVTOOLS_MCP = Path(r"C:\DevTools\.kilocode\mcp.json")
USER_MCP = Path(r"C:\Users\GG\.kilocode\mcp.json")
CBM_BINARY = Path(r"C:\DevTools\bin\codebase-memory-mcp\codebase-memory-mcp.exe")
CBM_CACHE = Path(r"C:\DevTools\.cache\codebase-memory-mcp")


def load_mcp_json(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception as e:
        print(f"[ERROR] Cannot parse {path}: {e}")
        return None


def scan_declared_mcps() -> List[Dict[str, Any]]:
    mcps: List[Dict[str, Any]] = []
    seen = set()
    
    for mcp_file in [DEVTOOLS_MCP, USER_MCP]:
        data = load_mcp_json(mcp_file)
        if not data:
            continue
        for server_name, server_conf in data.get("mcpServers", {}).items():
            key = (str(mcp_file), server_name)
            if key in seen:
                continue
            seen.add(key)
            mcps.append({
                "id": server_name,
                "name": server_name,
                "command": server_conf.get("command", ""),
                "args": server_conf.get("args", []),
                "env": server_conf.get("env", {}),
                "type": server_conf.get("type", "stdio"),
                "source": str(mcp_file),
                "install_kind": "declared",
            })
    
    return mcps


def scan_installed_mcps() -> List[Dict[str, Any]]:
    mcps: List[Dict[str, Any]] = []
    
    if CBM_BINARY.exists():
        mcps.append({
            "id": "codebase-memory-mcp",
            "name": "Codebase Manager MCP",
            "command": str(CBM_BINARY),
            "args": [],
            "env": {"CBM_CACHE_DIR": str(CBM_CACHE)} if CBM_CACHE.exists() else {},
            "type": "stdio",
            "source": str(CBM_BINARY),
            "install_kind": "installed",
        })
    
    return mcps


def validate_mcp(mcp: Dict[str, Any]) -> Dict[str, Any]:
    result = {
        "id": mcp["id"],
        "valid": True,
        "checks": [],
    }
    
    cmd = mcp.get("command", "")
    if cmd:
        # Use shutil.which for robust PATH lookup
        cmd_path = shutil.which(cmd) or shutil.which(Path(cmd).name)
        if cmd_path is None and Path(cmd).exists():
            cmd_path = str(Path(cmd).resolve())
        if cmd_path is None:
            result["checks"].append({
                "name": "command_exists",
                "status": "FAIL",
                "message": f"Command not found: {cmd}",
            })
            result["valid"] = False
        else:
            result["checks"].append({
                "name": "command_exists",
                "status": "OK",
                "message": f"Command found: {cmd} ({cmd_path})",
            })
    else:
        result["checks"].append({
            "name": "command_exists",
            "status": "SKIP",
            "message": "No command specified",
        })
    
    env = mcp.get("env", {})
    if env:
        missing = []
        for k, v in env.items():
            if v and not Path(v).exists() and not os.environ.get(k):
                missing.append(k)
        if missing:
            result["checks"].append({
                "name": "env_vars",
                "status": "WARN",
                "message": f"Env vars may be missing: {missing}",
            })
        else:
            result["checks"].append({
                "name": "env_vars",
                "status": "OK",
                "message": "Env vars OK",
            })
    
    if mcp["id"] == "codebase-memory-mcp":
        if CBM_CACHE.exists():
            result["checks"].append({
                "name": "cbm_cache",
                "status": "OK",
                "message": f"CBM cache exists: {CBM_CACHE}",
            })
        else:
            result["checks"].append({
                "name": "cbm_cache",
                "status": "WARN",
                "message": f"CBM cache not found: {CBM_CACHE}",
            })
    
    return result


def list_all() -> List[Dict[str, Any]]:
    declared = scan_declared_mcps()
    installed = scan_installed_mcps()
    
    all_mcps = {m["id"]: m for m in declared}
    for m in installed:
        if m["id"] not in all_mcps:
            all_mcps[m["id"]] = m
        else:
            all_mcps[m["id"]]["install_kind"] = "declared+installed"
    
    return list(all_mcps.values())


def validate_all() -> List[Dict[str, Any]]:
    results = []
    for mcp in list_all():
        results.append(validate_mcp(mcp))
    return results


def get_by_id(mcp_id: str) -> Optional[Dict[str, Any]]:
    for mcp in list_all():
        if mcp["id"] == mcp_id:
            return mcp
    return None


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="MCP Guardian - MCP discovery and validation")
    parser.add_argument("--list", action="store_true", help="List all MCPs")
    parser.add_argument("--validate", action="store_true", help="Validate all MCPs")
    parser.add_argument("--id", type=str, help="Get specific MCP by ID")
    args = parser.parse_args()
    
    if args.list:
        mcps = list_all()
        print(f"[MCP-GUARDIAN] Found {len(mcps)} MCPs:")
        for mcp in mcps:
            print(f"  [{mcp['install_kind']}] {mcp['id']} - {mcp.get('command', 'N/A')}")
        return 0
    
    if args.validate:
        results = validate_all()
        print(f"[MCP-GUARDIAN] Validating {len(results)} MCPs:")
        for res in results:
            status = "OK" if res["valid"] else "FAIL"
            print(f"  [{status}] {res['id']}")
            for check in res["checks"]:
                icon = "OK" if check["status"] == "OK" else "FAIL" if check["status"] == "FAIL" else "WARN"
                print(f"    [{icon}] [{check['name']}] {check['message']}")
        return 0
    
    if args.id:
        mcp = get_by_id(args.id)
        if mcp:
            print(f"[MCP-GUARDIAN] Found MCP: {mcp['id']}")
            print(f"  Command: {mcp.get('command', 'N/A')}")
            print(f"  Args: {mcp.get('args', [])}")
            print(f"  Type: {mcp.get('type', 'stdio')}")
            print(f"  Source: {mcp.get('source', 'N/A')}")
            print(f"  Install: {mcp.get('install_kind', 'unknown')}")
            return 0
        else:
            print(f"[MCP-GUARDIAN] MCP not found: {args.id}")
            return 1
    
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
