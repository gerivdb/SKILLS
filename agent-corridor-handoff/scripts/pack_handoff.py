#!/usr/bin/env python3
# pack_handoff.py
# Agent Corridor Handoff — Compacteur de contexte pour transfert inter-sessions
# Conforme à la règle agent-corridor-handoff (intent_hash: 0xAGENT_CORRIDOR_HANDOFF_20261025)

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path.cwd()
TRANSFERS_DIR = REPO_ROOT / ".kilo" / "transfers"
PAYLOAD_FILE = TRANSFERS_DIR / "HANDOFF_PAYLOAD.json"


def now_utc():
    return datetime.now(timezone.utc).isoformat()


def run_git(args, cwd=None):
    """Exécute une commande git et retourne sa sortie texte."""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True, text=True, cwd=cwd or REPO_ROOT, timeout=30
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def get_modified_files():
    """Retourne la liste des fichiers modifiés entre HEAD~1 et HEAD."""
    output = run_git(["diff", "HEAD~1..HEAD", "--name-status"])
    files = []
    if output:
        for line in output.splitlines():
            parts = line.split("\t", 1)
            if len(parts) == 2:
                status, path = parts
                files.append({"status": status, "path": path})
            elif len(parts) == 1:
                files.append({"status": "M", "path": parts[0]})
    return files


def get_test_files():
    """Retourne la liste des fichiers de tests modifiés ou ajoutes."""
    all_files = get_modified_files()
    test_files = []
    for f in all_files:
        path = f["path"].lower()
        if path.startswith("test") or "/test" in path or path.endswith("_test.py") or path.endswith("test.py"):
            test_files.append(f["path"])
    return test_files


def get_key_decisions():
    """Extrait les messages de commit récents comme décisions clés."""
    output = run_git(["log", "HEAD~3..HEAD", "--format=%s"])
    decisions = []
    if output:
        for line in output.splitlines():
            if line.strip():
                decisions.append(line.strip())
    return decisions


def get_session_id():
    """Tente d'extraire l'ID de session depuis agent-manager.json."""
    am_file = REPO_ROOT / ".kilo" / "agent-manager.json"
    if am_file.exists():
        try:
            with am_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
            sessions = data.get("sessions", {})
            if sessions:
                # Retourner la dernière session créée
                last_sid = list(sessions.keys())[-1]
                return last_sid
        except Exception:
            pass
    return "unknown"


def build_payload():
    """Construit le payload de handoff ultra-compact."""
    return {
        "session_id": get_session_id(),
        "timestamp_utc": now_utc(),
        "modified_files": [f["path"] for f in get_modified_files()],
        "test_files": get_test_files(),
        "key_decisions": get_key_decisions(),
        "open_questions": [],
        "next_actions": []
    }


def main():
    print("[AGENT-CORRIDOR-HANDOFF] Démarrage du pack de transfert")

    if not TRANSFERS_DIR.exists():
        TRANSFERS_DIR.mkdir(parents=True, exist_ok=True)
        print(f"[AGENT-CORRIDOR-HANDOFF] Répertoire créé : {TRANSFERS_DIR}")

    payload = build_payload()

    with PAYLOAD_FILE.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"[AGENT-CORRIDOR-HANDOFF] Payload écrit dans : {PAYLOAD_FILE}")
    print(f"[AGENT-CORRIDOR-HANDOFF] Fichiers modifiés : {len(payload['modified_files'])}")
    print(f"[AGENT-CORRIDOR-HANDOFF] Fichiers de test : {len(payload['test_files'])}")
    print(f"[AGENT-CORRIDOR-HANDOFF] Décisions clés : {len(payload['key_decisions'])}")
    print("[AGENT-CORRIDOR-HANDOFF] Terminé.")


if __name__ == "__main__":
    main()