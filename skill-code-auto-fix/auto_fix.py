#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto_fix.py — Skill Code Auto-Fix
Auto-correction de patterns de code défectueux dans les skills Python.
Usage: python auto_fix.py [--dry-run] [--files file1.py file2.py...] [--apply]
"""
import re
import sys
import ast
import json
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Any

SKILLS_DIR = Path(__file__).parent.parent

# Patterns de correction (regex search -> replacement)
FIX_PATTERNS = [
    {
        "name": "fix_double_cdp_send_while_recv",
        "search": r"(await\s+cdp_send\s*\([^)]*\))\s*\n\s*while\s+True:\s*await\s+ws\.recv\(\)",
        "replace": r"\1",
        "description": "Supprime double attente cdp_send + while ws.recv"
    },
    {
        "name": "fix_double_await_ws_recv",
        "search": r"(await\s+ws\.recv\(\))\s*\n\s*\1",
        "replace": r"\1",
        "description": "Supprime double await ws.recv()"
    },
    {
        "name": "fix_missing_ws_in_evaluate_js",
        "search": r"(await\s+evaluate_js\s*\()\s*(?!\s*ws\s*[,)])",
        "replace": r"\1ws, ",
        "description": "Ajoute ws en premier argument de evaluate_js"
    },
    {
        "name": "fix_double_cdp_send_while_true_recv",
        "search": r"(await\s+cdp_send\s*\([^)]*\))\s*\n\s*while\s+True:\s*await\s+ws\.recv\(\)",
        "replace": r"\1",
        "description": "Supprime await cdp_send + while True: await ws.recv()"
    },
]

FIX_PATTERNS_FILE = Path(__file__).parent / "patterns.json"


def load_fix_patterns() -> List[Dict[str, Any]]:
    """Charge les patterns de correction depuis patterns.json."""
    patterns_file = Path(__file__).parent / "patterns.json"
    try:
        with open(patterns_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("patterns", [])
    except Exception:
        return FIX_PATTERNS


def backup_file(filepath: Path) -> Path:
    """Crée une sauvegarde .bak du fichier."""
    bak_path = filepath.with_suffix(filepath.suffix + ".bak")
    shutil.copy2(filepath, bak_path)
    return bak_path


def restore_backup(filepath: Path, bak_path: Path):
    """Restaure le fichier depuis sa sauvegarde."""
    shutil.copy2(bak_path, filepath)
    bak_path.unlink(missing_ok=True)


def apply_fixes(content: str, patterns: List[Dict]) -> tuple[str, List[Dict]]:
    """Applique les patterns de correction sur le contenu."""
    fixes_applied = []
    modified_content = content
    
    for pattern_def in patterns:
        name = pattern_def["name"]
        search = pattern_def["search"]
        replace = pattern_def["replace"]
        desc = pattern_def["description"]
        
        # Compter les occurrences avant
        matches_before = list(re.finditer(search, modified_content))
        if matches_before:
            # Appliquer le remplacement
            new_content = re.sub(search, replace, modified_content, flags=re.MULTILINE | re.DOTALL)
            if new_content != modified_content:
                fixes_applied.append({
                    "pattern": name,
                    "description": pattern_def["description"],
                    "count": len(matches_before)
                })
                modified_content = new_content
    
    return modified_content, fixes_applied


def validate_python_syntax(content: str) -> tuple[bool, str]:
    """Valide la syntaxe Python du contenu."""
    try:
        ast.parse(content)
        return True, ""
    except SyntaxError as e:
        return False, f"SyntaxError: {e.msg} at line {e.lineno}"


def validate_python_compile(filepath: Path) -> tuple[bool, str]:
    """Valide le fichier avec python -m py_compile."""
    try:
        subprocess.run(
            [sys.executable, "-m", "py_compile", str(filepath)],
            capture_output=True, check=True, timeout=10
        )
        return True, ""
    except subprocess.CalledProcessError as e:
        return False, e.stderr.decode() if e.stderr else str(e)


def fix_file(filepath: Path, dry_run: bool = False) -> Dict[str, Any]:
    """Corrige un fichier Python."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return {"ok": False, "file": str(filepath), "error": f"Read error: {e}"}

    # Sauvegarder
    bak_path = backup_file(filepath)
    
    try:
        patterns = load_fix_patterns()
        modified_content, fixes = apply_fixes(content, patterns)
        
        if not fixes:
            # Pas de modification nécessaire
            bak_path.unlink(missing_ok=True)
            return {"ok": True, "file": str(filepath), "fixes": [], "changed": False}
        
        # Valider syntaxe
        ok, err = validate_python_syntax(modified_content)
        if not ok:
            restore_backup(filepath, bak_path)
            return {"ok": False, "file": str(filepath), "error": f"Syntax error after fix: {err}", "fixes_attempted": len(fixes)}
        
        if not dry_run:
            # Écrire le fichier modifié
            filepath.write_text(modified_content, encoding="utf-8")
            
            # Valider avec py_compile
            ok, err = validate_python_compile(filepath)
            if not ok:
                restore_backup(filepath, bak_path)
                return {"ok": False, "file": str(filepath), "error": f"Compile error: {err}", "fixes_attempted": len(fixes)}
            
            # Supprimer backup si tout OK
            bak_path.unlink(missing_ok=True)
            return {"ok": True, "file": str(filepath), "fixes": fixes, "changed": True}
        else:
            # Dry run : restaurer et reporter
            restore_backup(filepath, bak_path)
            return {"ok": True, "file": str(filepath), "fixes": fixes, "changed": True, "dry_run": True}
            
    except Exception as e:
        restore_backup(filepath, bak_path)
        return {"ok": False, "file": str(filepath), "error": f"Unexpected error: {e}"}


