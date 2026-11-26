#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chromium_hmr_watcher.py — Watcher HMR (Hot Module Replacement) pour extensions Chromium.

Surveille un dossier d'extension et, à chaque modification d'un fichier
JS/JSON/HTML/CSS, déclenche automatiquement le rechargement à chaud via CDP
(port 9222), avec anti-rebond (debounce 150 ms) et auto-réveil si l'extension
est désactivée.

Nécessite : chromium_cdp_cockpit.py (déjà dans le même dossier scripts/).
"""

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

COCKPIT_SCRIPT = r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\chromium-extension-cockpit\scripts\chromium_cdp_cockpit.py"

WATCHED_EXTENSIONS = {".js", ".json", ".html", ".css", ".py"}
DEBOUNCE_MS = 150


def file_hash(path):
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    except Exception:
        return None


def run_reload(ext_id):
    """Rechargement à chaud via le cockpit CDP (avec auto-réveil intégré)."""
    cmd = [sys.executable, COCKPIT_SCRIPT, "reload", "--id", ext_id]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return result.stdout.strip(), result.returncode


def run_clear_errors(ext_id):
    """Purge le journal d'erreurs via le cockpit CDP."""
    cmd = [sys.executable, COCKPIT_SCRIPT, "clear-errors", "--id", ext_id]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return result.stdout.strip(), result.returncode


def scan_changes(folder, file_hashes):
    """Détecte les fichiers modifiés depuis le dernier scan."""
    changes = []
    for p in folder.rglob("*"):
        if p.is_file() and p.suffix.lower() in WATCHED_EXTENSIONS:
            h = file_hash(p)
            prev = file_hashes.get(str(p))
            if prev is not None and h != prev:
                changes.append(str(p))
            file_hashes[str(p)] = h
    return changes


def init_hashes(folder):
    """Hash initial de tous les fichiers surveillés (sans déclencher de reload)."""
    hashes = {}
    for p in folder.rglob("*"):
        if p.is_file() and p.suffix.lower() in WATCHED_EXTENSIONS:
            hashes[str(p)] = file_hash(p)
    return hashes


def watch_folder(folder_path, ext_id, auto_clear=True):
    folder = Path(folder_path)
    if not folder.exists():
        print(json.dumps({"ok": False, "error": f"Dossier introuvable : {folder_path}"}, ensure_ascii=False))
        return 1

    print(json.dumps({
        "ok": True,
        "watching": str(folder),
        "ext_id": ext_id,
        "debounce_ms": DEBOUNCE_MS,
        "auto_clear": auto_clear
    }, ensure_ascii=False))

    file_hashes = init_hashes(folder)
    last_change = 0.0

    print(json.dumps({"status": "watcher_ready", "message": "Surveillance active. Modifiez un fichier pour déclencher le rechargement HMR."}, ensure_ascii=False))

    try:
        while True:
            changes = scan_changes(folder, file_hashes)
            if changes:
                now = time.time()
                if now - last_change >= DEBOUNCE_MS / 1000.0:
                    last_change = now
                    print(json.dumps({"status": "changes_detected", "files": changes}, ensure_ascii=False))

                    stdout, rc = run_reload(ext_id)
                    print(json.dumps({"status": "reload_triggered", "ext_id": ext_id, "rc": rc, "output": stdout}, ensure_ascii=False))

                    if auto_clear and rc == 0:
                        stdout2, rc2 = run_clear_errors(ext_id)
                        print(json.dumps({"status": "errors_cleared", "rc": rc2, "output": stdout2}, ensure_ascii=False))

            time.sleep(0.2)
    except KeyboardInterrupt:
        print(json.dumps({"status": "watcher_stopped"}, ensure_ascii=False))
        return 0


def main():
    parser = argparse.ArgumentParser(description="Watcher HMR pour extensions Chromium (CDP Cockpit)")
    parser.add_argument("folder", help="Dossier de l'extension à surveiller")
    parser.add_argument("--id", required=True, help="ID Chromium de l'extension")
    parser.add_argument("--no-auto-clear", action="store_true", help="Ne pas purger les erreurs après reload")
    args = parser.parse_args()
    return watch_folder(args.folder, args.id, auto_clear=not args.no_auto_clear)


if __name__ == "__main__":
    sys.exit(main())
