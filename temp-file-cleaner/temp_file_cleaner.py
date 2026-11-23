#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
temp_file_cleaner.py — Temp File Cleaner
Nettoie les fichiers temporaires orphelins (.tmp, .log anciens, .obj, etc.)
Usage: python temp_file_cleaner.py [--dry-run] [--paths path1,path2...] [--max-age-days 7] [--size-limit-mb 100]
"""
import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Config par défaut
DEFAULT_MAX_AGE_DAYS = 7
TMP_MAX_AGE_DAYS = 1
SIZE_LIMIT_MB = 100
PROTECTED_FILES = {"interception-log.txt"}

# Répertoires à nettoyer par défaut
DEFAULT_PATHS = [
    r"D:\DO\WEB\TOOLS\L4-TOOLS",
    r"D:\DO\WEB\TOOLS\L3-CITIZENS\CITIZENS",
    r"D:\DO\WEB\TOOLS\L3-CITIZENS\LOOPX",
]

# Extensions et âges max
FILE_PATTERNS = {
    ".tmp": 1,      # 1 jour
    ".log": 7,      # 7 jours
    ".obj": 7,
    ".pyc": 7,
    ".log": 7,
}

PROTECTED_FILES = {"interception-log.txt"}


def find_temp_files(paths: List[str], max_age_days: int = 7) -> List[Dict]:
    """Trouve les fichiers temporaires dépassant l'âge max."""
    results = []
    cutoff = datetime.now() - timedelta(days=max_age_days)
    
    for base_path in paths:
        base = Path(path)
        if not base.exists():
            continue
        
        for file_path in base.rglob("*"):
            if not file_path.is_file():
                continue
            
            # Ignorer les fichiers protégés
            if file_path.name in PROTECTED_FILES:
                continue
            
            # Vérifier l'extension
            ext = file_path.suffix.lower()
            if ext not in {".tmp", ".log", ".obj", ".pyc"}:
                continue
            
            # Vérifier l'âge
            try:
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if mtime < datetime.now() - timedelta(days=1 if file_path.suffix == ".tmp" else 7):
                    results.append({
                        "path": str(file_path),
                        "size_mb": round(file_path.stat().st_size / 1024 / 1024, 2),
                        "mtime": file_path.stat().st_mtime,
                        "age_days": (datetime.now() - mtime).days,
                        "extension": file_path.suffix
                    })
            except Exception:
                pass
    
    return results


def clean_files(files: List[Dict], dry_run: bool = True) -> Dict:
    """Supprime les fichiers temporaires."""
    purged = []
    kept = []
    errors = []
    total_freed = 0.0
    
    for f in files:
        try:
            path = Path(f["path"])
            size_mb = f["size_mb"]
            
            # Vérifier si fichier verrouillé
            try:
                with open(f["path"], "r+b") as f_test:
                    pass
            except IOError:
                errors.append({"path": f["path"], "error": "File locked"})
                continue
            
            # Vérifier taille
            if f["size_mb"] > 100:
                errors.append({"path": f["path"], "error": f"File too large ({f['size_mb']}MB) > 100MB limit"})
                continue
            
            if not dry_run:
                try:
                    os.remove(f["path"])
                    purged.append(f)
                    total_freed += f["size_mb"]
                except Exception as e:
                    errors.append({"path": f["path"], "error": f"Remove failed: {e}"})
            else:
                purged.append(f)
                total_freed += f["size_mb"]
                
        except Exception as e:
            errors.append({"path": f["path"], "error": str(e)})
    
    return {
        "purged": purged,
        "errors": errors,
        "total_freed_mb": round(total_freed, 2)
    }


def main():
    parser = argparse.ArgumentParser(description="Temp File Cleaner - Nettoie fichiers temporaires")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Lister sans supprimer (défaut)")
    parser.add_argument("--apply", action="store_true", help="Appliquer la suppression")
    parser.add_argument("--paths", nargs="*", default=[], help="Chemins à nettoyer (défaut: L4-TOOLS, CITIZENS, LOOPX)")
    parser.add_argument("--max-age-days", type=int, default=7, help="Âge max en jours (défaut 7, tmp=1 jour)")
    parser.add_argument("--size-limit-mb", type=int, default=100, help="Limite taille en MB (défaut 100)")
    
    args = parser.parse_args()
    
    dry_run = not args.apply
    
    paths = args.paths if args.paths else [r"D:\DO\WEB\TOOLS\L4-TOOLS", r"D:\DO\WEB\TOOLS\L3-CITIZENS\CITIZENS", r"D:\DO\WEB\TOOLS\L3-CITIZENS\LOOPX"]
    
    print(f"Scanning paths: {paths}", file=sys.stderr)
    print(f"Max age: {args.max_age_days} days (tmp: 1 day)", file=sys.stderr)
    print(f"Mode: {'APPLY' if not dry_run else 'DRY RUN'}", file=sys.stderr)
    
    # Trouver fichiers
    temp_files = find_temp_files(args.paths, args.max_age_days)
    
    if not temp_files:
        result = {
            "ok": True,
            "files_scanned": 0,
            "files_purged": 0,
            "files_kept": 0,
            "total_size_freed_mb": 0,
            "errors": [],
            "dry_run": dry_run,
            "message": "Aucun fichier temporaire trouvé."
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    
    print(f"Fichiers trouvés: {len(temp_files)}")
    for f in temp_files[:10]:
        print(f"  {f['path']} ({f['size_mb']} MB, {f['age_days']} jours, {f['extension']})", file=sys.stderr)
    if len(temp_files) > 10:
        print(f"  ... et {len(temp_files) - 10} autres", file=sys.stderr)
    
    # Vérifier tailles
    large_files = [f for f in temp_files if f["size_mb"] > 100]
    if large_files:
        print(f"ATTENTION: {len(large_files)} fichiers > 100MB détectés", file=sys.stderr)
        for f in large_files:
            print(f"  {f['path']} ({f['size_mb']} MB)", file=sys.stderr)
    
    # Nettoyer
    result = clean_files(temp_files, dry_run=dry_run)
    
    # Rapport
    report = {
        "ok": True,
        "files_scanned": len(temp_files),
        "files_purged": len(result["purged"]),
        "files_kept": len(temp_files) - len(result["purged"]),
        "total_size_freed_mb": round(sum(f["size_mb"] for f in result["purged"]), 2),
        "errors": result["errors"],
        "dry_run": dry_run
    }
    
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if len(result["errors"]) == 0 else 1


if __name__ == "__main__":
    import argparse
    sys.exit(main())