def load_fix_patterns() -> List[Dict]:
    """Charge les patterns de correction."""
    patterns_file = Path(__file__).parent / "patterns.json"
    try:
        with open(patterns_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("patterns", [])
    except Exception:
        return FIX_PATTERNS


# Patterns de correction par défaut (fallback)
FIX_PATTERNS = [
    {
        "name": "fix_double_cdp_send_while_recv",
        "search": r"(await\s+cdp_send\s*\([^)]*\))\s*\n\s*while\s+True:\s*await\s+ws\.recv\(\)",
        "replace": r"\1",
        "description": "Supprime double attente cdp_send + while ws.recv"
    },
    {
        "name": "fix_double_await_ws_recv",
        "search": r"(await\s+ws\.recv\(\))\s*\n\s*\1",
        "replace": r"\1",
        "description": "Supprime double await ws.recv()"
    },
    {
        "name": "fix_missing_ws_in_evaluate_js",
        "search": r"(await\s+evaluate_js\s*\()\s*(?!\s*ws\s*[,)])",
        "replace": r"\1ws, ",
        "description": "Ajoute ws en premier argument de evaluate_js"
    },
    {
        "name": "fix_double_cdp_send_while_true_recv",
        "search": r"(await\s+cdp_send\s*\([^)]*\))\s*\n\s*while\s+True:\s*await\s+ws\.recv\(\)",
        "replace": r"\1",
        "description": "Supprime await cdp_send + while True: await ws.recv()"
    },
]


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Code Auto-Fix - Auto-correction patterns Python")
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans modifier")
    parser.add_argument("--apply", action="store_true", help="Appliquer les corrections")
    parser.add_argument("--files", nargs="*", help="Fichiers spécifiques à corriger")
    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        print("ERREUR: Spécifier --dry-run ou --apply", file=sys.stderr)
        return 1

    dry_run = args.dry_run
    
    if args.files:
        files = [Path(f) for f in args.files if Path(f).exists()]
    else:
        # Scanner tous les .py dans SKILLS
        files = list(SKILLS_DIR.rglob("*.py"))
        files = [f for f in files if "__pycache__" not in str(f) and "test_" not in f.name]

    if not files:
        print(json.dumps({"ok": True, "message": "Aucun fichier à traiter"}))
        return 0

    results = []
    total_fixes = 0
    
    for f in files:
        result = fix_file(f, dry_run=dry_run)
        results.append(result)
        if result.get("fixes"):
            total_fixes += len(result["fixes"])

    summary = {
        "ok": all(r.get("ok", False) for r in results),
        "files_processed": len(files),
        "files_changed": sum(1 for r in results if r.get("changed")),
        "total_fixes_applied": total_fixes,
        "dry_run": dry_run,
        "results": results
    }

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if all(r.get("ok", False) for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())