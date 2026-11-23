#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
debug_enforcer.py — Skill Debug Enforcer
Gate pre-commit qui scanne les fichiers Python modifiés pour patterns anti-patterns.
Usage: python debug_enforcer.py [--strict] [--files file1.py file2.py...]
"""
import json
import re
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Any

PATTERNS_FILE = Path(__file__).parent / "patterns.json"

def load_patterns() -> List[Dict[str, Any]]:
    """Charge les patterns depuis patterns.json."""
    try:
        with open(PATTERNS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("patterns", [])
    except Exception as e:
        print(f"ERREUR chargement patterns: {e}", file=sys.stderr)
        return []

SEVERITY_ORDER = {"CRITICAL": 3, "WARNING": 2, "INFO": 1, "OK": 0}

def get_staged_python_files() -> List[Path]:
    """Récupère les fichiers .py staged via git diff --cached."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--", "*.py"],
            capture_output=True, text=True, check=True, timeout=10
        )
        files = [Path(f.strip()) for f in result.stdout.strip().split("\n") if f.strip()]
        return [f for f in files if f.exists()]
    except subprocess.CalledProcessError:
        return []

def scan_file(filepath: Path) -> List[Dict[str, Any]]:
    """Scanne un fichier pour les patterns interdits."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return [{"file": str(filepath), "line": 0, "pattern": "read_error", "severity": "CRITICAL", "context": str(e)}]

    lines = content.split("\n")
    violations = []

    for pattern_def in load_patterns():
        regex = pattern_def["regex"]
        severity = pattern_def["severity"]
        desc = pattern_def["description"]
        name = pattern_def["name"]

        for i, line in enumerate(lines, 1):
            if re.search(regex, line):
                violations.append({
                    "file": str(filepath),
                    "line": i,
                    "pattern": name,
                    "severity": severity,
                    "description": desc,
                    "context": line.strip()[:120]
                })

    return violations

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Debug Enforcer - Pre-commit gate for Python patterns")
    parser.add_argument("--strict", action="store_true", help="Bloquer aussi sur WARNING")
    parser.add_argument("--files", nargs="*", help="Fichiers spécifiques à scanner (défaut: git staged)")
    args = parser.parse_args()

    if args.files:
        files = [Path(f) for f in args.files if Path(f).exists()]
    else:
        files = get_staged_python_files()

    if not files:
        print(json.dumps({"ok": True, "files_scanned": 0, "violations": [], "message": "No Python files staged"}))
        return 0

    all_violations = []
    for f in files:
        all_violations.extend(scan_file(f))

    # Filtrer selon sévérité
    critical = [v for v in all_violations if v["severity"] == "CRITICAL"]
    warning = [v for v in all_violations if v["severity"] == "WARNING"]
    info = [v for v in all_violations if v["severity"] == "INFO"]

    result = {
        "ok": len(critical) == 0 and (not args.strict or len(warning) == 0),
        "files_scanned": len(files),
        "violations": {
            "critical": critical,
            "warning": warning,
            "info": info
        },
        "summary": {
            "critical_count": len(critical),
            "warning_count": len(warning),
            "info_count": len(info)
        }
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1

if __name__ == "__main__":
    sys.exit(main())