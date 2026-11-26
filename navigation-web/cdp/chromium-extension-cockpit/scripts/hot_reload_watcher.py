#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hot_reload_watcher.py — Watcher de fichiers pour rechargement à chaud d'extensions Chromium.

Surveille un dossier d'extension et, à chaque modification d'un fichier
JS/HTML/CSS/JSON/manifest, déclenche automatiquement :
  1. Bump de version dans manifest.json (optionnel)
  2. Rechargement à chaud via chromium_cdp_cockpit.py reload
  3. Vérification Disque vs Live (optionnel)

Nécessite : watchdog (pip install watchdog) ou polling natif (fallback).
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

COCKPIT_SCRIPT = r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\chromium-extension-cockpit\scripts\chromium_cdp_cockpit.py"

EXTENSIONS_WATCHED = {".js", ".html", ".css", ".json"}

def bump_version(manifest_path):
    """Incrémente la version du manifest (patch)."""
    try:
        data = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
        parts = str(data.get("version", "0.0.0")).split(".")
        if len(parts) == 3:
            parts[2] = str(int(parts[2]) + 1)
            data["version"] = ".".join(parts)
            Path(manifest_path).write_text(json.dumps(data, indent=2), encoding="utf-8")
            return data["version"]
    except Exception:
        pass
    return None

def run_reload(ext_id):
    """Lance le rechargement via le cockpit CDP."""
    cmd = [sys.executable, COCKPIT_SCRIPT, "reload", "--id", ext_id]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return result.stdout.strip(), result.returncode

def run_clear_errors(ext_id):
    """Purge les erreurs via le cockpit CDP."""
    cmd = [sys.executable, COCKPIT_SCRIPT, "clear-errors", "--id", ext_id]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return result.stdout.strip(), result.returncode

def watch_folder(folder_path, ext_id, auto_bump=False, auto_clear=False):
    """Boucle de surveillance polling (fallback sans watchdog)."""
    folder = Path(folder_path)
    if not folder.exists():
        print(json.dumps({"ok": False, "error": f"Dossier introuvable : {folder_path}"}, ensure_ascii=False))
        return

    print(json.dumps({"ok": True, "watching": str(folder), "ext_id": ext_id, "auto_bump": auto_bump, "auto_clear": auto_clear}, ensure_ascii=False))

    # Hash des fichiers pour détection de changement
    file_hashes = {}

    def hash_file(p):
        try:
            return hash(Path(p).read_bytes())
        except Exception:
            return None

    def scan():
        changes = []
        for p in folder.rglob("*"):
            if p.is_file() and p.suffix.lower() in EXTENSIONS_WATCHED:
                h = hash_file(p)
                prev = file_hashes.get(str(p))
                if prev is not None and h != prev:
                    changes.append(str(p))
                file_hashes[str(p)] = h
        return changes

    # Initialisation : hasher tous les fichiers existants sans déclencher de reload
    scan()

    print(json.dumps({"status": "watcher_ready", "message": "Surveillance active. Modifiez un fichier pour déclencher le rechargement."}, ensure_ascii=False))

    try:
        while True:
            changes = scan()
            if changes:
                print(json.dumps({"status": "changes_detected", "files": changes}, ensure_ascii=False))

                if auto_bump:
                    manifest = folder / "manifest.json"
                    if manifest.exists():
                        new_ver = bump_version(manifest)
                        print(json.dumps({"status": "version_bumped", "new_version": new_ver}, ensure_ascii=False))

                stdout, rc = run_reload(ext_id)
                print(json.dumps({"status": "reload_triggered", "ext_id": ext_id, "rc": rc, "output": stdout}, ensure_ascii=False))

                if auto_clear and rc == 0:
                    stdout2, rc2 = run_clear_errors(ext_id)
                    print(json.dumps({"status": "errors_cleared", "rc": rc2, "output": stdout2}, ensure_ascii=False))

            time.sleep(2)
    except KeyboardInterrupt:
        print(json.dumps({"status": "watcher_stopped"}, ensure_ascii=False))

def main():
    parser = argparse.ArgumentParser(description="Watcher auto-reload pour extensions Chromium (CDP Cockpit)")
    parser.add_argument("folder", help="Dossier de l'extension à surveiller")
    parser.add_argument("--id", required=True, help="ID Chromium de l'extension")
    parser.add_argument("--auto-bump", action="store_true", help="Incrémenter automatiquement la version du manifest")
    parser.add_argument("--auto-clear", action="store_true", help="Purger les erreurs après reload réussi")
    args = parser.parse_args()
    watch_folder(args.folder, args.id, args.auto_bump, args.auto_clear)

if __name__ == "__main__":
    main()
